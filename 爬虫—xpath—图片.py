import random
import requests
from lxml import etree
from urllib.parse import urljoin
import time
import re
import os
from tqdm import tqdm
def get_urls(base_url,max_page_num):
    try:
        page_num=int(input(f'请输入你要下载的页面数量（提示：最大下载页面数量为：{max_page_num}):'))
        if not 1 <= page_num <= max_page_num:
            raise ValueError
    except:
        print('输入无效，默认下载1页')
        page_num = 1
    urls = [f'{base_url}.html']
    for i in range(2,page_num+1):
        urls.append(f'{base_url}_{i}.html')
    return urls
def crawl_page(url,headers):
    try:
        response=requests.get(url,headers=headers,timeout=10)
        response.raise_for_status()
        response.encoding=response.apparent_encoding
        response=etree.HTML(response.text)
        time.sleep(random.uniform(0.1, 0.2))
        return response
    except requests.exceptions.ConnectionError:
        print("错误：连接失败，请检查网络或URL地址。")
    except requests.exceptions.Timeout:
        print("错误：请求超时。")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")
    return None
def mid_page(root_url,urls,headers):
    mid_pages=[]
    for url in urls:
        main_page_html=crawl_page(url,headers)
        time.sleep(random.uniform(0.1, 0.25))
        if not main_page_html:
            continue
        mid_page_href=main_page_html.xpath('//div[@class="bot-div"]/a/@href')
        for i in range(len(mid_page_href)):
            mid_page=urljoin(root_url,mid_page_href[i])
            mid_pages.append(mid_page)
    return mid_pages
def clean(img_name):
    return re.sub(r'[\\/*?:"<>|]', '', img_name)
def download_page(root_url,mid_pages,headers):
    download_pages = []
    img_names= []
    for mid_page in mid_pages:
        mid_page_html = crawl_page(mid_page,headers)
        src_list = mid_page_html.xpath('//div[@class="img-box"]/img/@src')
        name_list = mid_page_html.xpath("//h1[@class='name']/text()")
        if not src_list:
            print(f'未找到图片链接，跳过：{mid_page}')
            continue
        download_page = urljoin(root_url,src_list[0])
        if  name_list:
            img_name = clean(name_list[0])
        else:
            img_name = f"img_{int(time.time())}"
        download_pages.append(download_page)
        img_names.append(img_name)
        time.sleep(random.uniform(0.05, 0.15))
    return download_pages,img_names
def download_img(download_pages,img_names):
    os.makedirs("img", exist_ok=True)
    for index,img_name in enumerate(img_names):
        if not os.path.exists(os.path.join("img", f"{img_name}.jpg")):
            print(f"文件不存在，开始下载: {img_name}")
            try:
                resp_download_page = requests.get(download_pages[index], stream=True)
                resp_download_page.raise_for_status()
                total_size = int(resp_download_page.headers.get('content-length', 0))
                with open(os.path.join("img", f"{img_name}.jpg"), mode='wb') as f, tqdm(desc=img_name, total=total_size, unit='B',
                                                                            unit_scale=True, unit_divisor=1024, ) as bar:
                    for date in resp_download_page.iter_content(chunk_size=1024):
                        size = f.write(date)
                        bar.update(size)
                    time.sleep(random.uniform(0.7, 1.2))
            except requests.exceptions.RequestException as e:
                print(f"下载失败: {e}")
        else:
            print(f"文件已存在: {img_name}，跳过下载。")
def main():
    #一、设置常量
    root_url = 'https://sc.chinaz.com'
    base_url = 'https://sc.chinaz.com/tupian/meinvxiezhen'
    max_page_num = 110
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    headers = {'user-agent': random.choice(user_agents)}
    # 二、获取主页面
    urls=get_urls(base_url,max_page_num)
    # 三、获取子页面
    mid_pages=mid_page(root_url,urls, headers)
    # 四、获取下载面
    download_pages,img_names = download_page(root_url,mid_pages,headers)
    # 五、下载保存图片
    download_img(download_pages,img_names)
if __name__ == '__main__':
    main()
    print('全部图片下载完成！')
