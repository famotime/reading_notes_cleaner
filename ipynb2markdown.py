'''
批量转换Jupyter notebook(.ipynb文件)为Markdown文档
'''
import pathlib
import json
import re
import base64
import logging
logging.basicConfig(level=logging.DEBUG, filename='debug.log')


def ipynb2md(ipynb_file):
    """转换ipynb文件为markdown文件"""
    md_file = ipynb_file.with_suffix('.md')
    content = f'# {ipynb_file.stem}\n'
    image_num = 0
    with open(ipynb_file, encoding='utf-8') as f1:
        with open(md_file, 'w', encoding='utf-8') as f2:
            cells = json.loads(f1.read())['cells']
            for cell in cells:
                if cell["cell_type"] == "markdown":
                    try:
                        content += ''.join(cell["source"]) + '\n'
                    except Exception as e:
                        print(e)
                elif cell["cell_type"] == "code":
                    codes = re.sub(r'# *', '# ', ''.join(cell["source"]))   # 代码注释规范化
                    content += "\n```python\n" + codes + "\n```\n"
                    if cell["outputs"]:
                        try:
                            if "data" in cell["outputs"][0]:
                                # 保存图片
                                if "image/png" in cell["outputs"][0]["data"]:
                                    data = cell["outputs"][0]["data"]["image/png"]
                                    image_data = base64.b64decode(data)
                                    if not (ipynb_file.parent / "images").is_dir():
                                        (ipynb_file.parent / "images").mkdir()
                                    with open(ipynb_file.parent / f'images/image_{image_num}.png', 'wb') as f_image:
                                        f_image.write(image_data)
                                    content += f'![image](./images/image_{image_num}.png)\n'
                                    image_num += 1
                                else:
                                    content += '```\n' + ''.join(cell["outputs"][0]["data"]["text/plain"]) + '\n```\n'
                            # 采集print打印输出内容
                            if "text" in cell["outputs"][0]:
                                content += '```\n' + ''.join(cell["outputs"][0]["text"]) + '\n```\n'
                        except Exception as e:
                            logging.debug(e)
                            logging.debug(ipynb_file)
                            logging.debug(cell)
                            logging.debug('\n')

            f2.write(content)


if __name__ == "__main__":
    folder = pathlib.Path(r'D:\Python_Work\data_analysis\可视化\test')

    for count, ipynb_file in enumerate(folder.glob('*.ipynb'), 1):
        ipynb2md(ipynb_file)
    print(f"已转换{count}个ipynb文件为markdown文件，请到'{folder}'目录下查看。")
