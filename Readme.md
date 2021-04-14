
# JKLiveReserver

ニコニコ実況用の番組を CLI で予約するツールです。

## 注意

- このツールの利用には基本的にニコニコのプレミアムアカウントが必要です。  
  - 30分以上の生放送を行うためにはニコニコのプレミアムアカウントが必須です。  
- 生放送を行う際にはニコニコ側のユーザー生放送の制限がかかります。  
  - ユーザー生放送の最大配信時間は6時間までです。
  - 同一時間に同じユーザーで複数の配信はできません。
- ini 内のログイン情報を変更したときは、cookie.dump を一旦削除してから JKLiveReserver を実行してください。
  - cookie.dump は Cookie を保存しているファイルで、このファイルがあるとセッションが切れるまで再ログインを行いません。

## インストール

[ここ](https://github.com/tsukumijima/JKLiveReserver/releases)からダウンロードします。  
あるいは、GitHub の画面内にある緑色の［Code］ボタンをクリックすると［Download Zip］ボタンが表示されるので、ボタンをクリックしてダウンロードします。

ダウンロードできたら解凍し、適当なフォルダに配置します。

### 設定

JKLiveReserver を使う前には設定が必要です。まずは JKLiveReserver.example.ini を JKLiveReserver.ini にコピーしましょう。

その後、JKLiveReserver.ini を編集します。  
編集箇所は ニコニコにログインするメールアドレス・ニコニコにログインするパスワードの 2 つです。

nicologin_mail / nicologin_password にそれぞれニコニコにログインするメールアドレス / パスワードを指定します。  
前述の通り、基本的にプレミアムアカウントのログイン情報が必要です。

これで設定は完了です。

### 実行方法

JKLiveReserver は Python スクリプトですが、わざわざ環境をセットアップするのも少し手間かなと思ったので、単一の実行ファイルにまとめたものも同梱しています。  
JKLiveReserver.exe は Windows 用、拡張子なしの JKLiveReserver は Linux 用の実行ファイルです。  
こちらのバイナリを使ったほうが手軽ですが、一方で特に Windows の場合、Python から普通に実行するときと比べ起動に数秒時間がかかるというデメリットもあります。  
このほか Linux 環境では、ツールを実行する前に `chmod` で JKLiveReserver ファイルに実行許可を付与しておく必要があるかもしれません。

Python から普通に実行する場合は、別途依存ライブラリのインストールが必要です。  
`pip install -r requirements.txt` ( pip が Python2 の事を指すシステムの場合は pip3 ) と実行し、依存ライブラリをインストールします。  
Python 3.8 で検証しています。Python 2 系は論外として、3.8 未満のバージョンでは動かないかもしれません。

build.sh を実行すればバイナリを自ビルドできますが、PyInstaller と依存ライブラリ諸々が Windows と WSL 側両方に入っている事が前提のため、他の環境でビルドできるかは微妙です。

## License
[MIT License](License.txt)

