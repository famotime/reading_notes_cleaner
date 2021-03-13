'''
转换剪贴板HTML源码为Jupyter Notebook(.ipynb文件)
'''
import pathlib
import re
import pyperclip
import html2markdown_clipboard as h2mc
import markdown2ipynb


if __name__ == "__main__":
    folder = pathlib.Path(r'C:\Users\Administrator\Desktop')

    html = pyperclip.paste()
    markdown = h2mc.html2markdown(html)
    title = markdown.split('\n', maxsplit=1)[0].strip(' #')
    title = re.sub('[\/:*?"<>|]', '-', title)
    md_file = folder / (title + '.md')
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(markdown)

    markdown2ipynb.md2ipynb(md_file)
