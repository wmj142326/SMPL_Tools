# -*- coding = utf-8 -*-
# @time:2021/3/13 16:41
# Author:wmj
# @File:50_n50.py
# @Software:PyCharm
# @Function:

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

x1 = "50"
t1 = "50000"

count = len(re.findall(x1, content))  # re.findall()返回的是一个列表
print("re.findall()的返回值: ", re.findall(x1, content))
print("共有{}个{}".format(count, x1))

# 文件替换
xt1 = content.replace(x1, t1)
with open("main_window.py", "w") as f2:
    f2.write(xt1)

f1.close()
f2.close()

print("finished")
