BOT_NAME = "search-engine-crawler"

# Configure the spider modules
SPIDER_MODULES = ["src.spiders"]
NEWSPIDER_MODULE = "src.spiders"

# Configure logger
LOG_LEVEL = "INFO"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure the minimum words count per content item
MIN_WORDS_IN_CONTENT_ITEM = 10

# Configure the maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# Configure middlewares
SPIDER_MIDDLEWARES = {
    "src.middlewares.FilterMiddleware": 543
}

# Configure pipelines
ITEM_PIPELINES = {
    "src.pipelines.IndexPipeline": 300
}

# Configure scheduler
SCHEDULER_DISK_QUEUE = "scrapy.squeues.PickleFifoDiskQueue"

# Configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
