import re
import urllib.request

from lxml import html


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

    def keys(self):
        return ('name', 'sort', 'force_people_count')

    def __getitem__(self, item):
        return getattr(self, item)


class ScriptService:
    sort = 1

    def get_zhiyou_top_company(self, host, path):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        }
        url = host + path
        current_page_num = path[path.index('=') + 1: len(path)]
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
        company_list = []
        for company_div in all_company:
            # 公司名
            name = company_div.xpath('*//div[@class="company-segmetation"][1]/a/h3/text()')[0]
            # 关注人数
            force_count = 0
            force_count_str_arr = company_div.xpath('*//div[@class="company-segmetation"][2]/span/span[1]/text()')
            if len(force_count_str_arr) > 0:
                force_count_arr = [int(s) for s in re.findall(r'\d+', force_count_str_arr[0])]
                force_count = int(force_count_arr[0])

            company = Company(name, self.sort, force_count)
            self.sort = self.sort + 1
            # print(str(company.__dict__))
            print("公司名:{name}, 排名:{sort}, 关注人数:{force}".format(name=company.get_name(), sort=company.get_sort(),
                                                               force=company.get_force_people_count()))
            company_list.append(company)
        up_or_down = root.xpath('//a[@class="pg-updown"]/@href')
        if len(up_or_down) > 1:
            company_list.extend(self.get_zhiyou_top_company(host, up_or_down[1]))
        else:
            down = up_or_down[0]
            down_num = down[down.index('=') + 1: len(down)]
            if down_num > current_page_num:
                company_list.extend(self.get_zhiyou_top_company(host, down))
        return company_list


host = 'https://www.jobui.com'
run = ScriptService()
all_company = run.get_zhiyou_top_company(host=host, path='/rank/company/view/guangzhou/tongxin/2013/?n=1')
print('over! all company size:', len(all_company))
