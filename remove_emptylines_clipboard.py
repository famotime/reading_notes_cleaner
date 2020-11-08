"""删除剪贴板文本中所有空行"""
import pyperclip
import time
import re


text = ''
while True:
    # 获取剪贴板文本
    if text != pyperclip.paste():
        text = pyperclip.paste()
        # print(repr(text))
        text = re.sub(r'(\r?\n){2,}', r'\n', text)

        # 整理后文本拷贝到系统剪贴板
        pyperclip.copy(text)
        print('-' * 50)
        print('\n' + text)
        print('-' * 50)

    time.sleep(2)
