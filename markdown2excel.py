"""
将markdown文件中的表格导出为excel文件
"""
from pathlib import Path
import pandas as pd
import re

def extract_tables(markdown_text):
    """提取markdown文本中的所有表格"""
    # 匹配markdown表格的正则表达式
    table_pattern = r'\|.*\|[\r\n]\|[-: |]+\|[\r\n](?:\|.*\|[\r\n])*'
    tables = re.findall(table_pattern, markdown_text)
    return tables

def parse_table(table_text):
    """解析单个markdown表格文本为DataFrame，并保留超链接"""
    # 按行分割
    lines = table_text.strip().split('\n')

    # 提取表头
    headers = [col.strip() for col in lines[0].split('|')[1:-1]]

    # 跳过分隔行
    data = []
    for line in lines[2:]:  # 跳过表头和分隔行
        if line.strip():
            # 处理每个单元格
            cells = []
            row_cells = line.split('|')[1:-1]
            for cell in row_cells:
                cell = cell.strip()
                # 匹配markdown链接格式 [text](url)
                link_match = re.match(r'\[(.*?)\]\((.*?)\)', cell)
                if link_match:
                    # 使用Excel的HYPERLINK函数格式
                    text, url = link_match.groups()
                    cell = f'=HYPERLINK("{url}","{text}")'
                cells.append(cell)
            data.append(cells)

    return pd.DataFrame(data, columns=headers)

def markdown_to_excel(md_file_path, excel_file_path, merge_tables=True):
    """将markdown文件中的表格转换为excel文件

    Args:
        md_file_path: Markdown文件路径
        excel_file_path: Excel文件保存路径
        merge_tables: 是否合并所有表格
            - True: 所有表格合并为一个sheet
            - False: 每个表格保存为单独的sheet
    """
    # 读取markdown文件
    md_path = Path(md_file_path)
    markdown_text = md_path.read_text(encoding='utf-8')

    # 提取所有表格
    tables = extract_tables(markdown_text)

    if not tables:
        print("未找到任何表格！")
        return

    # 解析所有表格
    dfs = []
    for table in tables:
        df = parse_table(table)
        dfs.append(df)

    excel_path = Path(excel_file_path)

    if merge_tables:
        # 合并所有表格
        final_df = pd.concat(dfs, ignore_index=True)
        final_df.to_excel(excel_path, index=False)
        print(f"已将合并表格保存至: {excel_path}")
    else:
        # 创建Excel写入器
        with pd.ExcelWriter(excel_path) as writer:
            # 将每个表格写入不同的sheet
            for i, df in enumerate(dfs, 1):
                sheet_name = f'Table_{i}'
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"已将{len(dfs)}个表格分别保存至: {excel_path}")

if __name__ == '__main__':
    # 使用示例
    markdown_file = Path(r"D:\GitHub\awesome-mcp-servers-main\MCP datasheet.md")
    excel_file = markdown_file.with_suffix(".xlsx")

    # 合并为一个表格
    markdown_to_excel(markdown_file, excel_file, merge_tables=True)

    # 或者导出为多个sheet
    # excel_file_multi = markdown_file.with_suffix("_multi.xlsx")
    # markdown_to_excel(markdown_file, excel_file_multi, merge_tables=False)
