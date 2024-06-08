# FileMerge

## 概述
FileMerge是一个Python工具，用于将多个文本文件内容合并到一个新的TXT文件中。它支持在Windows环境中自动从拖放到窗体中的文件中读取内容，并将这些内容以GPT-4原生能够识别的格式拼接起来。

## 使用说明
1. 安装Python 3.11。
2. 下载并运行FileMerge.py。
3. 将要合并的文件拖放到窗体中。
4. 文件会被自动读取并合并到指定的TXT文件中。

## 导入库
```python
import tkinter as tk
from tkinter import filedialog
import os
import itertools
