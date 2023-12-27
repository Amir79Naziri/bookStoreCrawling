# Book Store Web Crawling

This project is a web crawler that scrapes data from a [book store](https://books.toscrape.com/) and saves it in a JSON and Postgres table. The web crawler can extract information such as book title, price, rating, and availability.

### Installation
To run this project, you need to have Python 3 and pip installed on your system. You also need to install the following framework:

* scrapy

You can install it by running the following command:

```
pip install -r requirements.txt
```
### Usage
To run the web crawler, you need to run the below command:

```
scrapy crawl bookSpider
```

Also, you need to add your database credentials () in a `.env` file.

```
DB_HOSTNAME=postgres-hostname
DB_USERNAME=postgres-username
DB_PASSWORD=postgres-password
DB_DATABASE=postgres-tablename
```
Moreover, to handle fake headers and user agents, we used [ScrapeOps](https://scrapeops.io/). First create an account there and then add below information to your `.env` file.

```
SCRAPOPS_API_KEY=your-api-key
SCRAPOPS_FAKE_HEADERS_URL=https://headers.scrapeops.io/v1/browser-headers
```