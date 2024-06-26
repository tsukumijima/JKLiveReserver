
# JKLiveReserver

ニコニコ実況用のコミュニティ番組を一括で自動予約（枠取り）するツールです。

## 概要

このツールを使うことで、**最大1週間分、指定した実況チャンネル (ex: jk161) の実況用番組を一気に自動で予約することができます！**  
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
つまり、**24 時間全自動で枠取りをする場合、実況チャンネルにつき 1 つのプレミアム会員アカウントが必要になります。**

現在存在するコミュニティチャンネル全てで 24 時間常に実況枠を確保するのなら、**事実上プレミアム会員アカウントを持っている最低 18 人の協力が必要です。**

> [!NOTE]
> 全自動枠取りをしない場合でも、BS 実況が盛り上がる時間帯はアニメが多く放送される深夜に集中しているため、実況チャンネルにつき 1 つのプレミアム会員アカウントが必要な事には変わりません。
> 
> たとえば BS日テレの実況枠を 2021/04/19 22:00～24:00 まで予約した場合、同じユーザーで BS-TBS の実況枠を 2021/04/19 23:00～25:00 まで予約することはできません。23:00 ～ 24:00 の間、BS日テレの実況枠と時間が重複しているためです。

現状、BSを始めとするニコニコ実況のコミュニティチャンネルの一部は有志による手動での枠取り（基本的には人が集まる時間帯の番組のみ）によってなんとか存続しています。  
しかし、多忙だったり、あるいは単に忘れていたりして、今後実況したいときに枠がない、といったことも考えられます。  
また、手動で枠取りしている関係で、24 時間常に実況枠を確保し続けることは難しいのが現状です。

プレミアム会員アカウントを持っていて、生主ではない方なら誰でも枠取りに参加できます。  
**ぜひ、公式実況チャンネル以外のニコニコ実況の安定した存続のため、皆さんのご協力をお願いします！**

> [!TIP]
> **2024/03/21 現在、コミュニティチャンネルのうち テレ玉・tvk・BS日テレ・BS朝日・BS-TBS・BSテレ東・BSフジ・BS松竹東急・AT-X の 9 チャンネルで 24 時間全自動で枠取りが行われています。**

**また、協力していただける方はぜひ [Discord コミュニティ](https://discord.gg/frJ9aYhaaM) へ参加してください！** 更新通知や連絡事項などをお知らせします。

## 注意

- **このツールの利用にはニコニコのプレミアム会員アカウントが必要です。**
  - **番組の配信予約、30分以上の配信にはプレミアム会員であることが必須のためです。**
  - 番組の配信自体は一般会員でも可能ですが、上記の制限により、**このツールをニコニコの一般会員アカウントで利用することはできません。**
- 番組の予約にはニコニコ側のユーザー生放送の制限がかかります。  
  - ユーザー生放送の最長放送可能時間は12時間までです。12時間以降は 04:00～16:00・16:00～04:00 のように番組を分割して予約します。
    - 2024年2月のニコニコ生放送の [仕様変更](https://blog.nicovideo.jp/niconews/213237.html) で最長放送可能時間が6時間から12時間に増加しました。
  - **同じユーザーで同一時間帯に複数のコミュニティの番組を予約することはできません。**
- ini 内のログイン情報を変更したときは、`cookie.dump` を一旦削除してから JKLiveReserver を実行してください。
  - `cookie.dump` はニコニコのログイン情報 (Cookie) を保存しているファイルです。このファイルがある時は、セッションが切れるまで再ログインを行いません。
- **2段階認証が有効化されたアカウントではログインに失敗します。お手数ですが、2段階認証を解除してください。**
- 番組を予約してそのまま真っ黒な画面を垂れ流しているだけとはいえ、一応システム上は生主ということになります。
  - そのため、しばらく枠取りを続けていると、ニコ生関連のバッジが増えたりニコニ広告のチケットが山程降ってきたりするみたいです。
- **自動枠取りを行っているチャンネルで、枠取りしているのと同じアカウントを使って実況（コメントを投稿）すると放送者コメント扱いになります。**
  - このため、**コメントは運営コメントのように上部に固定表示、コメントリスト上では赤文字になってしまいます。**
  - これを避けたいのなら、枠取りに使っていない別のアカウント（一般会員アカウントなど）でログインして実況するなどの一工夫が必要になります。
    - 公式実況チャンネルの場合、一般会員だとまれに追い出される事がありますが、そもそも BS 実況は人が地デジと比べると少なく旧実況でいう祭の状態になりにくいので、実際には追い出しはほぼ起きないと思います。少々面倒くさいのは事実ですが…
    - あまり見ない（実況しない）であろうコミュニティチャンネルで枠取りをするか、別アカウントを実況のメインにするかなど、適宜自分に合った方法で対応してください。

## インストール

<img width="650" src="https://user-images.githubusercontent.com/39271166/115256891-972f5900-a16a-11eb-8484-6094549a1654.png"><br>

[こちら](https://github.com/tsukumijima/JKLiveReserver/releases) のリリースから、最新のバージョンの［Source code (zip)］をクリックして、Zip ファイルをダウンロードします。

ダウンロードできたら解凍し、好きなフォルダに配置します。なお、`C:\Program Files` 以下のフォルダに配置するのは避けてください。

いろいろファイルがありますが、実際に触ることになるのは基本的に `JKLiveReserver.exe` (Windows) `JKLiveReserver` (Linux)・`JKLiveReserver.example.ini`・`JKLiveScheduler.exe` の 4 つだけです。

### 設定

<img width="650" src="https://user-images.githubusercontent.com/39271166/115255773-8df1bc80-a169-11eb-9029-8c4ff5b7461e.png">

JKLiveReserver を使う前には設定が必要です。まずは `JKLiveReserver.example.ini` を `JKLiveReserver.ini` へコピーしましょう。  

> [!NOTE]
> 具体的には、エクスプローラーで `JKLiveReserver.example.ini` を選択し、Ctrl + C を押した後続けて Ctrl + V を押すと、`JKLiveReserver.example- コピー.ini` が作成されます。  
> そのあと `JKLiveReserver.example- コピー.ini` を選択し、F2 キーを押してファイル名を編集できるようにし、入力欄に `JKLiveReserver.ini` を入力して Enter で確定します。  
> すると、`JKLiveReserver.example- コピー.ini` が `JKLiveReserver.ini` にリネームされるので、このファイルを編集していきます。

その後、`JKLiveReserver.ini` を編集します。  
編集箇所は ニコニコにログインするメールアドレス・ニコニコにログインするパスワード の 2 つです。

> [!TIP]
> お好きなテキストエディタがあれば全然それを使っていただいて構いません。  
> 特にテキストエディタを別途インストールしていない方は、  
> `JKLiveReserver.ini` を右クリックし [編集] をクリックするとメモ帳が開くので、そのメモ帳で編集してください。Ctrl + S を押すと保存できます。

-----

`nicologin_mail` / `nicologin_password` に、それぞれニコニコにログインするメールアドレス / パスワードを指定します。前述の通り、基本的にプレミアムアカウントのログイン情報が必要です。

> [!IMPORTANT]
> メールアドレスは `example@example.com` の部分を、パスワードは `example_password` の部分をそれぞれ自分のメールアドレスとパスワードに書き換えてください。

-----

`commentfilter_enabled` に、予約する番組でAIコメントフィルターを有効にするかどうかを `True` (有効)・`False` (無効) で指定します。
特別な理由がない限りは有効のままにしておくことを推奨します。基本的に編集する必要はありません。

-----

`tagedit_enabled` に、予約する番組でタグ編集を有効にするかどうかを `True` (有効)・`False` (無効) で指定します。
タグ荒らしがいるなどでなければ有効のままにしておくことを推奨します。こちらも基本的に編集する必要はありません。

-----

これで設定は完了です！

このほか、**事前に枠取りを行うコミュニティをフォローしておいてください！**  
枠取りを行うコミュニティをフォローしておかないと、「指定されたコミュニティでの放送権がありません」というエラーで枠取りに失敗します。

### 実行方法

> [!TIP]
> **要約: よくわからない方は JKLiveScheduler.exe を使う事をおすすめします。**

JKLiveReserver は Python スクリプトですが、わざわざ Python の実行環境をセットアップするのも手間なので、単一の実行ファイルにビルドした実行ファイルを同梱しています。

`JKLiveReserver.exe` は Windows 用、拡張子なしの `JKLiveReserver` は Linux 用の実行ファイルです。手軽で基本環境依存もないので、実行ファイルの方を使うことを推奨します。  
`JKLiveScheduler.exe` は、Windows 用のタスクスケジューラに JKLiveReserver の自動実行タスクを登録するツールです。

今後の手順では Windows 環境で `JKLiveReserver.exe` を使うことを前提に説明します。  
このほか Linux 環境では、実行する前に `chmod a+x ./JKLiveReserver` で拡張子なしの `JKLiveReserver` に実行許可を付与しておく必要があるかもしれません。

## 使い方

### (Windows) JKLiveScheduler でタスクスケジューラに登録して使う

一番簡単な使い方です。よくわからない方はまずはこの使い方で試してみてください。  
一度 JKLiveScheduler で登録してしまえば、あとは指定した曜日の時間に PC を起動しておきさえすれば、**毎週全自動で指定した実況チャンネルの1週間分の実況枠が予約されます。**

`JKLiveScheduler.exe` をダブルクリックします。  
「このアプリがデバイスに変更を加えることを許可しますか？」というダイヤログが表示されるので [はい] をクリックすると、以下の画像のように JKLiveScheduler の黒いウインドウが開きます。

#### 1. タスクの登録・変更

<img width="650" src="https://user-images.githubusercontent.com/39271166/117067817-70c20e00-ad65-11eb-9095-3be4eb3a88dd.png"><br>

まずはタスクを登録しましょう。タスクを登録すると、 JKLiveReserver が毎週自動で1週間分の実況枠を予約してくれるようになります。  
[タスクの操作] で 1 を入力します。入力したら、Enter キーで確定します。以降も同様に操作します。

-----

最初に、実況枠を予約する実況チャンネルの ID（ `jk161`・`jk222`・`jk333` のような形式の ID ）を入力します。コミュニティの ID ではないので注意してください。  
指定できる実況チャンネル ID・コミュニティ ID・チャンネル名 の対照は下記を参照してください。  

>（開発者向け）実況チャンネル ID・コミュニティ ID・チャンネル名 は [こちら](https://github.com/tsukumijima/JKLiveReserver/blob/main/JKLive.py#L13-L39) のコードにて定義されています。
> 以下の表にないコミュニティチャンネルを追加したい場合は [Issues](https://github.com/tsukumijima/JKLiveReserver/issues) までお願いします。

| 実況チャンネル ID | コミュニティ ID | チャンネル名 |
| ---- | ---- | ---- |
| jk10 | [co5253063](https://com.nicovideo.jp/community/co5253063) |  テレ玉 |
| jk11 | [co5215296](https://com.nicovideo.jp/community/co5215296) |  tvk |
| jk12 | [co5359761](https://com.nicovideo.jp/community/co5359761) |  チバテレビ |
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
| jk252 | [co5683458](https://com.nicovideo.jp/community/co5683458) |  WOWOW PLUS |
| jk260 | [co5682554](https://com.nicovideo.jp/community/co5682554) |  BS松竹東急 |
| jk263 | [co5682551](https://com.nicovideo.jp/community/co5682551) |  BSJapanext |
| jk265 | [co5682548](https://com.nicovideo.jp/community/co5682548) |  BSよしもと |
| jk333 | [co5245469](https://com.nicovideo.jp/community/co5245469) |  AT-X |

-----

次に、実況枠を予約する曜日を入力します。  
曜日は `日`・`月`・`火`・`水`・`木`・`金`・`土` から選んで入力します。  
`全` と入力すると、全ての曜日で毎日実況枠を予約します。

この項目で指定した曜日に PC を起動しておく必要があるので、各自「この日なら PC を起動しているだろう」という曜日にしておくと良いでしょう。PC が起動しているのなら、どの曜日でも構いません。  
もし毎日常時 PC を起動しているのなら、`全` と入力して毎日予約するのもありです。

-----

最後に、実況枠を予約する時間を入力します。  
時間は `09:15`・`13:00`・`21:30` のように入力します。

先ほど指定した曜日の、この項目で指定した時間に PC を起動しておく必要があるので、各自「この時間なら PC を起動しているだろう」という時間にしておくと良いでしょう。  
アニメ実況されている方であれば、実況のために PC を起動している深夜時間帯が良いかもしれません。

-----

その後、「タスクの登録に成功しました」と表示されていれば、タスクが正しく登録できています。お疲れさまでした！

基本失敗することはないと思う（入力した値が正しくない場合は再入力を求められる）のですが、もし失敗した場合はエラーメッセージも同時に表示されるので、その内容を確認してみてください。

> [!TIP]
> 予約した番組のタイトルは、自動的に `BS日テレ【ニコニコ実況】2021年04月20日 04:00～10:00` のように設定されます。

> [!TIP]
> 予約した番組の概要欄は、公式実況チャンネルのフォーマットにならい、公式実況チャンネルも含めた全ての実況チャンネルの一覧がチャンネル/コミュニティページへのリンクをつけて設定されます。

> [!TIP]
> 予約した番組のタグは、公式実況チャンネルのタグにならい、`ニコニコ実況`, `テレビ実況`, `実況`, `雑談` と、指定した実況チャンネルの名前（スペースを含む場合はアンダースコアに置換）が設定されます。

#### JKLiveReserver の実行時間になったら PC のスリープを解除する

JKLiveScheduler からタスクを登録した時点で、すでに「タスクを実行するためにスリープを解除する」ようにタスクスケジューラに設定してあります。  
ただノートパソコンでは、**別途 PC のスリープ関連の設定を変更しないと、スリープが解除されないことがあります。**

コントロールパネルを開き（ Windows の検索窓に「コントロール」と入れると出てきます）、`ハードウェアとサウンド` > `電源オプション` に移動します。  
ノートパソコンなら、タスクバー右下の電池アイコンを右クリックでもいけます。

次に、`プラン設定の変更` をクリックし、出てきた画面で `詳細な電源設定の変更` をクリックします。

<img width="350" src="https://user-images.githubusercontent.com/39271166/115280098-7ffc6580-a182-11eb-85d0-03b7d2f990a8.png"><br>

様々な項目がありますが、`スリープ` > `スリープ解除タイマーの許可` を開きます。

ノートパソコンの場合は `バッテリ駆動` と `電源に接続` の下に、デスクトップ PC の場合は単に `有効`・`無効`・`重要なスリープ解除タイマーのみ` のいずれかが表示されているはずです。
これを `有効` に変更する必要があります。すでに `有効` になっているのならそのままで OK です。  

> `重要なスリープ解除タイマーのみ` になっている場合も `有効` に変更してください。

> 実況枠を取るときはたいていノートパソコンでも電源に接続しているときでしょうから、バッテリ駆動の方は無効のままでもよいと思います。

> 残念ながら、ごく一部のノートパソコンでは設定を変更してもスリープ解除ができない事があるみたいです。  
> その場合はお手数ですが、適宜自動でスリープしないようにするなどの対策をお願いします。

以上で完了です。

#### 2. タスクを今すぐ実行

<img width="650" src="https://user-images.githubusercontent.com/39271166/115193783-8f9a9080-a127-11eb-95e0-d5d270cd4192.png"><br>

タスクを登録したら、今すぐ実際に予約してみましょう。JKLiveReserver を使ってすぐに1週間分の実況枠を予約することができます。  
`JKLiveScheduler.exe` をもう一度ダブルクリックします。[タスクの操作] で 2 を入力します。入力したら、Enter キーで確定します。

「タスクの実行に成功しました」と表示されていれば、登録したタスクが実行できています。失敗した場合は、タスクが正しく登録できていないものと考えられます。

実行ログは `JKLiveReserver.exe` と同じフォルダの `JKLiveReserver.log` に出力されます。  
タスクはバックグラウンドで実行されるので、1分ほど待ってから `JKLiveReserver.log` をメモ帳やお好みのエディタなどで確認してください。

全ての番組が「番組の予約に成功しました」になっていれば、1週間分の実況枠が正しく予約できています！  
タスクは先ほどの手順でスケジューリング済みのため、あとは基本何もしなくても指定した時刻に全自動で枠取りが行われるはずです。  

一部の番組が「番組の予約に失敗しました」になっている場合はエラーメッセージも出力されているので、適宜対応を行ってください。  
「メールアドレスとパスワードが間違っていてログインできない」「枠取りを行うコミュニティを枠取りに使うアカウントでフォローしていない」などがありがちなミスだと思います。

また、予約を行う時間に同じコミュニティで別のユーザーが予約している場合も失敗します。その場合、被っていない時間の予約は成功します。  
この他、ニコ生側でメンテナンスが予定されている時刻に被った場合も失敗します。これに関してはメンテナンスでニコ生自体が使えなくなるのでどうしようもない…。

> 毎日枠取りを実行する設定にした場合、「該当時間に同じユーザの別の放送予定があります」というエラーが出力されることがあります。  
> これは前日にも既に1週間分の枠取りを行っていることで、7日間（1週間）分のうち6日分の枠取りが前日分と重複してしまう事により起きるものです。異常ではないので、無視してください。

実際に実況枠が確保されているかどうかは、コミュニティページの [生放送] タブにて確認できます。

#### 3. タスクの削除

<img width="650" src="https://user-images.githubusercontent.com/39271166/115193790-92958100-a127-11eb-880d-385d6ff19e1e.png"><br>

あまり使う機会はないとは思いますが、タスクを削除することもできます。タスクを削除すると、今後は JKLiveReserver が自動で実況枠を予約しなくなります。  
[タスクの操作] で 3 を入力します。入力したら、Enter キーで確定します。

「タスクの削除に成功しました」と表示されていれば、登録したタスクが削除できています。失敗した場合は、タスクがそもそも登録されていないものと考えられます。

### (Linux) Crontab に登録して使う（上級者向け）

Linux で使う場合は、Crontab に登録すると、タスクスケジューラ同様に、指定した曜日の指定した時間に JKLiveReserver を実行することができます。  
Crontab の編集方法は割愛します。Linux を一通り操作できる時点で自己解決できるでしょうし…。

たとえば、水曜日の 21:30 にBS日テレの1週間分の実況枠を予約する場合は以下のようになります。  
あとは、お好きな方法で Crontab に登録するだけです。

```
30 21 * * WED /path/to/JKLiveReserver/JKLiveReserver jk141 --autorun-weekly --output-log
```

#### 解説

1. 実行する分が入ります。`30` は 30 分を意味します。
2. 実行する時間が入ります。`21` は 21 時を意味します。
3. 実行する日が入ります。`*` は全ての日を許容します。
4. 実行する月が入ります。`*` は全ての月を許容します。
5. 実行する曜日が入ります。`WED` は水曜日を意味します。
   - `0-6` の数字で指定することもできますが、`SUN,FRI` のように指定した方がわかりやすいです。
   - 曜日の省略表記は日～土がそれぞれ `MON,TUE,WED,THU,FRI,SAT,SUN` のようになります。
   - `*` を指定すると、全ての曜日で実行されます。
6. 実行するコマンドが入ります。
   - JKLiveReserver を実行したいので、JKLiveReserver バイナリのあるパスを指定します。
   - `/path/to/` の部分は適宜書き換えてください（分かっているとは思いますが）。
7. 実行する引数が入ります。
   - BS日テレの実況枠を取りたいので、`jk141 --autorun-weekly --output-log` を指定します。
   - `--autorun-weekly` オプションは毎週自動実行されているかどうかを JKLiveReserver に渡すためのオプションです。
     - 指定すると、予約した番組の説明欄に毎週指定された曜日（今回の場合は水曜日）に一括予約している旨を追記します。
     - 毎日自動実行されているかどうかを JKLiveReserver に渡す `--autorun-daily` オプションもあります。
   - `--output-log` オプションは実行ログを標準出力ではなく、JKLiveReserver バイナリと同じディレクトリの `JKLiveReserver.log` に書き出すオプションです。
     - JKLiveReserver ディレクトリへの書き込み権限がないとおそらく動作しません。

### 手動で実行して使う

24時間全て枠取りしたいわけではないが手動でポチポチ予約するのも面倒くさい… という場合に備え、（少しだけコマンド操作が必要ですが）手動で実行することもできます。

コマンドプロンプトまたは PowerShell を開き、JKLiveReserver のフォルダまで移動します。  
エクスプローラで JKLiveReserver のフォルダを開き、パス欄に `cmd` または `powershell` と入力するのが手っ取り早いと思います。Windows Terminal の方は `wt -d .` でも OK 。

引数などは以下のとおりです。

```
usage: JKLiveReserver [-h] [-d DATE] [-l LENGTH] [-o] [-v] Channel

ニコニコ実況用のコミュニティ番組を一括で予約（枠取り）するツール

必須の引数:
  Channel               予約する実況チャンネルのID (ex: jk161)

オプションの引数:
  -h, --help            このヘルプメッセージを表示して終了する
  -d DATE, --date DATE  予約する番組の開始時刻 (ex: 2021/04/15/04:00)
                        省略すると現在時刻以降の朝4時の日付に設定されます
  -l LENGTH, --length LENGTH
                        予約する番組の配信時間の長さ (時間単位) (ex: 24)
                        省略すると 168（7日間）に設定されます
                        最長放送可能時間が12時間までのため、12時間以降は番組を分割して予約します
  -aw, --autorun-weekly タスクスケジューラなどからの自動実行かどうか（毎週）
                        指定すると予約した番組の説明欄に毎週指定された曜日に自動で予約している旨を追記します
  -ad, --autorun-daily  タスクスケジューラなどからの自動実行かどうか（毎日）
                        指定すると予約した番組の説明欄に毎日自動で予約している旨を追記します
  -o, --output-log      実行ログをファイルに出力するかどうか
  -v, --version         バージョン情報を表示する
```

たとえば、2021/04/20 19:30 から 3 時間、BS-TBS の実況枠を予約し、結果のログをファイル ( `JKLiveReserver.log`) に出力する場合は以下のようになります。

```
.\JKLiveReserver.exe jk161 --date 2021/04/20/19:30 --length 3 --output-log
```

> 注意：`--output-log` オプションはコンソールへの出力自体をファイルに変更するため、コンソールでは何も表示されないまま終了します。

> `--date` オプションと `--length` オプションは両方必ず指定しないといけないわけではなく、どちらかを省略することもできます。  
> `--date` オプションは省略すると現在時刻以降の朝4時の日付に設定されます。  
> `--length` オプションは省略すると 168（7日間）に設定されます。

オプションを短縮して指定する場合は以下のようになります。

```
.\JKLiveReserver.exe jk161 -d 2021/04/20/19:30 -l 3 -o
```

別途 PowerShell・バッチファイル・シェルスクリプトなどを使い、毎日 22:00 から 23:00 までだけ予約する、といった高度な事もできると思います。

大方不具合は直したつもりですが、もし不具合を見つけられた場合は前述の Discord コミュニティか [Issues](https://github.com/tsukumijima/JKLiveReserver/issues) までお願いします。

## License
[MIT License](License.txt)
