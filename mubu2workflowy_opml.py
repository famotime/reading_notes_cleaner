"""把幕布软件导出的opml文件转换成可在workflowy直接粘贴的格式"""
import os
import re


def special_character_replace(matched_obj):
    """转换匹配文本中的特殊字符"""
    new_text = '"' + matched_obj.group(1).replace('&', '&amp;').replace('\n', '&#10;').replace('"', '&quot;').replace('<', '&amp;lt;').replace('>', '&amp;gt;') + '"'
    return new_text


if __name__ == "__main__":
    mubu_opml = r'.\python知识点.opml'

    workflowy_opml = os.path.basename(mubu_opml).split('.')[0] + '_workflowy.opml'
    with open(mubu_opml, encoding='utf-8') as f1:
        with open(workflowy_opml, 'w', encoding='utf-8') as f2:
            mubu_text = f1.read()
            # 查找被""包括的文本内容，并替换特殊字符
            workflowy_text = re.sub(r'"(.*?)"', special_character_replace, mubu_text, flags=re.DOTALL)
            f2.write(workflowy_text)
