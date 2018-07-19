import requests
import json

url = 'https://bbs.guahao.com/gateway/modulesns/mutualhelp/homepagewaterfall.json'
# url = 'https://bbs.guahao.com'
post_data = {
    "firstTime":1531964122946,
    "pageNo":4,
    "pageSize":20,
    "sortMethod":0,
    "tagGroupId":"",
    "type":0
}
headers = {
    "authority":"bbs.guahao.com",
    "method":"POST",
    "path":"/gateway/modulesns/mutualhelp/homepagewaterfall.json",
    "scheme":"https",
    "accept":"application/json",
    # "accept-encoding":"gzip, deflate, br",
    # "accept-language":"zh-CN,zh;q=0.9",
    # "content-length":"92",
    "Content-Type": "application/json",
    # "Cookie": "_yytsid_=15319638192110651957162; _jkhe_m=1531963819221; Hm_lvt_765f44137b89a56a0bc8ed87f1279f1a=1531963821; monitor_sid=1; mst=1531963821737; _fp_code_=9aa8d6f0d2553d622fa57f541c63b353; _sid_=15319638333460651956559; _e_m=1531963833356; Hm_lpvt_765f44137b89a56a0bc8ed87f1279f1a=1531964123; monitor_seq=9; mlt=1531964122836",
    # "Host":"bbs.guahao.com",
    "origin":"https://bbs.guahuao.com",
    "os-token-id": "9aa8d6f0d2553d622fa57f541c63b353",
    "referer": "https://bbs.guahao.com/help",

    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    # "user-agent": "Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50",
    "weiyi-appid": "p_web_weiyi",
    # "weiyi-authtoken":None,
    # "weiyi-version": "1.0"
    "x-requested-with": "XMLHttpRequest"
}
text = requests.post(url=url,
              # data=post_data,
              data=json.dumps(post_data),
              headers=headers)
# text = requests.post(url=url,
#                      data=post_data)
print(type(text.text))
text_dict = json.loads(text.text)
print(text_dict)
for item in text_dict['items']:
    print(item['questionId'])