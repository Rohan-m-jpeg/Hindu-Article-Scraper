import scrapy
import csv
import os

class HinduSpider(scrapy.Spider):
    name = "hindu_spider"

    def __init__(self, start_urls=None, output_file="output.csv", **kwargs):
        super().__init__(**kwargs)
        if isinstance(start_urls, str):
            self.start_urls = [start_urls]
        elif isinstance(start_urls, list):
            self.start_urls = start_urls
        else:
            self.start_urls = []
        self.output_file = output_file

        if not os.path.exists(self.output_file):
            with open(self.output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["title", "subtitle", "para", "date", "author"])

    def parse(self, response):
        title=" ".join(response.css("h1.title ::text").getall())
        subtitle=" ".join(response.css("h2.sub-title ::text").getall())
        para=" ".join(response.css(".article-section p::text").getall())
        date=" ".join(response.css(".article-section .update-publish-time .updated-time span, .article-section .update-publish-time .publish-time-new ::text").getall()).strip()
        author=" ".join(response.css("div.article-section div.author div.author-name ::text").getall())

        with open(self.output_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([title, subtitle, para, date, author])

        yield {
            "title": title,
            "subtitle": subtitle,
            "para": para,
            "date": date,
            "author": author
        }
