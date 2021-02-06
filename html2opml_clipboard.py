'''
转换剪贴板中html源码内容为opml大纲笔记内容
'''
import html2text
import pyperclip
import markdown2opml
import re


html = pyperclip.paste()

# markdown = html2text.html2text(html)
text_maker = html2text.HTML2Text()
text_maker.ignore_images = True
text_maker.single_line_break = True
text_maker.mark_code = True
markdown = text_maker.handle(html)
# print(repr(markdown))
# print('-' * 50)

markdown = re.sub(r'\n(#+) ', lambda x: f'\n{x.group(1)}# ', markdown)  # 所有标题等级都降一级
# markdown = re.sub(r'!\[\]\(.*?\)', '', markdown)    # 删除图片链接
print(markdown)
print('-'*50)

# markdown = re.sub(r'\s*\*\*(.*?)\*\*\n', lambda x: '\n#### ' + x.group(1) + '\n' if len(x.group(1))<15 else x.group(0), markdown)     # 加粗短行内容设为4级标题
markdown = re.sub(r'\n\s*?\*\*(.*?)\*\*\n', lambda x: '\n#### ' + x.group(1) + '\n', markdown)     # 加粗短行内容设为4级标题
markdown = re.sub(r'\n(#+)\s*?\*\*(.*?)\*\*\n', lambda x: x.group(1) + ' ' + x.group(2) + '\n', markdown)     # 去除标题行加粗标记**...**
markdown = markdown.replace('>>>', '\n>>>')     # python代码内容增加换行
print(markdown)
print('-' * 50)

opml = markdown2opml.md2opml(markdown)
pyperclip.copy(opml)
