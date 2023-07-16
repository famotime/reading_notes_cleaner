'''将html文本转换为markdown(.md)，jupyter notebook(.ipynb)，workflowy(.opml)文件'''
import time
import pyperclip
import html2text
import pyperclip
import re
import markdown2opml
import markdown2ipynb


def html2markdown(html):
    '''转换html源码内容为markdown笔记内容'''
    text_maker = html2text.HTML2Text()
    text_maker.ignore_images = True
    text_maker.body_width = 0
    text_maker.single_line_break = True
    text_maker.mark_code = True
    text_maker.skip_internal_links = True
    markdown = text_maker.handle(html)
    # print(repr(markdown))
    # print('-' * 50)

    markdown = re.sub(r'\n(#+) ', lambda x: f'\n{x.group(1)}# ', markdown)  # 所有标题等级都降一级
    # markdown = re.sub(r'!\[\]\(.*?\)', '', markdown)    # 删除图片链接
    print(markdown)
    print('-'*50)

    # markdown = re.sub(r'\s*\*\*(.*?)\*\*\n', lambda x: '\n#### ' + x.group(1) + '\n' if len(x.group(1))<15 else x.group(0), markdown)     # 加粗短行内容设为4级标题
    markdown = re.sub(r'\n\s*?\*\*(.*?)\*\*\s*?\n', lambda x: '\n#### ' + x.group(1) + '\n', markdown)     # 加粗短行内容设为4级标题
    markdown = re.sub(r'\n(#+)\s*?\*\*(.*?)\*\*\n', lambda x: x.group(1) + ' ' + x.group(2) + '\n', markdown)     # 去除标题行加粗标记**...**
    markdown = markdown.replace('>>>', '\n>>>')     # python代码内容增加换行
    markdown = re.sub(r'\n+?`([^`])', lambda x: ' `' + x.group(1), markdown)    # 去除`前面的多余换行
    print(markdown)
    print('-' * 50)

    return markdown


def html2ipynb_clipboard(folder_path):
    '''转换剪贴板HTML源码为Jupyter Notebook(.ipynb文件)'''
    folder = pathlib.Path(folder_path)

    html = pyperclip.paste()
    markdown = h2mc.html2markdown(html)
    title = markdown.split('\n', maxsplit=1)[0].strip(' #')
    title = re.sub('[\/:*?"<>|]', '-', title)
    md_file = folder / (title + '.md')
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(markdown)

    markdown2ipynb.md2ipynb(md_file)


def html2opml_clipboard():
    """转换剪贴板中html源码内容为opml大纲笔记内容（每隔2秒检测一次剪贴板内容）"""
    html = ''
    count = 0
    while count < 5:
        if html != pyperclip.paste():
            html = pyperclip.paste()
            markdown = html2markdown(html)
            # with open('test.md', 'w') as f:
            #     f.write(markdown)
            opml = markdown2opml.md2opml(markdown)
            pyperclip.copy(opml)
            html = opml
            count += 1
        time.sleep(2)


if __name__ == "__main__":
    # 转换剪贴板中html源码内容为markdown笔记内容
    html = pyperclip.paste()
    markdown = html2markdown(html)
    pyperclip.copy(markdown)
