import scrapy
from bookScraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookSpider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]
    
    
    # custom_settings = {
    #     "FEEDS": {
    #         "bookdata.json": {
    #             "format": "json",
    #             "overwrite": True
    #         }
    #     }
    # } we can define settings here too (instead of settings file)

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            book_page = book.css("h3 a").attrib["href"]

            if "catalogue/" in book_page:
                book_url = "https://books.toscrape.com/" + book_page
            else:
                book_url = "https://books.toscrape.com/catalogue/" + book_page

            yield response.follow(book_url, callback=self.book_parse)

        next_page = response.css("li.next a").attrib["href"]

        if next_page:
            if "catalogue/" in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page

            yield response.follow(next_page_url, callback=self.parse)

    def book_parse(self, response):
        table_rows = response.css("table.table.table-striped tr")

        bookItem = BookItem()

        bookItem["url"] = response.url
        bookItem["title"] = response.xpath(
            '//*[@id="content_inner"]/article/div[1]/div[2]/h1/text()'
        ).get()
        bookItem["upc"] = table_rows[0].css("td::text").get()
        bookItem["product_type"] = table_rows[1].css("td::text").get()
        bookItem["price_excl_tax"] = table_rows[2].css("td::text").get()
        bookItem["price_incl_tax"] = table_rows[3].css("td::text").get()
        bookItem["tax"] = table_rows[4].css("td::text").get()
        bookItem["availability"] = table_rows[5].css("td::text").get()
        bookItem["num_reviews"] = table_rows[6].css("td::text").get()
        bookItem["stars"] = response.css("p.star-rating").attrib["class"]
        bookItem["category"] = response.xpath(
            '//*[@id="default"]/div/div/ul/li[3]/a/text()'
        ).get()
        bookItem["description"] = response.xpath(
            '//*[@id="content_inner"]/article/p/text()'
        ).get()
        bookItem["price"] = response.xpath(
            '//*[@id="content_inner"]/article/div[1]/div[2]/p[1]/text()'
        ).get()

        yield bookItem
