import codecs
import json
import os
from PIL import ImageGrab
from PIL import Image
import numpy as np
import cv2
from dataload import FireState, Gun


def compare_parts(file,demo_dir,threshold):
    '''
    file:要比较的图像文件路径

    demo_dir:要与file比较的demo目录路径，以“\”结尾

    threshlod:设置汉明距离的阈值

    return:汉明距离
    '''
    min_distance = threshold # 定义一个变量 min_distance，其初始值为 threshold
    content = os.listdir(demo_dir) # 获取 demo_dir 目录下的所有文件名
    part = 'None' # 定义一个变量 part，其初始值为 'None'
    for each in content: # 遍历 content 中的每个文件名
        demopath = demo_dir + each # 计算出 demo 文件的路径
        tmp_dist = compare2pic(file,demopath,threshold-1) # 调用 compare2pic 函数比较 file 和 demo 文件的汉明距离
        if tmp_dist < min_distance: # 如果汉明距离小于 min_distance
            min_distance = tmp_dist # 更新 min_distance 的值
            part = str(each)[:-4] # 更新 part 的值
    return part # 返回 part 的值

def current_posture():
    '''
    早期的姿势识别函数，原理与武器配件一样使用汉明距离，现在已作废，目前姿势识别采用三点像素取样
    '''
    posture = 'None' # 定义一个变量 posture，其初始值为 'None'
    post_distance = 11 # 定义一个变量 post_distance，其初始值为 11
    print('姿势识别') # 打印字符串
    posture_screenshot() # 调用 posture_screenshot 函数进行截图
    posture_path = './picture/posture/' # 定义一个变量 posture_path，表示姿势图片的路径
    current_posture_path = './picture/equiment/posture.png' # 定义一个变量 current_posture_path，表示当前姿势图片的路径
    content = os.listdir(posture_path) # 获取 posture_path 目录下的所有文件名
    for each in content: # 遍历每个文件名
        demopath = posture_path + each # 计算出 demo 文件的路径
        tmp_dist = compare2pic(current_posture_path, demopath, 10) # 调用 compare2pic 函数比较当前姿势图片和 demo 文件的汉明距离
        if tmp_dist < post_distance: # 如果汉明距离小于 post_distance
            posture = str(each)[:-4] # 更新 posture 的值
            post_distance = tmp_dist # 更新 post_distance 的值
    print('当前姿势：'+posture) # 打印当前姿势
    return # 返回

def recognize_equiment():
    '''
    识别装备（枪械、瞄镜、握把、枪托、枪口）
    '''
    gun_1 = compare_parts('./picture/equiment/gun_1.png','./picture/gun/',6) # 获取第一把枪的名称
    gun_2 = compare_parts('./picture/equiment/gun_2.png','./picture/gun/',6) # 获取第二把枪的名称
    mirror_1 = compare_parts('./picture/equiment/mirror_1.png','./picture/mirrors/',6) # 获取第一个瞄准镜的名称
    mirror_2 = compare_parts('./picture/equiment/mirror_2.png', './picture/mirrors/', 6) # 获取第二个瞄准镜的名称
    grip_1 = compare_parts('./picture/equiment/grip_1.png','./picture/grip/',6) # 获取第一个握把的名称
    grip_2 = compare_parts('./picture/equiment/grip_2.png', './picture/grip/', 6) # 获取第二个握把的名称
    butt_1 = compare_parts('./picture/equiment/butt_1.png','./picture/butt/',6) # 获取第一个枪托的名称
    butt_2 = compare_parts('./picture/equiment/butt_2.png', './picture/butt/', 6) # 获取第二个枪托的名称
    muzzle_1 = 'None' # 定义一个变量 muzzle_1，其初始值为 'None'
    muzzle_2 = 'None' # 定义一个变量 muzzle_2，其初始值为 'None'
    if gun_1 != 'None': # 检查 gun_1 变量是否不等于 'None'
        try:
            with codecs.open("./枪械数据/game.json") as f: # 打开文件
                game_data = json.load(f) # 加载 JSON 数据
                gun_data = game_data['list'][gun_1] # 获取枪支数据
                guntype = gun_data['type'] # 获取枪支类型
                muzzle_path = './picture/muzzle/' + guntype + '/' # 计算出消音器的路径
                muzzle_1 = compare_parts('./picture/equiment/muzzle_1.png',muzzle_path, 6) # 获取第一个消音器的名称
        except Exception as e: # 如果发生异常
            print(type(e), '::', e)
    if gun_2 != 'None': # 检查 gun_2 变量是否不等于 'None'
        try:
            with codecs.open("./枪械数据/game.json") as f: # 打开文件
                game_data = json.load(f) # 加载 JSON 数据
                gun_data = game_data['list'][gun_2] # 获取枪支数据
                guntype = gun_data['type'] # 获取枪支类型
                muzzle_path = './picture/muzzle/' + guntype + '/' # 计算出消音器的路径
                muzzle_2 = compare_parts('./picture/equiment/muzzle_2.png', muzzle_path, 6) # 获取第二个消音器的名称
        except Exception as e: # 如果发生异常
            print(type(e), '::', e) # 打印异常信息
    print(gun_1,mirror_1,grip_1,muzzle_1,butt_1) # 打印第一把枪、第一个瞄准镜、第一个握把、第一个消音器和第一个枪托的名称
    print(gun_2, mirror_2, grip_2, muzzle_2, butt_2) # 打印第二把枪、第二个瞄准镜、第二个握把、第二个消音器和第二个枪托的名称
    Gun1 = Gun(gun_1, mirror_1, muzzle_1, grip_1, butt_1) # 创建一个 Gun 对象，表示第一把枪
    Gun2 = Gun(gun_2, mirror_2, muzzle_2, grip_2, butt_2) # 创建一个 Gun 对象，表示第二把枪
    return [Gun1,Gun2] # 返回包含两个 Gun 对象的列表

def is_bag_open():
    bag_chickpoint_screenshot()
    bag_path = './picture/chickpoint/bag.png'
    cureent_bag_state = './picture/equiment/bag.png'
    tmp_dist = compare2pic(bag_path,cureent_bag_state,5)
    if tmp_dist < 5:
        return True
    else:
        return False

def get_hash(img):
    '''
    get_hash 函数的功能是计算图像的感知哈希值。它接受一个参数 img，表示图像文件的路径。

    函数内部首先打开图像文件，并调整其大小为 9x8 像素，然后将其转换为灰度图。接着遍历每个像素，比较相邻两个像素的值。如果前一个像素的值大于后一个像素的值，则在字符串中添加 '1'；否则，在字符串中添加 '0'。最后，将字符串转换为十六进制，并返回结果。

    感知哈希算法是一种用于比较图像相似度的算法。它通过计算图像的哈希值，后续比较两个哈希值的汉明距离来判断两张图像是否相似。汉明距离越小，表示两张图像越相似。
    '''
    hash = '' # 定义一个空字符串
    image = Image.open(img) # 打开图像文件
    image = np.array(image.resize((9, 8), Image.ANTIALIAS).convert('L'), 'f') 
    for i in range(8): # 遍历每一行
        for j in range(8): # 遍历每一列
            if image[i, j] > image[i, j + 1]: # 比较相邻两个像素的值
                hash += '1' # 如果前一个像素的值大于后一个像素的值，则在字符串中添加 '1'
            else:
                hash += '0' # 否则，在字符串中添加 '0'
    hash = ''.join(map(lambda x: '%x' % int(hash[x: x + 4], 2), range(0, 64, 4))) # 将字符串转换为十六进制
    return hash # 返回结果

def get_Hamming(hash1, hash2):
    '''
    计算两张图像的哈希值的汉明距离，汉明距离越小，表示两张图像越相似。
    '''
    Hamming = 0 # 定义一个变量 Hamming，其初始值为 0
    for i in range(len(hash1)): # 遍历每个字符
        if hash1[i] != hash2[i]: # 比较两个字符串中对应位置的字符是否相同
            Hamming += 1 # 如果不同，则将 Hamming 的值加 1
    return Hamming # 返回结果

def compare2pic(equi, demo, threshold):
    '''
    计算两张图像的哈希值，然后比较它们的汉明距离来判断两张图像是否相似。如果汉明距离小于等于阈值，则认为两张图像相似；否则，认为它们不相似。
    '''
    equi_hash = get_hash(equi) # 调用 get_hash 函数获取 equi 图像的哈希值
    demo_hash = get_hash(demo) # 调用 get_hash 函数获取 demo 图像的哈希值
    distance = get_Hamming(equi_hash, demo_hash) # 调用 get_Hamming 函数计算两个哈希值的汉明距离
    if distance <= threshold: # 如果汉明距离小于等于阈值
        return distance # 返回汉明距离
    return threshold+1 # 否则，返回阈值加 1

#截图
def make_screenshot(x1, y1, x2,y2):
    bbox = (x1, y1, x2,y2)
    im = ImageGrab.grab(bbox)
    return im

# 一号位和二号位的武器图像处理
def equi_gun_screenshot(img):
    gun_1 = adaptive_binarization(np.array(img.crop((1825,125,1905,165)).convert('L'))) # 一号枪截图区（此数据适用2K分辨率，其余分辨率或者其余游戏自行调整）
    gun_2 = adaptive_binarization(np.array(img.crop((1825, 431, 1905, 471)).convert('L')))  # 二号枪截图区（此数据适用2K分辨率，其余分辨率或者其余游戏自行调整）
    cv2.imwrite('./picture/equiment/gun_1.png', gun_1)
    cv2.imwrite('./picture/equiment/gun_2.png', gun_2)

#当前姿势截图
def posture_screenshot():
    im_1 = make_screenshot(946, 1320, 989, 1367)  # 姿势截图区（此数据适用2K分辨率，其余分辨率或者其余游戏自行调整）
    im_1.save('./picture/equiment/posture.png')

def mirror_screenchot(img):
    #倍镜
    mirror_1 = adaptive_binarization(np.array(img.crop((2136, 160, 2198, 190)).convert('L')))
    mirror_2 = adaptive_binarization(np.array(img.crop((2136, 466, 2198, 496)).convert('L')))
    cv2.imwrite('./picture/equiment/mirror_1.png', mirror_1)
    cv2.imwrite('./picture/equiment/mirror_2.png', mirror_2)

def muzzle_screenchot(img):
    #枪口
    muzzle_1 = adaptive_binarization(np.array(img.crop((1780,336,1831,388)).convert('L')))
    muzzle_2 = adaptive_binarization(np.array(img.crop((1780, 642, 1831, 694)).convert('L')))
    cv2.imwrite('./picture/equiment/muzzle_1.png', muzzle_1)
    cv2.imwrite('./picture/equiment/muzzle_2.png', muzzle_2)
    # cv2.imwrite('./picture/muzzle/sub_compensate.png', muzzle_1)
    # cv2.imwrite('./picture/muzzle/sub_flame.png', muzzle_2)

def grip_screenchot(img):
    #握把
    grip_1 = adaptive_binarization(np.array(img.crop((1915,336,1965,388)).convert('L')))
    grip_2 = adaptive_binarization(np.array(img.crop((1915, 642, 1965, 694)).convert('L')))
    cv2.imwrite('./picture/equiment/grip_1.png', grip_1)
    cv2.imwrite('./picture/equiment/grip_2.png', grip_2)
    # cv2.imwrite('./picture/grip/thumb.png', grip_1)
    # cv2.imwrite('./picture/grip/half.png', grip_2)

def butt_screenchot(img):
    #枪托
    butt_1 = adaptive_binarization(np.array(img.crop((2344,340,2394,388)).convert('L')))
    butt_2 = adaptive_binarization(np.array(img.crop((2344, 646, 2394, 694)).convert('L')))
    cv2.imwrite('./picture/equiment/butt_1.png',butt_1)
    cv2.imwrite('./picture/equiment/butt_2.png', butt_2)

def adaptive_binarization(img):
    #自适应二值化
    maxval = 255
    blockSize = 5
    C = 5
    img2 = cv2.adaptiveThreshold(img, maxval, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C)
    return img2

#当前背包关键监测点截图
def bag_chickpoint_screenshot():
    # 1、2号装备截图对齐原则，适用2560*1440，横坐标不变，纵坐标加306
    img = ImageGrab.grab() #屏幕截图
    bag = img.crop((501,78,573,116)) #提取截屏背包检测点
    bag.save('./picture/equiment/bag.png')

    equi_gun_screenshot(img)
    mirror_screenchot(img)
    muzzle_screenchot(img)
    grip_screenchot(img)
    butt_screenchot(img)

def get_pixel_gray(pixel):
    gray = 0
    for color in pixel:
        gray += color
    return gray/3

def get_firestate():
    img = ImageGrab.grab()
    firetype = 0
    bullet1 = get_pixel_gray(img.getpixel((1226,1337)))
    bullet2 = get_pixel_gray(img.getpixel((1226,1343)))
    bullet3 = get_pixel_gray(img.getpixel((1223,1358)))
    if bullet1 < 230:
        firetype = 3
    if bullet1 >= 230 and bullet3 >= 230:
        firetype = 0
    if bullet1 >= 230 and bullet2 >= 230 and bullet3 < 230:
        firetype = 2
    if bullet1 >= 230 and bullet2 < 230 and bullet3 < 230:
        firetype = 1

    stand = get_pixel_gray(img.getpixel((964,1311)))
    squat = get_pixel_gray(img.getpixel((969,1338)))
    lie = get_pixel_gray(img.getpixel((981,1347)))
    if stand > squat:
        if stand > lie:
            posture = 0
        else:
            posture = 2
    else:
        if lie > squat:
            posture = 2
        else:
            posture = 1

    has_bullet = True
    bullet_check = img.getpixel((1286,1354))
    if bullet_check[0] == 255 and bullet_check[1] == 0 and bullet_check[2] == 0:
        has_bullet = False
    state = FireState(posture,firetype,has_bullet)
    return state

def bullet_check():
    """
    弹匣剩余数量检查
    """
    img = ImageGrab.grab()
    gray1 = get_pixel_gray(img.getpixel((1226,1337)))
    gray2 = get_pixel_gray(img.getpixel((1223, 1358)))
    # red = img.getpixel((1286,1346))
    # if red[0] == 255 and red[1] == 0 and red[2] == 0:
    #     return False
    if gray1 < 240 and gray2 < 230:
        return False
    return True

if __name__=="__main__":
    pass
