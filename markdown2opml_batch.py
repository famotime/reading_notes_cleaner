"""
合并处理各子目录下markdown/Rmarkdown文件，并转为opml文件
"""
import pathlib
import markdown2opml as md2ol


path = pathlib.Path(r'C:\QMDownload\Python Programming\Python_Work\GitHub\docker_practice-master')

# 处理每个子目录下markdown文件
total = ''
for item in path.glob("**/*"):
    if item.is_dir():
        sub_total = ''
        for md in item.glob("*.md"):
            if 'total' not in md.stem:
                # 添加文件名作为markdown一级标题内容
                with open(md, encoding='utf-8') as f:
                    content = f.read()
                    if not content.startswith(f"# {md.stem}"):
                        content = f"# {md.stem}\n" + f.read()
                    sub_total += content
                with open(md, 'w', encoding='utf-8') as f:
                    f.write(content)
        # 合并子目录下markdown文件内容为sub_total.md文件
        if sub_total:
            sub_total = f"# ---------------------{item.name}\n" + sub_total
            with open(item / 'sub_total.md', 'w', encoding='utf-8') as f:
                f.write(sub_total)
        total += sub_total

# 汇总保存所有子目录下的markdown文件内容
with open(path / 'total.md', 'w', encoding='utf-8') as f:
    f.write(total)

# 将全部markdown文件内容转为opml文件
md_files = list(path.glob('**/*.Rmd')) + list(path.glob('**/*.md'))
for md_file in md_files:
    md2ol.md_file2opml_file(md_file)

print(f"已转换{len(md_files)}个markdown文件为opml文件，请到'{path}'目录下查看。")
