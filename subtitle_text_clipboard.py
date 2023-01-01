import re
import pyperclip


text = pyperclip.paste()
new_text = text.replace('\n\n', '\n').replace('\n', '，')
pyperclip.copy(new_text)
print(new_text)
