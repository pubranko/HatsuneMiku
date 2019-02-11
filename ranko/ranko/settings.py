# -*- coding: utf-8 -*-

# Scrapy settings for ranko project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ranko'

SPIDER_MODULES = ['ranko.spiders']
NEWSPIDER_MODULE = 'ranko.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# リクエストに含まれるユーザーエージェントの指定
#USER_AGENT = 'ranko (+http://www.yourdomain.com)'
#USER_AGENT = 'User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 同寺平行処理するリクエストの最大値
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
# webサイトのドメインごとに、同寺平行処理するリクエストの最大値
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
# webサイトのIPごとの同時並行リクエストの最大値。これを指定すると、DOWNLOAD_DELAYもipごとになり、CONCURRENT_REQUESTS_PER_DOMAINは無視される。
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# Cookieを有効にするかどうか。
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# リクエストにデフォルトで含めるヘッダーをdictで指定する。
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# スパイダーのミドルウェアを作る場合に使用する。
#SPIDER_MIDDLEWARES = {
#    'ranko.middlewares.RankoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# ダウンロードのミドルウェアを自作のものを使いたい場合、以下の設定を変える。
#DOWNLOADER_MIDDLEWARES = {
#    'ranko.middlewares.RankoDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#アイテムのパイプラインの設定
#ITEM_PIPELINES = {
#    'ranko.pipelines.RankoPipeline': 300,
#}
#これは、mongodbに保存したあとRQでキューにジョブを追加するという流れになる。
ITEM_PIPELINES = {
    'ranko.pipelines.MongoPipeline': 802,
    'ranko.pipelines.RQPipeline': 803,
}
#    'ranko.pipelines.DuplicateCheckPipeline':801,

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPキャッシュを使うかどうかの指定。キャッシュを使うと、２回目以降はサーバーにリクエストが送られず、
# レスポンスがキャッシュから取得できる。
HTTPCACHE_ENABLED = True
# 上記でキャッシュを有効にした場合、有効な秒数を指定。0は無限。 900秒→15分
HTTPCACHE_EXPIRATION_SECS = 86400
# フォルダ名だけ指定した場合、こうなる「〜/myproject/.scrapy/scrapy_httpcache」
HTTPCACHE_DIR = '/var/cache/ranko/'
# レスポンスをキャッシュしないHTTPステータスコード。
HTTPCACHE_IGNORE_HTTP_CODES = []
# よくわからないが、ファイル自体のレスポンスに関する何か？
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

'''公式HPより使用可能なパラメータの一覧
    AJAXCRAWL_ENABLED
    AUTOTHROTTLE_DEBUG
    AUTOTHROTTLE_ENABLED
    AUTOTHROTTLE_MAX_DELAY
    AUTOTHROTTLE_START_DELAY
    AUTOTHROTTLE_TARGET_CONCURRENCY
    CLOSESPIDER_ERRORCOUNT
    CLOSESPIDER_ITEMCOUNT
    CLOSESPIDER_PAGECOUNT
    CLOSESPIDER_TIMEOUT
    COMMANDS_MODULE
    COMPRESSION_ENABLED
    COOKIES_DEBUG
    COOKIES_ENABLED
    FEED_EXPORTERS
    FEED_EXPORTERS_BASE
    FEED_EXPORT_ENCODING
    FEED_EXPORT_FIELDS
    FEED_EXPORT_INDENT
    FEED_FORMAT
    FEED_STORAGES
    FEED_STORAGES_BASE
    FEED_STORE_EMPTY
    FEED_URI
    FILES_EXPIRES
    FILES_RESULT_FIELD
    FILES_STORE
    FILES_STORE_S3_ACL
    FILES_URLS_FIELD
    GCS_PROJECT_ID
    HTTPCACHE_ALWAYS_STORE
    HTTPCACHE_DBM_MODULE
    HTTPCACHE_DIR
    HTTPCACHE_ENABLED
    HTTPCACHE_EXPIRATION_SECS
    HTTPCACHE_GZIP
    HTTPCACHE_IGNORE_HTTP_CODES
    HTTPCACHE_IGNORE_MISSING
    HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS
    HTTPCACHE_IGNORE_SCHEMES
    HTTPCACHE_POLICY
    HTTPCACHE_STORAGE
    HTTPERROR_ALLOWED_CODES
    HTTPERROR_ALLOW_ALL
    HTTPPROXY_AUTH_ENCODING
    HTTPPROXY_ENABLED
    IMAGES_EXPIRES
    IMAGES_MIN_HEIGHT
    IMAGES_MIN_WIDTH
    IMAGES_RESULT_FIELD
    IMAGES_STORE
    IMAGES_STORE_S3_ACL
    IMAGES_THUMBS
    IMAGES_URLS_FIELD
    MAIL_FROM
    MAIL_HOST
    MAIL_PASS
    MAIL_PORT
    MAIL_SSL
    MAIL_TLS
    MAIL_USER
    MEDIA_ALLOW_REDIRECTS
    METAREFRESH_ENABLED
    METAREFRESH_MAXDELAY
    REDIRECT_ENABLED
    REDIRECT_MAX_TIMES
    REFERER_ENABLED
    REFERRER_POLICY
    RETRY_ENABLED
    RETRY_HTTP_CODES
    RETRY_TIMES
    TELNETCONSOLE_HOST
    TELNETCONSOLE_PORT

ミドルウェアの優先順位は以下のとおり（公式より）
{
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
}
'''