#!/usr/bin/python3

import argparse
import configparser
import datetime as dt
import dateutil.parser
import json
import os
from pprint import pprint
import shutil
import sys

import JKLive

# バージョン情報
__version__ = '2.1.0'

def main():

    # 引数解析
    parser = argparse.ArgumentParser(description = 'ニコニコ実況用の番組を CLI で予約するツール', formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument('Channel', help='予約する実況チャンネルのID (ex: jk101)')
    parser.add_argument('DateTime', help='予約する番組の開始時刻 (ex: 2021/04/15/04:00) now を指定すると今日もしくは明日の朝4時に設定されます')
    parser.add_argument('Duration', help='予約する番組の放送時間の長さ (ex: 24) 最大放送時間が6時間までのため、6時間以降は番組が分割されます')
    parser.add_argument('-v', '--version', action='version', help='バージョン情報を表示する', version='JKLiveReserver version ' + __version__)
    args = parser.parse_args()

    # 実況ID
    jikkyo_id = args.Channel.rstrip()

    # 時刻
    now_datetime = dt.datetime.now().astimezone()
    max_datetime = (now_datetime + dt.timedelta(days=8)).astimezone()

    # 予約する番組の開始時刻
    # 今日もしくは明日の朝4時に設定
    if args.DateTime.rstrip() == 'now':
        # 今日の朝4時はもう過ぎた
        if now_datetime.replace(hour=4, minute=0, second=0, microsecond=0).astimezone() <= now_datetime:
            datetime = (now_datetime + dt.timedelta(days=1)).replace(hour=4, minute=0, second=0, microsecond=0).astimezone()
        # 今日の朝4時はこれから
        elif now_datetime.replace(hour=4, minute=0, second=0, microsecond=0).astimezone() > now_datetime:
            datetime = now_datetime.replace(hour=4, minute=0, second=0, microsecond=0).astimezone()
    # 指定された時刻を設定
    else:
        datetime = dateutil.parser.parse(args.DateTime.rstrip()).astimezone()

    # 予約する番組の放送時間の長さ
    duration = dt.timedelta(hours=int(args.Duration))

    # 行区切り
    print('=' * shutil.get_terminal_size().columns)

    # 予約可能期間外かチェック
    if datetime > max_datetime :
        print(f"生放送の予約に失敗しました。")
        print(f"エラー: {datetime.strftime('%Y/%m/%d %H:%M')} は予約可能時間外のため予約できません。予約可能な期間は予約日から1週間です。")
        print('=' * shutil.get_terminal_size().columns)
        sys.exit(1)
    if datetime < now_datetime :
        print(f"生放送の予約に失敗しました。")
        print(f"エラー: {datetime.strftime('%Y/%m/%d %H:%M')} はすでに過ぎた日付です。予約可能な期間は予約日から1週間です。")
        print('=' * shutil.get_terminal_size().columns)
        sys.exit(1)

    # ニコ生がメンテナンス中やサーバーエラーでないかを確認
    nicolive_status, nicolive_status_code = JKLive.JKLive.getNicoLiveStatus()
    if nicolive_status is False:
        print(f"生放送の予約に失敗しました。")
        if nicolive_status_code == 500:
            print('エラー: 現在、ニコ生で障害が発生しています。(HTTP Error 500)')
        elif nicolive_status_code == 503:
            print('エラー: 現在、ニコ生はメンテナンス中です。(HTTP Error 503)')
        else:
            print(f"エラー: 現在、ニコ生でエラーが発生しています。(HTTP Error {nicolive_status_code})")
        print('=' * shutil.get_terminal_size().columns)
        sys.exit(1)

    # 設定読み込み
    config_ini = os.path.dirname(os.path.abspath(sys.argv[0])) + '/JKLiveReserver.ini'
    if not os.path.exists(config_ini):
        print(f"生放送の予約に失敗しました。")
        print('エラー: JKLiveReserver.ini が存在しません。JKLiveReserver.example.ini からコピーし、\n適宜設定を変更して JKLiveReserver と同じ場所に配置してください。')
        print('=' * shutil.get_terminal_size().columns)
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(config_ini, encoding='UTF-8')

    # ログイン用のメールアドレスとパスワード
    nicologin_mail = config.get('Default', 'nicologin_mail')
    nicologin_password = config.get('Default', 'nicologin_password')

    print(f"{JKLive.JKLive.getJikkyoChannelName(jikkyo_id)} の実況番組を " +
          f"{datetime.strftime('%Y/%m/%d %H:%M')} から {(datetime + duration).strftime('%Y/%m/%d %H:%M')} まで予約します。")
    print('-' * shutil.get_terminal_size().columns)

    def post(real_datetime, real_duration):

        # コミュニティ ID が取得できなかったら終了
        if JKLive.JKLive.getNicoCommunityID(jikkyo_id) == None:
            print(f"生放送の予約に失敗しました。")
            print(f"エラー: 実況チャンネル {jikkyo_id} に該当するニコニコミュニティが見つかりませんでした。")
            print('=' * shutil.get_terminal_size().columns)
            sys.exit(1)

        # インスタンスを作成
        jklive = JKLive.JKLive(jikkyo_id, datetime, duration, nicologin_mail, nicologin_password)

        # 番組を予約する
        result = jklive.reserve()

        # 番組予約の成功/失敗
        if result['meta']['status'] == 201:
            print(f"生放送の予約に成功しました。放送 ID は {result['data']['id']} です。")
            print(f"URL: [https://live2.nicovideo.jp/watch/{result['data']['id']}]")
        else:
            print(f"生放送の予約に失敗しました。status: {result['meta']['status']} errorcode: {result['meta']['errorCode']}")
            print(f"エラー: {JKLive.JKLive.getReserveErrorMessage(result['meta']['errorCode'])}")
            print('=' * shutil.get_terminal_size().columns)
            sys.exit(1)

    # 番組予約を実行
    post(datetime, duration)

    # 行区切り
    print('=' * shutil.get_terminal_size().columns)


if __name__ == '__main__':
    main()
