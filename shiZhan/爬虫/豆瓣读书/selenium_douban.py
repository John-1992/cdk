#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File      :    selenium_douban.py
@Time      :    2020/1/8 14:56
@Author    :    Johnnie
@Version   :    1.0
@Contact   :    18883286752@163.com
@Desc      :    使用selenium爬取豆瓣读书
                保存内容后使用xpath解析
                url,https://search.douban.com/book/subject_search?search_text=python&cat=1001
@Software  :    PyCharm
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from lxml import etree
import json
import re
import queue

books = []


def get_douban_book(book_id):
    url = 'https://search.douban.com/book/subject_search?search_text=python&cat=1001&start={}'.format(book_id)

    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)

    driver.get(url)
    time.sleep(5)
    driver.save_screenshot('douban_book.png')

    with open('douban_book.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)

    book_name = content_parse('douban_book.html')

    driver.quit()
    return book_name


def content_parse(file):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # 生成xml树
    tree = etree.HTML(html)

    # 书名
    book_name = tree.xpath('//a[@class="title-text"]')
    # print(book_name)
    # print(book_name[0].text)

    # 评分
    grade = tree.xpath('//span[@class="rating_nums"]')
    # print(grade[0].text)

    # 评价人数
    evaluate_number = tree.xpath('//span[@class="pl"]')

    # 作者及价格
    author_and_price = tree.xpath('//div[@class="meta abstract"]')
    # text = author_and_price[0].text
    # print(text)
    # authorPrice = get_author(text)
    # print(authorPrice)
    # # 作者
    # print(authorPrice[0][0])
    # # 翻译
    # print(authorPrice[0][1])
    # # 出版社
    # print(authorPrice[0][2])
    # # 出版时间
    # print(authorPrice[0][3])
    # # 价格
    # print(authorPrice[0][4])

    # 将评分信息放进队列，因为有的书没此信息
    q_grade = queue.Queue()
    for i in grade:
        q_grade.put(i.text)

    # q_author = queue.Queue()
    # for i in author_and_price:
    #     q_author.put(i.text)

    # 保存数据
    for i in range(len(book_name)):
        # if book_name[i].text.upper() == 'PYTHON':
        #     try:
        #         # 如果书本名为Python，并且有作者和价格介绍，则取出来扔掉这条作者和价格信息
        #         print(author_and_price[i].text)
        #         useless = q_author.get()
        #         print('useless:{}'.format(useless))
        #     except:
        #         print('不需要书名为{}的信息！'.format(book_name[i].text))
        #     print(i,book_name[i].text)
        #     continue
        book = {}
        book['书名'] = book_name[i].text

        eva_num_list = check_evaluate_number(evaluate_number[i].text)
        if len(eva_num_list):
            book['评分'] = q_grade.get()
            book['评价人数'] = eva_num_list[0]
        else:
            book['评分'] = '暂无评分'
            book['评价人数'] = '评价人数不足'

        authorPrice = get_author(author_and_price[i].text)
        # print(authorPrice)
        if authorPrice:
            authorAndPrice = {}
            authorAndPrice['作者'] = authorPrice[0].strip()
            authorAndPrice['价格'] = authorPrice[-1].strip()

            book['作者及价格'] = authorAndPrice
        else:
            book['作者及价格'] = '未知'

        books.append(book)

    return book_name


def get_author(text):
    # patt = re.compile('(.+?) / (.+?) / (.+?) / (.+?) /.+?(.+)',re.S)
    # authorPirce = patt.findall(text)
    text_list = text.split('/')
    patt = re.compile('\d+\.\d+')
    price = patt.findall(text_list[-1])
    if price:
        return text_list
    return None


def check_evaluate_number(text):
    patt = re.compile('\d+')
    evaluate_num = patt.findall(text)
    return evaluate_num


if __name__ == '__main__':
    book_id = 0
    for i in range(10):
        book_name = get_douban_book(book_id)
        print('第{}页爬取完成'.format(i + 1))
        book_id += 15
        if not book_name:
            break

    with open('douban_book.json', 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False)
    # get_douban_book(book_id)
