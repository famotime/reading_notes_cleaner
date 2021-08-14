'''
当当云阅读App导出笔记整理成Markdown文档
'''
import re
import os
import shutil


def complete_notes(draftnotes, fullnotes, cleannotes):
    '''补齐笔记不完整行'''
    with open(draftnotes, encoding='utf-8-sig') as f1:
        with open(cleannotes, 'w', encoding='utf-8') as f2:
            count = 0
            for line in f1:
                # 查找不完整行替换为完整笔记
                if line.endswith('...\n'):
                    # fullnotes文件包含完整笔记，若是"uft-8-sig"编码文本文件，则首字符“\ufeff”会导致匹配失败
                    with open(fullnotes, 'r', encoding='utf-8-sig') as f3:
                        for complete_line in f3:
                            # 去除空格差异，比较前100个字符
                            if line.replace(' ', '')[:100] == complete_line.replace(' ', '')[:100]:
                                # print(f'{line}替换为\n{complete_line}\n')
                                count += 1
                                line = complete_line
                                break

                f2.write(line)
            print(f'共补齐{count}处笔记。')
    return count


def create_tmpnotes(cleannotes):
    tmpnotes = os.path.splitext(cleannotes)[0] + '_tmp.md'
    shutil.copy2(cleannotes, tmpnotes)
    return tmpnotes


def remove_timemark(cleannotes):
    '''常规清理：删除时间标记'''
    with open(tmpnotes, encoding='utf-8-sig') as f1:
        with open(cleannotes, 'w', encoding='utf-8') as f2:
            count = 0
            for line in f1:
                # 去除笔记记录时间，替换为空行
                if re.match(r'\d\d\d\d-\d\d-\d\d', line):
                    line = '\n'
                    count += 1
                # 删除空行
                if not line.strip():
                    line = ''
                line = line.replace('· ', '\n· ')
                f2.write(line)
            print(f'删除时间标记{count}次。')

    return count


def add_markdown_tag(cleannotes):
    '''常规清理：按笔记段落层次生成MD章节'''
    with open(tmpnotes, encoding='utf-8-sig') as f1:
        with open(cleannotes, 'w', encoding='utf-8') as f2:
            count = 0
            # 首行作为标题
            first_line = f1.readline()
            f2.write('# ' + first_line)
            count += 1
            last_line = ''
            for line in f1:
                if line.strip() and re.sub(r'[# \t\u3000]', '', line) != re.sub(r'[# \t\u3000]', '', last_line):   # 删除前后相邻重复句子（如章节名称等）
                # if line.strip('# ').replace(' ', '') != last_line.strip('# ').replace(' ', ''):   # 删除前后相邻重复句子（如章节名称等）
                    if line.strip():
                        last_line = line

                    # 以相关关键词开头行，添加markdown标记(章节标题)
                    if re.match(r'(第.{1,2}[章讲])|(前言\n)|(.{,5}序言?\s)|(?:第.讲 )|附录', line):
                        line = '## ' + line
                        count += 1
                    elif re.match(r'\d{1,2}[\.\-]\d{1,2}[\.\-]\d{1,2}', line):  # 形如：1.1.1，1-1-1；
                        line = '#### ' + line
                        count += 1
                    elif re.match(r'\d{1,2}[\.\-]\d{1,2}[^\.\-]|(\d{1,2}[\.\-])', line):    # 形如：1.1，1-1；1. ，1- ；
                        line = '### ' + line
                        count += 1
                    # 末尾无标点短句作为小标题加粗显示
                    elif len(line) < 15 and not line.startswith('#') and not re.match(r'[。？！，、；：“”‘（）《》〈〉【】『』「」﹃﹄〔〕…—～﹏￥]', line[::-1]):
                        line = "**" + line.strip() + "**\n"
                        count += 1

                    # 列表项增加换行，匹配“1）...12）...；a）...b）...”或“（2）...”或“1. ”模式
                    line = re.sub('(?P<number>（?[1-9a-j]{1,2}[）．.])', lambda x: '\n' + x.group('number'), line)

                    # 文末标记
                    if line.startswith('当当云阅读笔记'):
                        line = '\n---\n' + line

                    # 针对为知笔记导出的Markdown文件，纠正图片链接
                    # line = line.replace('index_files/', title + '_files/')
                    f2.write(line)
            print(f'添加markdown标记{count}次。')

    return count


def add_code_mark(cleannotes):
    '''增加python代码块标记'''
    with open(tmpnotes, encoding='utf-8-sig') as f1:
        with open(cleannotes, 'w+', encoding='utf-8') as f2:
            count = 0
            code_flag = False
            for line in f1:
                # 查询当前行是否包含中文字符
                line_remove_string = re.sub(r"'.*?'|\".*?\"", '', line)
                chinese_character = re.search('[\u4e00-\u9fa5]', line_remove_string)  # \u4e00-\u9fa5为中文字符utf8编码
                # 查询IPython行标记
                InOut = re.match(r'(In \[\d+\]: )|(Out\[\d+\]: )', line)
                if not code_flag:
                    # 包含'>>>'、全句无中文、以#开头、包含IPython标记的非空行视为代码行
                    if line.strip() and (line.startswith('>>>') or not chinese_character or line.startswith('# ') or InOut):
                        # 增加代码块起始标记```python
                        line = '\n```python\n' + line
                        code_flag = True
                        count += 1

                if code_flag:
                    # 以数字开头的章节前增加代码块结束标记```
                    if re.match(r'(\d+\.)', line.strip()):
                        line = '\n```\n' + line
                        code_flag = False
                        count += 1
                    # 不包含'#'及'"""'的行中，在首个中文字符前增加代码块结束标记```
                    elif not re.search('#|(""")', line) and chinese_character:
                        line = re.sub(chinese_character.group(), '\n```\n' + chinese_character.group(), line, count=1)
                        code_flag = False
                        count += 1

                f2.write(line)
            print(f'代码块标记增加{count}次。')

    return count


def split_code_line(cleannotes):
    '''python代码分段换行'''
    with open(tmpnotes, encoding='utf-8-sig') as f1:
        with open(cleannotes, 'w+', encoding='utf-8') as f2:
            count = 0
            code_flag = False
            for line in f1:
                if line.startswith('```python'):
                    code_flag = True
                elif line.endswith('```'):
                    code_flag = False
                if code_flag:
                    # 将中文全角空格\u3000替换为英文空格
                    line = line.replace('\u3000', ' ')
                    # 4个以上连续空格前增加换行
                    line = re.sub(r'\s{4,}', lambda x: '\n'+x.group(), line)
                    count += 1

                    # 相应关键词（包括缩进空格）前增加换行
                    pre_keywords = ['from ', '(?<! )import ', 'for ', 'mpl\.', 'plt\.', 'assert ', 'break', 'continue', 'del ', 'else:', 'except ', 'finally:', 'global ', '(el)?if ', 'nonlocal ', 'pass', 'raise ', 'try:', 'while ', 'with ', r'p?print\(', 'def ', 'Traceback ', 'return ', 'yield ', 'class ', '# ', 'np\.', r'\.\.\.', ' """.*?"""', 'conda', 'pip', 'sns', '\w*? = ']
                    for keyword in pre_keywords:
                        # new_word = '\n'+keyword.replace('\.', '.') if keyword.endswith('.') else '\n'+keyword
                        if re.search(keyword, line):
                            count += 1
                            # 关键词前只有空格则不处理，若有其他字符则在空格前增加换行
                            line = re.sub(rf'\s*?{keyword}', lambda x: x.group() if x.group().startswith('\n') else '\n' + x.group(), line)

                    # 非行首的>>>增加换行
                    if '>>>' in line:
                        line = re.sub(r'([^\n\t ]*)>>>', lambda x: x.group(1)+'\n>>>', line)
                        count += 1

                    # IPython行标记In[]及Out[]、前导符号...:前增加换行
                    line = re.sub(r'(In \[\d+\]:\n?)|(Out\[\d+\]:\n?)|( *\.+:\n?)', lambda x: '\n'+x.group().strip(), line)
                    count += 1

                    # 相应字符串后增加换行
                    post_keywords = ['as np', 'break', 'continue']
                    for keyword in post_keywords:
                        if keyword in line and (not line.endswith(keyword)):
                            line = re.sub(keyword, keyword + '\n', line)
                            count += 1
                            # print(line)

                    # 去除相关符号后的换行
                    line = re.sub(r'([=(>])\n', lambda x: x.group(1), line)

                f2.write(line)
            print(f'代码格式整理{count}次。')

            # 消除连续空行（3个以上）
            f2.seek(0)
            content = re.sub(r'\n{3,}', '\n', f2.read())
    with open(cleannotes, 'w', encoding='utf-8') as f2:
        f2.write(content)

    return count


def remove_linenum(cleannotes):
    '''删除代码块中的行号，如56. ，12 '''
    with open(tmpnotes, encoding='utf-8-sig') as f1:
        with open(cleannotes, 'w+', encoding='utf-8') as f2:
            count = 0
            code_flag = False
            for line in f1:
                if line.startswith('```python'):
                    code_flag = True
                elif line.endswith('```'):
                    code_flag = False
                if code_flag:
                    # oldline = line
                    line, num = re.subn(r'(?<!\=|\+|\-|\*|\/)\d{1,3}\.? *$', '', line)
                    if num:
                        count += num
                        # print(oldline)
                        # print(line)
                f2.write(line)
            print(f'共删除{count}处代码行数标记。')
    return count


if __name__ == "__main__":
    draftnotes = 'draftnotes.txt'   # 原始笔记内容粘贴至此文件
    fullnotes = 'fullnotes.txt'     # 完整的笔记段落内容粘贴至此文件

    # 取文件首行内容为Markdown文件名，注意文件编码格式
    with open(draftnotes, encoding='utf-8-sig') as f:
        title = f.readline().strip()
    cleannotes = title + '.md'

    count = 0
    count += complete_notes(draftnotes, fullnotes, cleannotes)  # 补全缺失笔记内容

    # 处理函数列表：remove_timemark, add_code_mark, split_code_line, remove_linenum, add_markdown_tag
    # 先使用add_code_mark再使用split_code_line、remove_linenum
    # 最后再使用add_markdown_tag添加markdown标记

    fn_list = [remove_timemark, add_markdown_tag]   # 针对普通笔记清洗策略
    # fn_list = [remove_timemark, add_code_mark, split_code_line, add_code_mark, add_markdown_tag]   # 针对编程笔记清洗策略
    # fn_list = [remove_timemark, add_code_mark, split_code_line, remove_linenum, add_markdown_tag]   # 针对编程笔记清洗策略(清除代码行号)
    for fn in fn_list:
        tmpnotes = create_tmpnotes(cleannotes)
        count += fn(cleannotes)
        os.remove(tmpnotes)

    print(f"共完成{count}次操作，已输出笔记文件《{title + '.md'}》。")
