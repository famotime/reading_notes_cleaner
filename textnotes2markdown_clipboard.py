"""将剪贴板的原始笔记文本（从多看阅读、当当云阅读等app中导出）规范为markdown格式，再贴回到剪贴板"""
import pyperclip
import time
import re


text = ''
i = 1
while i > 0:
    # 获取剪贴板文本，查看是否有变化
    if text != pyperclip.paste():
        text = pyperclip.paste()
        # print(repr(text))
        count = 0

        # 按笔记段落层次生成MD章节'''
        text = '# ' + text       # 首行作为标题
        count += 1
        lines = text.split('\r\n')

        # 处理后续行
        last_line = ''
        new_lines = []
        for line in lines:
            if line.strip('# ').replace(' ', '') != last_line.strip('# ').replace(' ', ''):   # 删除前后相邻重复句子（如章节名称等）
                if line.strip():
                    last_line = line

                # 标注以日期格式开头的行
                line = re.sub(r'^\d\d\d\d-\d\d-\d\d', '日期'*20, line)

                # 以相关关键词开头行，添加markdown标记(章节标题)
                if re.match(r'(第 ?.{1,3} ?[章节篇讲回])|(前言)|(引言)|(.{,5}序言?\s)|(?:第.讲 )|附录', line):
                    line = '## ' + line
                    count += 1
                elif re.match(r'\d{1,2}[\.\-]\d{1,2}[\.\-]\d{1,2}', line):  # 形如：1.1.1，1-1-1；
                    line = '#### ' + line
                    count += 1
                elif re.match(r'(\d{1,2}[\.\-]\d{1,2}[^\.\-])|(\d{1,2}[\.\-\s]\s?[\u4e00-\u9fa5]{1,10})', line):    # 形如：1.1，1-1；1. ，1- ，1 XXX；
                    line = '### ' + line
                    count += 1
                # 文末标记
                elif line.startswith('当当云阅读笔记') or line.startswith('多看笔记'):
                    line = '\n---\n' + line
                elif line.startswith('# 定义(粉红)假设(蓝色)分析(黄色)'):
                    line = ''
                # 短内容作为小标题加粗显示
                elif line and (not line.startswith(('#', '——'))) and len(line) < 20 and not line.endswith(('。', '？', '！', '；', '。”', '，”', '…', '，', '.', '?', ';', '"', '：', '”')):
                    line = "\n**" + line.strip() + "**"
                    count += 1

                if line.strip('* \n'):
                    # 替换日期行为空行
                    if line.startswith("日期"*20):
                        line = "\n\n"

                    new_lines.append(line)
        print(f'添加markdown标记{count}次。')

        text = '\n'.join(new_lines)

        # 整理后文本拷贝到系统剪贴板
        pyperclip.copy(text)
        print('-' * 50)
        # print('\n' + text)
        # print('-' * 50)
        i -= 1

    time.sleep(2)   # 每隔2秒检测一次剪贴板
