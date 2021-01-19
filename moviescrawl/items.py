# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# from scrapy.contrib.djangoitem import DjangoItem
from scrapy_djangoitem import DjangoItem
from movies.models import Movie

class MoviescrawlItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = Movie
