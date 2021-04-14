
import datetime as dt
import json
import os
import pickle
from pprint import pprint
import requests
import sys


class JKLive:

    # 実況 ID とチャンネル/コミュニティ ID の対照表
    jikkyo_channel_table = {
        'jk1': {'type': 'channel', 'id': 'ch2646436', 'name': 'NHK総合'},
        'jk2': {'type': 'channel', 'id': 'ch2646437', 'name': 'NHK Eテレ'},
        'jk4': {'type': 'channel', 'id': 'ch2646438', 'name': '日本テレビ'},
        'jk5': {'type': 'channel', 'id': 'ch2646439', 'name': 'テレビ朝日'},
        'jk6': {'type': 'channel', 'id': 'ch2646440', 'name': 'TBSテレビ'},
        'jk7': {'type': 'channel', 'id': 'ch2646441', 'name': 'テレビ東京'},
        'jk8': {'type': 'channel', 'id': 'ch2646442', 'name': 'フジテレビ'},
        'jk9': {'type': 'channel', 'id': 'ch2646485', 'name': 'TOKYO MX'},
        'jk10': {'type': 'community', 'id': 'co5253063', 'name': 'テレ玉'},
        'jk11': {'type': 'community', 'id': 'co5215296', 'name': 'tvk'},
        'jk12': {'type': 'community', 'id': 'co5359761', 'name': 'チバテレビ'},
        'jk101': {'type': 'community', 'id': 'co5214081', 'name': 'NHK BS1'},
        'jk103': {'type': 'community', 'id': 'co5175227', 'name': 'NHK BSプレミアム'},
        'jk141': {'type': 'community', 'id': 'co5175341', 'name': 'BS日テレ'},
        'jk151': {'type': 'community', 'id': 'co5175345', 'name': 'BS朝日'},
        'jk161': {'type': 'community', 'id': 'co5176119', 'name': 'BS-TBS'},
        'jk171': {'type': 'community', 'id': 'co5176122', 'name': 'BSテレ東'},
        'jk181': {'type': 'community', 'id': 'co5176125', 'name': 'BSフジ'},
        'jk191': {'type': 'community', 'id': 'co5251972', 'name': 'WOWOW PRIME'},
        'jk192': {'type': 'community', 'id': 'co5251976', 'name': 'WOWOW LIVE'},
        'jk193': {'type': 'community', 'id': 'co5251983', 'name': 'WOWOW CINEMA'},
        'jk211': {'type': 'channel',   'id': 'ch2646846', 'name': 'BS11'},
        'jk222': {'type': 'community', 'id': 'co5193029', 'name': 'BS12'},
        'jk236': {'type': 'community', 'id': 'co5296297', 'name': 'BSアニマックス'},
        'jk333': {'type': 'community', 'id': 'co5245469', 'name': 'AT-X'},
    }

    # 生放送のエラーメッセージの対照表
    reserve_error_table = {
        'INVALID_PARAMETER': 'リクエストに無効なパラメータがあります。',
        'INVALID_TAGS': '無効なタグ指定があります。',
        'OVERLAP_MAINTENANCE': '番組放送時間にメンテナンス時間が重複しています。',
        'AUTHENTICATION_FAILED': 'ログインセッションが無効です。メールアドレスとパスワードを確認してください。',
        'NO_COMMUNITY_OWNED': '指定されたコミュニティでの放送権がありません。',
        'COMMUNITY_NOT_FOUND': '指定されたコミュニティが存在しません。',
        'PENALIZED_COMMUNITY': '放送ペナルティを受けたコミュニティでは放送できません。',
        'OVERLAP_COMMUNITY': '同一コミュニティで他に重複した別ユーザの放送の予定があります。',
        'NOT_PREMIUM_USER': 'プレミアムユーザではないため、番組を予約できません。',
        'PENALIZED_USER': '配信ペナルティを受けています。',
        'OVERLAP_PROGRAM_PROVIDER': '該当時間に別の同ユーザの放送予定があります。',
        'NO_PERMISSION': '許可のない操作が行われました。',
        'UNDER_MANTENANCE': 'メンテナンス中です。',
        'SERVICE_ERROR': '一時的なサーバ不調によりリクエストに失敗しました（リトライすると直る可能性もありますし、障害の可能性もあります）。',
    }

    def __init__(self, jikkyo_id, datetime, duration, nicologin_mail, nicologin_password):

        # 実況 ID
        self.jikkyo_id = jikkyo_id

        # 実況チャンネル名
        self.jikkyo_channel = self.getJikkyoChannelName(self.jikkyo_id)

        # 実況 ID に紐づくコミュニティ ID
        self.community_id = self.getNicoCommunityID(self.jikkyo_id)

        # 予約する番組の日付時刻
        self.datetime = datetime

        # 予約する番組の長さ
        self.duration = duration

        # メールアドレス・パスワード
        self.nicologin_mail = nicologin_mail
        self.nicologin_password = nicologin_password

    # 番組を予約する
    def reserve(self):

        # API の URL
        url = 'http://live2.nicovideo.jp/unama/api/v2/programs'

        # ログインセッションを取得
        user_session = self.__login()

        # タグ
        tags = [
            {'label':'ニコニコ実況', 'isLocked': True},
            {'label':'テレビ実況', 'isLocked': True},
            {'label':'実況', 'isLocked': True},
            {'label':'雑談', 'isLocked': True},
            {'label':self.jikkyo_channel.replace(' ', '_'), 'isLocked': True},
        ]

        # API に渡すヘッダー
        headers = {
            'X-niconico-session' : user_session,
            'Accept' : 'application/json',
            'Content-Type': 'application/json',
        }

        # API に渡すペイロード
        payload = {
            # コミュニティID
            'communityId': self.community_id,
            # タイトル
            'title': f"{self.jikkyo_channel}【ニコニコ実況】{self.datetime.strftime('%Y年%m月%d日 %H:%M')}～{(self.datetime + self.duration).strftime('%H:%M')}",
            # 説明
            'description': 'ニコニコ実況は、放送中のテレビ番組や起きているイベントに対して、みんなでコメントをし盛り上がりを共有する、リアルタイムコミュニケーションサービスです。',
            # 番組開始時刻
            'reservationBeginTime': self.datetime.isoformat(),
            # 番組時間（分単位）
            # 参考: https://qiita.com/ksato9700/items/f8a2ea86c20ac0f34538
            'durationMinutes': int(self.duration / dt.timedelta(minutes=1)),
            # カテゴリ
            'category': '一般(その他)',
            # タグ
            'tags': tags,
            # タグ編集をロックするか
            'isTagOwnerLock': False,
            # 最大画質（実況番組では常に真っ黒で画質を上げても何の意味もないため、最低の画質に設定する）
            'maxQuality': '384kbps288p',
            # コミュニティ限定番組にするか
            'isMemberOnly': False,
            # タイムシフトを利用するか
            'isTimeshiftEnabled': True,
            # ニコニ広告を利用するか
            'isUadEnabled': True,
            # ニコニコ市場を利用するか
            'isIchibaEnabled': True,
            # ［Amazon商品］［ニコニコQ］の貼り付け制限
            'isOfficialIchibaOnly': False,
            # 他番組から生放送引用されるのを許可するか
            'isQuotable': True,
            # AIによるコメントのフィルタリングを許可するか
            'isAutoCommentFilterEnabled': True,
        }

        #print(payload)

        # API にアクセス
        response = requests.post(url, json.dumps(payload), headers=headers).json()

        # ログインセッション切れの場合はもう一度ログイン
        if response['meta']['status'] != 201 and response['meta']['errorCode'] == 'AUTHENTICATION_FAILED':

            # 再ログイン
            user_session = self.__login(True)

            # もう一度 API にアクセス
            response = requests.post(url, json.dumps(payload), headers = headers).json()

        # レスポンスを返す
        # 成功/失敗判定は結果を受け取った側で行う
        return response

    # 実況 ID から実況チャンネル名を取得
    @staticmethod
    def getJikkyoChannelName(jikkyo_id):
        if jikkyo_id in JKLive.jikkyo_channel_table:
            return JKLive.jikkyo_channel_table[jikkyo_id]['name']
        else:
            return None

    # 実況 ID からニコニコミュニティの ID を取得
    # jk1 のような公式実況チャンネルでは None を返す
    @staticmethod
    def getNicoCommunityID(jikkyo_id):
        if jikkyo_id in JKLive.jikkyo_channel_table and JKLive.jikkyo_channel_table[jikkyo_id]['type'] == 'community':
            return JKLive.jikkyo_channel_table[jikkyo_id]['id']
        else:
            return None

    # ニコ生がメンテナンス中やサーバーエラーでないかを確認
    @staticmethod
    def getNicoLiveStatus():
        nicolive_url = 'https://live.nicovideo.jp/'
        response = requests.get(nicolive_url)  # レスポンスを取得
        # HTTP ステータスコードで判定
        if response.status_code == 200:
            return [True, response.status_code]
        else:
            return [False, response.status_code]

    # 予約失敗時のエラーコードからエラーメッセージを取得する
    @staticmethod
    def getReserveErrorMessage(error_code):
        if error_code in JKLive.reserve_error_table:
            return JKLive.reserve_error_table[error_code]
        else:
            return None

    # ニコニコにログインする
    def __login(self, force=False):

        cookie_dump = os.path.dirname(os.path.abspath(sys.argv[0])) + '/cookie.dump'

        # ログイン済み & 強制ログインでないなら以前取得した Cookieを再利用
        if os.path.exists(cookie_dump) and force is False:

            with open(cookie_dump, 'rb') as f:
                cookies = pickle.load(f)
                return cookies.get('user_session')

        else:

            # ログインを実行
            url = 'https://account.nicovideo.jp/api/v1/login'
            post = {'mail': self.nicologin_mail, 'password': self.nicologin_password}
            session = requests.session()
            session.post(url, post)

            # Cookie を保存
            with open(cookie_dump, 'wb') as f:
                pickle.dump(session.cookies, f)

            return session.cookies.get('user_session')
