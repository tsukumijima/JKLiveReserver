#!/usr/bin/env python3

import argparse
import configparser
import copy
import dateutil.parser
import locale
import os
import shutil
import sys
import time
from datetime import datetime
from datetime import timedelta
from typing import Any

from JKLive import JKLive, __version__


# ユーザー番組の最長放送可能時間 (時間単位)
## ユーザーレベル 40 以降なら 24 時間配信可能だが、基本ユーザーレベル 40 に達し得ないため 12 時間に設定
## ref: https://blog.nicovideo.jp/niconews/213237.html
USER_PROGRAM_MAX_HOUR = 12  # 12時間

# このファイルが存在するフォルダの絶対パス
CURRENT_FOLDER = os.path.dirname(os.path.abspath(sys.argv[0]))

# ターミナルの横幅
# conhost.exe だと -1px しないと改行されてしまう
TERMINAL_COLUMNS = shutil.get_terminal_size().columns - 1


def main() -> None:

    # locale モジュールで時間のロケールを日本語に変更する
    # 参考: https://qiita.com/jusotech10/items/89685331f017cf9386fd
    locale.setlocale(locale.LC_ALL, '')

    # 引数解析
    parser = argparse.ArgumentParser(description='ニコニコ実況用のコミュニティ番組を一括で予約（枠取り）するツール', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('Channel', help='予約する実況チャンネルのID (ex: jk161)')
    parser.add_argument('-d', '--date', default=None, help='予約する番組の開始時刻 (ex: 2021/04/15/04:00)\n省略すると現在時刻以降の朝4時の日付に設定されます')
    parser.add_argument('-l', '--length', default=168, help='予約する番組の配信時間の長さ (時間単位) (ex: 24)\n省略すると 168（7日間）に設定されます\n最長放送可能時間が通常12時間までのため、12時間以降は番組を分割して予約します')
    parser.add_argument('-o', '--output-log', action='store_true', help='実行ログをファイルに出力するかどうか')
    parser.add_argument('-aw', '--autorun-weekly', action='store_true', help='タスクスケジューラなどからの自動実行かどうか（毎週）\n指定すると予約した番組の説明欄に毎週指定された曜日に自動で予約している旨を追記します')
    parser.add_argument('-ad', '--autorun-daily', action='store_true', help='タスクスケジューラなどからの自動実行かどうか（毎日）\n指定すると予約した番組の説明欄に毎日自動で予約している旨を追記します')
    parser.add_argument('-v', '--version', action='version', help='バージョン情報を表示する', version='JKLiveReserver version ' + __version__)
    args = parser.parse_args()

    # タスクスケジューラなどからの自動実行かどうか
    autorun_weekly = args.autorun_weekly  # 毎週
    autorun_daily = args.autorun_daily  # 毎日

    # 標準出力をファイルに変更
    if args.output_log is True:
        sys.stdout = open(CURRENT_FOLDER + '/JKLiveReserver.log', mode='w', encoding='UTF-8')
        sys.stderr = open(CURRENT_FOLDER + '/JKLiveReserver.log', mode='w', encoding='UTF-8')

    # 実況ID
    jikkyo_id = args.Channel.rstrip()

    # 時刻
    now_datetime = datetime.now().astimezone()
    max_datetime = (now_datetime + timedelta(days=8)).astimezone()

    # 予約する番組の開始時刻
    # 次の朝4時の日付に設定
    target_datetime: datetime | None = None
    if args.date is None:
        # 今日の朝4時はもう過ぎた
        if now_datetime.replace(hour=4, minute=0, second=0, microsecond=0).astimezone() <= now_datetime:
            target_datetime = (now_datetime + timedelta(days=1)).replace(hour=4, minute=0, second=0, microsecond=0).astimezone()
        # 今日の朝4時はこれから
        elif now_datetime.replace(hour=4, minute=0, second=0, microsecond=0).astimezone() > now_datetime:
            target_datetime = now_datetime.replace(hour=4, minute=0, second=0, microsecond=0).astimezone()
        assert target_datetime is not None
    # 指定された時刻を設定
    else:
        target_datetime = dateutil.parser.parse(args.date.rstrip()).astimezone()

    # 予約する番組の配信時間の長さ
    length = timedelta(hours=int(args.length))
    duration_hours = int(args.length)

    # 行区切り
    print('=' * TERMINAL_COLUMNS)

    # 予約可能期間外かチェック
    if target_datetime > max_datetime:
        print(f"番組の予約に失敗しました。")
        print(f"エラー: {target_datetime.strftime('%Y/%m/%d %H:%M')} は予約可能時間外のため予約できません。予約可能な期間は予約日から1週間です。")
        print('=' * TERMINAL_COLUMNS)
        sys.exit(1)
    if target_datetime < now_datetime:
        print(f"番組の予約に失敗しました。")
        print(f"エラー: {target_datetime.strftime('%Y/%m/%d %H:%M')} はすでに過ぎた日付です。予約可能な期間は予約日から1週間です。")
        print('=' * TERMINAL_COLUMNS)
        sys.exit(1)
    if duration_hours > 168 or duration_hours < 1:
        print(f"番組の予約に失敗しました。")
        print(f"エラー: 予約する番組の配信時間が不正です。")
        print('=' * TERMINAL_COLUMNS)
        sys.exit(1)

    # コミュニティ ID が取得できなかったら終了
    if JKLive.getNicoCommunityID(jikkyo_id) is None:
        print(f"番組の予約に失敗しました。")
        print(f"エラー: 実況チャンネル {jikkyo_id} に該当するニコニコミュニティが見つかりませんでした。")
        print('=' * TERMINAL_COLUMNS)
        sys.exit(1)

    # ニコ生がメンテナンス中やサーバーエラーでないかを確認
    nicolive_status, nicolive_status_code = JKLive.getNicoLiveStatus()
    if nicolive_status is False:
        print(f"番組の予約に失敗しました。")
        if nicolive_status_code == 500:
            print('エラー: 現在、ニコ生で障害が発生しています。(HTTP Error 500)')
        elif nicolive_status_code == 503:
            print('エラー: 現在、ニコ生はメンテナンス中です。(HTTP Error 503)')
        else:
            print(f"エラー: 現在、ニコ生でエラーが発生しています。(HTTP Error {nicolive_status_code})")
        print('=' * TERMINAL_COLUMNS)
        sys.exit(1)

    # 設定読み込み
    config_ini = CURRENT_FOLDER + '/JKLiveReserver.ini'
    if not os.path.exists(config_ini):
        print(f"番組の予約に失敗しました。")
        print('エラー: JKLiveReserver.ini が存在しません。JKLiveReserver.example.ini からコピーし、')
        print('適宜設定を変更して JKLiveReserver と同じ場所に配置してください。')
        print('=' * TERMINAL_COLUMNS)
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(config_ini, encoding='UTF-8')

    # ログイン用のメールアドレスとパスワード
    nicologin_mail = config.get('Default', 'nicologin_mail')
    nicologin_password = config.get('Default', 'nicologin_password')

    # 予約する番組でAIコメントフィルターを有効にするか
    try:
        commentfilter_enabled = config.get('Default', 'commentfilter_enabled')
        if commentfilter_enabled == 'False':
            commentfilter_enabled = False  # 無効
        else:
            commentfilter_enabled = True  # 有効
    except configparser.NoOptionError:  # キーが存在しない場合は有効にする
        commentfilter_enabled = True

    # 予約する番組でタグ編集を有効にするか
    try:
        tagedit_enabled = config.get('Default', 'tagedit_enabled')
        if tagedit_enabled == 'False':
            tagedit_enabled = False  # 無効
        else:
            tagedit_enabled = True  # 有効
    except configparser.NoOptionError:  # キーが存在しない場合は有効にする
        tagedit_enabled = True

    # 実況チャンネル名
    jikkyo_channel = JKLive.getJikkyoChannelName(jikkyo_id)

    print(f"{jikkyo_channel} の実況番組を " +
          f"{target_datetime.strftime('%Y/%m/%d %H:%M')} から {(target_datetime + length).strftime('%Y/%m/%d %H:%M')} まで予約します。")

    def post(reservation_begin_time: datetime, reservation_duration: timedelta) -> dict[str, Any]:

        # 0.5 秒待つ
        time.sleep(0.5)

        # インスタンスを作成
        jklive = JKLive(
            jikkyo_id,
            reservation_begin_time,
            reservation_duration,
            nicologin_mail,
            nicologin_password,
            autorun_weekly,
            autorun_daily,
            commentfilter_enabled,
            tagedit_enabled,
        )

        print('-' * TERMINAL_COLUMNS)
        print(f"番組タイトル: {jklive.generateTitle()}")
        print(f"番組開始時刻: {reservation_begin_time.strftime('%Y/%m/%d %H:%M:%S')}  " +
              f"番組終了時刻: {(reservation_begin_time + reservation_duration).strftime('%Y/%m/%d %H:%M:%S')}")

        # 番組を予約する
        result = jklive.reserve()

        # 番組予約の成功/失敗
        if result['meta']['status'] == 201:
            print(f"番組の予約に成功しました。放送 ID は {result['data']['id']} です。")
            print(f"URL: https://live.nicovideo.jp/watch/{result['data']['id']}")
        else:
            print(f"番組の予約に失敗しました。status: {result['meta']['status']} errorcode: {result['meta']['errorCode']}")
            if 'data' in result:
                print(f"エラー: {JKLive.getReserveErrorMessage(result['meta']['errorCode'])} ({result['data'][0]})")
            else:
                print(f"エラー: {JKLive.getReserveErrorMessage(result['meta']['errorCode'])}")

        return result['meta']

    # 番組の配信時間長が最長放送可能時間以下の場合
    if duration_hours <= USER_PROGRAM_MAX_HOUR:

        # 番組予約をそのまま実行
        post(target_datetime, length)

    # ユーザー番組の最長放送可能時間を超える場合、番組を分割する
    elif duration_hours > USER_PROGRAM_MAX_HOUR:

        # 予約開始時刻
        reservation_begin_time = copy.copy(target_datetime)

        # 残り配信時間長
        remain_duration_hours = copy.copy(duration_hours)

        while True:

            # 残り配信時間長が最長放送可能時間より長い場合
            if remain_duration_hours > USER_PROGRAM_MAX_HOUR:

                # 配信時間長を最長放送可能時間に設定
                reservation_duration = timedelta(hours=USER_PROGRAM_MAX_HOUR)

            # 残り配信時間長が最長放送可能時間以下の場合
            else:

                # 配信時間長を残り配信時間長に設定
                reservation_duration = timedelta(hours=remain_duration_hours)

            # 残り配信時間長分の長さの番組を予約
            result = post(reservation_begin_time, reservation_duration)

            # 06:00 ～ 08:30 にかけての定期メンテナンスとの重複時
            # 04:00 ～ 06:00 の枠と 08:30 ～ 16:00 までの枠に分割する
            if (result['errorCode'] == 'OVERLAP_MAINTENANCE') and (reservation_begin_time.strftime('%H:%M') == '04:00'):

                print('-' * TERMINAL_COLUMNS)
                print('06:00 ～ 08:30 はおそらく定期メンテナンス中のため、04:00 ～ 06:00 と 08:30 ～ 16:00 の枠に分割して予約します。')

                # 04:00 ～ 06:00 の枠（2時間）
                ## メンテナンス開始時刻が 06:30 より前の場合 (稀にある: 03:30 〜 08:30 など) は予約に失敗するが、
                ## そうした状況では 04:00 〜 06:00 の時間帯全体がメンテナンスで埋まっていることが多いため、エラーを無視する
                result = post(reservation_begin_time, timedelta(hours=2))

                # 08:30 ～ 16:00 の枠（7時間30分）
                # 4時間30分という値は 04:00 からの 08:30 までの時間を示す
                post(reservation_begin_time + timedelta(hours=4, minutes=30), timedelta(hours=7, minutes=30))

            # 次の予約開始時刻をずらす
            reservation_begin_time = reservation_begin_time + reservation_duration

            # 残り配信時間長を減らす
            remain_duration_hours = remain_duration_hours - (reservation_duration.total_seconds() / 60 / 60)

            # 残り配信時間長が1時間未満なら終了
            if remain_duration_hours < 1:
                break

    print('-' * TERMINAL_COLUMNS)
    print(f"番組の予約を完了しました。")
    print('=' * TERMINAL_COLUMNS)


if __name__ == '__main__':
    main()
