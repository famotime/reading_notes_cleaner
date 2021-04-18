"""将vs code的交互式py文件转换为Jupyter Notebook文件"""
import pathlib
import json


def get_cells(py_file):
    """获取所有单元格内容"""
    cells = []
    cell_init = False
    with open(py_file, encoding='utf-8') as f:
        for line in f:
            if line.startswith('# %%') or line.startswith('#%%'):
                if cell_init:
                    cell["source"][-1] = cell["source"][-1].strip()
                    cells.append(cell)
                cell = {}
                cell_init = True
                if line.startswith('# %% [markdown]') or line.startswith('#%% [markdown]'):
                    cell["cell_type"] = "markdown"
                    cell["source"] = []
                    cell["metadata"] = {}
                else:
                    cell["cell_type"] = "code"
                    cell["execution_count"] = None
                    cell["metadata"] = {}
                    cell["outputs"] = []
                    cell["source"] = []
            elif cell_init:
                cell["source"].append(line)
        cells.append(cell)
    return cells


def save_ipynb_content(cells, ipynb_file):
    """补齐notebook文件框架内容，并保存到ipynb文件"""
    ipynb_content = {
                "metadata": {
                    "language_info": {
                        "codemirror_mode": {
                            "name": "ipython",
                            "version": 3
                            },
                        "file_extension": ".py",
                        "mimetype": "text/x-python",
                        "name": "python",
                        "nbconvert_exporter": "python",
                        "pygments_lexer": "ipython3",
                        "version": 3
                    },
                    "orig_nbformat": 2
                    },
                "nbformat": 4,
                "nbformat_minor": 2,
                }

    ipynb_content["cells"] = cells

    with open(ipynb_file, 'w', encoding='utf-8') as f:
        json.dump(ipynb_content, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    folder = pathlib.Path(r'C:\QMDownload\Python Programming\Python_Work\GitHub\Beautiful-Visualization-with-python-master\第11章 数据可视化案例\11.4_动态数据可视化演示')

    py_files = list(folder.glob('*.py'))
    for py_file in py_files:
        print(f'正在转换文件：{py_file}……')
        ipynb_file = py_file.with_suffix('.ipynb')
        cells = get_cells(py_file)
        save_ipynb_content(cells, ipynb_file)
    print(f"共将{len(py_files)}个Python脚本文件转换为Jupyter Notebook文件，请查看。")
