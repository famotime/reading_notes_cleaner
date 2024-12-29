"""将剪贴板的原始笔记文本（从多看阅读、当当云阅读等app中导出）规范为markdown格式，再贴回到剪贴板"""
import pyperclip
import time
import re

def process_line(line: str, last_line: str) -> tuple[str, str]:
    """处理单行文本，返回处理后的行文本和最后一行记录"""
    # 跳过重复内容
    if line.strip('# ').replace(' ', '') == last_line.strip('# ').replace(' ', ''):
        return '', last_line
    if not line.strip():
        return '', last_line

    last_line = line

    # 标注日期格式
    line = re.sub(r'^\d\d\d\d-\d\d-\d\d', '日期'*20, line)

    # 处理各种标题格式
    if re.match(r'(第 ?.{1,3} ?[章节篇讲回部])|(前言)|(引言)|(.{,5}序言?\s)|(?:第.讲 )|附录', line):
        return '## ' + line, last_line
    elif re.match(r'\d{1,2}[\.\-]\d{1,2}[\.\-]\d{1,2}', line):
        return '#### ' + line, last_line
    elif re.match(r'(\d{1,2}[\.\-]\d{1,2}[^\.\-])|(\d{1,2}[\.\-\s]\s?[\u4e00-\u9fa5]{1,10})', line):
        return '### ' + line, last_line

    # 处理特殊标记
    if line.startswith('当当云阅读笔记') or line.startswith('多看笔记'):
        return '\n---\n' + line, last_line
    elif line.startswith('# 定义(粉红)假设(蓝色)分析(黄色)'):
        return '', last_line

    # 处理短内容
    if (not line.startswith(('#', '——'))) and len(line) < 20 and \
        not line.endswith(('。', '？', '！', '；', '。"', '，"', '…', '，', '.', '?', ';', '"', '：', '"', '”')):
        return "\n**" + line.strip() + "**", last_line

    # 处理日期行
    if line.startswith("日期"*20):
        return "\n", last_line

    return line, last_line

def convert_to_markdown(text: str) -> tuple[str, int]:
    """将文本转换为markdown格式"""
    count = 1  # 从1开始计数（考虑到首行标题）
    text = '# ' + text  # 首行作为标题

    lines = text.split('\r\n')
    new_lines = []
    last_line = ''

    for line in lines:
        processed_line, last_line = process_line(line, last_line)
        if processed_line:
            new_lines.append(processed_line)
            if processed_line.startswith(('#', '**')):
                count += 1

    return '\n'.join(new_lines), count


if __name__ == '__main__':
    text = ''
    while True:
        clipboard_text = pyperclip.paste()
        if text != clipboard_text:
            text = clipboard_text
            converted_text, count = convert_to_markdown(text)
            pyperclip.copy(converted_text)
            print(f'添加markdown标记{count}次。')
            print('-' * 50)
            break
        time.sleep(2)
