import json
import time

import scrapy
from scrapy_splash import SplashRequest

class CasetrackerSpider(scrapy.Spider):
    name = "casetracker"
    allowed_domains = ["www.casestatusext.com"]
    # start_urls = ["https://www.casestatusext.com/cases/IOE0918743038"]

    script = '''
    function main(splash, args)
      -- method 1 to change user agent
      splash:set_user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
      -- method 2 to change user agent
      --headers = {
      --  ['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
      --}
      --splash:set_custom_headers(headers)    
      
      -- method 3 to change user agent
      --splash:on_request(function(request)
      --	   request:set_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
      --    end)  
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
        FileName = 'case_status.txt'
        with open(FileName, 'w') as file:
            file.write('')
        yield SplashRequest(url='https://www.casestatusext.com/cases/IOE0918743038', callback=self.parse_onepage,
                            endpoint='execute', args={'lua_source': self.script})

    def parse_onepage(self, response):
        html_content = response.data['html']
        json_start = html_content.rfind('cases')
        json_end = html_content.rfind('</script></body></html>')
        cases_html = html_content[json_start:json_end]
        json_start = cases_html.find('[')
        json_end = cases_html.find(']')
        cases_array = cases_html[json_start:json_end+2]
        start_pos = cases_array.find("IOE")
        while start_pos != -1:
            end_pos = cases_array.find("\\", start_pos)
            id_value = cases_array[start_pos:end_pos]
            start_pos = cases_array.find("IOE", end_pos)
            time.sleep(4)
            yield scrapy.Request(url=f'https://www.casestatusext.com/cases/{id_value}', callback=self.parse)

    def parse(self, response):
        casenumber = response.xpath('//td[@class="ant-descriptions-item-content"]/span/text()').extract_first()
        status = response.xpath('//ul[contains(@class,"ant-timeline")]')
        timelines = status.xpath('.//li')
        FileName = 'case_status.txt'
        last_change_date = timelines[-1].xpath('.//div[@class="ant-timeline-item-label"]/text()').get()
        if last_change_date > '2023-08-01':
            with open(FileName, 'a') as file:
                file.write(casenumber + '\n')
                for timeline in timelines:
                    time = timeline.xpath('.//div[@class="ant-timeline-item-label"]/text()').get()
                    status = timeline.xpath('.//div[@class="ant-timeline-item-content"]/text()').get()
                    file.write(time + status + '\n')
            file.close()

