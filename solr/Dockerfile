#FROM openjdk:11-stretch
FROM ubuntu:latest

#LABELでメタ情報を入れることができる
#LABEL maintainer="Martijn Koster \"mak-docker@greenhills.co.uk\""
LABEL maintainer="test"
#LABEL repository="https://github.com/docker-solr/docker-solr"
LABEL repository="none"

# CLI 上から引数を代入するキーを指定するコマンド。 
# ARG <key> といった感じに書いておいて、 --build-arg <key>=<value> オプションで代入することで、 
# Dockerfile 内で の値は使い回しすることができる。
# 要は、dockerコマンドとdockerfile間で情報をやり取りするための変数を定義しているようだ。
# このサンプルでは、solr8.1.1がデフォルトだが、バージョンを変えることでダウンロード先のバージョンを指定できる。
# Override the solr download location with e.g.:
#   docker build -t mine --build-arg SOLR_DOWNLOAD_SERVER=http://www-eu.apache.org/dist/lucene/solr .
ARG SOLR_DOWNLOAD_SERVER

#　まずapt-getを最新化しているようだ。その後、必要なものをインストールしている。その後、不要なリスト？を消している。
#  javaの実行環境が足りなかったので、openjdk-8-jreを追加。
#  またテスト用にsudo treeを追加
RUN apt-get update && \
  apt-get -y install acl dirmngr gpg lsof procps wget openjdk-8-jre sudo tree && \
  rm -rf /var/lib/apt/lists/*

#環境変数をセットするコマンド。 Dockerfile 内で定義して以降、使い回したり、値を上書きできたりする。
ENV SOLR_USER="solr" \
    SOLR_UID="8983" \
    SOLR_GROUP="solr" \
    SOLR_GID="8983" \
    SOLR_VERSION="8.1.1" \
    SOLR_URL="${SOLR_DOWNLOAD_SERVER:-https://archive.apache.org/dist/lucene/solr}/8.1.1/solr-8.1.1.tgz" \
    SOLR_SHA256="b515598c11f53fe28d682e3d71238642e9f34509194e3c4746e39bb7d7bb46a1" \
    SOLR_KEYS="F23F054D9EC50F2397FF2B814E67A2711D053DDB" \
    PATH="/opt/solr/bin:/opt/docker-solr/scripts:$PATH" \
    SOLR_INCLUDE=/etc/default/solr.in.sh \
    SOLR_HOME=/var/solr/data \
    SOLR_PID_DIR=/var/solr \
    SOLR_LOGS_DIR=/var/solr/logs \
    LOG4J_PROPS=/var/solr/log4j2.xml

ENV GOSU_VERSION 1.11
ENV GOSU_KEY B42F6819007F00F88E364FD4036A9C25BF357DD4

#新規グループ・ユーザーを作成。 上の環境変数で指定されたid="8983"で"solr"がグループとユーザーになるようだ。
#-rでシステムユーザーを作っている。
#一時的にsudoユーザー(mikuras)を追加
RUN groupadd -r --gid "$SOLR_GID" "$SOLR_GROUP" && \
    useradd -r --uid "$SOLR_UID" --gid "$SOLR_GID" "$SOLR_USER" &&\
    groupadd -g 1000 USER && \
    useradd  -g      USER -G sudo -m -s /bin/bash USER && \
    echo 'USER:PASSWORD' | chpasswd && \
    echo 'Defaults visiblepw' >> /etc/sudoers && \
    echo 'iganari ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# set -e パイプやサブシェルで実行したコマンドが1つでもエラーになったら直ちにシェルを終了する。
# 次以降は、”gnupg”,"gpg"に関する設定のようだ。
# exportで環境変数"$GNUPGHOME"を定義。オーナーの権限をフル権限にしている。
# "disable-ipv6"の文字列を、"dirmngr.conf"に追記している。
RUN set -e; \
  export GNUPGHOME="/tmp/gnupg_home" && \
  mkdir -p "$GNUPGHOME" && \
  chmod 700 "$GNUPGHOME" && \
  echo "disable-ipv6" >> "$GNUPGHOME/dirmngr.conf" && \
  # SOLR_KEYSとGOSU_KEYを順に繰り返し処理
  # found変数を初期化
  # 3つのサーバーを順に繰り返し処理
  # hkpとは→keyserver.netなどのPGP公開鍵サーバーは、HKP(Howrowitz Key Protocol)と
  #          呼ばれるHTTP互換プロトコルを用いて鍵を検索（おそらく登録も）行うことが出来ます
  # gpg --batch→ --batch オプションを付けて起動することで対話モードを回避し，かつアルゴリズム等の詳細な指定をすることもできる。
  # gpg --keyserver→ 公開鍵を鍵サーバに送信する
  for key in $SOLR_KEYS $GOSU_KEY; do \
    found=''; \
    for server in \
      ha.pool.sks-keyservers.net \
      hkp://keyserver.ubuntu.com:80 \
      hkp://p80.pool.sks-keyservers.net:80 \
      pgp.mit.edu \
    ; do \
      echo "  trying $server for $key"; \
      gpg --batch --keyserver "$server" --keyserver-options timeout=10 --recv-keys "$key" && found=yes && break; \
      gpg --batch --keyserver "$server" --keyserver-options timeout=10 --recv-keys "$key" && found=yes && break; \
    done; \
    test -z "$found" && echo >&2 "error: failed to fetch $key from several disparate servers -- network issues?" && exit 1; \
  done; \
  exit 0

RUN set -e; \
  export GNUPGHOME="/tmp/gnupg_home" && \
  #githubより、対になっている必要なソースをダウンロード。
  #
  #※ .ascとは、PGPによって生成された公開鍵のファイルに付く拡張子のことである。
  pkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" && \
  wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$pkgArch" && \
  wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$pkgArch.asc" && \
  # gpg --verify→検証とは署名に使われた秘密鍵と対になっている公開鍵を使って, 署名されたファイルの差出人が確かに本人であること, 
  #               ファイルの内容が不正に改変されていないことを確かめる行為です.
  #               署名の検証は --verify コマンドで行えます
  # ここでは２ファイルを検証している。
  gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu && \
  #gosu.ascの方は検証後に削除
  rm /usr/local/bin/gosu.asc && \
  #
  chmod +x /usr/local/bin/gosu && \
  gosu nobody true && \
  #ここでsolrをダウンロードしている。
  echo "downloading $SOLR_URL" && \
  wget -nv "$SOLR_URL" -O "/opt/solr-$SOLR_VERSION.tgz" && \
  #solrのセキュリティー設定
  echo "downloading $SOLR_URL.asc" && \
  wget -nv "$SOLR_URL.asc" -O "/opt/solr-$SOLR_VERSION.tgz.asc" && \
  echo "$SOLR_SHA256 */opt/solr-$SOLR_VERSION.tgz" | sha256sum -c - && \
  (>&2 ls -l "/opt/solr-$SOLR_VERSION.tgz" "/opt/solr-$SOLR_VERSION.tgz.asc") && \
  #ここで署名の検証。問題なければ解凍。
  gpg --batch --verify "/opt/solr-$SOLR_VERSION.tgz.asc" "/opt/solr-$SOLR_VERSION.tgz" && \
  tar -C /opt --extract --file "/opt/solr-$SOLR_VERSION.tgz" && \
  (cd /opt && ln -s "solr-$SOLR_VERSION" solr) && \
  rm "/opt/solr-$SOLR_VERSION.tgz"* && \
  rm -Rf /opt/solr/docs/ && \
  #solr内のファイル・権限設定
  mkdir -p /opt/solr/server/solr/lib /docker-entrypoint-initdb.d /opt/docker-solr && \
  chown -R 0:0 "/opt/solr-$SOLR_VERSION" && \
  find "/opt/solr-$SOLR_VERSION" -type d -print0 | xargs -0 chmod 0755 && \
  find "/opt/solr-$SOLR_VERSION" -type f -print0 | xargs -0 chmod 0644 && \
  chmod -R 0755 "/opt/solr-$SOLR_VERSION/bin" && \
  cp /opt/solr/bin/solr.in.sh /etc/default/solr.in.sh && \
  mv /opt/solr/bin/solr.in.sh /opt/solr/bin/solr.in.sh.orig && \
  mv /opt/solr/bin/solr.in.cmd /opt/solr/bin/solr.in.cmd.orig && \
  chown root:0 /etc/default/solr.in.sh && \
  chmod 0664 /etc/default/solr.in.sh && \
  mkdir -p /var/solr/data /var/solr/logs && \
  (cd /opt/solr/server/solr && cp solr.xml zoo.cfg /var/solr/data/) && \
  cp /opt/solr/server/resources/log4j2.xml /var/solr/log4j2.xml && \
  find /var/solr -type d -print0 | xargs -0 chmod 0770 && \
  find /var/solr -type f -print0 | xargs -0 chmod 0660 && \
  sed -i -e "s/\"\$(whoami)\" == \"root\"/\$(id -u) == 0/" /opt/solr/bin/solr && \
  sed -i -e 's/lsof -PniTCP:/lsof -t -PniTCP:/' /opt/solr/bin/solr && \
  chown -R "0:0" /opt/solr-$SOLR_VERSION /docker-entrypoint-initdb.d /opt/docker-solr && \
  chown -R "$SOLR_USER:0" /var/solr

# COPY --chownは、作成されたすべてのディレクトリの所有者を変更しません
# このdockerfileの作成者が用意している色々な初期設定を行うシェルスクリプトを
# コンテナ内にコピーしている。
# ついでにsecurity.jsonをフォルダ内に準備しておいた。
COPY --chown=0:0 scripts /opt/docker-solr/scripts
# security.jsonを所定のフォルダに格納し、basicのセキュリティをかける。
# また、solr.in.sh（各種設定）のカスタマイズ版を、所定の位置に格納する。
RUN cp /opt/docker-solr/scripts/security.json /var/solr/data/security.json && \
    cp /opt/docker-solr/scripts/solr.in.sh /etc/default/solr.in.sh

#VOLUME 命令は指定した名前でマウントポイントを作成し、他のホストやコンテナから外部マウント可能なボリュームにします
VOLUME /var/solr
#EXPOSE 命令は、特定のネットワーク・ポートをコンテナが実行時にリッスンすることを Docker に伝えます。
#ただ、これだけではアクセスできず、-pフラグを使う。
EXPOSE 8983
#cdみたいなもの
WORKDIR /opt/solr
#USER 命令セットはユーザ名か UID を使います。
#これはイメージを RUN 、 CMD 、 ENTRYPOINT 命令で実行時のものであり、 Dockerfile で指定します。
USER $SOLR_USER
#コマンドラインで docker run <イメージ> コマンドに引数を付けますと、exec 形式 の ENTRYPOINT で指定した全要素の後に追加します。
#要は、コマンドの末尾にdocker-entrypoint.shを引数として渡されるようだ。
ENTRYPOINT ["docker-entrypoint.sh"]
#
CMD ["solr-foreground"]
