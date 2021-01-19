import scrapy
from moviescrawl.items import MoviescrawlItem
import logging
logger = logging.getLogger(__name__)

class MoviesSpider(scrapy.Spider):
    name = "imdbcrawl"
    start_urls = [
        'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating',
    ]

    def parse_movie(self,response):
        mydict = response.meta['data']
        mydict['release_date'] = response.xpath('//div[@class="subtext"]/a[@title="See more release dates"]/text()').extract_first()
        mydict['release_date'] = self.clean_data(mydict['release_date'])
        mydict['country']= response.xpath('//h4[text()="Country:"]/following-sibling::a/text()').extract()
        mydict['language'] = response.xpath('//h4[text()="Language:"]/following-sibling::a/text()').extract()
        mydict['year'] = response.xpath('.//span[@id="titleYear"]/a/text()').extract_first()
        # mydict['synopsis'] = response.xpath('.//div[@class="summary_text"]/text()').extract_first()
        mydict['synopsis'] = response.xpath('.//div[@class="summary_text"]//text()').extract()
        mydict['storyline'] = response.xpath('.//div[@class="inline canwrap"]/p/span/text()').extract_first()
        mydict['storyline'] = self.clean_data(mydict['storyline'])
        mydict['synopsis'] = self.parse_synopsis(mydict['synopsis'])
        # print("synopsis",mydict['synopsis'])
        self.list_repr(mydict,['country','language','directors','actors'])
        movieItem = MoviescrawlItem(**mydict)
        # yield mydict
        # logger.debug("I am here")
        yield movieItem

    def clean_data(self,str1):
        if str1 is not None:
            str1 = str1.replace("\n","").strip()
            str1 = str1.replace('"',"")
        return str1
    
    def parse_synopsis(self,list1):
        if list1 is not None:
            str1 = "".join(list1)
            str1 = str1.replace("\n","").strip()
            str1 = str1.replace('"',"")
            return str1
        return None

    def list_repr(self,mydict,keys):
        for key in keys:
            if mydict[key] is not None:
                mydict[key] = ", ".join(mydict[key])
            

    def clean_runtime(self,str1):
        if str1 is not None:
            int1 = int(str1.split(" ")[0])
            return int1
        return 0
    def parse(self, response):
        movies = response.xpath('//div[@class="lister-item-content"]')
        for movie in movies:
            mydict = {
                'ranking': movie.xpath('.//span[@class="lister-item-index unbold text-primary"]/text()').extract_first(),
                'movie': movie.xpath('.//h3[@class="lister-item-header"]/a/text()').extract_first(),
                'rating': movie.xpath('.//div[@class="inline-block ratings-imdb-rating"]/@data-value').extract_first(),
                'metascore': movie.xpath('.//div[@class="inline-block ratings-metascore"]/span/text()').extract_first(),
                'certification': movie.xpath('.//p[@class="text-muted "]/span[@class="certificate"]/text()').extract_first(),
                'runtime': movie.xpath('.//span[@class="runtime"]/text()').extract_first(),
                'genre': movie.xpath('.//span[@class="genre"]/text()').extract_first(),
                'directors': movie.xpath('p[3]/span/preceding-sibling::a/text()').extract(),
                'actors': movie.xpath('p[3]/span/following-sibling::a/text()').extract(),
                'votes': movie.xpath('.//p[@class="sort-num_votes-visible"]/span[@name="nv"][1]/@data-value').extract_first(),
            }
            mydict['ranking'] = mydict['ranking'].replace(",","")
            mydict['genre'] = self.clean_data(mydict['genre'])
            mydict['runtime'] = self.clean_runtime(mydict['runtime'])
            movie_url = movie.xpath('.//h3[@class="lister-item-header"]/a/@href').extract_first()
            movie_url = response.urljoin(movie_url)
            yield scrapy.Request(movie_url, self.parse_movie, meta = {'data': mydict})

        relative_url = movies.xpath('//a[@class="lister-page-next next-page"]/@href').extract_first()
        relative_url = response.urljoin(relative_url)
        print("next_page",relative_url) 
        yield scrapy.Request(relative_url, callback=self.parse)
