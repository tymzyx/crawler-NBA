# -*- coding:utf-8
import requests
from bs4 import BeautifulSoup
import threading
import time

from db import db

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# ---------------球员数据结构--------------- #
#   名称            类型        说明
#   id              int         id
#   team_id         int         球队id
#   name            string      中文名
#   alias           string      中文简称
#   eng_name        string      英文名
#   number          string      球员号码
#   position        string      球员位置
#   age             int         球员年龄
#   birth_date      string      球员出生日期
#   first_year      int         进入nba年份
#   height          float       身高-英寸
#   weight          float       体重-磅
#   wage            string      薪资
#   salary          string      合同薪水
#   country         string      国家
#   draft_year      int         选秀年份
#   draft_round     int         选秀轮数
#   draft_pick      int         选秀顺位
#   high_school     string      高中
#   college_school  string      大学
#   wingspan        string      臂展
#   standing_reach  string      站立摸高
#   contract        string      合同明细
#   player_link     string      球员信息介绍页
#   photo_link      string      头像地址
#   big_photo_link  string      大头像地址
#   positionZH      string      场上位置（中文）
#   height_fix      string      身高-米
#   weight_fix      string      体重-公斤
# ----------------------------------------- #


netease_url = 'http://nba.sports.163.com/player/'
netease_min_id = 1000000001
netease_max_id = 1000000567
netease_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'nba.sports.163.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Content-Type': 'text/html; charset=utf-8',
    'Cookie': 'usertrack=ezq0pVqWgpZeb7tOBOkGAg==; _ntes_nnid=fa3d965e626690aee08c793acb6fc238,1519813271877; _ntes_nuid=fa3d965e626690aee08c793acb6fc238; _ga=GA1.2.996601362.1519813272; __f_=1520472527161; P_INFO=songlihtt@163.com|1521768170|0|other|00&99|bej&1521263912&mail163#bej&null#10#0#0|&0|mail163|songlihtt@163.com; vjuids=550012edf.162b8954638.0.f2d345276eb0b; __gads=ID=b3b1fe79888ec379:T=1523515214:S=ALNI_Ma_l-x1kcPK7h9O9UKwICQSQ3gqeQ; JSESSIONID-WYZBS=dTuiz5qX8bK%5C6cS5ns%2B%2Fc1O%5Cx476T%5CMMqYs3De3HMb1isFeR11IwbZ1NOoc%5C%2FhKY4ZKkdvXeUu4MZw%5C75qlFxdZ7IAnZONtGWbebFjWEwzeykvFjn%2FsNMoo8NGPO78o%2FrxaD4fzVewg%5CJ939tHT3EbBe9UVt4cZBVSjukSrqJ1%5CpW%2Fkx%3A1525238252743; _dxd9zbs=30; vjlast=1523515213.1525336098.11; ne_analysis_trace_id=1525336097969; s_n_f_l_n3=2b2629cfb0a287a31525336097971; NNSSPID=fdd23fec5914415d9edb41e74be3e0bc; pgr_n_f_l_n3=c411f57defe6351d15253360979707203; Province=010; City=010; vinfo_n_f_l_n3=2b2629cfb0a287a3.1.0.1525336097970.0.1525336113823'
}

sohu_players_url = 'http://data.sports.sohu.com/nba/nba_players.html'
sohu_base_url = 'http://data.sports.sohu.com/nba/'
sohu_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'data.sports.sohu.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Content-Type': 'text/html; charset=utf-8',
    'Cookie': 'SUV=1802261529166276; t=1525257503714; gidinf=x099980109ee0dc2f8611ac1e0006627e6372d479f57; IPLOC=CN1100; vjuids=3f54ff2a9.1635c3b0f4c.0.384806958e8f2; vjlast=1526260764.1526260764.30'
}


class MyThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, thread_id, thread_name, thread_func, collection, base_info, count=0, start_index=0):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.thread_func = thread_func
        self.collection = collection
        self.base_info = base_info
        self.count = count
        self.start_index = start_index

    def run(self):
        print 'Starting ' + self.thread_name
        self.thread_func(self.base_info, self.count, self.start_index, self.collection, self.thread_name)
        print 'Exiting ' + self.thread_name


# 网易
def main_netease(url, headers):
    temp_url = url + str(netease_min_id) + '/'
    html = requests.get(temp_url, headers).text
    soup = BeautifulSoup(html, 'lxml')
    player_info = {}
    player_card = soup.find_all('span', class_='nor-dblue')
    name, eng_name, number, positionZH = player_card[0].get_text().split('|')
    print player_card[1].get_text()


# 搜狐
def get_players_url(headers):
    global sohu_players_url
    players_url = []
    players_html = requests.get(sohu_players_url, headers).text
    players_soup = BeautifulSoup(players_html, 'lxml')
    name_boxs = players_soup.find_all('div', class_='nameBox')
    for name_box in name_boxs:
        ul = name_box.find('ul', class_='w250')
        for li in ul.find_all('li'):
            players_url.append(li.find('a')['href'])
    return players_url


def main_sohu(headers):
    mongo = db.connect_db('nba')
    collection = mongo.sohu_players
    players_url = get_players_url(headers)
    insert_num = 50  # 每次插入数据库数据量
    players_length = len(players_url)
    thread_num = players_length / insert_num + 1
    remainder = players_length % insert_num
    print players_length / insert_num, players_length % insert_num, players_length
    thread_list = []
    for i in range(thread_num):
        count = insert_num if i < thread_num - 1 else remainder
        start_index = i * insert_num
        thread = MyThread(i, 'thread_' + str(i), sohu_thread_func, collection, players_url, count, start_index)
        thread_list.append(thread)
        thread.start()


def sohu_thread_func(players_url, count, start_index, collection, thread_name):
    global sohu_base_url, sohu_headers
    insert_data = []
    for i in range(start_index, start_index + count):
        player_url = players_url[i]
        url = sohu_base_url + player_url + '&type=1#data_box'
        html = requests.get(url, sohu_headers)
        html.encoding = 'gbk'
        soup = BeautifulSoup(html.text, 'lxml')
        name_doc = soup.find('title').get_text().split('|')
        player_id = player_url.split('=')[1]
        name = name_doc[0]  # 中文名
        print 'now is on ' + thread_name + ', getting player: ' + name + ', url: ' + player_url
        eng_name = name_doc[1]  # 英文名
        base_doc = soup.find('div', class_='pt')
        avatar = base_doc.find('img')['src']  # 头像地址
        base_li_list = base_doc.find_all('li')
        team = base_li_list[0].get_text().split(u'：')[1]  # 球队名称
        team_id = base_li_list[0].find('a')['href'].split('=')[1]  # 球队id
        born_city = base_li_list[1].get_text().split(u'：')[1]  # 出生城市
        born_date = base_li_list[2].get_text().split(u'：')[1]  # 出生日期
        position = base_li_list[3].get_text().split(u'：')[1]  # 场上位置
        height = base_li_list[4].get_text().split(u'：')[1]  # 身高/cm
        weight = base_li_list[5].get_text().split(u'：')[1]  # 体重/kg
        num = base_li_list[6].get_text().split(u'：')[1]  # 球衣号码
        career_doc = soup.find_all('table')
        career_sum_doc = career_doc[0]
        career_avg_doc = career_doc[1]
        career_info = {'avg': {}, 'sum': {}}
        career_sum_trs = career_sum_doc.find_all('tr')
        for j in range(1, len(career_sum_trs)):
            career_tds = career_sum_trs[j].find_all('td')
            season = career_tds[0].get_text(strip=True)
            if j == len(career_sum_trs)-1:
                season = 'career'
            career_info['sum'][season] = {
                'season': season,                                                                   # 赛季
                'team': career_tds[1].get_text(),                                                   # 球队
                'played': float(career_tds[2].get_text()) if career_tds[2].get_text() else 0,       # 出场
                'main': float(career_tds[3].get_text()) if career_tds[3].get_text() else 0,         # 首发
                'time': float(career_tds[4].get_text()) if career_tds[4].get_text() else 0,         # 时间
                'hit': career_tds[5].get_text(),                                                    # 命中
                'three': career_tds[6].get_text(),                                                  # 三分
                'penalty': career_tds[7].get_text(),                                                # 罚球
                'ofRebound': float(career_tds[8].get_text()) if career_tds[8].get_text() else 0,    # 进攻篮板
                'deRebound': float(career_tds[9].get_text()) if career_tds[9].get_text() else 0,    # 防守篮板
                'rebound': float(career_tds[10].get_text()) if career_tds[10].get_text() else 0,    # 篮板
                'assist': float(career_tds[11].get_text()) if career_tds[11].get_text() else 0,     # 助攻
                'steal': float(career_tds[12].get_text()) if career_tds[12].get_text() else 0,      # 抢断
                'block': float(career_tds[13].get_text()) if career_tds[13].get_text() else 0,      # 盖帽
                'miss': float(career_tds[14].get_text()) if career_tds[14].get_text() else 0,       # 失误
                'foul': float(career_tds[15].get_text()) if career_tds[15].get_text() else 0,       # 犯规
                'score': float(career_tds[16].get_text()) if career_tds[16].get_text() else 0       # 得分
            }
        career_avg_trs = career_avg_doc.find_all('tr')
        for j in range(1, len(career_avg_trs)):
            career_tds = career_avg_trs[j].find_all('td')
            season = career_tds[0].get_text(strip=True)
            if j == len(career_avg_trs)-1:
                season = 'career'
            career_info['avg'][season] = {
                'season': season,                                                                   # 赛季
                'team': career_tds[1].get_text(),                                                   # 球队
                'played': float(career_tds[2].get_text()) if career_tds[2].get_text() else 0,       # 出场
                'main': float(career_tds[3].get_text()) if career_tds[3].get_text() else 0,         # 首发
                'time': float(career_tds[4].get_text()) if career_tds[4].get_text() else 0,         # 时间
                'hit': float(career_tds[5].get_text()) if career_tds[5].get_text() else 0,          # 命中
                'three': float(career_tds[6].get_text()) if career_tds[6].get_text() else 0,        # 三分
                'penalty': float(career_tds[7].get_text()) if career_tds[7].get_text() else 0,      # 罚球
                'ofRebound': float(career_tds[8].get_text()) if career_tds[8].get_text() else 0,    # 进攻篮板
                'deRebound': float(career_tds[9].get_text()) if career_tds[9].get_text() else 0,    # 防守篮板
                'rebound': float(career_tds[10].get_text()) if career_tds[10].get_text() else 0,    # 篮板
                'assist': float(career_tds[11].get_text()) if career_tds[11].get_text() else 0,     # 助攻
                'steal': float(career_tds[12].get_text()) if career_tds[12].get_text() else 0,      # 抢断
                'block': float(career_tds[13].get_text()) if career_tds[13].get_text() else 0,      # 盖帽
                'miss': float(career_tds[14].get_text()) if career_tds[14].get_text() else 0,       # 失误
                'foul': float(career_tds[15].get_text()) if career_tds[15].get_text() else 0,       # 犯规
                'score': float(career_tds[16].get_text()) if career_tds[16].get_text() else 0       # 得分
            }
        insert_data.append({
            'playerId': player_id,
            'name': name,
            'engName': eng_name,
            'bornCity': born_city,
            'bornDate': born_date,
            'position': position,
            'height': float(height),
            'weight': float(weight),
            'team': team,
            'teamId': team_id,
            'number': num,
            'avatar': avatar,
            'career': career_info
        })
        time.sleep(1)
    # 插入数据库
    print 'insert to mongodb'
    collection.insert_many(insert_data)


if __name__ == '__main__':
    # main_netease(netease_url, netease_headers)
    main_sohu(sohu_headers)
