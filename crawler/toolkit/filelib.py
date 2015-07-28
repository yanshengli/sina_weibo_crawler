# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def size(file_path):
    return os.path.getsize(file_path)


def remove(file_path):
    os.remove(file_path)


# 判断文件(夹)是否存在,存在返回True,否则返回False
def exists(file_path):
    return os.path.exists(file_path)


# 判断是否文件,是则返回True,否则返回False
def is_file(file_path):
    return os.path.isfile(file_path)


# 判断是否文件夹,是则返回True,否则返回False
def is_dir(dir_path):
    return os.path.isdir(dir_path)


# 创建文件夹路径,成功返回True,失败返回False
def create_dir(path):
    is_success = True
    try:
        if not exists(path):
            os.makedirs(path)
    except:
        print '创建文件夹', path, '失败'
        is_success = False
    return is_success


# 创建文件,成功返回写入器,失败返回None
def create_file(path, name=None):
    writer = None
    try:
        if name != None:  # 提供文件夹路径与文件名分开
            if path[len(path) - 1] != '/':
                path = path + '/'
            file_path = path + name
            if not exists(file_path):
                if not create_dir(path):
                    return None
        else:  # 将路径和文件名合在一起
            file_path = path
            if not exists(path):
                seg_pos = path.rfind('/')
                dir_path = path[:seg_pos]
                if not create_dir(dir_path):
                    return None
        writer = open(file_path, 'w')
    except:
        print '创建文件', filePath, '失败'
        writer = None
    return writer


# 获取路劲下有多少个文件
def count(path):
    return sum([len(files) for root, dirs, files in os.walk(path)])


# 获取指定目录下的所有文件路径,recursion指定是否递归获取
# 子目录下的文件;listdir指定是否获取目录,目录以/结尾
def get_dir_filepaths(dir_path, recursion=False, listdir=False):
    file_list = []
    cur_dir_path = dir_path
    for root, subdirs, files in os.walk(dir_path, True):
        for file_name in files:
            file_list.append(os.path.join(root, file_name))
        if (listdir):
            for subdir in subdirs:
                file_list.append(os.path.join(root, subdir + '/'))
        if (not recursion):
            break
    return file_list


# 获取指定目录下的所有文件名,listdir指定是否获取目录名
def get_dir_filenames(dir_path, listdir=False):
    filename_list = []
    for root, subdirs, files in os.walk(dir_path, True):
        for file_name in files:
            filename_list.append(file_name)
        if listdir:
            for subdir in subdirs:
                filename_list.append(subdir + '/')
    return filename_list


if __name__ == '__main__':
    # print get_dir_filenames('../wbcrawler/data', False);
    print get_dir_filenames('../blogcrawler/data')