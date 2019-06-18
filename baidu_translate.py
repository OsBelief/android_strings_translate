# /usr/bin/env baidu_translate
# coding=utf8

import http.client
from hashlib import md5
import urllib
import random
from xml.etree import ElementTree as ET
import json as js
import os

filePath = "/Users/colorful/Desktop/ME20_40简体中文_繁体中文/cameracontrol/strings.xml"     # 设置strings.xml的路径

appid = '20190617000308218'  # 你的appid
secretKey = 'ntwK9usqie7s0ojom0gP'  # 你的密钥

httpClient = None
myurl = '/api/trans/vip/translate'
fromLang = 'zh'
toLang = 'cht'
salt = random.randint(32768, 65536)

ET.register_namespace('tools', "http://schemas.android.com/tools")
tree = ET.parse(filePath)
root = tree.getroot()

result = True

for child in root:
    sign = appid + child.text + str(salt) + secretKey
    m1 = md5(sign.encode("utf-8"))
    sign = m1.hexdigest()
    requestUrl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        child.text) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    print("requestUrl", requestUrl)
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', requestUrl)

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

    except Exception as e:
        result = False
        print("请求百度翻译接口失败！", e.args)
        print("翻译失败-------", child.text)
    finally:
        if httpClient:
            httpClient.close()

if result is False:
    print("存在翻译失败的字符串, 退出程序!")
    exec(0)

xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, method='xml', encoding="UTF-8").decode(
    "UTF-8")  # 避免声明是单引号
print(xml_str)
targetFile = os.path.dirname(filePath) + "/strings_" + toLang + ".xml"

with open(targetFile, 'w') as xml_file:
    xml_file.write(xml_str)

print("-----XML字段更新完毕！")
