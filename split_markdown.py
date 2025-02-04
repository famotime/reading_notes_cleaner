"""
将 Markdown 文件按标题级别拆分成多个独立的 .md 文件

功能特点:
- 自动识别文件中的标题级别
- 将每个标题级别下的内容分别保存为独立的 .md 文件
- 自动清理文件名中的非法字符
- 支持交互式选择要处理的文件
"""

from pathlib import Path
import re

def split_markdown_by_level(input_file, heading_level=2):
    # 读取输入文件
    content = Path(input_file).read_text(encoding='utf-8')

    # 创建输出子目录
    output_dir = Path(input_file).parent / f"split_level_{heading_level}"
    output_dir.mkdir(exist_ok=True)

    # 根据标题级别生成正则表达式模式
    pattern = r'^' + '#' * heading_level + r' '
    sections = re.split(pattern, content, flags=re.MULTILINE)

    # 处理每个部分
    for section in sections:
        if not section.strip():
            continue

        # 提取标题作为文件名
        lines = section.strip().split('\n')
        if lines[0].startswith('#' * heading_level + ' '):
            title = lines[0].replace('#' * heading_level + ' ', '').strip()
        else:
            title = lines[0].strip()

        # 清理文件名中的非法字符
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)

        # 创建输出文件在子目录中
        output_file = output_dir / f"{safe_title}.md"

        # 写入内容
        output_file.write_text(section.strip(), encoding='utf-8')
        print(f'已创建文件: {output_file}')

if __name__ == '__main__':
    # 获取目录下的所有md文件
    folder_path = input("请输入要处理的文件夹路径: ")
    markdown_files = list(Path(folder_path).glob('*.md'))

    if not markdown_files:
        print("当前目录下没有找到Markdown文件")
        exit()

    print("请选择要拆分的Markdown文件：")
    for i, file in enumerate(markdown_files, 1):
        print(f"{i}. {file.name}")

    try:
        choice = int(input("请输入文件编号: "))
        if 1 <= choice <= len(markdown_files):
            try:
                heading_level_input = input("请输入要拆分的标题级别（1-6，默认为2）: ")
                heading_level = int(heading_level_input) if heading_level_input.strip() else 2
                if 1 <= heading_level <= 6:
                    selected_file = markdown_files[choice-1]
                    split_markdown_by_level(selected_file, heading_level)
                else:
                    print("无效的标题级别，应该在1-6之间")
            except ValueError:
                print("无效的输入，使用默认值2")
                selected_file = markdown_files[choice-1]
                split_markdown_by_level(selected_file, 2)
        else:
            print("无效的选择")
    except ValueError:
        print("请输入有效的数字")