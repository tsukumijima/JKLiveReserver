#!/usr/bin/python3

import argparse
import configparser
import copy
import datetime as dt
import dateutil.parser
import json
import os
from pprint import pprint
import shutil
import sys
import time

from JKLive import JKLive

# バージョン情報
__version__ = '3.0.0'

# このファイルが存在するフォルダの絶対パス
current_folder = os.path.dirname(os.path.abspath(sys.argv[0]))

# ターミナルの横幅
# conhost.exe だと -1px しないと改行されてしまう
terminal_columns = shutil.get_terminal_size().columns - 1

def main():

    # 引数解析
    parser = argparse.ArgumentParser(description = 'ニコニコ実況用のコミュニティ番組を一括で予約（枠取り）するツール', formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument('Channel', help='予約する実況チャンネルのID (ex: jk101)')
    parser.add_argument('-d', '--date', default=None, help='予約する番組の開始時刻 (ex: 2021/04/15/04:00)\n省略すると現在時刻以降の朝4時の日付に設定されます')
    parser.add_argument('-l', '--length', default=168, help='予約する番組の配信時間の長さ (ex: 24)\n省略すると 168（7日間）に設定されます\n最大配信時間が6時間までのため、6時間以降は番組を分割して予約します')
    parser.add_argument('-v', '--version', action='version', help='バージョン情報を表示する', version='JKLiveReserver version ' + __version__)
    args = parser.parse_args()

    # 実況ID
    jikkyo_id = args.Channel.rstrip()

    # 時刻
    now_datetime = dt.datetime.now().astimezone()
    max_datetime = (now_datetime + dt.timedelta(days=8)).astimezone()

    # 予約する番組の開始時刻
    # 次の朝4時の日付に設定
    if args.date is None:
        # 今日の朝4時はもう過ぎた
        if now_datetime.replace(hour=4, minute=0, second=0, microsecond=0).astimezone() <= now_datetime:
            datetime = (now_datetime + dt.timedelta(days=1)).replace(hour=4, minute=0, second=0, microsecond=0).astimezone()
        # 今日の朝4時はこれから
        elif now_datetime.replace(hour=4, minute=0, second=0, microsecond=0).astimezone() > now_datetime:
            datetime = now_datetime.replace(hour=4, minute=0, second=0, microsecond=0).astimezone()
    # 指定された時刻を設定
    else:
        datetime = dateutil.parser.parse(args.date.rstrip()).astimezone()

    # 予約する番組の配信時間の長さ
    length = dt.timedelta(hours=int(args.length))
    length_hour = int(args.length)

    # 行区切り
    print('=' * terminal_columns)

    # 予約可能期間外かチェック
    if datetime > max_datetime:
        print(f"生放送の予約に失敗しました。")
        print(f"エラー: {datetime.strftime('%Y/%m/%d %H:%M')} は予約可能時間外のため予約できません。予約可能な期間は予約日から1週間です。")
        print('=' * terminal_columns)
        sys.exit(1)
    if datetime < now_datetime:
        print(f"生放送の予約に失敗しました。")
        print(f"エラー: {datetime.strftime('%Y/%m/%d %H:%M')} はすでに過ぎた日付です。予約可能な期間は予約日から1週間です。")
        print('=' * terminal_columns)
        sys.exit(1)
    if length_hour > 168 or length_hour < 1 :
        print(f"生放送の予約に失敗しました。")
        print(f"エラー: 予約する番組の配信時間が不正です。")
        print('=' * terminal_columns)
        sys.exit(1)

    # コミュニティ ID が取得できなかったら終了
    if JKLive.getNicoCommunityID(jikkyo_id) == None:
        print(f"生放送の予約に失敗しました。")
        print(f"エラー: 実況チャンネル {jikkyo_id} に該当するニコニコミュニティが見つかりませんでした。")
        print('=' * terminal_columns)
        sys.exit(1)

    # ニコ生がメンテナンス中やサーバーエラーでないかを確認
    nicolive_status, nicolive_status_code = JKLive.getNicoLiveStatus()
    if nicolive_status is False:
        print(f"生放送の予約に失敗しました。")
        if nicolive_status_code == 500:
            print('エラー: 現在、ニコ生で障害が発生しています。(HTTP Error 500)')
        elif nicolive_status_code == 503:
            print('エラー: 現在、ニコ生はメンテナンス中です。(HTTP Error 503)')
        else:
            print(f"エラー: 現在、ニコ生でエラーが発生しています。(HTTP Error {nicolive_status_code})")
        print('=' * terminal_columns)
        sys.exit(1)

    # 設定読み込み
    config_ini = current_folder + '/JKLiveReserver.ini'
    if not os.path.exists(config_ini):
        print(f"生放送の予約に失敗しました。")
        print('エラー: JKLiveReserver.ini が存在しません。JKLiveReserver.example.ini からコピーし、\n適宜設定を変更して JKLiveReserver と同じ場所に配置してください。')
        print('=' * terminal_columns)
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(config_ini, encoding='UTF-8')

    # ログイン用のメールアドレスとパスワード
    nicologin_mail = config.get('Default', 'nicologin_mail')
    nicologin_password = config.get('Default', 'nicologin_password')

    # 実況チャンネル名
    jikkyo_channel = JKLive.getJikkyoChannelName(jikkyo_id)

    print(f"{jikkyo_channel} の実況番組を " +
        f"{datetime.strftime('%Y/%m/%d %H:%M')} から {(datetime + length).strftime('%Y/%m/%d %H:%M')} まで予約します。")

    def post(real_datetime, real_length):

        # 0.5 秒待つ
        time.sleep(0.5)

        # インスタンスを作成
        jklive = JKLive(jikkyo_id, real_datetime, real_length, nicologin_mail, nicologin_password)

        print('-' * terminal_columns)
        print(f"番組タイトル: {jklive.generateTitle()}")
        print(f"番組開始時刻: {real_datetime.strftime('%Y/%m/%d %H:%M:%S')}  " +
              f"番組終了時刻: {(real_datetime + real_length).strftime('%Y/%m/%d %H:%M:%S')}")

        # 番組を予約する
        result = jklive.reserve()

        # 番組予約の成功/失敗
        if result['meta']['status'] == 201:
            print(f"生放送の予約に成功しました。放送 ID は {result['data']['id']} です。")
            print(f"URL: https://live.nicovideo.jp/watch/{result['data']['id']}")
        else:
            print(f"生放送の予約に失敗しました。status: {result['meta']['status']} errorcode: {result['meta']['errorCode']}")
            if 'data' in result:
                print(f"エラー: {JKLive.getReserveErrorMessage(result['meta']['errorCode'])} ({result['data'][0]})")
            else:
                print(f"エラー: {JKLive.getReserveErrorMessage(result['meta']['errorCode'])}")
            return

    # 番組の配信時間の長さが6時間以内
    if length_hour <= 6:

        # 番組予約をそのまま実行
        post(datetime, length)

    # 番組の配信時間の長さが7時間以上
    # ユーザー生放送は最長6時間までのため、番組を分割する
    elif length_hour > 6:

        # 予約した6時間ごとの番組に合わせてずらす時間
        seek_datetime = copy.copy(datetime)

        # 残り配信時間
        length_hour_count = copy.copy(length_hour)

        while True:

            # 残り配信時間が7時間以上なら
            if length_hour_count > 6:

                # 6時間までの番組を予約
                post(seek_datetime, dt.timedelta(hours=6))

                # 時間をずらす
                seek_datetime = seek_datetime + dt.timedelta(hours=6)

                # 残り配信時間を減らす
                length_hour_count = length_hour_count - 6

            # 残り配信時間が6時間以下なら
            else:

                # 残り配信時間分の長さの番組を予約
                post(seek_datetime, dt.timedelta(hours=length_hour_count))

                # 時間をずらす
                seek_datetime = seek_datetime + dt.timedelta(hours=length_hour_count)

                # 残り配信時間を減らす
                length_hour_count = length_hour_count - length_hour_count

            # 残り時間が1時間未満なら終了
            if length_hour_count < 1:
                break

    # 行区切り
    print('=' * terminal_columns)


if __name__ == '__main__':
    main()
