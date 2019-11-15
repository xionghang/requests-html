
from requests_html import HTMLSession
import requests
import time
import json
import random
import sys
import getopt

session = HTMLSession()
list_url = 'http://www.allitebooks.com/page/'

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]
# 目录页
def get_list(url):
    book_link_count = 0
    response = session.get(url)
    all_link = response.html.find('.entry-title a')
    for link in all_link:
        if getBookUrl(link.attrs['href']) == 0:
            book_link_count = book_link_count + 1
    return book_link_count

# 详情页
def getBookUrl(url):
    response = session.get(url)
    lin = response.html.find('.download-links a', first=True)
    if lin is not None:
        link = lin.attrs['href'];
        print(link)
        savelink(link)
        #文件下载
        download(link)
        return 0
    return -1

#导出图书下载地址清单
def savelink(url):
    #获取文件名
    filename = 'data/' + "link.txt"
    if ".pdf" in url:
        with open(filename, 'a') as f:
            f.write(url+'\n')
# 文件下载
def download(url):
    # 随机浏览器 User-Agent
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    # 获取文件名
    filename = url.split('/')[-1]
    # 如果 url 里包含 .pdf
    if ".pdf" in url:
        file = 'data/' + filename
        with open(file, 'wb') as f:
            print("正在下载 %s" % filename)
            response = requests.get(url, stream=True, headers=headers)
            # 获取文件大小
            total_length = response.headers.get('content-length')
            # 如果文件大小不存在，则返回
            if total_length is None:
                f.write(response.content)
            else:
                # 下载进度条
                dl = 0
                total_length = int(total_length)  # 文件大小
                fsize = total_length/1024
                print("文件大小：%d k，正在下载..." % fsize)
                for data in response.iter_content(chunk_size=4096):  # 每次响应获取 4096 字节
                    dl += len(data)
                    f.write(data)
                    done = int(100 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (100 - done)))  # 打印进度条
                    sys.stdout.write("已下载：%d k" %( dl/1024))
                    sys.stdout.flush()
            print(filename + '下载完成！')

def exit_and_print_help(exit_code):
    print('Exam_crawler.py -k <keyword> -n <max_page_num>')
    sys.exit(exit_code)
    
if __name__ == '__main__':
   keyword = ''
   max_page_num = 5
   argv = sys.argv[1:]
   try:
      opts, args = getopt.getopt(argv,"hk:n:",[])
   except getopt.GetoptError:
      exit_and_print_help(1)
   for opt, arg in opts:
      if opt == '-h':
         exit_and_print_help(0)
      elif opt in ("-k", ):
         keyword = arg
      elif opt in ("-n", "--ofile"):
         max_page_num = int(arg)
   if len(keyword) < 1:
      exit_and_print_help(1)

   print('开始关键词搜索：' + keyword)
   for x in range(1, max_page_num + 1):
       print('当前页面: ' + str(x))
       if get_list(list_url + str(x) + '/?s=' + keyword) < 1:
           break   # 页面总数小于max_page_num,处理完成
   print('完成')
