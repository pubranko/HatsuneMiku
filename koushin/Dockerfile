FROM ubuntu:18.04

WORKDIR /root

# ロケール設定(pipenvでPipfile.lockを作るときにエラーで怒られた為)
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
# solrへの接続情報→ここでの定義廃止。docker run -eかdocker-compose側に移植
# ENV SOLR_URL=  SOLR_CORE=  SOLR_READ_USER=  SOLR_READ_PASS=

# shellをbashに指定
SHELL ["/bin/bash", "-c"]

# 最新状態へ
RUN apt update
RUN apt -y upgrade

# 必要なコマンドのインストール
# テスト環境の確認やら設定の実験等のためvim,systemdも追加
RUN apt -y install build-essential curl git zlib1g-dev libssl-dev libbz2-dev libreadline-dev libsqlite3-dev wget vim systemd

# nginxのインストール
RUN apt -y install nginx

# pythonまわりのインストール
RUN wget https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tgz && \
tar -zxvf Python-3.6.7.tgz && \
cd ./Python-3.6.7 && \
./configure && \
make && \
make install

RUN pip3 install --upgrade pip
RUN pip3 install pipenv
WORKDIR /tmp
COPY ./requirements.txt  ./requirements.txt
RUN pip3 install -r requirements.txt

# groupadd　-r:システムアカウント、-g：新しいグループ
# useradd   -r:システムアカウント、-g：ユーザーが所属するグループの指定、-G:新しいアカウントの補足グループのリスト
RUN groupadd -r nginx && \
    useradd -r -g nginx nginx && \
    groupadd -g 1000 uuuuu && \
    useradd  -g      uuuuu -G sudo -m -s /bin/bash uuuuu && \
    echo 'uuuuu:ppppp' | chpasswd && \
    echo 'Defaults visiblepw' >> /etc/sudoers && \
    echo 'iganari ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

#コード転送
WORKDIR /app
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./uwsgi.ini ./uwsgi.ini
COPY ./koushin ./koushin

#ライブラリのインストール(pipenv syncではNGらしい https://github.com/pypa/pipenv/issues/2650)
RUN pipenv install --deploy --system

EXPOSE 80

CMD uwsgi uwsgi.ini & nginx -g "daemon off;"