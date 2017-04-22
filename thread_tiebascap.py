# import urllib.request
# import requests
# from bs4 import BeautifulSoup
# from PIL import Image
# from io import BytesIO

# # r = requests.get(image_url, headers=headers)
# # i = Image.open(BytesIO(r.content))
# # i.convert('RGB').save('{0}{1}xx{2}.jpg'.format(path,ii,xx),'jpeg')

# path = r'G:/ps  temp/'
# imagetxt_path = r'G:/Recent use of documents/scrapytest/'
# # url = 'http://tieba.baidu.com/p/4998862427'  #要爬的百度贴吧的网址
# url = 'https://tieba.baidu.com/p/4035665862'

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
#         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
#         }
# with open('{0}tieba_image.txt'.format(imagetxt_path),'r') as f:
#     image_i = f.read()
# image_init = image_i = int(image_i)
# rep = requests.get(url, headers=headers)
# max = BeautifulSoup(rep.text,'lxml').find('li', class_='l_reply_num').find_all('span')[1].get_text()
# for i in range(1,int(max)+1):
#     rep=requests.get(url, headers=headers, params={'pn':i})
#     lists_cont = BeautifulSoup(rep.text,'lxml').find_all('div', class_='d_post_content_main')
#     for cont in lists_cont:
#         images = cont.find_all('img',class_='BDE_Image')
#         for image in images:
#             image_url = image['src']
#             r = requests.get(image_url, headers=headers)
#             image_file = Image.open(BytesIO(r.content))
#             image_file.convert('RGB').save('{0}{1}.jpg'.format(path,image_i),'jpeg')
#             image_i = image_i + 1
# print("这次爬到{0}张图片".format(image_i-image_init))
# with open('{0}tieba_image.txt'.format(imagetxt_path),'w') as f:
#     f.write(str(image_i))


import urllib.request
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from thread_pool import ThreadPool
from threading import Lock
import time
time_start = time.clock()
# r = requests.get(image_url, headers=headers)
# i = Image.open(BytesIO(r.content))
# i.convert('RGB').save('{0}{1}xx{2}.jpg'.format(path,ii,xx),'jpeg')


pool = ThreadPool()
lock = Lock()
path = r'G:/ps  temp/'
imagetxt_path = r'G:/Recent use of documents/scrapytest/'
# url = 'http://tieba.baidu.com/p/4998862427'  #要爬的百度贴吧的网址
url = 'http://tieba.baidu.com/p/5070890482'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
with open('{0}tieba_image.txt'.format(imagetxt_path),'r') as f:
    image_i = f.read()
image_init = image_i = int(image_i)

def down_image(image_url):
    r = requests.get(image_url, headers=headers)
    image_file = Image.open(BytesIO(r.content))
    image_file.convert('RGB').save('{0}{1}.jpg'.format(path,image_i),'jpeg')
    with lock:
        global image_i
        image_i += 1

def get_image(i):
    rep=requests.get(url, headers=headers, params={'pn':i})
    lists_cont = BeautifulSoup(rep.text,'lxml').find_all('div', class_='d_post_content_main')
    for cont in lists_cont:
        images = cont.find_all('img',class_='BDE_Image')
        for image in images:
            image_url = image['src']
            # down_image(image_url)
            pool.add_task(down_image,image_url)

def get_eachpage(url):
    rep = requests.get(url, headers=headers)
    max = BeautifulSoup(rep.text,'lxml').find('li', class_='l_reply_num').find_all('span')[1].get_text()
    for i in range(1,int(max)+1):
        # get_image(i)
        pool.add_task(get_image,i)

get_eachpage(url)
pool.wait_complete()
print("这次爬到{0}张图片".format(image_i-image_init))
with open('{0}tieba_image.txt'.format(imagetxt_path),'w') as f:
    f.write(str(image_i))

time_end = time.clock()
print(time_end-time_start)