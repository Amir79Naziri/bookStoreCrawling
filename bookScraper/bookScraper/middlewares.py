# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class BookscraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BookscraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


from urllib.parse import urlencode
import requests
from random import randint
from scrapy.http import Headers

class ScrapOpsFakeHeadersMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.api_key = settings.get("SCRAPOPS_API_KEY")
        self.url = settings.get("SCRAPOPS_FAKE_HEADERS_URL")
        self.enabled = settings.get("SCRAPOPS_FAKE_HEADERS_ENABLED")
        self.num_results = settings.get("SCRAPOPS_FAKE_HEADERS_RESULTS_NUMBER")
        self.fake_headers_list = self.retieve_fake_headers()

    def retieve_fake_headers(self):
        params = {
            "api_key": self.api_key,
            "num_results": self.num_results if self.num_results else 1,
        }

        response = requests.get(url=self.url, params=urlencode(params))

        results = response.json()

        return results.get("result", [])

    def process_request(self, request, spider):
        if self.enabled:
            fake_headers = self.fake_headers_list[
                randint(0, (self.num_results if self.num_results else 1) - 1)
            ]
            
            request.headers = Headers(fake_headers)

            # request.headers["upgrade-insecure-requests"] = fake_headers[
            #     "upgrade-insecure-requests"
            # ]
            # request.headers["user-agent"] = fake_headers["user-agent"]
            # request.headers["accept"] = fake_headers["accept"]
            # request.headers["sec-ch-ua"] = fake_headers["sec-ch-ua"]
            # request.headers["sec-ch-ua-mobile"] = fake_headers["sec-ch-ua-mobile"]
            # request.headers["sec-ch-ua-platform"] = fake_headers["sec-ch-ua-platform"]
            # request.headers["sec-fetch-site"] = fake_headers["sec-fetch-site"]
            # request.headers["sec-fetch-mod"] = fake_headers["sec-fetch-mod"]
            # request.headers["sec-fetch-user"] = fake_headers["sec-fetch-user"]
            # request.headers["accept-encoding"] = fake_headers["accept-encoding"]
            # request.headers["accept-language"] = fake_headers["accept-language"]

            print('******* New Headers Attached! *******')
