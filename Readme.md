
# JKLiveReserver

ニコニコ実況用のコミュニティ番組を一括で予約（枠取り）するツールです。

## 概要

このツールを使うことで、**最大1週間分、指定した実況チャンネル (ex: jk101) の実況用番組を一気に自動で予約することができます！**  
1週間に1度 JKLiveReserver を実行するだけで、公式実況チャンネルと同様に24時間常に実況用番組を放送できます。  
JKLiveReserver を使えば、もう毎日のように手動で枠取りする必要はありません。

-----

さらに、JKLiveScheduler を使えば、**1週間に1度 JKLiveReserver を実行する手順も自動化できます！**  
4つの質問に答えるだけで、1週間に1度、指定された曜日と時間に1週間分の実況枠を一括で予約するよう、Windows のタスクスケジューラに簡単に登録できます。

指定した曜日の時間に PC を起動させておく必要はありますが、実行時に自動でスリープから復帰するため、起動さえしていればスリープ状態でも構いません（別途ちょっと設定が必要です）。  
もちろん、登録したタスクの変更や削除も可能です。タスクスケジューラを開く必要はありません。

-----

Linux でも実行できます。上級者向けなので細かい説明は省きますが、Crontab に登録して使うこともできます。

## お願い

ただし、残念ながらニコ生側の制限で、1 つのプレミアム会員アカウントで複数の実況チャンネルの番組を予約することはできません。  
つまり、**24 時間全自動枠取りをする場合、実況チャンネルにつき 1 つのプレミアム会員アカウントが必要になります。**

現在存在するコミュニティチャンネル全てで 24 時間常に実況枠を確保するのなら、**事実上プレミアム会員アカウントを持っている 16 人の協力が必要です。**

> 全自動枠取りをしない場合でも、BS 実況が盛り上がる時間帯はアニメが多く放送される深夜に集中しているため、実況チャンネルにつき 1 つのプレミアム会員アカウントが必要な事には代わりありません。
> 
> たとえば BS日テレの実況枠を 2021/04/19 22:00～24:00 まで予約した場合、同じユーザーで BS-TBS の実況枠を 2021/04/19 23:00～25:00 まで予約することはできません。23:00 ～ 24:00 の間、BS日テレの実況枠と時間が重複しているためです。

現状、BSを始めとするニコニコ実況のコミュニティチャンネルは有志による手動での枠取り（基本的には人が集まる番組のみ）によってなんとか成立しています。  
しかし、多忙だったり、あるいは単に忘れていたりして、今後実況したいときに枠がない、といったことも考えられます。

また、手動という関係上、24 時間常に実況枠を確保し続けることは（ JKLiveReserver のフォーク元である nicoLiveReserver が使われている NHK BS1 (jk101) を除いて）できていません。

プレミアム会員アカウントを持っていて、生主ではない方なら誰でも枠取りに参加できます。  
**ぜひ、公式チャンネル以外のニコニコ実況の安定した存続のため、皆さんのご協力をお願いします。**

## 注意

- **このツールの利用にはニコニコのプレミアム会員アカウントが必要です。**
  - 番組の予約、30分以上の配信にはプレミアム会員であることが必須です。
  - 番組の配信自体は一般会員でも可能ですが、上記の制限により、**このツールをニコニコの一般会員アカウントで利用することはできません。**
- 番組の予約にはニコニコ側のユーザー生放送の制限がかかります。  
  - ユーザー生放送の最大配信時間は6時間までです。6時間以降は番組を分割して予約します。
  - **同一時間に同じユーザーで複数のコミュニティの番組を予約することはできません。**
- ini 内のログイン情報を変更したときは、`cookie.dump` を一旦削除してから JKLiveReserver を実行してください。
  - `cookie.dump` はニコニコのログイン情報 (Cookie) を保存しているファイルで、このファイルがあるとセッションが切れるまで再ログインを行いません。

## インストール

[こちら](https://github.com/tsukumijima/JKLiveReserver/releases) のリリースから、［Source code (zip)］をクリックして Zip ファイルをダウンロードします。  
ダウンロードできたら解凍し、適当なフォルダに配置します。なお、`C:\Program Files` 以下のフォルダに配置するのは避けてください。

### 設定

JKLiveReserver を使う前には設定が必要です。まずは `JKLiveReserver.example.ini` を `JKLiveReserver.ini` へコピーしましょう。

その後、`JKLiveReserver.ini` を編集します。  
編集箇所は ニコニコにログインするメールアドレス・ニコニコにログインするパスワードの 2 つです。

`nicologin_mail` / `nicologin_password` にそれぞれニコニコにログインするメールアドレス / パスワードを指定します。前述の通り、基本的にプレミアムアカウントのログイン情報が必要です。

これで設定は完了です。

### 実行方法

JKLiveReserver は Python スクリプトですが、わざわざ Python の実行環境をセットアップするのも手間だと思うので、単一の実行ファイルにビルドしたものを同梱しています。  
`JKLiveReserver.exe` は Windows 用、拡張子なしの `JKLiveReserver` は Linux 用の実行ファイルです。手軽で基本環境依存もないので、実行ファイルの方を使うことを推奨します。  
また、`JKLiveScheduler.exe` は Windows 用のタスクスケジューラに JKLiveReserver の自動実行タスクを登録するツールです。

今後の手順では Windows 環境で `JKLiveReserver.exe` を使うことを前提に説明します。  
このほか Linux 環境では、実行する前に `chmod a+x ./JKLiveReserver` で拡張子なしの `JKLiveReserver` に実行許可を付与しておく必要があるかもしれません。

`build.sh` を WSL で実行すれば実行ファイルを自ビルドできますが、PyInstaller と依存ライブラリ等が Windows と WSL 側両方に入っている事が前提のため、他の環境でビルドできるかは微妙です。

## 使い方

### (Windows) JKLiveScheduler でタスクスケジューラに登録して使う

一番簡単な使い方です。よくわからない方はまずはこの使い方で試してみてください。  
一度 JKLiveScheduler で登録してしまえば、あとは指定した曜日の時間に PC を起動しておきさえすれば、**毎週全自動で指定した実況チャンネルの1週間分の実況枠が予約されます。**

#### 1. タスクの登録・変更

<img width="482" alt="727" src="https://user-images.githubusercontent.com/39271166/115193769-8c9fa000-a127-11eb-956c-6d2d038a4c1a.png">

まずはタスクを登録しましょう。  
[タスクの操作] で 1 を入力します。入力したら、Enter キーで確定します。以降も同様に操作します。

-----

最初に、実況枠を予約する実況チャンネルの ID（ jk101・jk222・jk333 のような形式の ID ）を入力します。コミュニティの ID ではないので注意してください。  
指定できる実況チャンネル ID・コミュニティ ID・チャンネル名 の対照は下記を参照してください。  
<small>（開発者向け）実況チャンネル ID・コミュニティ ID・チャンネル名 は [こちら](https://github.com/tsukumijima/JKLiveReserver/blob/main/JKLive.py#L13-L40) のコードにて定義されています。</small>

| 実況チャンネル ID | コミュニティ ID | チャンネル名 |
| ---- | ---- | ---- |
| jk10 | [co5253063](https://com.nicovideo.jp/community/co5253063) |  テレ玉 |
| jk11 | [co5215296](https://com.nicovideo.jp/community/co5215296) |  tvk |
| jk12 | [co5359761](https://com.nicovideo.jp/community/co5359761) |  チバテレビ |
| jk101 | [co5214081](https://com.nicovideo.jp/community/co5214081) |  NHK BS1 |
| jk103 | [co5175227](https://com.nicovideo.jp/community/co5175227) |  NHK BSプレミアム |
| jk141 | [co5175341](https://com.nicovideo.jp/community/co5175341) |  BS日テレ |
| jk151 | [co5175345](https://com.nicovideo.jp/community/co5175345) |  BS朝日 |
| jk161 | [co5176119](https://com.nicovideo.jp/community/co5176119) |  BS-TBS |
| jk171 | [co5176122](https://com.nicovideo.jp/community/co5176122) |  BSテレ東 |
| jk181 | [co5176125](https://com.nicovideo.jp/community/co5176125) |  BSフジ |
| jk191 | [co5251972](https://com.nicovideo.jp/community/co5251972) |  WOWOW PRIME |
| jk192 | [co5251976](https://com.nicovideo.jp/community/co5251976) |  WOWOW LIVE |
| jk193 | [co5251983](https://com.nicovideo.jp/community/co5251983) |  WOWOW CINEMA |
| jk222 | [co5193029](https://com.nicovideo.jp/community/co5193029) |  BS12 |
| jk236 | [co5296297](https://com.nicovideo.jp/community/co5296297) |  BSアニマックス |
| jk333 | [co5245469](https://com.nicovideo.jp/community/co5245469) |  AT-X |

-----

次に、実況枠を予約する曜日を入力します。  
曜日は 日・月・火・水・木・金・土 から選んで入力します。

この項目で指定した曜日に PC を起動しておく必要があるので、各自「この日なら PC を起動しているだろう」という曜日にしておくと良いでしょう。PC が起動しているのなら、どの曜日でも構いません。

-----

最後に、実況枠を予約する時間を入力します。  
時間は 09:15・13:00・21:30 のように入力します。

先ほど指定した曜日の、この項目で指定した時間に PC を起動しておく必要があるので、各自「この時間なら PC を起動しているだろう」という時間にしておくと良いでしょう。  
アニメ実況されている方であれば、実況のために PC を起動している深夜時間帯が良いかもしれません。

-----

その後、「タスクの登録に成功しました」と表示されていれば、タスクが正しく登録できています。お疲れさまでした！

基本失敗することはないと思う（入力した値が正しくない場合は再入力を求められる）のですが、もし失敗した場合はエラーメッセージも同時に表示されるので、その内容を確認してみてください。

#### 2. タスクを今すぐ実行

<img width="482" alt="728" src="https://user-images.githubusercontent.com/39271166/115193783-8f9a9080-a127-11eb-95e0-d5d270cd4192.png">

タスクを登録したら、実際に予約してみましょう。  
[タスクの操作] で 2 を入力します。入力したら、Enter キーで確定します。

「タスクの実行に成功しました」と表示されていれば、登録したタスクが実行できています。失敗した場合は、タスクが正しく登録できていないものと考えられます。

実行ログは `JKLiveReserver.exe` と同じフォルダの `JKLiveReserver.log` に出力されます。  
タスクはバックグラウンドで実行されるので、1分ほど待ってから `JKLiveReserver.log` をメモ帳やお好みのエディタなどで確認してください。

全ての番組が「番組の予約に成功しました」になっていれば、1週間分の実況枠が正しく予約できています！  
「番組の予約に失敗しました」になっている場合はエラーメッセージも出力されているので、適宜対応を行ってください。  
「メールアドレスとパスワードが間違っていてログインできない」「枠取りを行うコミュニティを枠取りに使うアカウントでフォローしていない」などがありがちなミスだと思います。  
また、予約を行う時間に同じコミュニティで別のユーザーが予約している場合も失敗します（その場合、被っていない時間の予約は成功します）。

#### 3. タスクの削除

<img width="482" alt="729" src="https://user-images.githubusercontent.com/39271166/115193790-92958100-a127-11eb-880d-385d6ff19e1e.png">

あまり使う機会はないとは思いますが、タスクを削除することもできます。  
[タスクの操作] で 3 を入力します。入力したら、Enter キーで確定します。

「タスクの削除に成功しました」と表示されていれば、登録したタスクが削除できています。失敗した場合は、タスクがそもそも登録されていないものと考えられます。

### (Linux) Crontab に登録して使う（上級者向け）

執筆中…

### 手動で実行して使う

執筆中…

## License
[MIT License](License.txt)
