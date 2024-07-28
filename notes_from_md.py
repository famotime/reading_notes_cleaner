"""从markdown文本中摘取章节名称和粗体字内容"""
import pyperclip
import re

s = pyperclip.paste()
lines = s.split('\n')
contents = []
for i in lines:
    if i.startswith('#'):
        contents.append(i)
    elif '**' in i:
        line = re.findall(r"\*\*(.*?)\*\*", i)
        contents.append(''.join(line))

s1 = '\n\n'.join(contents)
# print(s1)
pyperclip.copy(s1)
