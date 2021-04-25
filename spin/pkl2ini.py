# -*- coding = utf-8 -*-
# @time:2021/3/9 10:19
# Author:wmj
# @File:pkl2ini.py
# @Software:PyCharm
# @Function:pkl_to_ini转换

import joblib
import numpy as np
import os
import shutil
import configparser
import cv2


# 去除省略号，初始化
def initializtion():
    np.set_printoptions(suppress=True)  # 取消科学计数法输出
    np.set_printoptions(threshold=np.inf)  # 取消省略号
    return 0


# 建立一个存放生成ini文件的文件夹
def create_ini_dir(filename):
    if os.path.exists(filename):
        pass
    else:
        os.mkdir(filename)


# 读取.pkl文件
def pkl_read(path):
    inf = joblib.load(path)

    print(inf.keys())
    # for k, v in inf[0].items():
        # print(k, np.shape(v))
    # print(inf[0]["global_orient"][0])
    return inf

# 从pkl提取shape参数
def get_shape_pkl(inf):
    shape_zeros = np.zeros(300, )  # 创建shape参数初始化
    # print(inf[0]["beats"][0])
    shape_zeros[0:10] = (inf[0]["beats"][0])#*(5/9)
    shape_str = str(shape_zeros)  # 仅读取第一帧
    shape_str = shape_str[1:-1]  # 去除中括号
    shape_line = shape_str.split()  # 将其分割成一个字符列表
    shape_new_line = ','.join(shape_line)  # 将字符列表用','拼接成一个新字符串
    shape_new_line = shape_new_line.strip(',')  # 将新字符串尾部产生的','去掉
    return shape_new_line


# 从pkl提取pose参数
def get_pose_pkl(inf):
    pose_E = []
    pose_R = inf[0]["pose"][0]
    for pose_R_id in pose_R:
        pose_E_id = cv2.Rodrigues(pose_R_id)[0]
        pose_E.append(pose_E_id)
    pose_re = np.array(pose_E).reshape(1, -1)

    global_rot_R = inf[0]["global_orient"][0][0]
    global_rot_E = cv2.Rodrigues(global_rot_R)[0]
    global_rot_E = np.array(global_rot_E).reshape(1, -1)
    # print(global_rot_E[0])

    pose_zeros = np.zeros(72, )  # 创建pose参数初始化
    pose_zeros[0:3] = global_rot_E[0]
    pose_zeros[3:] = pose_re[0]

    pose_str = str(pose_zeros.astype(float))[1:-1]
    pose_line = pose_str.split()
    pose_new_line = ','.join(pose_line)
    pose_new_line = pose_new_line.strip(',')
    return pose_new_line


# 将从pkl提取的参数导入ini文件
def ini_write(shape, pose, rename):
    shutil.copyfile('../rest_pose.ini', '../ini_file/{}.ini'.format(rename))
    ini_path = '../rest_pose.ini'
    rest = configparser.ConfigParser()
    rest.read(ini_path, encoding='utf-8')
    sections = rest.sections()
    # 写入shape和pose参数
    rest.set(sections[0], "shape", shape)
    rest.set(sections[0], "pose", pose)

    rest.write(open('../ini_file/{}.ini'.format(rename), "r+", encoding="utf-8"))  # r+模式


if __name__ == '__main__':
    # 初始化
    initializtion()

    # 创建ini文件夹
    ini_dir = 'ini_file'
    create_ini_dir(ini_dir)

    # 写入ini文件
    pkl_folder_name = 'pkl_file'
    pkl_files = os.listdir(pkl_folder_name)  # 返回指定路径下的文件和文件夹列表
    os.chdir(pkl_folder_name)
    num = -1
    for pkl_file in pkl_files:

        # 读取pkl文件
        pkl_inf = pkl_read(pkl_file)

        # 从pkl提取参数
        shape = get_shape_pkl(pkl_inf)
        pose = get_pose_pkl(pkl_inf)

        # 将参数写入ini文件
        (rename, extension) = os.path.splitext(pkl_file)
        ini_write(shape, pose, rename)
        num = num+1
        print("\r" + "完成进度: %d / %d \n\n" % (num, len(pkl_files)-1), end='')
    print("\npkl --> ini has finished")
