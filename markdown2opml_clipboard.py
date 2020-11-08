'''
拷贝到剪贴板的Markdown文档内容转为workflowy支持的opml文件内容（带层次结构）
所有标题行（#...）作为清单项，非标题行作为备注
'''
import pyperclip
import markdown2opml


md_content = pyperclip.paste()
opml_content = markdown2opml.md2opml(md_content)
pyperclip.copy(opml_content)
