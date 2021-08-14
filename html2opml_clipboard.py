'''
转换剪贴板中html源码内容为opml大纲笔记内容（每隔2秒检测一次剪贴板内容）
'''
import time
import pyperclip
import markdown2opml
import html2markdown_clipboard as h2mc


if __name__ == "__main__":
    html = ''
    while True:
        if html != pyperclip.paste():
            html = pyperclip.paste()
            markdown = h2mc.html2markdown(html)
            opml = markdown2opml.md2opml(markdown)
            pyperclip.copy(opml)
            html = opml
        time.sleep(2)
