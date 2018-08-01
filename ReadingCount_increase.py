# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from threading import Thread

# 目标网站
TARGET_URL = 'https://blog.csdn.net/qq_31998745/article/details/81323443'
# 代理API接口
PROXY_URL = 'http://localhost:5000/random'
# 请求头
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
}
# 计数
COUNT = 0
# 线程数
THREAD_COUNT = 8

def get_proxy(proxy_url):
    """
    代理ip获取
    :param proxy_url: 代理API接口
    :return: 代理ip
    """
    try:
        response = requests.get(proxy_url)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None

def start_requests(url, proxy):
    """
    使用代理请求目标网址
    :param url: 目标网址
    :param proxy: 代理ip
    """
    global COUNT
    proxies = {
        'http':'http://' + proxy,
        'https':'https://' + proxy,
    }
    try:
        # 使用requests请求，参数包含代理，请求头和超时限制（10s）
        response = requests.get(url, proxies=proxies, headers=HEADERS,timeout=10)
        # BeautifulSoup解析器对象创建
        soup = BeautifulSoup(response.text, 'lxml')
        # 定位阅读量元素并输出
        read_count = soup.find_all('span', class_='read-count')[0]
        print(read_count)
    except:
        print('加载未成功...')
    finally:
        # 每连接一次，不管连接是否成功，计数器+1
        COUNT += 1
        print('已尝试次数：', COUNT)

def run(url, proxy_url):
    """
    多线程运行
    :param url: 目标网址
    :param proxy_url: 代理API接口
    :return:
    """
    threads = []

    # 同时开启8个线程运行，可修改
    for i in range(THREAD_COUNT):
        proxy = get_proxy(proxy_url)
        threads.append(Thread(target=start_requests, args=(url, proxy)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    while True:
        run(TARGET_URL, PROXY_URL)




