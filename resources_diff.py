from xml.etree import ElementTree as ET
import os

src_file_path = "/Users/colorful/Desktop/ME20_40_translate/NE60/strings.xml"
dst_file_path = "/Users/colorful/Desktop/ME20_40_translate/NE60/strings_rtw.xml"

ET.register_namespace('tools', "http://schemas.android.com/tools")
srcTree = ET.parse(src_file_path)
srcRoot = srcTree.getroot()

srcList = []
for srcChild in srcRoot:
    srcList.append(srcChild.attrib["name"])

dstTree = ET.parse(dst_file_path)
dstRoot = dstTree.getroot()
dstList = []
for dstChild in dstRoot:
    dstList.append(dstChild.attrib["name"])

# 遍历时删除的方法[:]
for srcChild in srcRoot[:]:
    if srcChild.attrib["name"] in dstList:
        srcRoot.remove(srcChild)

xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(srcRoot, method='xml', encoding="UTF-8").decode(
    "UTF-8")  # 避免声明是单引号
targetFile = os.path.dirname(src_file_path) + "/strings_out.xml"

with open(targetFile, 'w') as xml_file:
    xml_file.write(xml_str)

print("文件差分对比结束！")
