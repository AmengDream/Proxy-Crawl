import requests
import threading
import sys
# import subprocess

#创建锁对象用于写入文件
lock = threading.Lock() 

def logo():
    logos = r"""
     ____              _                               
    | __ ) _   _      / \   _ __ ___   ___ _ __   __ _ 
    |  _ \| | | |    / _ \ | '_ ` _ \ / _ \ '_ \ / _` |
    | |_) | |_| |   / ___ \| | | | | |  __/ | | | (_| |
    |____/ \__, |  /_/   \_\_| |_| |_|\___|_| |_|\__, |
            |___/                                 |___/ 
            
    @Github  : https://github.com/AmengDream
    @FileName: ProxyHealth.py                                     
    @Version : v1.0    
    """    
    sys.stdout.write(logos+"\n")

# # 调用ping命令探测主机是否存活(该函数没有调用)
# def check_host_alive(ip):
#     command = ['ping', '-c', '1', ip]        
#     try:
#         process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         output, error = process.communicate()
#         if process.returncode == 0:
#             return True
#         else:
#             return False
#     except Exception as e:
#         # print("Error:", e)
#         return False

#探测代理是否存活
def check_proxy_alive(proxy):
    try:
        # 使用代理发送GET请求
        response = requests.get('http://www.baidu.com/', proxies={'http': 'http://'+proxy, 'https': 'https://'+proxy}, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        # print("Error:", e)
        return False

#多线程处理    
def check_proxy_alive_thread(proxy):
    if check_proxy_alive(proxy):
        with lock:
            with open('alive_proxy.txt','a',encoding='utf-8') as file:
                file.write(proxy+'\n')
        print('\033[92m' + f"{proxy}>>存活" + '\033[0m')
    else:
        print('\033[91m'+f"{proxy}>>>不存活"+'\033[0m')

if __name__ == "__main__":
    logo()
    
    with open('./proxy_kdl.txt','r',encoding='utf-8') as f:
        file_lines = f.readlines()  
    proxy_list = [i.strip() for i in file_lines]  #去除换行符

    # 创建并启动线程
    threads = []
    
    for proxy in proxy_list:
        thread = threading.Thread(target=check_proxy_alive_thread, args=(proxy,))
        thread.start()
        threads.append(thread)
        
        
    # 等待所有线程结束
    for thread in threads:
        thread.join()
