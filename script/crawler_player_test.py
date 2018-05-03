# -*- coding:utf-8
import requests
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

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


url = 'http://nba.sports.163.com/player/'
min_id = 1000000001
max_id = 1000000567
headers = {
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


def main():
    global url, headers
    temp_url = url + str(min_id) + '/'
    html = requests.get(temp_url, headers).text
    soup = BeautifulSoup(html, 'lxml')
    player_info = {}
    player_card = soup.find_all('span', class_='nor-dblue')
    name, eng_name, number, positionZH = player_card[0].get_text().split('|')
    print player_card[1].get_text()


if __name__ == '__main__':
    main()

