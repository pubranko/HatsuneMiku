#!/bin/bash
#
# docker-entrypoint for docker-solr
echo "################"
echo "################"
echo "################"
echo "docker-entrypoint.sh 実行開始"
echo "################"
echo "################"
echo "################"

#コマンドがゼロ以外のステータスで終了した場合は、直ちに終了します。
set -e

if [[ "$VERBOSE" = "yes" ]]; then
    #コマンドとその引数を実行時に表示します。
    set -x
fi

#SOLRポートの数値チェック。
#SOLR_PORT変数が存在し、数値以外であれば8983へ置き換えを行う。
#    [[ ]]でtest
#    -v オプションは、シェルスクリプト内でこれから実行されるコマンドを表示する。
#       変数が使用されている場合は -x オプションとは異なり、変数名がそのまま表示される。
#
#    "${SOLR_PORT:-}" →SOLR_PORTの値を取り出し。
#    < << 通常入力とヒアドキュメントの機能を使って、上記の値そのものをファイルとしてgrepに渡す。
#    grep -E：PATTERN を拡張正規表現とする
#             ^[0-9]+$：先頭から末尾まですべて数値であることをチェック
#    grep -q：grepの結果をコンソールに表示しない。
#    export：環境変数SOLR_PORTに反映させる。
if [[ -v SOLR_PORT ]] && ! grep -E -q '^[0-9]+$' <<<"${SOLR_PORT:-}"; then
  SOLR_PORT=8983
  export SOLR_PORT
fi

# when invoked with e.g.: docker run solr -help
# docker run solr のあとの最初の引数が-で始まっている場合
if [ "${1:0:1}" = '-' ]; then
    #位置パラメータ（実行時の引数）の先頭に、solr-foregraoundを追加し、その後ろに引数すべて($@)を配置する。
    set -- solr-foreground "$@"
fi

# execute command passed in as arguments.
# The Dockerfile has specified the PATH to include
# /opt/solr/bin (for Solr) and /opt/docker-solr/scripts (for our scripts
# like solr-foreground, solr-create, solr-precreate, solr-demo).
# Note: if you specify "solr", you'll typically want to add -f to run it in
# the foreground.
# 要は、上記の引数の変更を反映させている。
exec "$@"

echo "################"
echo "################"
echo "################"
echo "docker-entrypoint.sh 実行終了"
echo "################"
echo "################"
echo "################"

