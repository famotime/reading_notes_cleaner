"""
合并处理各子目录下markdown/Rmarkdown/mdx文件，并转为opml文件
"""
import pathlib
import datetime
import markdown2opml as md2ol


def add_title(md, rewrite=False):
    """添加文件名作为markdown一级标题内容"""
    with open(md, encoding='utf-8') as f:
        content = f.read().strip()
        if not content.startswith(f"# {md.stem}"):
            content = f"\n\n# {md.stem}\n" + content + "\n\n"
    if rewrite:
        with open(md, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        content += "\n\n"
    return content


def create_total_markdown(path, md_suffix):
    """汇总所有markdown文件内容为total_日期.md文件"""
    # 处理指定目录下markdown文件
    today = datetime.date.today()
    total = ''

    md_files = find_markdown_files(path, md_suffix)
    for md in md_files:
        content = add_title(md)
        total = total + "\n\n" + content + "\n"

    # 处理每个子目录下markdown文件
    # for item in path.glob("**/*"):
    #     if item.is_dir():
    #         sub_total = ''
    #         for md in find_markdown_files(item, md_suffix):
    #             content = add_title(md)
    #             sub_total += content
    #         if sub_total:
    #             # 合并子目录下markdown文件内容
    #             sub_total = f"\n\n# ----------{item.relative_to(path)}-------------\n" + sub_total
    #             # with open(item / f'sub_total_{today}.md', 'w', encoding='utf-8') as f:
    #             #     f.write(sub_total)

    #         total += sub_total

    # 汇总保存所有子目录下的markdown文件内容为total_日期.md文件
    total_file_path = path / f'total_{today}.md'
    with open(path / total_file_path, 'w', encoding='utf-8') as f:
        f.write(total)

    return path / total_file_path


def find_markdown_files(directory, md_suffix):
    """获取指定目录及其子目录下所有特定后缀名的文件路径"""
    markdown_files = []
    for file_path in directory.glob('**/*'):
        if file_path.is_file() and file_path.suffix.lower() in md_suffix:
            markdown_files.append(file_path)

    return markdown_files


if __name__ == "__main__":
    path = pathlib.Path(r'D:\Python_Work\GitHub\comflowy-main')

    md_suffix = ['.md', '.rmd', '.mdx']     # 文件名后缀列表

    # 汇总保存指定目录（含子目录）下所有markdown文件内容为total_日期.md文件，并转为opml文件
    total_file_path = create_total_markdown(path, md_suffix)
    md2ol.md_file2opml_file(total_file_path)

    # 将全部markdown文件转为opml文件
    # md_files = find_markdown_files(path, md_suffix)
    # for md_file in md_files:
    #     md2ol.md_file2opml_file(md_file)
    # print(f"已转换{len(md_files)}个markdown文件为opml文件，请到'{path}'目录下查看。")
