"""Markdown读书笔记处理辅助脚本：
- 剪贴板文本处理:
    - 删除多余空行
    - 删除时间标记
    - 处理markdown标题层级
    - 提取并处理图片链接
- 文件处理:
    - 删除非代码区域空行
    - 复制markdown文件及其图片
    - 转换图片相对路径为绝对路径
    - 批量处理OPML文件到Workflowy
    - 提取Python脚本文档字符串生成概览

使用方法:
大部分函数可以直接调用，部分函数(如remove_emptylines_clipboard)
会持续监听剪贴板变化并自动处理。
"""
import pathlib
import pyperclip
import time
import re
import pyautogui


def remove_emptylines_clipboard():
    """删除剪贴板文本中所有多余空行"""
    text = ''
    while True:
        # 获取剪贴板文本
        if text != pyperclip.paste():
            text = pyperclip.paste()
            # print(repr(text))
            text = re.sub(r'\n\s*[\r\n]', r'\n', text)

            # 整理后文本拷贝到系统剪贴板
            pyperclip.copy(text)
            print('-' * 50)
            print('\n' + text)
            print('-' * 50)
        time.sleep(2)


def remove_noncode_emptylines(file_path):
    """删除文本文件中非代码区域的所有空行"""
    file_path = pathlib.Path(file_path)
    new_path = file_path.with_name(file_path.stem + '_new' + file_path.suffix)

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


def remove_timemark_clipboard():
    """删除剪贴板文本中所有时间标记"""
    text = pyperclip.paste()
    # print(repr(text))
    text = re.sub(r'\n\d\d\d\d-\d\d-\d\d.*', '\n', text)
    pyperclip.copy(text)


def copy_md_with_img(file_path):
    """将md文件及内容中包含的图片文件拷贝到指定目录"""
    md_path = pathlib.Path(file_path)

    dest_folder = md_path.parent / "export"
    dest_folder.mkdir(exist_ok=True)

    with open(md_path, encoding='utf-8') as f:
        content = f.read()
    img_list = re.findall(r'!\[.*?\]\((.*?)\)', content)

    (dest_folder / md_path.name).write_text(content)
    for img in img_list:
        data = (md_path.parent / img).read_bytes()
        img_folder = dest_folder / img
        img_folder.parent.mkdir(exist_ok=True)
        img_folder.write_bytes(data)


def md_with_abs_imgpath(md_file):
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


def md_pic2workflowy():
    """批量提取剪贴板markdown文本中的图片链接，以便批量上传workflowy"""
    content = ''
    while True:
        # 获取剪贴板文本
        if content != pyperclip.paste():
            content = pyperclip.paste()

            # 处理剪贴板代码
            if '![' in content:
                links = re.findall(r'!\[.*\]\((.*)\)', content)
                print(links)
                # complete_links = [r'"C:\QMDownload\Python Programming\Python_Work\GitHub\seaborn-doc-zh-master\docs' + ('/'+x).replace("/", "\\") + '"' for x in links]   # 补齐绝对路径
                complete_links = ['"' + x.replace("img/", "") + '"' for x in reversed(links)]   # 截取文件名（因为绝对路径太长）
                content = ' '.join(complete_links)
                # content = (r'C:\QMDownload\Python Programming\Python_Work\GitHub\seaborn-doc-zh-master\docs' + '\\' + content.strip('()')).replace('/', '\\')

            # 整理后文本拷贝到系统剪贴板
            pyperclip.copy(content)
            print('-' * 50)
            print('\n' + content)
            print('-' * 50)

        time.sleep(2)


def batch_opml2workflowy(folder_path):
    """将指定目录下opml文件内容批量复制到workflowy（自动键鼠操作）"""
    pyautogui.FAILSAFE = True
    # pyautogui.PAUSE = 1
    folder = pathlib.Path(folder_path)

    opml_files = sorted(folder.glob('**/*.opml'), key=lambda x: x.stem)
    time.sleep(5)
    for num, opml in enumerate(opml_files, 1):
        with open(opml, encoding='utf-8') as f:
            content = f.read()
        pyperclip.copy(content)
        pyautogui.hotkey('ctrl', 'v')   # 粘贴
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'up')  # 折叠
        time.sleep(1)
        pyautogui.press(['end', 'enter'])   # 在粘贴内容后新建item

    pyautogui.press(['end', 'enter'])
    pyperclip.copy(f'已完成{num}个文件内容粘贴，请查看。')
    pyautogui.hotkey('ctrl', 'v')   # 粘贴


def markdown_title_correction():
    """markdown文件标题层级修正"""
    content = ''
    while True:
        if pyperclip.paste() != content and pyperclip.paste().startswith('#'):
            content = pyperclip.paste()
            content = content.replace('#', '##').replace('-', '').strip()
            pyperclip.copy(content)
            print(content)
        time.sleep(2)


def extract_md_descriptions(folder_path):
    """提取指定目录下python脚本描述内容，生成脚本概览(markdown文件)"""
    path = pathlib.Path(folder_path)
    folder = path.parts[-1]
    python_scripts = [file for file in path.glob("*.py")]

    content = f'# {folder}\n'
    for pyfile in python_scripts:
        with open(pyfile, encoding='utf-8') as f:
            try:
                description = re.match(r"('''|\"\"\")(.*?)('''|\"\"\")", f.read(), flags=re.DOTALL).group(2).strip().replace('\n', '; ')
                content += '- **{}:** {}'.format(pyfile.name, description + '\n')
            except Exception:
                print(f"{pyfile.name}解析失败，跳过……")

    output = path / (folder + '_脚本描述.md')
    with open(output, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'已生成脚本概览"{output}"。')


def extract_headings_and_bold(text: str = None) -> str:
    """从markdown文本中提取标题和粗体内容

    Args:
        text: 要处理的markdown文本，如果为None则从剪贴板读取

    Returns:
        str: 提取出的标题和粗体内容，以双换行符分隔
    """
    if text is None:
        text = pyperclip.paste()

    lines = text.split('\n')
    contents = []

    for line in lines:
        if line.startswith('#'):
            contents.append(line)
        elif '**' in line:
            bold_texts = re.findall(r"\*\*(.*?)\*\*", line)
            contents.append(''.join(bold_texts))

    return '\n\n'.join(contents)

def extract_to_clipboard():
    """从剪贴板读取markdown文本，提取标题和粗体内容后写回剪贴板"""
    result = extract_headings_and_bold()
    pyperclip.copy(result)


if __name__ == "__main__":
    # 将文件夹内所有md文件中的图片相对路径改为绝对路径
    # md_folder = pathlib.Path(r'C:\QMDownload\Python Programming\Python_Work\Web Spider\my_douban_books\my_douban_data')
    # for md_file in [x for x in md_folder.glob('*.md') if not '_abs' in x.stem]:
    #     md_with_abs_imgpath(md_file)

    # 将markdown文件中的图片相对路径改为绝对路径
    # md_file = pathlib.Path(r"C:\QMDownload\Backup\Wiz Knowledge\exported_md\My Drafts\我看不懂，但我大受震撼——AI绘画初体验.md")
    # md_with_abs_imgpath(md_file)

    # 提取剪贴板markdown文本中的标题和粗体内容
    extract_to_clipboard()
    