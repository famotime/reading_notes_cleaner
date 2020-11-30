'''
每隔2秒自动整理剪贴的python代码，并保存到系统剪贴板
'''
import re
import time
import pyperclip


def add_newline(codes):
    """按规则分段换行"""
    # 相应字符串前增加换行
    patterns = ['import', '# ', 'mpl\.', 'plt\.', 'x =', 'y =', ]
    for pattern in patterns:
        new_word = '\n'+pattern.replace('\.', '.') if pattern.endswith('.') else '\n'+pattern
        tidy_code = re.sub(pattern, new_word, codes)
    # 相应字符串后增加换行
    tidy_code = re.sub('as np', 'as np'+'\n', tidy_code)
    # 查找相关变量名，在变量名前增加换行
    x_args = re.findall(r'x = (.*)', tidy_code)
    y_args = re.findall(r'y = (.*)', tidy_code)
    for arg in (x_args + y_args):
        tidy_code = re.sub(arg+' =', '\n'+arg+' =', tidy_code)
    # print(args)

    # 增加python代码块标注
    tidy_code = '```python' + tidy_code + '\n```\n'

    return tidy_code


def linenum2newline(codes):
    """将的行号信息(形如1: , 2: )替换为换行"""
    tidy_code = re.sub(r'\d{1,2}:\s', '\n', codes)
    return tidy_code


def remove_linenum(codes):
    """删除以(数字)或(空格+数字)方式开头的行号，如1， 1，1:"""
    tidy_code = re.sub(r'\n\s*\d+:? ?', '', codes)
    return tidy_code


def remove_presign(codes):
    """去除交互式编程环境的前导符号>>>"""
    tidy_code = re.sub(r'>>> ?', '\n', codes)
    tidy_code = re.sub(r'\n\n', '\n', tidy_code)
    return tidy_code


def python3_print(codes):
    """转换Python2的Print语句为Python3的Print函数"""
    tidy_code = re.sub(r'print (.*)', lambda x: f'print({x.group(1)})', codes)
    return tidy_code


if __name__ == "__main__":
    # draft_code = input('请输入错乱代码：')
    # tidy_code = draft_code

    tidy_code = ''

    while True:
        # 获取剪贴板文本
        if tidy_code != pyperclip.paste():
            tidy_code = pyperclip.paste()

            # 处理剪贴板代码
            # functions = [python3_print, add_newline, linenum2newline, remove_linenum, remove_presign]
            functions = [remove_presign]
            for function in functions:
                tidy_code = function(tidy_code)

            # 整理后文本拷贝到系统剪贴板
            pyperclip.copy(tidy_code)
            print('-' * 50)
            print('\n' + tidy_code)
            print('-' * 50)

        time.sleep(2)
