import pytest
import time, math, random
import hashlib
import requests
from .const import *

class Test_httpbin():
    def test_get_ip(self):
        url = BASE_URL + IP_URL
        r = requests.get(url)
        # print(r.headers)
        response_data = r.json()
        # print(data)
        assert 200 == r.status_code
        assert LOCAL_IP == response_data["origin"]

    def test_post_method(self):
        url = BASE_URL + POST_URL
        data = {
            'name': 'xiaohang',
            'password': '123456'
        }
        html = requests.post(url, data=data)
        response_data = html.json()
        assert 200 == html.status_code
        assert data['name'] == response_data['form']['name']
        assert data['password'] == response_data['form']['password']

    def test_put_method(self):
        url = BASE_URL + PUT_URL
        data = {
            'word': 'put'
        }
        html = requests.put(url, data=data)
        response_data = html.json()
        assert 200 == html.status_code
        assert data['word'] == response_data['form']['word']

    def test_youdaofanyi(self):
        url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

        #测试的值是 为什么，那么需要翻译的结果就是 why 做一个简单的测试
        name = '为什么'
        translate = 'why'

        #破解各个参数
        ts = math.floor(time.time() * 1000)
        salt = ts + int(random.random() * 10)

        sign = hashlib.md5(('fanyideskweb' + name + str(salt) + 'Nw(nmmbP%A-r6U3EUn]Aj').encode('utf-8')).hexdigest()
        bv = hashlib.md5(('5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36').encode('utf-8')).hexdigest()

        data = {
            'i': name,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'ts': ts,
            'bv': bv,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/81.0.4044.122Safari/537.36',
            'Referer': 'http://fanyi.youdao.com/',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-663190711@10.108.160.208; JSESSIONID=aaaSCBXzWKbSjbjSZU5gx; OUTFOX_SEARCH_USER_ID_NCOO=1960148676.254038;___rl__test__cookies=1587959055068'
        }

        html = requests.post(url, headers=headers, data=data)

        assert data['i'] == html.json()['translateResult'][0][0]['src']
        assert translate == html.json()['translateResult'][0][0]['tgt']