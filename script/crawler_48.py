# coding=utf-8

"""
Created on 2018-01-31 @author: Sl
功能: 爬取BEJ成员信息并存储为json
"""

import urllib2
import json
import os

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# 设置代理IP
proxy_address = "122.241.72.191:808"


# 定义页面打开函数
def use_proxy(url):
    global proxy_address
    req = urllib2.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    # ------ proxy result in urlopen error [Error 10060] ------ #
    # proxy = urllib2.ProxyHandler({'http': proxy_address})
    # opener = urllib2.build_opener(proxy, urllib2.HTTPHandler)
    # urllib2.install_opener(opener)
    data = urllib2.urlopen(req).read().decode('utf-8', 'ignore')
    return data


def get_member_info():
    url = "http://h5.snh48.com/resource/jsonp/members.php?gid=20"
    data = use_proxy(url)
    content = json.loads(data)['rows']
    if not os.path.exists('detail-json'):
        os.makedirs('detail-json')
    key = 0
    all_info = {
        'B': [],
        'E': [],
        'J': []
    }
    for info in content:
        save_info = {}
        save_info['key'] = key
        save_info['name'] = info['sname'] + '|' + info['pinyin']
        save_info['srcImg'] = 'http://www.bej48.com/images/member/zp_' + info['sid'] + '.jpg'
        save_info['headInfo'] = info['sname'] + ' ' + info['pinyin'] + ' | BEJ48 ' + info['tname'] + '(Team ' + \
                               info['tname'] + ')'
        save_info['lists'] = ['昵称: ' + info['nickname'], '生日: ' + info['birth_day'], '血型: ' + info['blood_type'],
                             '出生地: ' + info['birth_place'], '星座: ' + info['star_sign_12'],
                             '个人特长: ' + info['speciality'], '身高: ' + info['height'], '兴趣爱好: ' + info['hobby'],
                             '加入时间: ' + info['join_day'], '最终所属: BEJ48 ' + info['tname'],
                             '加入所属: ' + info['pname'], '所属公司: ' + info['company']]
        save_info['experiences'] = '经历备注:' + ';'.join(info['experience'].split('<br>'))
        save_info['srcTeamImg'] = info['tname']
        key += 1
        all_info[info['tname']].append(save_info)
        print 'save ' + info['pinyin'] + ' info completed ' + str(key)
    for team in all_info:
        with open('detail-json/' + team + '.json', 'w') as f:
            # ensure_ascii=False http://blog.csdn.net/xiaosongbk/article/details/65446351
            f.write(json.dumps(all_info[team], ensure_ascii=False))


if __name__ == "__main__":
    get_member_info()