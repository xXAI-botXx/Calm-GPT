<h1 style="text-align:center">Kivy Deployment</h1>



This project using Kivy to create an mobile implementation of the nice-bot.

### Features:
- [x] History
- [x] Sound
- [x] Focus on current message
- [x] load screen
- [x] better colors orange and blue (like in picture)
- [x] Bot parallel (no new message during loading)
- enter for sending a message
- make the model offline available (also the tokenizer)
- [x] min width and height
- [x] add windows icon and add name
- add dynamic background (color changing?)
- transfer to android (playstore version)
- [x] Increase Output-Size
- [x] Upgrade to V6 model



### Kivy2Android

1. Install Ubtuntu from Windows Store
2. Activate "VM-Plattform" and "Windows-Subsystem für Linux" in Windows-Features
3. Download latest Linux-Kernel-Updates [see here](https://learn.microsoft.com/de-de/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)
4. Start Ubuntu App and type user-name and passport as the app asks
5. update installing manager "sudo apt update"
6. Install Git "sudo apt-get install git"
7. Clone buildozer repo "git clone https://github.com/kivy/buildozer.git"
8. Install python and PyPI "sudo apt install python3 python3-pip ipython3"
9. Install cython "sudo apt install cython3"
10. Install auto-conf "sudo apt-get install autoconf"
11. Install Java "sudo apt-get install openjdk-8-jdk"
12. Install some additional libraries "sudo apt install build-essential libltdl-dev libffi-dev libssl-dev libboost-python-dev"
13. Install unzip "sudo apt-get install unzip"
14. Install unzip "sudo apt-get install zip"
15. Install/Upgrade  cypthon "sudo pip3 install --upgrade cython"
16. Copy your project to your VM environment (with the explorer or with git clone or else) and check it with "ls"
17. Install buildozer
    1. cd buildozer
    2. sudo python3 setup.py install
    3. cd ..
18. Run buildozer on project
    1. cd calm-bot (your-project-folder name)
    2. sudo buildozer init
19. Modify the buildozer.spec file
    1. source.include_exts = py,png,jpg,kv,atlas,pt,mp3,jpeg,json,safetensors,txt,md
    2. requirements = python3,kivy,kivymd,torch,transformers
    3. presplash.filename = %(source.dir)s/data/logo.jpeg
    4. icon.filename = %(source.dir)s/data/logo.jpeg
    5. osx.kivy_version = 2.3.0
    6. android.logcat_filters = *:S python:D
20. Now run buildozer (we are in the prject folder)
    1. hint: for cleaning use: sudo buildozer android clean
    2. sudo buildozer android debug
    3. sudo apt-get install -y autoconf automake build-essential libtool
    4. sudo apt-get install libffi-dev
    5. sudo pip3 install cython==0.29.26
    6. sudo pip3 install --upgrade jnius
    7. sudo buildozer android update
    8. sudo pip3 install certifi
    9. sudo apt install gradle
21. Other steps:
    1. sudo apt update
    2. sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    3. pip3 install --user --upgrade Cython==0.29.33 virtualenv  # the --user should be removed if you do this in a venv
    4. export PATH=$PATH:~/.local/bin/
    5. add following line to buildozer.spec file:
       - android.gradle_dependencies = 'classpath com.android.tools.build:gradle:4.1.0'
    6. sudo apt install default-jdk
22. Update Gradle
    1. sudo add-apt-repository ppa:cwchien/gradle
    2. sudo apt-get update
    3. sudo apt upgrade gradle

23. Debug with:
    1. sudo buildozer android clean
    2. sudo buildozer android debug




> Use 'apt search packagename*' if some package is not available and find a alternative.



> You may find help here: https://github.com/Android-for-Python/Android-for-Python-Users#unsupported-class-file-major-version-62




### Ressources:
- https://www.youtube.com/watch?v=RpaMF9upgtQ
- https://www.youtube.com/watch?v=p3tSLatmGvU
- https://www.youtube.com/watch?v=_g4BiBcYdZQ
- https://www.youtube.com/watch?v=Miydkti_QVE
- https://www.youtube.com/watch?v=iM3kjbbKHQU (tkinter)

