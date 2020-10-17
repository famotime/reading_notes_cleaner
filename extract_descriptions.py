"""提取指定目录下python脚本描述内容，生成脚本概览(markdown文件)"""
import pathlib
import re


path = r'C:\QMDownload\Python Programming\Python_Work\reading_notes_cleaner'

path = pathlib.Path(path)
folder = path.parts[-1]
python_scripts = [file for file in path.glob("*.py")]

content = f'# {folder}\n'
for pyfile in python_scripts:
    with open(pyfile, encoding='utf-8') as f:
        description = re.match(r"('''|\"\"\")(.*?)('''|\"\"\")", f.read(), flags=re.DOTALL).group(2).strip().replace('\n', '; ')
        content += '- **{}:** {}'.format(pyfile.name, description + '\n')

output = path / (folder + '.md')
with open(output, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'已生成脚本概览"{output}"。')
