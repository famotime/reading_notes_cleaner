"""
按如下示例，将markdown文件中的行，转换为二级标题：

《不要错过AI时代的巨大红利：竞争力养成指南【先导片】》 -> ## 不要错过AI时代的巨大红利：竞争力养成指南【先导片】
**《关于记忆与注意力的探讨》** -> ## 关于记忆与注意力的探讨

"""

from pathlib import Path
import re

file_path = Path('【汤质看本质】高手的黑箱：AI时代学习 思考与创作_modified.md')
modified_file_path = Path('【汤质看本质】高手的黑箱：AI时代学习 思考与创作_modified_title.md')

content = file_path.read_text(encoding='utf-8')

# 使用正则表达式仅匹配以《开头并以》结尾的行
updated_content = re.sub(r'^\*?\*?《(.*?)》$', r'## \1', content, flags=re.MULTILINE)

# 将更新后的内容写回文件
modified_file_path.write_text(updated_content, encoding='utf-8')

