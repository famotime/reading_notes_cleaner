"""删除剪贴板文本中所有时间标记"""
import pyperclip
import re


text = pyperclip.paste()
# print(repr(text))
text = re.sub(r'\n\d\d\d\d-\d\d-\d\d.*', '\n', text)

pyperclip.copy(text)
