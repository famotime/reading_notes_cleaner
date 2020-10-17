# clean_notes

- **extract_descriptions.py:** 抽取指定目录下python脚本描述内容，生成脚本概览(markdown文件)
- **markdown2ipynb.py:** Markdown文档转为Jupyter的ipynb文件
- **markdown2opml.py:** Markdown文档批量转为workflowy、幕布等导图软件支持的opml文件（带层次结构）; Markdown文件须以标题行开头（# XX）; 所有标题行作为清单项，非标题行作为备注
- **markdown_clipboard_2opml.py:** 拷贝到剪贴板的Markdown文档内容转为workflowy支持的opml文件内容（带层次结构）; 所有标题行（#...）作为清单项，非标题行作为备注
- **mubu2workflowy_opml.py:** 把幕布软件导出的opml文件转换成可在workflowy直接张贴的格式
- **pasted_code_cleaner.py:** 每隔2秒自动整理剪贴的python代码，并保存到系统剪贴板
- **readnotes2markdown.py:** 当当云阅读App导出笔记整理成Markdown文档
- **remove_noncode_empty_lines.py:** 删除文本文件中非代码区域的所有空行
