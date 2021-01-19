# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import json
logger = logging.getLogger(__name__)
myDict = {'language' :set(),'country':set(),'year':set(),'certification':set(),'genre':set()}
class MoviescrawlPipeline(object):
    def process_item(self, item, spider):
        try: 
            item.save()
        except Exception as e:
            logger.debug(str(e))
        logger.debug("i am in pipeline")
        # print("abcd")
        self.unique_entries(item)
        item.save()
        return item

    def unique_entries(self,item):
        for key in myDict.keys():
            if item[key] is not None:
                if type(item[key]) is int:
                    myDict[key].add(item[key])
                elif type(item[key]) is str and "," not in item[key]:
                    myDict[key].add(item[key])
                
                elif type(item[key]) is str and "," in item[key]:
                    elements = set(item[key].split(", "))
                    myDict[key] = myDict[key].union(elements)
        
    def close_spider(self,spider):
        for key in myDict:
            myDict[key] = sorted(list(myDict[key]))
        print(myDict)
        with open("data/unique_vals.txt","w") as jsonfile:
            json.dump(myDict,jsonfile)