#!/usr/bin/python3

import ctypes
import datetime as dt
import os
import shutil
import subprocess
import sys

from JKLive import JKLive

# このファイルが存在するフォルダの絶対パス
current_folder = os.path.dirname(os.path.abspath(sys.argv[0]))

# ターミナルの横幅
# conhost.exe だと -1px しないと改行されてしまう
terminal_columns = shutil.get_terminal_size().columns - 1

# 参考: https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():

    # 曜日の対照表
    dayofweek = {
        '日': 'Sunday',
        '月': 'Monday',
        '火': 'Tuesday',
        '水': 'Wednesday',
        '木': 'Thursday',
        '金': 'Friday',
        '土': 'Saturday',
    }

    print('=' * terminal_columns)
    print('  ***** JKLiveScheduler *****')
    print('=' * terminal_columns)
    print('  毎週、指定された曜日に１週間分の実況枠を一括で予約するよう、')
    print('  タスクスケジューラにタスクを登録するスクリプトです。')
    print('-' * terminal_columns)

    print('  1. タスクを登録・変更する場合は 1 を、')
    print('     削除する場合は 2 を入力してください。')
    while True:
        operation = input('     タスクの操作：')
        if (int(operation) == 1 or int(operation) == 2):
            operation = int(operation)
            break
        else:
            print('     値が不正です。もう一度入力してください。')

    print('-' * terminal_columns)

    # タスクの登録・変更
    if operation == 1:

        print('  2. 実況枠を予約する実況チャンネルの ID を入力してください。')
        print('     例：jk101・jk222・jk333')
        while True:
            jikkyo_id = input('     実況枠を予約する実況チャンネルの ID：')
            flg = False
            for jikkyo_id_compare in JKLive.getJikkyoChannelList():
                # 存在する実況 ID でかつ、コミュニティチャンネルの場合のみ
                if jikkyo_id_compare == jikkyo_id and JKLive.getNicoCommunityID(jikkyo_id_compare) is not None:
                    flg = True
            if flg is True:
                break
            else:
                print('     値が不正です。もう一度入力してください。')

        print('-' * terminal_columns)

        print('  3. 実況枠を予約する曜日を入力してください。')
        print('     曜日は 日・月・火・水・木・金・土 から選んで入力します。')
        while True:
            day = input('      実況枠を予約する曜日：')
            flg = False
            for day_compare in dayofweek:
                if day_compare == day:
                    flg = True
            if flg is True:
                break
            else:
                print('     値が不正です。もう一度入力してください。')

        print('-' * terminal_columns)

        print('  4. 実況枠を予約する時間を入力してください。')
        print('     時間は 18:30 のように入力します。')
        while True:
            time = input('     実況枠を予約する時間：')
            flg = False
            if ':' in time:
                # 参考: http://ututel.blog121.fc2.com/blog-entry-205.html
                try:
                    dt.datetime.strptime(f"2021-04-01T{time}:00", '%Y-%m-%dT%H:%M:%S')
                    flg = True
                except ValueError:  # 不正な時刻フォーマット
                    pass
            if flg is True:
                break
            else:
                print('     値が不正です。もう一度入力してください。')

        print('-' * terminal_columns)

        # 存在してもしなくてもとりあえず前のタスクを削除する
        subprocess.run(f"schtasks /Delete /F /TN \\JKLiveReserver", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # schtasks に登録する用の XML を錬成する
        # encoding は UTF-16 のままで OK
        xml = f"""<?xml version="1.0" encoding="UTF-16"?>
            <Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
                <RegistrationInfo>
                    <Date>2021-04-01T00:00:00</Date>
                    <URI>\\JKLiveReserver</URI>
                </RegistrationInfo>
                <Triggers>
                    <CalendarTrigger>
                        <StartBoundary>2021-04-01T{time}:00</StartBoundary>
                        <Enabled>true</Enabled>
                        <ScheduleByWeek>
                            <DaysOfWeek>
                                <{dayofweek[day]} />
                            </DaysOfWeek>
                            <WeeksInterval>1</WeeksInterval>
                        </ScheduleByWeek>
                    </CalendarTrigger>
                </Triggers>
                <Principals>
                    <Principal id="Author">
                        <UserId>S-1-5-18</UserId>
                        <RunLevel>LeastPrivilege</RunLevel>
                    </Principal>
                </Principals>
                <Settings>
                    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
                    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
                    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
                    <AllowHardTerminate>true</AllowHardTerminate>
                    <StartWhenAvailable>true</StartWhenAvailable>
                    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
                    <IdleSettings>
                        <StopOnIdleEnd>true</StopOnIdleEnd>
                        <RestartOnIdle>false</RestartOnIdle>
                    </IdleSettings>
                    <AllowStartOnDemand>true</AllowStartOnDemand>
                    <Enabled>true</Enabled>
                    <Hidden>false</Hidden>
                    <RunOnlyIfIdle>false</RunOnlyIfIdle>
                    <WakeToRun>true</WakeToRun>
                    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
                    <Priority>7</Priority>
                </Settings>
                <Actions Context="Author">
                    <Exec>
                        <Command>{current_folder}\\JKLiveReserver.exe</Command>
                        <Arguments>{jikkyo_id} --output-log</Arguments>
                    </Exec>
                </Actions>
            </Task>
        """

        # XML を一時的に出力
        xml_file = current_folder + '/JKLiveReserver.xml'
        f = open(xml_file, 'w', encoding='UTF-8')
        f.write(xml)
        f.close()

        # schtasks /Create を実行
        process = subprocess.run(f"schtasks /Create /F /TN \\JKLiveReserver /XML {xml_file}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if process.returncode == 0:
            print('  タスクの登録に成功しました。')
        else:
            print('  タスクの登録に失敗しました。')

        # XML を削除
        os.unlink(xml_file)

    # タスクの削除
    elif operation == 2:

        # schtasks /Delete を実行
        process = subprocess.run(f"schtasks /Delete /F /TN \\JKLiveReserver", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if process.returncode == 0:
            print('  タスクの削除に成功しました。')
        else:
            print('  タスクの削除に失敗しました。タスクが存在しない可能性があります。')

    # 何か入力されたら終了
    input('  終了するには何かキーを入力してください：')
    print('=' * terminal_columns)


if __name__ == '__main__':
    if os.name == 'nt' and is_admin():
        # OS が Windows で管理者権限があれば
        main()
    elif os.name == 'nt':
        # OS が Windows で管理者権限がないなら、gsudo で管理者権限で再実行する
        gsudo_exe = os.path.dirname(os.path.abspath(sys.argv[0])) + '/gsudo.exe'
        if '.exe' in sys.argv[0]:  # PyInstaller で exe 化した場合のみ
            gsudo_cmd = f"{gsudo_exe} {sys.executable} {' '.join(sys.argv[1:])}"
        else:  # 通常
            gsudo_cmd = f"{gsudo_exe} {sys.executable} {' '.join(sys.argv)}"
        # subprocess.run() で実行
        subprocess.run(gsudo_cmd)
    else:
        print('=' * terminal_columns)
        print('  ***** JKLiveScheduler *****')
        print('=' * terminal_columns)
        print('  このスクリプトは Windows 以外では実行できません。')
        print('=' * terminal_columns)
