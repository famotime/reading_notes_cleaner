"""将markdown文件中的图片相对路径改为绝对路径"""
import pathlib
import re


def md_abs_img_path(md_file):
    """将markdown文件中的图片相对路径改为绝对路径"""
    with open(md_file, encoding='utf-8') as f:
        content = f.read()
    if '![' in content:
        content = re.sub(r'!\[.*?\]\((.*?)\)', lambda x: f"![]({(md_file.parent / pathlib.Path(x.group(1))).absolute()})", content)
        md_file_abs = md_file.with_name(md_file.stem + '_abs.md')
        with open(md_file_abs, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"已保存文件{md_file_abs.absolute()}。")
    else:
        print(f"在{md_file.absolute()}未发现图片链接，跳过……")


if __name__ == "__main__":
    # 处理文件夹内所有md文件
    # md_folder = pathlib.Path(r'C:\QMDownload\Python Programming\Python_Work\Web Spider\my_douban_books\my_douban_data')
    # for md_file in [x for x in md_folder.glob('*.md') if not '_abs' in x.stem]:
    #     md_abs_img_path(md_file)

    # 处理单个md文件
    md_file = pathlib.Path(r"C:\QMDownload\Python Programming\Python_Work\Web Spider\my_douban_books\my_douban_data\2022年6月读书小记.md")
    md_abs_img_path(md_file)
