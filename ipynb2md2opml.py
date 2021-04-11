import pathlib
from ipynb2markdown import ipynb2md
from markdown2opml import md_file2opml_file


folder = pathlib.Path(r'C:\QMDownload\Python Programming\Python_Work\GitHub\Beautiful-Visualization-with-python-master\第11章 数据可视化案例\11.5. 中国疫情新冠肺炎COVID-19动图')

for count, ipynb_file in enumerate(folder.glob('*.ipynb'), 1):
    ipynb2md(ipynb_file)
print(f"已转换{count}个ipynb文件为markdown文件，请到'{folder}'目录下查看。")

for count, md_file in enumerate(folder.glob('*.md'), 1):
    md_file2opml_file(md_file)
print(f"已转换{count}个markdown文件为opml文件，请到'{folder}'目录下查看。")
