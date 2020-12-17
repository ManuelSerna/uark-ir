# Crawlers
This directory contains a couple of implementations of web crawlers/spiders.

## scrapy_scraper
A web crawler made with the [Scrapy](https://scrapy.org/) crawler framework for Python. Although Scrapy is primarily meant for scraping _specific_ web pages, this project adapts a Scrapy project for broad crawling (i.e. crawling any pages) and downloading the HTML pages into a sub-directory called ```downloads```.

To ```cd``` into project directory
```bash
cd scrapy_scraper/scrapy_scraper/spiders
```
To run the Scrapy project (invocating no log flag)
```bash
scrapy runspider msa_spider.py --nolog
```

## serna_spider
My own Python implementation of a web crawler.

To ```cd``` into the project directory
```bash
cd serna_spider
```

To run a crawl on 1,000 pages max (can swap 1,000 with other numbers).

```bash
./run.sh 1000
```
