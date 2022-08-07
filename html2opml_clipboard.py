'''
转换剪贴板中html源码内容为opml大纲笔记内容（每隔2秒检测一次剪贴板内容）
'''
import time
import pyperclip
import markdown2opml
import html2markdown_clipboard as h2mc


if __name__ == "__main__":
    html = ''
    count = 0
    while count < 100:
        if html != pyperclip.paste():
            html = pyperclip.paste()
            markdown = h2mc.html2markdown(html)
            # with open('test.md', 'w') as f:
            #     f.write(markdown)
            opml = markdown2opml.md2opml(markdown)
            pyperclip.copy(opml)
            html = opml
            count += 1
        time.sleep(2)
