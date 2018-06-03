import scrapy
import json
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

# API URI: https://www.cse.lk/api/tradeSummary
class SymbolsSpider(scrapy.Spider):
    name = "symbols"
    start_urls = [
        "https://www.cse.lk/api/tradeSummary"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse_httpbin,
                errback=self.errback_httpbin,
                method="POST",
            )

    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))

        # something useful goes here...
        jsonresponse = json.loads(response.text)
        print(jsonresponse["reqTradeSummery"])


    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
