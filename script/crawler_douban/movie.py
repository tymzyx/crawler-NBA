# -*- coding:utf-8
import requests
from bs4 import BeautifulSoup
from base import *
import threading
import json


type_url = 'https://movie.douban.com/chart'


def get_type_info():
    html = requests.get(type_url, headers).text
    soup = BeautifulSoup(html, 'lxml')
    type_nodes = soup.find('div', class_='types').find_all('a')

    def get_single_info(x):
        href = x['href']
        type_id = href.split('&')[1].split('=')[1]
        name = x.get_text()
        return {'name': name, 'id': type_id}

    types = map(get_single_info, type_nodes)
    print types


def get_movie_detail():
    rank_url = 'https://movie.douban.com/typerank?type_name=剧情片&type=11&interval_id=100:90&action='
    rank_html = requests.get(rank_url, headers).text
    rank_soup = BeautifulSoup(rank_html, 'lxml')
    get_url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100:90&action=&start=0&limit=20'
    response = requests.get(get_url, movie_headers)
    response = response.json()
    for single_movie_detail in response:
        detail_url = single_movie_detail['url']
        detail_html = requests.get(detail_url, headers).text
        detail_soup = BeautifulSoup(detail_html, 'lxml')
        img_url = detail_soup.find('a', class_='nbgnbg').find('img')['src']
        get_movie_img('movie', img_url, img_url.split('/')[-1])  # 存储海报图片
        movie_img_url = img_url.split('/')[-1]  # 海报路径
        rating_pers_node = detail_soup.find_all('span', class_='rating_per')
        rating_pers = map(lambda x: x.get_text(), rating_pers_node)  # 评价分布
        movie_base_info_node = detail_soup.find('div', class_='subject clearfix').find('div', id='info')
        movie_base_info_node_children0 = movie_base_info_node.find_all('span', 'attrs')
        director = movie_base_info_node_children0[0].get_text(strip=True).split('/')  # 导演
        scriptwriter = movie_base_info_node_children0[1].get_text(strip=True).split('/')  # 编剧
        release_date_nodes = movie_base_info_node.find_all('span', property='v:initialReleaseDate')  # 上映日期
        release_date = map(lambda x: x.get_text(), release_date_nodes)  # 上映日期
        run_time_nodes = movie_base_info_node.find_all('span', property='v:runtime')
        run_time = map(lambda x: x.get_text(), run_time_nodes)  # 片长
        indent_nodes = detail_soup.find_all('div', class_='indent')
        indent_content_summary = indent_nodes[1].find('span', property='v:summary')
        if indent_content_summary:
            indent_content_intro = indent_content_summary.get_text(strip=True)  # 剧情简介
        else:
            indent_content_intro = indent_nodes[1].find('span', class_='all hidden')  # 剧情简介

        # ----------------- 影人信息 ----------------- #
        def celebrity_map(x):
            celebrity_img_url = x.find('div', class_='avatar')['style'][22:-1]
            get_movie_img('person', celebrity_img_url, celebrity_img_url.split('/')[-1])  # 存储影人图片
            celebrity_img_url = celebrity_img_url.split('/')[-1]  # 影人图片路径
            celebrity_info_node = x.find('div', class_='info')
            celebrity_name = celebrity_info_node.find('span', class_='name').find('a').get_text()
            celebrity_role = celebrity_info_node.find('span', class_='role')
            celebrity_role = celebrity_role.get_text() if celebrity_role else ''
            celebrity_work_nodes = celebrity_info_node.find('span', class_='works').find_all('a')
            celebrity_works = map(lambda y: y.get_text(), celebrity_work_nodes)  # 代表作
            return {
                'name': celebrity_name,
                'img_url': celebrity_img_url,
                'role': celebrity_role,
                'works': celebrity_works
            }

        celebrities = []  # 影人信息
        celebrities_url = detail_url + 'celebrities'
        celebrities_html = requests.get(celebrities_url, headers).text
        celebrities_soup = BeautifulSoup(celebrities_html, 'lxml')
        celebrity_type_nodes = celebrities_soup.find('div', class_='celebrities').find_all('div', class_='list-wrapper')
        celebrity_director_nodes = celebrity_type_nodes[0].find_all('li', class_='celebrity')
        celebrities.extend(map(celebrity_map, celebrity_director_nodes))
        celebrity_actor_nodes = celebrity_type_nodes[1].find_all('li', class_='celebrity')
        celebrities.extend(map(celebrity_map, celebrity_actor_nodes))

        regular_tag_nodes = detail_soup.find('div', class_='tags-body').find_all('a')
        regular_tag = map(lambda x: x.get_text(), regular_tag_nodes)  # 常用标签

        # ----------------- 剧照 ----------------- #
        photos = []
        photos_url = detail_url + 'all_photos'
        photos_html = requests.get(photos_url, headers).text
        photos_soup = BeautifulSoup(photos_html, 'lxml')
        photos_node = photos_soup.find('ul', class_='pic-col5').find_all('li')
        if len(photos_node) > 10:
            for i in range(10):
                photo_path = photos_node[i].find('img')['src'].replace('/sqxs/', '/l/')
                get_movie_img('still', photo_path, photo_path.split('/')[-1])
                photo_path = photo_path.split('/')[-1]
                photos.append(photo_path)
        else:
            for photo_node in photos_node:
                photo_path = photo_node.find('img')['src'].replace('/sqxs/', '/l/')
                get_movie_img('still', photo_path, photo_path.split('/')[-1])
                photo_path = photo_path.split('/')[-1]
                photos.append(photo_path)

        award_wrapper_node = detail_soup.find('div', class_='mod')
        award = []  # 获奖情况
        if award_wrapper_node:
            awards_node = award_wrapper_node.find_all('ul', class_='award')
            for award_node in awards_node:
                award.append(award_node.get_text('-', strip=True))
                print award_node.get_text('-', strip=True)
        print release_date, run_time
        break


def get_movie_img(category, img_url, img_name):
    base_img_path = '../../assets/images/douban/' + category + '/'
    with open(base_img_path + img_name, 'wb') as f:
        f.write(requests.get(img_url).content)


if __name__ == '__main__':
    # get_type_info()
    get_movie_detail()
