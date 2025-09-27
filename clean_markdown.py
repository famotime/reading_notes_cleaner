"""
清理从网页拷贝的markdown文本：
1. 指定原始markdown文本文件；
2. 读取文件内容，按规则清理文本；
  - 删除所有英文网站和网址文本，包括markdown链接以及非链接的网址文本；
  - 一行文本少于25个字，且以数字开头，则作为3级标题；
  - 一行文本少于25个字，且以中文或英文冒号结尾，则作为4级标题；
  - 去除所有空白行；
  - 一行文本只包含"•"，则删除该行；
  - 若一行文本不以标点符号结尾，则去除换行符；
3. 将清理后的文本保存到新的文件中。
"""
from pathlib import Path
import re

def clean_markdown(input_file: Path) -> str:
    """
    清理markdown文本

    Args:
        input_file: 输入文件路径

    Returns:
        清理后的文本内容
    """
    # 读取文件内容
    content = input_file.read_text(encoding='utf-8')

    # 按行处理文本
    cleaned_lines = []
    prev_line = ''

    for line in content.splitlines():
        line = line.strip("# ")
        # 跳过空白行
        if not line.strip() or line.strip() == '•':
            continue

        # 删除markdown链接 [文本](链接)
        line = re.sub(r'\[.*?\]\(.*?\)', '', line)
        # 删除普通网址 http:// 或 https:// 开头的文本
        line = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', line)

        # 处理数字开头的短文本（如：1. 2. 3.）转为三级标题
        if re.match(r'^\d+', line.strip()):
            line = f'### {line}\n'

        # 处理冒号结尾的短文本转为四级标题
        if line.strip().endswith(':') or line.strip().endswith('：'):
            line = f'#### {line.strip(":：")}\n'

        # # 处理项目符号
        # elif line.strip() == '•':
        #     line = '- '

        # 检查行尾是否有标点符号（中英文标点都包括）
        if not re.search(r'[，。！？、：；,.!?:;"”]$', line.strip()):
            # 如果不是以标点符号结尾，且不是标题行或列表项
            if not line.strip().startswith(('#', '-')):
                line = line.rstrip()   # 去除换行符
        else:
            line = line + '\n'  # 有标点符号结尾的保留换行符

        if not line.startswith('#') and line.startswith('**'):
            line = '- ' + line
        cleaned_lines.append(line)

    new_content = '\n'.join(cleaned_lines).replace('\n。', '。')

    return new_content

def main():
    # 设置输入输出路径
    input_path = Path(r'H:\BaiduSyncdisk\思维模型\查理芒格的100个思维模型研究（中文信息源）.md')
    output_path = input_path.with_stem(input_path.stem + '_cleaned')

    # 处理文件
    if input_path.exists():
        cleaned_content = clean_markdown(input_path)
        output_path.write_text(cleaned_content, encoding='utf-8')
        print(f'清理完成！输出文件：{output_path}')
    else:
        print(f'错误：找不到输入文件 {input_path}')

if __name__ == '__main__':
    main()
