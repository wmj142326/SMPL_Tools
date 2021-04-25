# -*- coding = utf-8 -*-
# @time:2021/3/9 10:19
# Author:wmj
# @File:ini2pkl.py
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


# 建立一个存放生成pkl文件的文件夹
def create_re_pkl_file(filename):
    if os.path.exists(filename):
        pass
    else:
        os.mkdir(filename)


# 从ini中提取shape参数
def ini_to_pkl(file):
    rest = configparser.ConfigParser()
    rest.read(file, encoding='utf-8')
    sections = rest.sections()

    shape_ini = rest.get(sections[0], 'shape')
    shape_ini_list = shape_ini.split(",")
    shape_ini = np.array(shape_ini_list[0:10])
    shape = np.random.rand(10)
    for i in range(10):
        shape[i] = shape_ini[i]
    # print(shape)

    pose_ini = rest.get(sections[0], 'pose')
    pose_ini_list = pose_ini.split(",")
    pose_ini = np.array(pose_ini_list[:])
    pose = np.random.rand(72)
    for i in range(72):
        pose[i] = pose_ini[i]
    # print(pose)

    step = 3
    pose_E = [pose[i:i + step] for i in range(0, len(pose), step)]
    pose_R = []
    for pose_E_id in pose_E:
        pose_R_id = cv2.Rodrigues(pose_E_id)[0]
        pose_R.append(pose_R_id)
    # print(pose_R)



    (filename, extension) = os.path.splitext(file)
    filename = filename.split("/")[-1]
    pkl_file = shutil.copyfile('../pkl_file/{}.pkl'.format(filename), '../re_pkl_file/{}.pkl'.format(filename))
    inf = joblib.load(pkl_file)

    for i in range(10):
        inf[0]["beats"][0][i] = shape_ini[i]
    # print(inf[0]["beats"][0])

    for i in range(23):
        inf[0]["pose"][0][i] = pose_E[i+1]

    inf[0]["global_orient"][0] = pose_E[0]

    print(pose_E[0])

if __name__ == '__main__':
    # 初始化
    initializtion()

    # 创建ini文件夹
    pkl_dir = 're_pkl_file'
    create_re_pkl_file(pkl_dir)

    # ini_file = "re_ini_file/frame_1.ini"
    # ini_to_pkl(ini_file)

    num = -1
    path = "ini_file"
    ini_files = os.listdir(path)
    os.chdir(path)
    for ini_file in ini_files:
        ini_to_pkl(ini_file)
        num = num + 1
        print("\r" + "完成进度: %d / %d (from 0 to ...)" % (num, len(ini_files)-1), end='')
    print("\npkl2ini has finished")