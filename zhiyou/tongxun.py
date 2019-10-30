import urllib.request
from lxml import html
import re


class Company:
    __name = ''
    __sort = 0
    __force_people_count = 0

    def __init__(self, name, sort, force_people_count):
        self.__name = name
        self.__sort = sort
        self.__force_people_count = force_people_count

    def get_name(self):
        return self.__name

    def get_sort(self):
        return self.__sort

    def get_force_people_count(self):
        return self.__force_people_count


class ScriptService:
    def get_zhiyou_top_company(self):
        url = 'https://www.jobui.com/rank/company/view/guangzhou/tongxin/2013/?n=1'
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=header)
        res = urllib.request.urlopen(req).read()
        etree = html.etree
        root = etree.HTML(str(res, 'UTF-8'))
        # all_company_name = root.xpath(
        #     '//div[@class="c-company-list"]//div[@class="company-segmetation"][1]/a/h3/text()')
        # all_company_sort = root.xpath(
        #     '//div[@class="c-company-list"]//div[@class="company-segmetation"][2]/span/span[1]/text()')

        all_company = root.xpath(
            '//div[@class="c-company-list"]')
        sort = 1
        company_list = []
        for company_div in all_company:
            name = company_div.xpath('*//div[@class="company-segmetation"][1]/a/h3/text()')[0]
            force_count_str = company_div.xpath('*//div[@class="company-segmetation"][2]/span/span[1]/text()')[0]
            force_count = [int(s) for s in re.findall(r'\d+', force_count_str)]
            company = Company(name, sort, int(force_count[0]))
            sort = sort + 1
            # print(str(company.__dict__))
            print("公司名:{name}, 排名:{sort}, 关注人数:{force}".format(name=company.get_name(), sort=company.get_sort(),
                                                               force=company.get_force_people_count()))
            company_list.append(company)

        return company_list


run = ScriptService()
run.get_zhiyou_top_company()
