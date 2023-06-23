import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
import sys

#https://www.kuaidaili.com/free/inha/1/

file = open('proxy_kdl.txt','a+',encoding='utf-8')

def logo():
    logos = r"""
     ____              _                               
    | __ ) _   _      / \   _ __ ___   ___ _ __   __ _ 
    |  _ \| | | |    / _ \ | '_ ` _ \ / _ \ '_ \ / _` |
    | |_) | |_| |   / ___ \| | | | | |  __/ | | | (_| |
    |____/ \__, |  /_/   \_\_| |_| |_|\___|_| |_|\__, |
            |___/                                 |___/ 
            
    @Github  : https://github.com/AmengDream
    @FileName: kuaidaili-free.py                                      
    @Version : v1.0    
    """    
    sys.stdout.write(logos+"\n")

#解析页面进行爬取
def proxy_kdl(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    try:
        html = requests.get(url,headers=headers,timeout=5).text
    except Exception as e:
        print(e)
        
    soup = BeautifulSoup(html,features="lxml")    
    tr_tags =soup.find_all("tr")    
    proxy_list = []    
    for tr in tr_tags:
        ip_tag = tr.find('td',{'data-title':'IP'})
        port_tag = tr.find('td',{'data-title':'PORT'})
        if ip_tag and port_tag:
            ip = ip_tag.text
            port = port_tag.text            
            proxy_list.append(ip+":"+port)             
    return proxy_list           

#将结果写入文件
def write_proxy(proxys_list):
    proxys_list = proxys_list.result()
    if proxys_list:
        print('爬取成功，正在写入文件。。。')
        for ip_port in proxys_list:
            file.write(str(ip_port)+'\n')
    else:
        print("爬取失败。。。")
    
    
    
if __name__ == "__main__":
    logo()
    num = 11        #爬取页数 num-1
    pool = ThreadPoolExecutor(1)
    threads = []
    for i in range(num):
        if i == 0:
            continue
        #设置爬取间隔，防止被ban
        time.sleep(3)
        url = f"https://www.kuaidaili.com/free/inha/{i}/"
        print(f"正在爬取快代理-免费高匿代理第{i}页")
        
        thread = pool.submit(proxy_kdl, url)
        thread.add_done_callback(write_proxy)
        threads.append(thread)
    
    # 等待所有线程执行完成
    for thread in threads:
        thread.result()

    # 关闭线程池
    pool.shutdown()
    
    # 关闭文件
    file.close()