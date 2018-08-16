# -*- coding:utf-8
import requests
from bs4 import BeautifulSoup
from base import *
import threading

tag_url = 'https://book.douban.com/tag/'


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


def get_tag_info():
    html = requests.get(tag_url, headers).text
    soup = BeautifulSoup(html, 'lxml')
    title_nodes = soup.find_all('a', class_='tag-title-wrapper')
    content_table_nodes = soup.find_all('table', class_='tagCol')
    tag_info = {}
    for i in range(len(title_nodes)):
        title_node = title_nodes[i]
        content_row_nodes = content_table_nodes[i].find_all('tr')
        temp_tag_content = []
        for j in range(len(content_row_nodes)):
            content_nodes = content_row_nodes[j].find_all('td')
            for content_node in content_nodes:
                tag_name = content_node.find('a').get_text()
                tag_num = content_node.find('b').get_text()
                temp_tag_content.append({
                    'tag_name': tag_name,
                    'tag_num': tag_num[1:len(tag_num)-1]
                })
        tag_info[title_node['name']] = temp_tag_content


def get_book_detail(tag_type):
    insert_data = []
    for page in range(25):
        start_num = page * 20
        url = tag_url + tag_type + '?start=' + str(start_num) + '&type=S'
        html = requests.get(url, headers).text
        soup = BeautifulSoup(html, 'lxml')
        book_item_nodes = soup.find_all('li', class_='subject-item')
        for book_item_node in book_item_nodes:
            img_url = book_item_node.find('div', class_='pic').find('img')['src']
            get_book_img(img_url, img_url.split('/')[-1])
            book_img_url = img_url.split('/')[-1]  # 图片路径
            book_other_detail = book_item_node.find('div', class_='pub').get_text().strip().split('/')
            if len(book_other_detail) == 5:
                author = book_other_detail[0].strip()  # 作者
                translator = book_other_detail[1].strip()  # 译者
                press = book_other_detail[2].strip()  # 出版社
                publish_date = book_other_detail[3].strip()  # 出版时间
                price = book_other_detail[4].strip()  # 价格
            else:
                author = book_other_detail[0].strip()  # 作者
                press = book_other_detail[1].strip()  # 出版社
                translator = ''
                publish_date = book_other_detail[2].strip()  # 出版时间
                price = book_other_detail[3].strip()  # 价格
            detail_url = book_item_node.find('div', class_='info').find('a')['href']
            book_id = detail_url.split('/')[-2]  # 图书编号
            detail_html = requests.get(detail_url, headers).text
            detail_soup = BeautifulSoup(detail_html, 'lxml')
            book_name = detail_soup.find('h1').find('span').get_text()  # 书名
            book_rating = detail_soup.find('strong', class_='rating_num').get_text()  # 评分
            rating_people = detail_soup.find('a', class_='rating_people').find('span').get_text()  # 评价人数
            rating_pers_node = detail_soup.find_all('span', class_='rating_per')
            rating_pers = map(lambda x: x.get_text(), rating_pers_node)  # 评价分布
            indent_nodes = detail_soup.find_all('div', class_='indent')
            indent_content_intros = indent_nodes[1].find_all('div', class_='intro')
            if len(indent_content_intros) > 1:
                indent_content_intro = '-'.join(map(lambda x: x.get_text(), indent_content_intros[1].find_all('p')))  # 内容简介
            else:
                indent_content_intro = '-'.join(map(lambda x: x.get_text(), indent_content_intros[0].find_all('p')))  # 内容简介
            indent_author_intro = indent_nodes[2].find('div', class_='intro').get_text()  # 作者简介
            print 'dir_' + book_id + '_full'
            indent_catalog_intro = \
                detail_soup.find('div', id='dir_' + book_id + '_full', ).get_text('-', strip=True).split('-')
            indent_catalog_intro = indent_catalog_intro[:-3]  # 目录
            regular_tag = []  # 常用标签
            regular_tag_nodes = detail_soup.find('div', id='db-tags-section').find('div', class_='indent').find_all('a')
            for tag_node in regular_tag_nodes:
                regular_tag.append({
                    'name': tag_node.get_text(),
                    'href': tag_node['href']
                })
            series_book_node = detail_soup.find('div', class_='subject_show block5')
            if series_book_node:
                series_book = series_book_node.find('div').get_text(strip=True).replace('\n', '')  # 丛书信息
            else:
                series_book = ''
            relation_like_nodes = detail_soup.find('div', id='db-rec-section').find_all('dd')
            relation_likes = []  # 相关喜欢书籍
            for relation_like_node in relation_like_nodes:
                relation_like_tag = relation_like_node.find('a')
                relation_likes.append({
                    'name': relation_like_tag.get_text(strip=True),
                    'id': relation_like_tag['href'].split('/')[-2]
                })
            insert_data.append({
                'id': book_id,
                'name': book_name,
                'author': author,
                'translator': translator,
                'press': press,
                'publishDate': publish_date,
                'price': price,
                'img': book_img_url,
                'rating': book_rating,
                'ratingNum': rating_people,
                'ratingPer': rating_pers,
                'contentIntro': indent_content_intro,
                'authorIntro': indent_author_intro,
                'catalogIntro': indent_catalog_intro,
                'seriesBook': series_book,
                'regularTag': regular_tag,
                'relationLikes': relation_likes
            })


def get_book_img(img_url, img_name):
    base_img_path = '../../assets/images/douban/book/'
    with open(base_img_path + img_name, 'wb') as f:
        f.write(requests.get(img_url).content)


def main_crawler():
    return


if __name__ == '__main__':
    # get_tag_info()
    # get_book_img()
    get_book_detail('小说')
