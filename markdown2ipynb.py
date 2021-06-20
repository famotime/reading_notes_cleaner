'''
批量转换Markdown文档为Jupyter Notebook(.ipynb文件)
'''
import pathlib


# ipynb文件头、文件尾、markdown单元格头、代码单元格头、单元格尾
header = '''{
 "nbformat": 4,
 "nbformat_minor": 2,
 "metadata": {
  "language_info": {
   "name": "python",
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "version": "3.7.4"
  },
  "orig_nbformat": 2,
  "file_extension": ".py",
  "mimetype": "text/x-python",
  "name": "python",
  "npconvert_exporter": "python",
  "pygments_lexer": "ipython3",
  "version": 3
 },
 "cells": [
'''
tail = '''   ]
  }
 ]
}'''
mdcell_header = '''  {
   "cell_type": "markdown",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
'''
codecell_header = '''  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
'''
cell_tail = "\n   ]\n  },\n"


def md2ipynb(md_file):
    """转换markdown文件为ipynb文件"""
    ipynb_file = md_file.with_suffix('.ipynb')
    # 注意文件编码格式
    with open(md_file, 'r', encoding='utf-8-sig') as f1:
        with open(ipynb_file, 'w', encoding='utf-8') as f2:
            f2.write(header)

            # 代码块标记计数初始化
            codesign_count = 0

            # ipynb文件以markdown单元格开头
            if not codesign_count:
                f2.write(mdcell_header)
                first_element = True

            for line in f1:
                # ```符号未闭合（单数），写入代码块单元格头，否则写入markdown单元格头
                if line.startswith('```'):
                    codesign_count += 1
                    # 闭合上一个单元格
                    f2.write(cell_tail)
                    if codesign_count % 2 != 0:
                        f2.write(codecell_header)
                    else:
                        f2.write(mdcell_header)
                    first_element = True
                    continue
                else:
                    # 替换markdown文档中的"和\n，并用""括起来
                    line = '    "' + line.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'
                    # 单元格首行内容直接写入
                    if first_element:
                        f2.write(line)
                        first_element = False
                    # 单元格非首行内容先补齐上一行的逗号及换行（,\n），再写入
                    else:
                        line = ',\n' + line
                        f2.write(line)

            # 写入ipynb文件尾
            f2.write(tail)
            print(f'已保存{ipynb_file}，请查看。')


if __name__ == "__main__":
    folder = pathlib.Path(r'C:\Users\Administrator\Desktop')

    for md_file in folder.glob('*.md'):
        md2ipynb(md_file)
