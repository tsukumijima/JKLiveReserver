
import json
import os
import pickle
import requests
import sys
from datetime import datetime
from datetime import timedelta
from typing import Any


# バージョン情報
__version__ = '3.5.0'


class JKLive:

    # User-Agent
    USER_AGENT = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 JKLiveReserver/{__version__}'

    # 実況 ID とチャンネル/コミュニティ ID の対照表
    JIKKYO_CHANNELS = {
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
        'jk101': {'type': 'channel', 'id': 'ch2647992', 'name': 'NHK BS1'},
        # 'jk103': {'type': 'community', 'id': 'co5175227', 'name': 'NHK BSプレミアム'},  # 閉局に伴い削除
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
        'jk252': {'type': 'community', 'id': 'co5683458', 'name': 'WOWOW PLUS'},
        'jk260': {'type': 'community', 'id': 'co5682554', 'name': 'BS松竹東急'},
        'jk263': {'type': 'community', 'id': 'co5682551', 'name': 'BSJapanext'},
        'jk265': {'type': 'community', 'id': 'co5682548', 'name': 'BSよしもと'},
        'jk333': {'type': 'community', 'id': 'co5245469', 'name': 'AT-X'},
    }

    # 生放送のエラーメッセージの対照表
    RESERVE_ERROR_CODES = {
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
        'OVERLAP_PROGRAM_PROVIDER': '該当時間に同じユーザの別の放送予定があります。',
        'NO_PERMISSION': '許可のない操作が行われました。',
        'UNDER_MANTENANCE': 'メンテナンス中です。',
        'SERVICE_ERROR': '一時的なサーバ不調によりリクエストに失敗しました（リトライすると直る可能性もありますし、障害の可能性もあります）。',
    }


    def __init__(self,
        jikkyo_id: str,
        reservation_begin_time: datetime,
        reservation_duration: timedelta,
        nicologin_mail: str,
        nicologin_password: str,
        autorun_weekly: bool = False,
        autorun_daily: bool = False,
        commentfilter_enabled: bool = True,
        tagedit_enabled: bool = True,
    ) -> None:

        # 実況 ID
        self.jikkyo_id = jikkyo_id

        # 実況チャンネル名
        jikkyo_channel = self.getJikkyoChannelName(self.jikkyo_id)
        assert jikkyo_channel is not None, f'実況 ID {jikkyo_id} は存在しません。'
        self.jikkyo_channel = jikkyo_channel

        # 実況 ID に紐づくコミュニティ ID
        self.community_id = self.getNicoCommunityID(self.jikkyo_id)

        # 予約する番組の日付時刻
        self.reservation_begin_time = reservation_begin_time

        # 予約する番組の長さ
        self.reservation_duration = reservation_duration

        # メールアドレス・パスワード
        self.nicologin_mail = nicologin_mail
        self.nicologin_password = nicologin_password

        # タスクスケジューラなどからの自動実行かどうか
        self.autorun_weekly = autorun_weekly  # 毎週
        self.autorun_daily = autorun_daily  # 毎日

        # 予約する番組でAIコメントフィルターを有効にするか
        self.commentfilter_enabled = commentfilter_enabled

        # 予約する番組でタグ編集を有効にするか
        self.tagedit_enabled = tagedit_enabled


    # 番組を予約する
    def reserve(self) -> dict[str, Any]:

        # API の URL
        url = 'https://live2.nicovideo.jp/unama/api/v2/programs'

        # ログインセッションを取得
        user_session = self.__login()

        # 番組タイトル
        title = self.generateTitle()

        # 番組説明
        description = self.generateDescription()

        # タグ
        tags = [
            {'label': 'ニコニコ実況', 'isLocked': True},
            {'label': 'テレビ実況', 'isLocked': True},
            {'label': '実況', 'isLocked': True},
            {'label': '雑談', 'isLocked': True},
            {'label': self.jikkyo_channel.replace(' ', '_'), 'isLocked': True},
            {'label': self.jikkyo_id, 'isLocked': True},
        ]

        # API に渡すヘッダー
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': self.USER_AGENT,
            'X-niconico-session': user_session,
        }

        # API に渡すペイロード
        payload = {
            # コミュニティID
            'communityId': self.community_id,
            # 番組タイトル
            'title': title,
            # 番組説明
            'description': description,
            # 番組開始時刻
            'reservationBeginTime': self.reservation_begin_time.isoformat(),
            # 番組時間（分単位）
            # 参考: https://qiita.com/ksato9700/items/f8a2ea86c20ac0f34538
            'durationMinutes': int(self.reservation_duration / timedelta(minutes=1)),
            # カテゴリ
            'category': '一般(その他)',
            # タグ
            'tags': tags,
            # AIコメントフィルターを有効にするか
            'isAutoCommentFilterEnabled': self.commentfilter_enabled,
            # タグ編集を無効にするか
            'isTagOwnerLock': not self.tagedit_enabled,  # True と False を反転させる
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
            # [Amazon商品] [ニコニコQ] の貼り付け制限
            'isOfficialIchibaOnly': False,
            # 他番組から生放送引用されるのを許可するか
            'isQuotable': True,
        }

        # API にアクセス
        response = requests.post(url, json.dumps(payload), headers=headers).json()

        # ログインセッション切れの場合はもう一度ログイン
        if response['meta']['status'] == 401 and response['meta']['errorCode'] == 'AUTHENTICATION_FAILED':

            # 再ログイン
            user_session = self.__login(True)
            headers['X-niconico-session'] = user_session

            # もう一度 API にアクセス
            response = requests.post(url, json.dumps(payload), headers=headers).json()

        # レスポンスを返す
        # 成功/失敗判定は結果を受け取った側で行う
        return response


    # ニコニコにログインする
    def __login(self, force: bool = False) -> str:

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
            session.post(url, post, headers={'User-Agent': self.USER_AGENT})

            # Cookie を保存
            with open(cookie_dump, 'wb') as f:
                pickle.dump(session.cookies, f)

            return session.cookies.get('user_session')


    # 番組タイトルを生成する
    def generateTitle(self) -> str:

        return f'{self.jikkyo_channel}【ニコニコ実況】{self.reservation_begin_time.strftime("%Y年%m月%d日 %H:%M")}～{(self.reservation_begin_time + self.reservation_duration).strftime("%H:%M")}'


    # 番組説明を生成する
    def generateDescription(self) -> str:

        description = 'ニコニコ実況は、放送中のテレビ番組や起きているイベントに対して、みんなでコメントをし盛り上がりを共有する、リアルタイムコミュニケーションサービスです。<br>'
        if self.autorun_weekly is True:  # 毎週自動実行
            description += f'この実況枠は JKLiveReserver https://git.io/JOGdT によって毎週{datetime.now().astimezone().strftime("%a")}曜日に1週間分自動予約されています。<br>'
        elif self.autorun_daily is True:  # 毎日自動実行
            description += 'この実況枠は JKLiveReserver https://git.io/JOGdT によって毎日1週間分自動予約されています。<br>'
        else:  # それ以外
            description += 'この実況枠は JKLiveReserver https://git.io/JOGdT によって自動予約されています。<br>'
        description += '<br>'

        for jikkyo_id, jikkyo_channel in self.JIKKYO_CHANNELS.items():

            # 文字数制限 (1000文字) に収まりきらないので、ほぼ利用されていない WOWOW は番組説明から省く
            if jikkyo_id in ['jk191', 'jk192', 'jk193', 'jk252']:
                continue

            # 見出しを入れる
            if jikkyo_id == 'jk1':
                description += '<b>地デジ</b><br>'
            if jikkyo_id == 'jk101':
                description += '<br>'
                description += '<b>BS・CS</b><br>'

            # 現在のチャンネルの情報を追記していく
            description += f'{jikkyo_channel["name"]}：https://live.nicovideo.jp/watch/{jikkyo_channel["id"]} ({jikkyo_id})'
            if self.jikkyo_id == jikkyo_id:
                description += '<b> ⬅️ NOW</b>'
            description += '<br>'

        description += '<br>BS総合避難所：co5117214 (全実況チャンネル一覧もこちらから)'

        return description


    # 実況 ID リストを取得
    @staticmethod
    def getJikkyoChannelList():
        return JKLive.JIKKYO_CHANNELS.keys()


    # 実況 ID から実況チャンネル名を取得
    @staticmethod
    def getJikkyoChannelName(jikkyo_id) -> str | None:
        if jikkyo_id in JKLive.JIKKYO_CHANNELS:
            return JKLive.JIKKYO_CHANNELS[jikkyo_id]['name']
        else:
            return None


    # 実況 ID からニコニコミュニティの ID を取得
    # jk1 のような公式実況チャンネルでは None を返す
    @staticmethod
    def getNicoCommunityID(jikkyo_id) -> str | None:
        if jikkyo_id in JKLive.JIKKYO_CHANNELS and JKLive.JIKKYO_CHANNELS[jikkyo_id]['type'] == 'community':
            return JKLive.JIKKYO_CHANNELS[jikkyo_id]['id']
        else:
            return None


    # 予約失敗時のエラーコードからエラーメッセージを取得する
    @staticmethod
    def getReserveErrorMessage(error_code: str) -> str | None:
        if error_code in JKLive.RESERVE_ERROR_CODES:
            return JKLive.RESERVE_ERROR_CODES[error_code]
        else:
            return None


    # ニコ生がメンテナンス中やサーバーエラーでないかを確認
    @staticmethod
    def getNicoLiveStatus() -> tuple[bool, int]:
        response = requests.get('https://live.nicovideo.jp/')  # レスポンスを取得
        # HTTP ステータスコードで判定
        if response.status_code == 200:
            return (True, response.status_code)
        else:
            return (False, response.status_code)
