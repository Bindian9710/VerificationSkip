import hashlib
import json
import re
import time
import math
import random
import execjs
import requests
from PIL import Image
from io import BytesIO


site_key = '95059ebc73a95c13d50ceb8e06939c94'
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
url = f'https://captcha.luosimao.com/api/widget?k={site_key}&l=zh-cn&s=normal&i=_joz8wviny'
request_url = f'https://captcha.luosimao.com/api/request?k={site_key}&l=zh-cn'
frame_img_url = 'https://captcha.luosimao.com/api/frame?s={}&i=_joz8wviny&l=zh-cn'
urer_verify_url = 'https://captcha.luosimao.com/api/user_verify'

headers = {'User-Agent': User_Agent,'Referer': url,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
           'Content-type': 'application/x-www-form-urlencoded',
           'Host': 'captcha.luosimao.com',
           'Origin': 'https://captcha.luosimao.com',
           'Sec-Fetch-Mode': 'cors',
           'Sec-Fetch-Site': 'same-origin',
           'X-Requested-With': 'XMLHttpRequest',
}
with open('luosimao.js','r') as f:
    AESJS = execjs.compile(f.read())

def get_datavalue(body):
    data_token = re.search(r'data-token="(.*?)"', body).group(1)
    return data_token

def execute_JavaScript(value,encrypt_key):
    result = AESJS.call('AES',value,encrypt_key)
    return result

def getpoint(imgcontent, position):
    """
    复原图片
    """
    img = Image.open(BytesIO(imgcontent))
    img.save('download.png')
    w, h = img.size

    print("图片宽为{},高为{}".format(w, h))
    img_click = Image.new('RGB', (300, 160))
    position = position
    for i in range(30):
        p = position[i]
        pic = img.crop((int(p[0]), int(p[1]), int(p[0]) + 20, int(p[1]) + 80))
        if i < 15:
            box = (20 * i, 0, 20 * (i + 1), 80)
        else:
            box = (20 * (i - 15), 80, 20 * (i + 1 - 15), 160)
        img_click.paste(pic, box)
    img_click.save('click.png')

session = requests.session()

r = session.get(url, headers=headers)
data_token = get_datavalue(r.text)
print(data_token)

raw_bg = f'{User_Agent}||{data_token}||1920:1080||win32||webkit'
times = int(time.time() * 1000)
b_xy = random.randint(100,300)
raw_b = f"{b_xy},38:{times-407023}||{b_xy+2},19:{times}"

bg = execute_JavaScript(raw_bg,'c28725d494c78ad782a6199c341630ee')
b = execute_JavaScript(raw_b,'c28725d494c78ad782a6199c341630ee')
form_data = {'bg':bg,'b':b}


r_1 = session.post(request_url,data=form_data, headers=headers)

r_json = r_1.json()

t = r_json['t']
h = r_json['h']
i = r_json['i']
s = r_json['s']
w = r_json['w']

click = re.search(r'<i>(.*)<\/i>',w).group(1)
print(click)

frame_img = session.post(frame_img_url.format(s))

img_url = re.search(r"https://i5-captcha.luosimao.com.*?png",frame_img.text).group()
position = re.search(r"l: (.*?);",frame_img.text).group()
position = position.replace('l: ', '').replace(']};', '') + "]"
position = json.loads(position)
print(img_url)
img_content = session.get(img_url).content

getpoint(img_content,position)


one = input('输入第一个坐标点:')
two = input('输入第二个坐标点:')
three = input('输入第三个坐标点:')
xy = '#'.join([three,two,one])

v = execute_JavaScript(xy,i)
v = v.replace('=', '').replace('+', '-').replace('/', '_')
m = hashlib.md5()
m.update(xy.encode("utf-8"))
s = m.hexdigest()
datas = {
        'h': h,
        'v': v,
        's': s
    }

rsp = session.post("http://captcha.luosimao.com/api/user_verify", data=datas, headers=headers)
print(rsp.text)
print(rsp.status_code)
