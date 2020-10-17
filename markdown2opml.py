'''
Markdown文档批量转为workflowy、幕布等导图软件支持的opml文件（带层次结构）
Markdown文件须以标题行开头（# XX）
所有标题行作为清单项，非标题行作为备注
'''
import os


def md2opml(md_file, opml_file):
    # 注意文件编码格式
    with open(md_file, 'r', encoding='utf-8-sig') as f1:
        with open(opml_file, 'w', encoding='utf-8') as f2:
            # opml文件头
            header = "<?xml version='1.0'?>\n<opml version='2.0'>\n  <head>\n    <ownerEmail>\n      quincy.zou@gmail.com\n    </ownerEmail>\n  </head>\n  <body>\n"
            f2.write(header)

            # 首行缩进4格，spaces列表（记录缩进信息）等数据初始化
            first_line = f1.readline().strip('# ').replace('\n', '&#10;').replace('"', '&quot;').replace('<', '&amp;lt;').replace('>', '&amp;gt;')
            last_line = first_line
            space = last_space = 4
            spaces = []
            notes = ''
            codesign_count = 0

            # 处理后续行
            for line in f1:
                # 替换markdown文档中的特殊字符
                line = line.replace('&', '&amp;').replace('\n', '&#10;').replace('"', '&quot;').replace('<', '&amp;lt;').replace('>', '&amp;gt;')

                # 判断是否为代码块内容（```符号未闭合），是则直接设置为备注，代码块内#开头的注释行不作为标题
                if line.startswith('```'):
                    codesign_count += 1
                if codesign_count % 2 != 0:
                    space = None
                    notes += line
                # 非代码块内容，#开头行作为标题行处理，配置缩进空格
                else:
                    if line.startswith('# '):
                        space = 4
                    elif line.startswith('## '):
                        space = 6
                    elif line.startswith('### '):
                        space = 8
                    elif line.startswith('#### '):
                        space = 10
                    elif line.startswith('##### '):
                        space = 12
                    else:
                        space = None
                        # 非标题行累积加入备注
                        notes += line

                # 标题行作为清单项，非标题行作为备注
                if space:
                    last_line = last_line.strip('# ')
                    # 此前存有备注信息则写入note字段，否则只将上次存储信息写入outline字段
                    if notes:
                        # 删除notes开头空行
                        if notes.startswith('&#10;'): notes = notes.lstrip('&#10;')
                        content = ' ' * last_space + f'<outline text="{last_line}" _note="{notes}"'
                    else:
                        content = ' ' * last_space + f'<outline text="{last_line}"'
                    # 下级标题，则写入此前存储文字，开放outline标签
                    if space > last_space:
                        f2.write(content + '>\n')
                        spaces.append(last_space)
                    # 同级标题，则把前次同级outline标签补齐关闭
                    elif space == last_space:
                        f2.write(content + ' />\n')
                    # 上级标题，则把此前outline标签补齐关闭（通过space列表pop操作取出历史记录）
                    elif space < last_space:
                        f2.write(content + ' />\n')
                        num = int((last_space-space)/2)
                        for i in range(num):
                            f2.write(' ' * spaces.pop() + '</outline>\n')
                    # 上一行内容写入文件后，重新初始化数据
                    last_line = line
                    notes = ''
                    last_space = space
            # 处理最后遗留段落
            last_line = last_line.strip('# ')
            if notes:
                if notes.startswith('&#10;'): notes = notes.lstrip('&#10;')
                content = ' ' * last_space + f'<outline text="{last_line}" _note="{notes}"'
            else:
                content = ' ' * last_space + f'<outline text="{last_line}"'
            f2.write(content + ' />\n')
            while spaces:
                f2.write(' ' * spaces.pop() + '</outline>\n')

            # opml文件尾
            tail = "  </body>\n</opml>"
            f2.write(tail)


if __name__ == "__main__":
    folder = r"c:\QMDownload\Python Programming\Python_Work\data_analysis\可视化\Python数据可视化之matplotlib精进"

    os.chdir(folder)
    md_files = [md_file for md_file in os.listdir() if md_file.endswith('.md')]
    for md_file in md_files:
        opml_file = os.path.splitext(md_file)[0] + '.opml'
        md2opml(md_file, opml_file)
