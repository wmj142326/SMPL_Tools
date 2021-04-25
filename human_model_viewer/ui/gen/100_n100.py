# -*- coding = utf-8 -*-
# @time:2021/3/13 0:02
# Author:wmj
# @File:100_n100.py
# @Software:PyCharm
# @Function:

# 文件查找
import re   # 引用re模块

f1 = open("main_window.py", "r")
content = f1.read()

x1 = "100"
t1 = "100000"

x2 = '"value", 50'
t2 = '"value", 50000'

count = len(re.findall(x2, content))  # re.findall()返回的是一个列表
print("re.findall()的返回值: ", re.findall(x2, content))
print("共有{}个{}".format(count, x2))

# 文件替换
xt1 = content.replace(x1, t1)
xt2 = content.replace(x2, t2)
with open("main_window.py", "w") as f2:
    f2.write(xt1)
with open("main_window.py", "w") as f3:
    f3.write(xt2)

f1.close()
f2.close()
f3.close()
print("finished")