'''
Markdown文档批量转为workflowy、幕布等导图软件支持的opml文件（带层次结构）
Markdown文件应以标题行开头（# XX）
所有标题行作为清单项，非标题行作为备注
'''
import pathlib


def md2opml(md_content):
    """将markdown文本转换为opml文本"""
    md_content_lines = [line + '\n' for line in md_content.split('\n')]
    opml_content = ''
    # opml文件头
    header = "<?xml version='1.0'?>\n<opml version='2.0'>\n  <head>\n    <ownerEmail>\n      quincy.zou@gmail.com\n    </ownerEmail>\n  </head>\n  <body>\n"
    opml_content += header

    # 数据初始化: levels列表（记录层级信息）等
    first_line = True
    levels = []
    notes = ''
    codesign_count = 0

    for line in md_content_lines:
        # 替换markdown文档中的特殊字符
        line = line.replace('&', '&amp;').replace('\n', '&#10;').replace('"', '&quot;').replace('<', '&amp;lt;').replace('>', '&amp;gt;')
        # 判断是否为代码块内容（```符号未闭合），是则直接设置为备注，代码块内#开头的注释行不作为标题
        if line.startswith('```'):
            codesign_count += 1
        if codesign_count % 2 != 0:
            level = 0
            notes += line
        # 非代码块内容，#开头行作为标题行处理，配置缩进空格
        else:
            if line.startswith('# '):
                level = 1
            elif line.startswith('## '):
                level = 2
            elif line.startswith('### '):
                level = 3
            elif line.startswith('#### '):
                level = 4
            elif line.startswith('##### '):
                level = 5
            else:
                level = 0
                # 非标题行累积加入备注
                notes += line

        # 首行初始化
        if first_line:
            last_line = line
            last_level = level
            levels.append(level)
            first_line = False
            continue

        # 标题行作为清单项，非标题行作为备注
        if level:
            last_line = last_line.strip('# ')
            # 此前存有备注信息则写入note字段，否则只将上次存储信息写入outline字段
            if notes:
                # 删除notes开头空行
                if notes.startswith('&#10;'): notes = notes.lstrip('&#10; ')
                content = '  ' * last_level + f'<outline text="{last_line}" _note="{notes}"'
            else:
                content = '  ' * last_level + f'<outline text="{last_line}"'
            # 下级标题，则写入此前存储文字，开放outline标签
            if level > last_level:
                opml_content += content + '>\n'
                level = last_level + 1  # 修正标题层级的跳级
                levels.append(level)
            # 同级标题，则把前次同级outline标签补齐关闭
            elif level == last_level:
                opml_content += content + ' />\n'
            # 上级标题，则把此前outline标签补齐关闭（通过level列表pop操作取出历史记录）
            elif level < last_level:
                opml_content += content + ' />\n'
                if levels:
                    for i in range(levels.pop()-level, 0, -1):
                        opml_content += '  ' * i + '</outline>\n'
            # 上一行内容写入文件后，重新初始化数据
            last_line = line
            notes = ''
            last_level = level
    # 处理最后遗留段落
    last_line = last_line.strip('# ')
    if notes:
        if notes.startswith('&#10;'): notes = notes.lstrip('&#10;')
        content = '  ' * last_level + f'<outline text="{last_line}" _note="{notes}"'
    else:
        content = '  ' * last_level + f'<outline text="{last_line}"'
    opml_content += content + ' />\n'
    while levels:
        opml_content += '  ' * levels.pop() + '</outline>\n'

    # opml文件尾
    tail = "  </body>\n</opml>"
    opml_content += tail

    opml_content = opml_content.replace('_note="```python&#10;', '_note="')

    return opml_content


def md_file2opml_file(md_file):
    """将markdown文件转换为opml文件"""
    opml_file = md_file.with_suffix('.opml')
    # 注意文件编码格式
    with open(md_file, 'r', encoding='utf-8-sig') as f1:
        with open(opml_file, 'w', encoding='utf-8') as f2:
            opml_content = md2opml(f1.read())
            f2.write(opml_content)


if __name__ == "__main__":
    folder = pathlib.Path(r"C:\Users\Administrator\Desktop")

    for count, md_file in enumerate(folder.glob('*.md'), 1):
        md_file2opml_file(md_file)
    print(f"已转换{count}个markdown文件为opml文件，请到'{folder}'目录下查看。")
