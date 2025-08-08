# 导入所需的库
import codecs
import json
import os
from PIL import ImageGrab, Image
import numpy as np
import cv2
from dataload import FireState, Gun

# --- 图像识别核心功能 ---

def compare_parts(file_path, demo_dir, threshold):
    """
    将一张图片与指定目录下的所有模板图片进行比较，找出最相似的图片。

    Args:
        file_path (str): 待比较的图像文件路径。
        demo_dir (str): 包含模板图片的目录路径（以“/”或“\\”结尾）。
        threshold (int): 汉明距离的相似度阈值。

    Returns:
        str: 最相似的模板图片的文件名（不含扩展名），如果没有找到相似图片则返回 'None'。
    """
    min_distance = threshold + 1  # 初始化一个大于阈值的距离
    most_similar_part = 'None'
    
    # 遍历模板目录中的所有文件
    for demo_file in os.listdir(demo_dir):
        demo_path = os.path.join(demo_dir, demo_file)
        
        # 比较两张图片的汉明距离
        tmp_dist = compare2pic(file_path, demo_path, threshold)
        
        # 如果找到更相似的图片，则更新最小距离和最相似文件名
        if tmp_dist < min_distance:
            min_distance = tmp_dist
            most_similar_part = os.path.splitext(demo_file)[0]
            
    return most_similar_part

def recognize_equipment():
    """
    识别当前游戏屏幕中背包界面内的装备（主副枪、瞄镜、握把、枪托、枪口）。
    该函数通过截图和图像识别来判断装备类型。

    Returns:
        list: 包含两个 Gun 对象的列表，分别代表主武器和副武器。
    """
    # 识别主副武器
    gun_1_name = compare_parts('./picture/equiment/gun_1.png', './picture/gun/', 6)
    gun_2_name = compare_parts('./picture/equiment/gun_2.png', './picture/gun/', 6)
    
    # 识别瞄准镜
    mirror_1_name = compare_parts('./picture/equiment/mirror_1.png', './picture/mirrors/', 6)
    mirror_2_name = compare_parts('./picture/equiment/mirror_2.png', './picture/mirrors/', 6)
    
    # 识别握把
    grip_1_name = compare_parts('./picture/equiment/grip_1.png', './picture/grip/', 6)
    grip_2_name = compare_parts('./picture/equiment/grip_2.png', './picture/grip/', 6)
    
    # 识别枪托
    butt_1_name = compare_parts('./picture/equiment/butt_1.png', './picture/butt/', 6)
    butt_2_name = compare_parts('./picture/equiment/butt_2.png', './picture/butt/', 6)
    
    muzzle_1_name = 'None'
    muzzle_2_name = 'None'
    
    # 根据枪械类型识别枪口（因为不同枪械的枪口模板不同）
    try:
        if gun_1_name != 'None':
            with codecs.open("./枪械数据/game.json", "r", "utf-8") as f:
                game_data = json.load(f)
                gun_type = game_data['list'][gun_1_name]['type']
                muzzle_path = f'./picture/muzzle/{gun_type}/'
                muzzle_1_name = compare_parts('./picture/equiment/muzzle_1.png', muzzle_path, 6)
        
        if gun_2_name != 'None':
            with codecs.open("./枪械数据/game.json", "r", "utf-8") as f:
                game_data = json.load(f)
                gun_type = game_data['list'][gun_2_name]['type']
                muzzle_path = f'./picture/muzzle/{gun_type}/'
                muzzle_2_name = compare_parts('./picture/equiment/muzzle_2.png', muzzle_path, 6)
    except (FileNotFoundError, KeyError) as e:
        print(f"识别枪口时出错: {type(e)} - {e}")

    # 打印识别结果以供调试
    print(f"主武器: {gun_1_name}, 瞄镜: {mirror_1_name}, 握把: {grip_1_name}, 枪口: {muzzle_1_name}, 枪托: {butt_1_name}")
    print(f"副武器: {gun_2_name}, 瞄镜: {mirror_2_name}, 握把: {grip_2_name}, 枪口: {muzzle_2_name}, 枪托: {butt_2_name}")
    
    # 创建 Gun 对象并返回
    gun1 = Gun(gun_1_name, mirror_1_name, muzzle_1_name, grip_1_name, butt_1_name)
    gun2 = Gun(gun_2_name, mirror_2_name, grip_2_name, muzzle_2_name, butt_2_name)
    return [gun1, gun2]

def get_fire_state():
    """
    通过对屏幕指定像素点的颜色进行采样，判断当前的开火模式、玩家姿势和子弹状态。
    这个方法比图像识别更快、更准确。

    Returns:
        FireState: 一个包含姿势、开火模式和子弹状态的 FireState 对象。
    """
    img = ImageGrab.grab()
    
    # 1. 判断开火模式
    firetype = 0
    # 获取像素点的灰度值，用于判断单发/连发/全自动模式
    bullet1_gray = get_pixel_gray(img.getpixel((1226, 1337)))
    bullet2_gray = get_pixel_gray(img.getpixel((1226, 1343)))
    bullet3_gray = get_pixel_gray(img.getpixel((1223, 1358)))
    
    if bullet1_gray < 230:
        firetype = 3  # 全自动
    elif bullet1_gray >= 230 and bullet3_gray >= 230:
        firetype = 0  # 单发
    elif bullet1_gray >= 230 and bullet2_gray >= 230 and bullet3_gray < 230:
        firetype = 2  # 两连发
    elif bullet1_gray >= 230 and bullet2_gray < 230 and bullet3_gray < 230:
        firetype = 1  # 3连发
        
    # 2. 判断玩家姿势
    posture = 0
    stand_gray = get_pixel_gray(img.getpixel((964, 1311)))
    squat_gray = get_pixel_gray(img.getpixel((969, 1338)))
    lie_gray = get_pixel_gray(img.getpixel((981, 1347)))
    
    # 通过比较像素灰度值来判断姿势
    if stand_gray > squat_gray and stand_gray > lie_gray:
        posture = 0  # 站立
    elif lie_gray > squat_gray and lie_gray > stand_gray:
        posture = 2  # 卧倒
    else:
        posture = 1  # 蹲下

    # 3. 判断是否还有子弹
    has_bullet = True
    bullet_check_pixel = img.getpixel((1286, 1354))
    # 检查屏幕上的子弹图标是否为红色（没子弹）
    if bullet_check_pixel[0] == 255 and bullet_check_pixel[1] == 0 and bullet_check_pixel[2] == 0:
        has_bullet = False
        
    return FireState(posture, firetype, has_bullet)

def is_bag_open():
    """
    检查游戏背包是否打开。
    通过截图并比较一个关键点的汉明距离来判断。

    Returns:
        bool: 如果背包打开返回 True，否则返回 False。
    """
    bag_chickpoint_screenshot()
    bag_template_path = './picture/chickpoint/bag.png'
    current_bag_path = './picture/equiment/bag.png'
    
    # 比较背包关键点截图与模板的汉明距离
    tmp_dist = compare2pic(bag_template_path, current_bag_path, 5)
    return tmp_dist < 5

# --- 图像处理和截图功能 ---

def make_screenshot(x1, y1, x2, y2):
    """
    对屏幕指定区域进行截图。

    Args:
        x1, y1 (int): 截图区域的左上角坐标。
        x2, y2 (int): 截图区域的右下角坐标。

    Returns:
        Image: 截图得到的 PIL Image 对象。
    """
    return ImageGrab.grab((x1, y1, x2, y2))

def adaptive_binarization(img):
    """
    对图像进行自适应二值化处理。
    
    Args:
        img (np.array): 灰度图像的 NumPy 数组。

    Returns:
        np.array: 二值化后的图像。
    """
    maxval = 255
    blockSize = 5
    C = 5
    # cv2.ADAPTIVE_THRESH_MEAN_C 表示使用局部邻域的平均值作为阈值
    img_bin = cv2.adaptiveThreshold(img, maxval, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C)
    return img_bin

def bag_chickpoint_screenshot():
    """
    对游戏屏幕中的装备栏进行截图，用于后续的识别。
    这个函数会截取枪械、瞄镜、枪口、握把和枪托的区域。
    """
    img = ImageGrab.grab()  # 屏幕截图
    
    # 提取并保存背包关键点的截图
    bag_img = img.crop((501, 78, 573, 116))
    bag_img.save('./picture/equiment/bag.png')
    
    # 提取并保存各装备的截图，并进行二值化处理
    equi_gun_screenshot(img)
    mirror_screenchot(img)
    muzzle_screenchot(img)
    grip_screenchot(img)
    butt_screenchot(img)

def equi_gun_screenshot(img):
    """截取主副武器图标区域"""
    gun_1 = adaptive_binarization(np.array(img.crop((1825, 125, 1905, 165)).convert('L')))
    gun_2 = adaptive_binarization(np.array(img.crop((1825, 431, 1905, 471)).convert('L')))
    cv2.imwrite('./picture/equiment/gun_1.png', gun_1)
    cv2.imwrite('./picture/equiment/gun_2.png', gun_2)

def mirror_screenchot(img):
    """截取瞄准镜图标区域"""
    mirror_1 = adaptive_binarization(np.array(img.crop((2136, 160, 2198, 190)).convert('L')))
    mirror_2 = adaptive_binarization(np.array(img.crop((2136, 466, 2198, 496)).convert('L')))
    cv2.imwrite('./picture/equiment/mirror_1.png', mirror_1)
    cv2.imwrite('./picture/equiment/mirror_2.png', mirror_2)

def muzzle_screenchot(img):
    """截取枪口图标区域"""
    muzzle_1 = adaptive_binarization(np.array(img.crop((1780, 336, 1831, 388)).convert('L')))
    muzzle_2 = adaptive_binarization(np.array(img.crop((1780, 642, 1831, 694)).convert('L')))
    cv2.imwrite('./picture/equiment/muzzle_1.png', muzzle_1)
    cv2.imwrite('./picture/equiment/muzzle_2.png', muzzle_2)

def grip_screenchot(img):
    """截取握把图标区域"""
    grip_1 = adaptive_binarization(np.array(img.crop((1915, 336, 1965, 388)).convert('L')))
    grip_2 = adaptive_binarization(np.array(img.crop((1915, 642, 1965, 694)).convert('L')))
    cv2.imwrite('./picture/equiment/grip_1.png', grip_1)
    cv2.imwrite('./picture/equiment/grip_2.png', grip_2)

def butt_screenchot(img):
    """截取枪托图标区域"""
    butt_1 = adaptive_binarization(np.array(img.crop((2344, 340, 2394, 388)).convert('L')))
    butt_2 = adaptive_binarization(np.array(img.crop((2344, 646, 2394, 694)).convert('L')))
    cv2.imwrite('./picture/equiment/butt_1.png', butt_1)
    cv2.imwrite('./picture/equiment/butt_2.png', butt_2)
    
# --- 图像哈希和距离计算 ---

def get_hash(img_path):
    """
    计算图像的感知哈希值 (phash)。
    
    Args:
        img_path (str): 图像文件路径。

    Returns:
        str: 图像的十六进制哈希值。
    """
    image = Image.open(img_path)
    # 调整图像大小、转为灰度图并转换为 NumPy 数组
    image = np.array(image.resize((9, 8), Image.Resampling.LANCZOS).convert('L'), 'f')
    
    hash_str = ''
    # 比较相邻像素的灰度值，生成哈希字符串
    for i in range(8):
        for j in range(8):
            if image[i, j] > image[i, j + 1]:
                hash_str += '1'
            else:
                hash_str += '0'
    
    # 将哈希字符串转换为十六进制格式
    return ''.join(map(lambda x: '%x' % int(hash_str[x: x + 4], 2), range(0, 64, 4)))

def get_Hamming(hash1, hash2):
    """
    计算两个哈希值之间的汉明距离。
    
    Args:
        hash1 (str): 第一个十六进制哈希值。
        hash2 (str): 第二个十六进制哈希值。

    Returns:
        int: 汉明距离。
    """
    hamming_distance = 0
    for i in range(len(hash1)):
        # 比较两个字符串的对应字符，不相同则距离加一
        if hash1[i] != hash2[i]:
            hamming_distance += 1
    return hamming_distance

def compare2pic(equi_path, demo_path, threshold):
    """
    通过比较感知哈希值的汉明距离来判断两张图片是否相似。

    Args:
        equi_path (str): 第一张图片的路径。
        demo_path (str): 第二张图片的路径。
        threshold (int): 汉明距离的阈值。

    Returns:
        int: 如果汉明距离小于或等于阈值，则返回汉明距离；否则返回阈值加1。
    """
    try:
        equi_hash = get_hash(equi_path)
        demo_hash = get_hash(demo_path)
        distance = get_Hamming(equi_hash, demo_hash)
        
        if distance <= threshold:
            return distance
        return threshold + 1
    except Exception as e:
        print(f"图片比较出错: {e}")
        return threshold + 1

def get_pixel_gray(pixel):
    """
    计算一个 RGB 像素点的灰度值。
    """
    return sum(pixel) / 3

def current_posture():
    """
    过时的姿势识别函数，已废弃。
    现在姿势识别采用 get_fire_state() 函数中的像素取样方法。
    """
    print('姿势识别 - 此函数已废弃，请使用 get_fire_state()')
    posture_screenshot()
    # 后续的代码因为已废弃，故不再详细注释

def posture_screenshot():
    """
    截取玩家姿势图标的区域。过时，已废弃。
    """
    im_1 = make_screenshot(946, 1320, 989, 1367)
    im_1.save('./picture/equiment/posture.png')

def bullet_check():
    """
    过时的子弹检查函数，已废弃。
    现在子弹检查采用 get_fire_state() 函数中的像素取样方法。
    """
    print('子弹检查 - 此函数已废弃，请使用 get_fire_state()')
    img = ImageGrab.grab()
    gray1 = get_pixel_gray(img.getpixel((1226, 1337)))
    gray2 = get_pixel_gray(img.getpixel((1223, 1358)))

    if gray1 < 240 and gray2 < 230:
        return False
    return True

if __name__ == "__main__":
    pass