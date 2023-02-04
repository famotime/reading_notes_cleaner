"""
合并处理各子目录下markdown/Rmarkdown文件，并转为opml文件
"""
import pathlib
import datetime
import markdown2opml as md2ol


def add_title(md):
    """添加文件名作为markdown一级标题内容"""
    rewrite = False
    with open(md, encoding='utf-8') as f:
        content = f.read().strip()
        if not content.startswith(f"# {md.stem}"):
            content = f"\n\n# {md.stem}\n" + content + "\n\n"
            rewrite = True
    if rewrite:
        with open(md, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        content += "\n\n"
    return content


def create_total_markdown(path):
    """汇总保存指定目录（含子目录）下所有markdown文件内容为total_日期.md文件"""
    # 处理指定目录下markdown文件
    today = datetime.date.today()
    total = ''
    for md in path.glob("*.md"):
        content = add_title(md)
        total = total + "\n\n" + content + "\n"

    # 处理每个子目录下markdown文件
    for item in path.glob("**/*"):
        if item.is_dir():
            sub_total = ''
            for md in item.glob("*.md"):
                content = add_title(md)
                sub_total += content
            if sub_total:
                # 合并子目录下markdown文件内容
                sub_total = f"\n\n# ----------{item.relative_to(path)}-------------\n" + sub_total
                # with open(item / f'sub_total_{today}.md', 'w', encoding='utf-8') as f:
                #     f.write(sub_total)

            total += sub_total

    # 汇总保存所有子目录下的markdown文件内容为total_日期.md文件
    with open(path / f'total_{today}.md', 'w', encoding='utf-8') as f:
        f.write(total)


if __name__ == "__main__":
    path = pathlib.Path(r'D:\Python_Work\GitHub\docker-master')

    # 汇总保存指定目录（含子目录）下所有markdown文件内容为total_日期.md文件
    create_total_markdown(path)
    # 将全部markdown文件转为opml文件
    md_files = list(path.glob('**/*.Rmd')) + list(path.glob('**/*.md'))
    for md_file in md_files:
        md2ol.md_file2opml_file(md_file)
    print(f"已转换{len(md_files)}个markdown文件为opml文件，请到'{path}'目录下查看。")
