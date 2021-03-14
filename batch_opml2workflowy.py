"""将指定目录下opml文件内容批量复制到workflowy"""
import pathlib
import time
import pyautogui
import pyperclip
pyautogui.FAILSAFE = True
# pyautogui.PAUSE = 1


folder = pathlib.Path(r'C:\QMDownload\Python Programming\Python_Work\GitHub\seaborn-doc-zh-master\docs')

opml_files = sorted(folder.glob('*.opml'), key=lambda x: int(x.stem))

time.sleep(5)
for num, opml in enumerate(opml_files, 1):
    with open(opml, encoding='utf-8') as f:
        content = f.read()
    pyperclip.copy(content)
    pyautogui.hotkey('ctrl', 'v')   # 粘贴
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'up')  # 折叠
    time.sleep(1)
    pyautogui.press(['end', 'enter'])   # 在粘贴内容后新建item

pyautogui.press(['end', 'enter'])
pyperclip.copy(f'已完成{num}个文件内容粘贴，请查看。')
pyautogui.hotkey('ctrl', 'v')   # 粘贴
