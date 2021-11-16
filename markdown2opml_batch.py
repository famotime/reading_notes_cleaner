"""
合并处理各子目录下markdown文件，并转为opml文件
"""
import pathlib
import markdown2opml as md2ol


path = pathlib.Path(r'C:\QMDownload\Python Programming\Python_Work\GitHub\html_css\Web-master')

# 处理每个子目录下markdown文件
for item in path.glob("**/*"):
    if item.is_dir():
        total = ''
        for md in item.glob("*.md"):
            # 添加文件名作为markdown一级标题内容
            with open(md, encoding='utf-8') as f:
                content = f"# {md.stem}\n" + f.read()
                total += content
            with open(md, 'w', encoding='utf-8') as f:
                f.write(content)
        # 合并markdown文件内容为total.md文件
        with open(item / 'total.md', 'w', encoding='utf-8') as f:
            f.write(total)

md_files = list(path.glob('**/*.Rmd')) + list(path.glob('**/*.md'))
for md_file in md_files:
    md2ol.md_file2opml_file(md_file)
print(f"已转换{len(md_files)}个markdown文件为opml文件，请到'{path}'目录下查看。")
