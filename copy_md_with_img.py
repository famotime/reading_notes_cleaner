# 将md文件及内容中包含的图片文件拷贝到指定目录
md_path = pathlib.Path(r"C:\QMDownload\Python Programming\Python_Work\Web Spider\豆瓣\理想的生活，永远在别处——2022年4月读书小记.md")

dest_folder = md_path.parent / "export"
dest_folder.mkdir(exist_ok=True)

with open(md_path, encoding='utf-8') as f:
    content = f.read()
img_list = re.findall(r'!\[.*?\]\((.*?)\)', content)

(dest_folder / md_path.name).write_text(content)
for img in img_list:
    data  = (md_path.parent / img).read_bytes()
    img_folder = dest_folder / img
    img_folder.parent.mkdir(exist_ok=True)
    img_folder.write_bytes(data) 