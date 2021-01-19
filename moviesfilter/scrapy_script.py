import scrapy
from scrapy.crawler import CrawlerProcess

class MySpider(scrapy.Spider):
    # Your spider definition
    pass

    
class IMDbSpider(scrapy.Spider):
    name = "imdb"
    start_urls = [
        'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating',
    ]
    def parse_movie(self,response):
        mydict = response.meta['data']
        mydict['release_date'] = response.xpath('//div[@class="subtext"]/a[@title="See more release dates"]/text()').extract_first()
        mydict['Country']= response.xpath('//h4[text()="Country:"]/following-sibling::a/text()').extract()
        mydict['Language'] = response.xpath('//h4[text()="Language:"]/following-sibling::a/text()').extract()
        yield mydict

    def parse(self, response):
        movies = response.xpath('//div[@class="lister-item-content"]')
        for movie in movies:
            mydict = {
                'ranking': movie.xpath('.//span[@class="lister-item-index unbold text-primary"]/text()').extract_first(),
                'movie': movie.xpath('.//h3[@class="lister-item-header"]/a/text()').extract_first(),
                'rating': movie.xpath('.//div[@class="inline-block ratings-imdb-rating"]/@data-value').extract_first(),
                'metascore': movie.xpath('.//div[@class="inline-block ratings-metascore"]/span/text()').extract_first(),
                'certification': movie.xpath('.//p[@class="text-muted "]/span[@class="certificate"]/text()').extract_first(),
                'year' : movie.xpath('.//span[@class="lister-item-year text-muted unbold"]/text()').extract_first()[1:-1],
                'runtime': movie.xpath('.//span[@class="runtime"]/text()').extract_first(),
                'genre': movie.xpath('.//span[@class="genre"]/text()').extract_first(),
                'Directors': movie.xpath('p[3]/span/preceding-sibling::a/text()').extract(),
                'Actors': movie.xpath('p[3]/span/following-sibling::a/text()').extract(),
                'Votes': movie.xpath('.//p[@class="sort-num_votes-visible"]/span[@name="nv"][1]/@data-value').extract_first(),
                
            }
            movie_url = movie.xpath('.//h3[@class="lister-item-header"]/a/@href').extract_first()
            movie_url = response.urljoin(movie_url)
            yield scrapy.Request(movie_url, self.parse_movie, meta = {'data': mydict})

        relative_url = movies.xpath('//a[@class="lister-page-next next-page"]/@href').extract_first()
        relative_url = response.urljoin(relative_url)
        # print("next_page",relative_url) 
        yield scrapy.Request(relative_url, callback=self.parse)

            
process = CrawlerProcess(settings={
    "FEEDS": {
        "items_1000.json": {"format": "json","overwrite":True},
        "imdb_1000.csv":{"format":"csv", "overwrite":True},
    },
})

process.crawl(IMDbSpider)
process.start()
