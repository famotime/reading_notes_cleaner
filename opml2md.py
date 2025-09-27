"""
将opml文件转换为多层次目录结构下的多个markdown文件
1. 目录节点：一个outline节点如果没有_note属性，则以节点名称创建目录；子节点如果没有_note属性，则以子节点名称创建子目录；
2. 文档节点：一个outline节点如果有_note属性，则以节点名称为文件名创建markdown文件，文件内容为_note属性内容，节点名称为一级标题；markdown文件应创建在对应的目录中；
3. 文档节点的子节点如果有_note属性，子文档节点需要以父文档节点名称为前缀+子节点名称作为新文档名称创建markdown文档，新文档名称作为文件名，文件内容为子节点_note属性内容，新文档名称为一级标题；
4. 需要遍历每一个outline节点并按上述规则处理，包括目录节点和文档节点的子节点；
5. 以输出目录为根目录创建相应的目录结构和markdown文件；

使用方法：
1. 直接运行：修改 main() 函数中的文件路径，然后运行 python opml2md.py
2. 命令行运行：python opml2md.py input_file.opml -o output_dir
"""

import xml.etree.ElementTree as ET
import argparse
from pathlib import Path
import html
import re


def clean_filename(filename):
    """清理文件名，移除或替换不合法字符"""
    # 移除或替换Windows文件名中不允许的字符
    invalid_chars = r'[<>:"/\\|?*]'
    filename = re.sub(invalid_chars, '_', filename)
    # 移除首尾空格和点
    filename = filename.strip(' .')
    # 限制长度
    if len(filename) > 200:
        filename = filename[:200]
    return filename


def html_unescape(text):
    """HTML实体解码"""
    if not text:
        return text
    return html.unescape(text)


def clean_html_entities_in_attributes(text):
    """
    清理text和_note属性中的HTML转义符号
    
    Args:
        text: 属性值字符串
        
    Returns:
        清理后的字符串
    """
    if not text:
        return text
    
    # 处理常见的HTML转义符号
    replacements = {
        '&lt;/a&gt;&#10;': '</a>\n',  # 链接结束标签 + 换行符
        '&lt;a href=&quot;': '<a href="',  # 链接开始标签
        '&quot;&gt;': '">',  # 链接属性结束
        '&lt;/a&gt;': '</a>',  # 链接结束标签
        '&lt;': '<',  # 小于号
        '&gt;': '>',  # 大于号
        '&quot;': '"',  # 双引号
        '&#10;': '\n',  # 换行符
        '&#13;': '\r',  # 回车符
        '&#9;': '\t',  # 制表符
        '&amp;': '&',  # 和号（需要最后处理）
    }
    
    # 按顺序进行替换
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def process_outline(outline, output_dir, current_path=None, parent_text=""):
    """
    递归处理outline节点
    
    Args:
        outline: outline节点
        output_dir: 输出根目录
        current_path: 当前路径（Path对象）
        parent_text: 父节点文本（用于生成子文档名称）
    """
    if current_path is None:
        current_path = output_dir
    
    # 获取节点文本并清理HTML转义符号
    text = outline.get('text', '').strip()
    if text:
        text = clean_html_entities_in_attributes(text)
    
    
    
    # 清理文件名
    clean_text = clean_filename(text) if text else ""
    
    # 检查是否有_note属性并清理HTML转义符号
    note = outline.get('_note', '').strip()
    if note:
        note = clean_html_entities_in_attributes(note)
    
    # 检查子节点是否有_note属性
    has_children_with_notes = False
    for child in outline:
        if child.tag == 'outline' and child.get('_note', '').strip():
            has_children_with_notes = True
            break
    
    # 如果text为空，只处理子节点
    if not text:
        # 处理子节点
        for child in outline:
            if child.tag == 'outline':
                process_outline(child, output_dir, current_path, parent_text)
        return
    
    if note:
        # 有_note属性，创建markdown文件
        # 解码HTML实体
        note_content = html_unescape(note)
        text_content = html_unescape(text)
        
        # 生成文件名（如果有父节点，包含父节点前缀）
        if parent_text:
            combined_name = f"{parent_text} - {text}"
            clean_combined_name = clean_filename(combined_name)
            md_filename = f"{clean_combined_name}.md"
        else:
            md_filename = f"{clean_text}.md"
        
        md_file_path = current_path / md_filename
        
        # 确保目录存在
        current_path.mkdir(parents=True, exist_ok=True)
        
        # 写入markdown文件
        with open(md_file_path, 'w', encoding='utf-8') as f:
            if parent_text:
                combined_text_content = html_unescape(combined_name)
                f.write(f"# {combined_text_content}\n\n")
            else:
                f.write(f"# {text_content}\n\n")
            f.write(note_content)
        
        print(f"创建文件: {md_file_path}")
        
        # 处理子节点
        for child in outline:
            if child.tag == 'outline':
                child_note = child.get('_note', '').strip()
                if child_note:
                    child_note = clean_html_entities_in_attributes(child_note)
                child_text = child.get('text', '').strip()
                if child_text:
                    child_text = clean_html_entities_in_attributes(child_text)
                
                
                if child_note:
                    # 子节点有_note属性，创建以父节点+子节点为名称的文档
                    if child_text:
                        # 生成组合文档名称
                        combined_name = f"{text} - {child_text}"
                        
                        clean_combined_name = clean_filename(combined_name)
                        child_note_content = html_unescape(child_note)
                        combined_text_content = html_unescape(combined_name)
                        
                        # 创建markdown文件
                        md_filename = f"{clean_combined_name}.md"
                        md_file_path = current_path / md_filename
                        
                        # 确保目录存在
                        current_path.mkdir(parents=True, exist_ok=True)
                        
                        # 写入markdown文件
                        with open(md_file_path, 'w', encoding='utf-8') as f:
                            f.write(f"# {combined_text_content}\n\n")
                            f.write(child_note_content)
                        
                        print(f"创建文件（子文档）: {md_file_path}")
                        
                        # 检查子节点是否还有子节点需要处理（只处理子节点的子节点，不重复处理子节点本身）
                        for grandchild in child:
                            if grandchild.tag == 'outline':
                                process_outline(grandchild, output_dir, current_path, combined_name)
                else:
                    # 子节点没有_note属性，递归处理
                    process_outline(child, output_dir, current_path, text)
    else:
        # 没有_note属性，创建目录（目录节点）
        dir_path = current_path / clean_text
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"创建目录（目录节点）: {dir_path}")
        
        # 更新当前路径
        current_path = dir_path
        
        # 处理子节点
        for child in outline:
            if child.tag == 'outline':
                child_note = child.get('_note', '').strip()
                if child_note:
                    child_note = clean_html_entities_in_attributes(child_note)
                    # 子节点有_note属性，创建以父节点+子节点为名称的文档
                    child_text = child.get('text', '').strip()
                    if child_text:
                        child_text = clean_html_entities_in_attributes(child_text)
                        # 生成组合文档名称
                        if parent_text:
                            combined_name = f"{parent_text} - {child_text}"
                        else:
                            combined_name = child_text
                        
                        clean_combined_name = clean_filename(combined_name)
                        child_note_content = html_unescape(child_note)
                        combined_text_content = html_unescape(combined_name)
                        
                        # 创建markdown文件
                        md_filename = f"{clean_combined_name}.md"
                        md_file_path = current_path / md_filename
                        
                        # 确保目录存在
                        current_path.mkdir(parents=True, exist_ok=True)
                        
                        # 写入markdown文件
                        with open(md_file_path, 'w', encoding='utf-8') as f:
                            f.write(f"# {combined_text_content}\n\n")
                            f.write(child_note_content)
                        
                        print(f"创建文件（子文档）: {md_file_path}")
                        
                        
                        # 检查子节点是否还有子节点需要处理（只处理子节点的子节点，不重复处理子节点本身）
                        for grandchild in child:
                            if grandchild.tag == 'outline':
                                process_outline(grandchild, output_dir, current_path, combined_name)
                else:
                    # 子节点没有_note属性，递归处理
                    process_outline(child, output_dir, current_path, parent_text)


def convert_opml_to_markdown(opml_file, output_dir):
    """
    将OPML文件转换为markdown文件结构
    
    Args:
        opml_file: OPML文件路径
        output_dir: 输出目录路径
    """
    # 解析OPML文件
    try:
        tree = ET.parse(opml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"解析OPML文件失败: {e}")
        return
    except FileNotFoundError:
        print(f"文件不存在: {opml_file}")
        return
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 查找body节点
    body = root.find('body')
    if body is None:
        print("未找到body节点")
        return
    
    # 处理所有outline节点
    for outline in body.findall('outline'):
        process_outline(outline, output_path)
    
    print(f"转换完成！输出目录: {output_path.absolute()}")


def main_cli():
    """命令行版本的主函数"""
    parser = argparse.ArgumentParser(description='将OPML文件转换为多层次目录结构下的多个markdown文件')
    parser.add_argument('opml_file', help='输入的OPML文件路径')
    parser.add_argument('-o', '--output', default='output', help='输出目录路径（默认为output）')
    
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    if not Path(args.opml_file).exists():
        print(f"错误: 文件不存在 - {args.opml_file}")
        return
    
    # 执行转换
    convert_opml_to_markdown(args.opml_file, args.output)


if __name__ == "__main__":
    # ========== 在这里修改文件路径 ==========
    opml_file = r"input\WF_-_Prompt_化样例_-_250927-170931.opml"  
    output_dir = "output"  # 输出目录路径
    # ======================================
    
    # 检查输入文件是否存在
    if not Path(opml_file).exists():
        print(f"错误: 文件不存在 - {opml_file}")
    
    # 执行转换
    convert_opml_to_markdown(opml_file, output_dir)
