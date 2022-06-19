"""markdown文件标题层级修正"""

import pyperclip
import time


content = ''
while True:
    if pyperclip.paste() != content and pyperclip.paste().startswith('#'):
        content = pyperclip.paste()
        content = content.replace('#', '##').replace('-', '').strip()
        pyperclip.copy(content)
        print(content)
    time.sleep(2)
