# 利用Python进行数据分析(原书第2版)
（美）韦斯·麦金尼（Wes McKinney）
### 3.2 函数
#### 3.2.1 命名空间、作用域和本地函数
在Python中另一种更贴切地描述变量作用域的名称是命名空间。在函数内部，任意变量都是默认分配到本地命名空间的。本地命名空间是在函数被调用时生成的，并立即由函数的参数填充。当函数执行结束后，本地命名空间就会被销毁（除了一些本章范围外的特殊情况）。
通常全局变量用来存储系统中的某些状态。如果你发现你大量使用了全局变量，可能表明你需要面向对象编程（使用类）。
#### 3.2.3 函数是对象

```python

In [171]: states = [' Alabama ', 'Georgia!', 'Georgia', 'georgia', 'FlOrIda',

.....: 'south carolina##', 'West virginia?']

```
需要做：去除空格，移除标点符号，调整适当的大小写。一种方式是使用内建的字符串方法，结合标准库中的正则表达式模块re：
另一种会让你觉得有用的实现就是将特定的列表操作应用到某个字符串的集合上： 

```python

def remove_punctuation(value):
     return re.sub('[!#?]', '', value) clean_ops = [str.strip, remove_punctuation, str.title]
 def clean_strings(strings, ops):
     result = []
     for value in strings:
         for function in ops:
             value = function(value)
         result.append(value)
     return result

```
像这种更为函数化的模式可以使你在更高层次上方便地修改字符串变换方法。clean_strings函数现在也具有更强的复用性和通用性。
你可以将函数作为一个参数传给其他的函数，比如内建的map函数，可以将一个函数应用到一个序列上： 
In [176]: for x in map(remove_punctuation, states):

.....: print(x) Alabama Georgia Georgia