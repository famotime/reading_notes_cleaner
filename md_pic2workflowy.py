"""批量提取剪贴板markdown文本中的图片链接，以便批量上传workflowy"""
import pyperclip
import time
import re


content = ''
while True:
    # 获取剪贴板文本
    if content != pyperclip.paste():
        content = pyperclip.paste()

        # 处理剪贴板代码
        if '![' in content:
            links = re.findall(r'!\[.*\]\((.*)\)', content)
            print(links)
            # complete_links = [r'"C:\QMDownload\Python Programming\Python_Work\GitHub\seaborn-doc-zh-master\docs' + ('/'+x).replace("/", "\\") + '"' for x in links]   # 补齐绝对路径
            complete_links = ['"' + x.replace("img/", "") + '"' for x in reversed(links)]   # 截取文件名（因为绝对路径太长）
            content = ' '.join(complete_links)
            # content = (r'C:\QMDownload\Python Programming\Python_Work\GitHub\seaborn-doc-zh-master\docs' + '\\' + content.strip('()')).replace('/', '\\')

        # 整理后文本拷贝到系统剪贴板
        pyperclip.copy(content)
        print('-' * 50)
        print('\n' + content)
        print('-' * 50)

    time.sleep(2)