from django.core.management.base import BaseCommand
from moviescrawl.spiders.movies_spider import MoviesSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class Command(BaseCommand):
    help = "Release the Arachnide"

    def handle(self, *args,**kwargs):
        process = CrawlerProcess(get_project_settings())
        # print("settings",get_project_settings())
        process.crawl(MoviesSpider)
        process.start()