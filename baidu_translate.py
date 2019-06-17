# /usr/bin/env baidu_translate
# coding=utf8

import http.client  # 修改引用的模块
from hashlib import md5
import urllib
import random
from xml.etree import ElementTree as ET
import json as js

filePath = "/Users/colorful/Desktop/ME20_40简体中文_繁体中文/call/strings_tw.xml";

appid = '20190617000308218'  # 你的appid
secretKey = 'ntwK9usqie7s0ojom0gP'  # 你的密钥

httpClient = None
myurl = '/api/trans/vip/translate'
fromLang = 'zh'
toLang = 'cht'
salt = random.randint(32768, 65536)

tree = ET.parse(filePath)
root = tree.getroot()

for child in root:
    sign = appid + child.text + str(salt) + secretKey
    m1 = md5(sign.encode("utf-8"))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        child.text) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result = response.read()
        print("response", result)
        result.decode('utf-8')
        print("result", result)

        x = js.loads(result)
        trans_result = x["trans_result"]
        print("src:", trans_result[0]["src"], "dst:", trans_result[0]["dst"])
        child.text = trans_result[0]["dst"]
    # except Exception as e:
    #     print("请求百度翻译接口失败！", e.args)
    finally:
        if httpClient:
            httpClient.close()
tree.write(filePath, encoding="utf-8", xml_declaration=True, method='xml')
print("-----XML字段更新完毕！")
