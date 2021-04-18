#!/bin/bash

# WSL で作業していて、かつ Windows 側にも Python の環境があり、
# さらに requirements.txt 内のライブラリが全て入っていることが条件

# Windows 版バイナリをビルド
pwsh.exe -Command pyinstaller JKLiveReserver.py --onefile --exclude-module numpy --exclude-module pandas
mv dist/JKLiveReserver.exe JKLiveReserver.exe
chmod a+x JKLiveReserver.exe

pwsh.exe -Command pyinstaller JKLiveScheduler.py --onefile --exclude-module numpy --exclude-module pandas
mv dist/JKLiveScheduler.exe JKLiveScheduler.exe
chmod a+x JKLiveScheduler.exe

# Linux 版バイナリをビルド
pyinstaller JKLiveReserver.py --onefile --exclude-module numpy --exclude-module pandas
mv dist/JKLiveReserver JKLiveReserver
chmod a+x JKLiveReserver
