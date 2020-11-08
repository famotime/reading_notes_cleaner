"""删除文本文件中非代码区域的所有空行"""


path = r'C:\QMDownload\Python Programming\Python_Work\data_analysis\可视化\Python数据可视化编程实战\Python数据可视化编程实战(第2版).md'
new_path = r'C:\QMDownload\Python Programming\Python_Work\data_analysis\可视化\Python数据可视化编程实战\Python数据可视化编程实战(第2版)_new.md'

code_mark = 0
f = []
with open(path, 'r', encoding='utf-8') as f1:
    for line in f1:
        if line.startswith('```'):
            code_mark += 1
        if code_mark % 2 == 0:
            if line.strip():
                f.append(line)
        else:
            f.append(line)

with open(new_path, 'w', encoding='utf-8') as f2:
    f2.writelines(f)
