import pathlib
from ipynb2markdown import ipynb2md
from markdown2opml import md_file2opml_file


folder = pathlib.Path(r'C:\QMDownload\Python Programming\Python_Work\GitHub\numpy-cn-1.17\docs\article')

for count, ipynb_file in enumerate(folder.glob('**/*.ipynb'), 1):
    print(f'正在处理文件：{ipynb_file}……')
    ipynb2md(ipynb_file)
try:
    print(f"已转换{count}个ipynb文件为markdown文件，请到'{folder}'目录下查看。")
except Exception as e:
    print("未发现.ipynb文件。")

for count, md_file in enumerate(folder.glob('**/*.md'), 1):
    print(f'正在处理文件：{md_file}……')
    md_file2opml_file(md_file)
print(f"已转换{count}个markdown文件为opml文件，请到'{folder}'目录下查看。")
