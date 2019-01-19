import logging  # 日志处理库
import os
import random
import re
import requests
import sys
import time
from urllib import request
from lxml import etree


COOKIE = 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1547555739,1547555783; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1547735534'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'


# 定义日志处理函数
def logger(
    log_file="",
    log_console=False,
    log_format="%(asctime)s - %(levelname)s - %(message)s",
    log_setlevel=logging.DEBUG,
):
    # 如果未设置日志文件和控制台，返回None，结束运行
    if log_file == "" and log_console is False:
        return None
    else:
        # 日志处理基本设置
        logger = logging.getLogger(__name__)  # 新建一个logging对象
        logger.setLevel(level=log_setlevel)  # 设置日志记录等级
        logging_formatter = logging.Formatter(log_format)
        # 如果定义了日志文件，则设置日志文件
        if log_file != "":
            # 设置日志文件
            logging_file = logging.FileHandler(log_file)
            logging_file.setLevel(level=log_setlevel)
            logging_file.setFormatter(logging_formatter)
            logger.addHandler(logging_file)
        # 如果定义了控制台，则设置控制台
        if log_console is True:
            # 设置控制台
            logging_console = logging.StreamHandler(stream=sys.stdout)
            logging_console.setLevel(level=log_setlevel)
            logging_console.setFormatter(logging_formatter)
            logger.addHandler(logging_console)
        return logger


# 页面处理函数，返回所需的数据
def web_elements_traversal(web_page_url_prefix='', web_page_url_index=-1, web_page_url_suffix='', web_page_request_headers={}, web_page_elements_xpath_expression='', timeout=10, logger=logger):
    if web_page_url_index >= 0:
        web_page_url = web_page_url_prefix + str(web_page_url_index) + web_page_url_suffix
    else:
        web_page_url = web_page_url_prefix + web_page_url_suffix
    web_page_elements_got = False
    web_page_err_status = 0
    while web_page_elements_got is False and web_page_err_status <= 10:
        try:
            web_page_request = request.Request(web_page_url, headers=web_page_request_headers)
            web_page_http_response = request.urlopen(web_page_request, timeout=60)
            web_page_html = web_page_http_response.read().decode('utf-8')
            web_page_tree = etree.HTML(web_page_html)
            web_page_elements = web_page_tree.xpath(web_page_elements_xpath_expression)
            web_page_elements_got = True
        except Exception:
            web_page_err_status += 1
            logger.debug(
                "错误。网址：" + web_page_url + " 。搜索表达式：" + web_page_elements_xpath_expression + "。尝试次数：" + str(web_page_err_status) + " 。"
            )
            random_time = random.randint(15, 30)
            logger.debug("睡眠 " + str(random_time) + " 秒钟后重启遍历任务。")
            time.sleep(random_time)
    logger.info("成功。网址：" + web_page_url + " 。搜索表达式：" + web_page_elements_xpath_expression + "。尝试次数：" + str(web_page_err_status) + " 。")
    return web_page_elements


if __name__ == '__main__':
    # 设置数据处理的根目录
    main_dir = 'E:\\e-hentai\\'
    # 设置日志处理对象 logger
    log_file = main_dir + 'log.txt'
    logger = logger(log_file=log_file, log_console=True)

    # 1111111111111111111111111
    # 网页页面循环，取出所有卡通页面的URL
    for web_page_url_index in range(0, 17560 + 1):
        logger.info('网页索引：' + str(web_page_url_index))
        web_page_url_prefix = 'https://e-hentai.org/?p='
        web_page_url_suffix = ''
        if web_page_url_index == 0:
            web_page_request_headers_referer = web_page_url_prefix + str(1)
        else:
            web_page_request_headers_referer = web_page_url_prefix + str(web_page_url_index - 1)
        web_page_request_headers = {
            'Referer': web_page_request_headers_referer,
            'Cookie': COOKIE,
            'User-Agent': USER_AGENT
        }
        web_page_items_data_request_xpath_expression = "//div[@class='it5']/a"
        web_page_items_data = web_elements_traversal(web_page_url_prefix=web_page_url_prefix, web_page_url_index=web_page_url_index, web_page_url_suffix=web_page_url_suffix, web_page_request_headers=web_page_request_headers, web_page_elements_xpath_expression=web_page_items_data_request_xpath_expression, timeout=10, logger=logger)
        # 2222222222222222222222222
        # 遍历卡通页面，找出所有卡通图片页面URL
        for web_page_item_datum in web_page_items_data:
            cartoon_page_items_prefix = web_page_item_datum.attrib['href'] + '?p='
            cartoon_page_items_suffix = ''
            cartoon_page_items_index = 0
            cartoon_page_items_url = cartoon_page_items_prefix + str(cartoon_page_items_index) + cartoon_page_items_suffix
            cartoon_page_num_request_headers_referer = cartoon_page_items_url
            cartoon_page_num_request_headers = {
                'Referer': cartoon_page_num_request_headers_referer,
                'Cookie': COOKIE,
                'User-Agent': USER_AGENT
            }
            # 卡通 网页页数
            cartoon_page_num_data_xpath_expression = "//table[@class='ptb']//a"
            cartoon_page_num_data = web_elements_traversal(web_page_url_prefix=cartoon_page_items_prefix, web_page_url_index=cartoon_page_items_index, web_page_url_suffix=cartoon_page_items_suffix, web_page_request_headers=cartoon_page_num_request_headers, web_page_elements_xpath_expression=cartoon_page_num_data_xpath_expression, timeout=60, logger=logger)
            if len(cartoon_page_num_data) == 1:
                cartoon_page_num = 1
            else:
                cartoon_page_num = int(cartoon_page_num_data[-2].text)
            # 卡通 post 日期
            cartoon_page_post_date_data_xpath_expression = "//div[@id='gdd']//td[@class='gdt2']"
            cartoon_page_post_date_data = web_elements_traversal(web_page_url_prefix=cartoon_page_items_prefix, web_page_url_index=cartoon_page_items_index, web_page_url_suffix=cartoon_page_items_suffix, web_page_request_headers=cartoon_page_num_request_headers, web_page_elements_xpath_expression=cartoon_page_post_date_data_xpath_expression, timeout=60, logger=logger)
            cartoon_page_post_date = cartoon_page_post_date_data[0].text
            # 卡通名称
            cartoon_page_title_data_xpath_expression = "//h1[@id='gn']"
            cartoon_page_title_data = web_elements_traversal(web_page_url_prefix=cartoon_page_items_prefix, web_page_url_index=cartoon_page_items_index, web_page_url_suffix=cartoon_page_items_suffix, web_page_request_headers=cartoon_page_num_request_headers, web_page_elements_xpath_expression=cartoon_page_title_data_xpath_expression, timeout=60, logger=logger)
            cartoon_page_title = cartoon_page_title_data[0].text
            # 卡通图片页 URL
            cartoon_page_picture_urls = []
            cartoon_page_picture_urls_data_xpath_expression = "//div[@class='gdtm']//a"
            for cartoon_page_items_index in range(0, cartoon_page_num):
                cartoon_page_picture_urls_data = web_elements_traversal(web_page_url_prefix=cartoon_page_items_prefix, web_page_url_index=cartoon_page_items_index, web_page_url_suffix=cartoon_page_items_suffix, web_page_request_headers=cartoon_page_num_request_headers, web_page_elements_xpath_expression=cartoon_page_picture_urls_data_xpath_expression, timeout=60, logger=logger)
                for cartoon_page_picture_urls_datum in cartoon_page_picture_urls_data:
                    cartoon_page_picture_urls.append(cartoon_page_picture_urls_datum.attrib['href'])
            # 创建 目录，用于保存图片
            # 去除目录中的特殊字符： \/:*?"<>|
            cartoon_dir_name = re.sub(r'[\/:*?"<>|]', '', cartoon_page_post_date + ' - ' + cartoon_page_title)
            cartoon_dir = main_dir + cartoon_dir_name + '\\'
            # 建立目录，用于保存图片
            if os.path.exists(cartoon_dir) is False:
                try:
                    os.makedirs(cartoon_dir, 0o777)
                    logger.info('创建目录：' + cartoon_dir)
                except Exception:
                    logger.debug('创建目录 ' + cartoon_dir + ' 出错。')
            # 遍历 卡通图片页 ，取出对应的 卡通图片 URL
            cartoon_img_index = 0   # 加入图片前缀，防止图片乱序，无法阅读
            for each_cartoon_page_picture_url in cartoon_page_picture_urls:
                cartoon_img_page__prefix = each_cartoon_page_picture_url
                cartoon_img_page_suffix = ''
                cartoon_img_page_request_headers_referer = cartoon_img_page__prefix
                cartoon_img_page_request_headers = {
                    'Referer': cartoon_page_num_request_headers_referer,
                    'Cookie': COOKIE,
                    'User-Agent': USER_AGENT
                }
                cartoon_img_urls_data_xpath_expression = "//div[@id='i3']//img"
                cartoon_img_url_data = web_elements_traversal(web_page_url_prefix=cartoon_img_page__prefix,  web_page_url_suffix=cartoon_img_page_suffix, web_page_request_headers=cartoon_img_page_request_headers, web_page_elements_xpath_expression=cartoon_img_urls_data_xpath_expression, timeout=60, logger=logger)
                cartoon_img_url = cartoon_img_url_data[0].attrib['src']
                cartoon_img_url_split = cartoon_img_url.split('/', -1)
                cartoon_img_file_name = cartoon_img_url_split[-1]
                cartoon_img_download_requests_headers = {
                    # 'Referer': cartoon_img_url,
                    # 'Cookie': COOKIE,
                    'User-Agent': USER_AGENT
                }
                cartoon_img_downloaded = False
                cartoon_img_download_err_status = 0
                while cartoon_img_downloaded is False and cartoon_img_download_err_status <= 10:
                    try:
                        cartoon_img_html = requests.get(cartoon_img_url, headers=cartoon_img_download_requests_headers, timeout=60)
                        with open(cartoon_dir + '\\' + str(cartoon_img_index) + ' ' + cartoon_img_file_name, 'wb') as cartoon_img_file:
                            cartoon_img_file.write(cartoon_img_html.content)
                        cartoon_img_downloaded = True
                        logger.info('图片下载成功。地址：' + cartoon_img_url)
                    except Exception:
                        cartoon_img_download_err_status += 1
                        random_time = random.randint(30, 60)
                        logger.debug('下载出错。地址：  ' + cartoon_img_url + ' 睡眠 ' + str(random_time) + ' 秒钟后重启。')
                        time.sleep(random_time)
                cartoon_img_index += 1
        random_time = random.randint(30, 60)
        logger('卡通 ' + cartoon_page_title + ' 下载完成。睡眠 ' + random_time + ' 后重启任务。')
        time.sleep(random_time)
        # 2222222222222222222222222
    # 1111111111111111111111111
