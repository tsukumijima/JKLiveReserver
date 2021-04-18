
# JKLiveReserver

ニコニコ実況用のコミュニティ番組を一括で予約（枠取り）するツールです。

## 注意

- このツールの利用にはニコニコのプレミアム会員アカウントが必要です。  
  - 番組の予約、30分以上の配信にはプレミアム会員であることが必須です。
  - 番組の配信自体は一般会員でも可能ですが、上記の制限により、このツールをニコニコの一般会員アカウントで利用することはできません。
- 番組の予約にはニコニコ側のユーザー生放送の制限がかかります。  
  - ユーザー生放送の最大配信時間は6時間までです。6時間以降は番組を分割して予約します。
  - 同一時間に同じユーザーで複数のコミュニティで配信することはできません。
- ini 内のログイン情報を変更したときは、`cookie.dump` を一旦削除してから JKLiveReserver を実行してください。
  - `cookie.dump` は Cookie を保存しているファイルで、このファイルがあるとセッションが切れるまで再ログインを行いません。

## インストール

[こちら](https://github.com/tsukumijima/JKLiveReserver/releases) のリリースから、［Source code］をクリックしてダウンロードします。  
ダウンロードできたら解凍し、適当なフォルダに配置します。なお、`C:\Program Files` と `C:\Users` 以下に配置するのは避けてください。

### 設定

JKLiveReserver を使う前には設定が必要です。まずは `JKLiveReserver.example.ini` を `JKLiveReserver.ini` にコピーしましょう。

その後、`JKLiveReserver.ini` を編集します。  
編集箇所は ニコニコにログインするメールアドレス・ニコニコにログインするパスワードの 2 つです。

`nicologin_mail` / `nicologin_password` にそれぞれニコニコにログインするメールアドレス / パスワードを指定します。  
前述の通り、基本的にプレミアムアカウントのログイン情報が必要です。

これで設定は完了です。

### 実行方法

JKLiveReserver は Python スクリプトですが、わざわざ Python の実行環境をセットアップするのも手間だと思うので、単一の実行ファイルにまとめたものを同梱しています。  
`JKLiveReserver.exe` は Windows 用、拡張子なしの `JKLiveReserver` は Linux 用の実行ファイルです。

手軽で基本環境依存もないので、基本的には実行ファイルの方を使うことを推奨します。今後の手順では `JKLiveReserver.exe` を使うことを前提に説明します。
このほか Linux 環境では、ツールを実行する前に `chmod` で拡張子なしの `JKLiveReserver` に実行許可を付与しておく必要があるかもしれません。

（非推奨）Python から普通に実行する場合は、別途依存ライブラリのインストールが必要です。  
`pip install -r requirements.txt` ( pip が Python2 の事を指すシステムの場合は pip3 ) と実行し、依存ライブラリをインストールします。  
Python 3.8 で検証しています。Python 2 系は論外として、3.8 未満のバージョンでは動かないかもしれません。  

`build.sh` を WSL で実行すれば実行ファイルを自ビルドできますが、PyInstaller と依存ライブラリ諸々が Windows と WSL 側両方に入っている事が前提のため、他の環境でビルドできるかは微妙です。

## 使い方

### (Windows) JKLiveScheduler でタスクスケジューラに登録して使う

執筆中…

### (Linux) Crontab に登録して使う

執筆中…

### 手動で実行して使う

執筆中…

## License
[MIT License](License.txt)
