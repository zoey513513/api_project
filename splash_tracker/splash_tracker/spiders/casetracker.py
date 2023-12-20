import scrapy
from scrapy_splash import SplashRequest

class CasetrackerSpider(scrapy.Spider):
    name = "casetracker"
    allowed_domains = ["www.casestatusext.com"]
    # start_urls = ["https://www.casestatusext.com/cases/IOE0918743038"]

    script = '''
    function main(splash, args)
      splash.private_mode_disabled = false
      assert(splash:go(args.url))
      assert(splash:wait(2))
      btn = splash:select('.ant-pagination-item-link')
      btn:mouse_click()
      assert(splash:wait(3))
      splash:set_viewport_full()
    
      return {
        html = splash:html(),
        png = splash:png(),
      }
    end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://www.casestatusext.com/cases/IOE0918743038', callback=self.parse,
                            endpoint='execute', args={'lua_source': self.script})
    def parse(self, response):
        print(response.body)
