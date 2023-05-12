from ghub import *
import time
from recognize import *

def fire(dict):
    Guns = [] # 定义一个空列表 Guns
    while True: # 无限循环
        if dict['bag_signal']: # 检查字典中的 bag_signal 键是否为真
            if is_bag_open(): # 调用 is_bag_open 函数检查背包是否打开
                Guns = recognize_equiment() # 调用 recognize_equiment 函数识别装备，并将结果存储在 Guns 列表中
            dict['bag_signal'] = False # 将字典中的 bag_signal 键设置为假
        if dict['fire_signal']: # 检查字典中的 fire_signal 键是否为真  
            if not bullet_check(): # 调用 bullet_check 函数检查子弹是否充足
                continue # 如果子弹不足，则继续下一次循环   

            start_time = time.perf_counter()* 1000 # 获取当前时间（以毫秒为单位）

            # start_time = round(time.perf_counter(), 3) * 1000 # 获取当前时间（以毫秒为单位）

            firestate_struct = get_firestate() # 调用 get_firestate 函数获取开火状态
            dict['posture'] = firestate_struct.posture # 将开火状态中的姿势存储在字典的 posture 键中
            dict['firemode'] = firestate_struct.firetype # 将开火状态中的开火类型存储在字典的 firemode 键中
            if len(Guns) > dict['switch']: # 检查 Guns 列表的长度是否大于字典中的 switch 键
                gun = Guns[dict['switch']] # 获取列表中对应索引的枪支对象
                if gun.name == 'None': # 检查枪支对象的名称是否为 'None'
                    continue # 如果名称为 'None'，则继续下一次循环
                i = 0 # 初始化一个变量i，用于后面计数使用
                if gun.single == False:  # 如果该枪不是单发模式
                    while True: # 进入循环
                        posture_ratio = gun.posture_states[dict['posture']] # 根据字典中的 posture 键获取枪支对象的姿势状态，并计算出姿势比例
                        down = gun.para_range[i] * posture_ratio * gun.k # 根据枪支对象的 para_range 属性、姿势比例和 k 属性计算出下移量
                        print('第{}发,压{}'.format( i+1, down))
                        i += 1 # 将 i 变量加 1
                        if i == gun.maxBullets or not dict['fire_signal']: # 检查 i 是否等于枪支对象的 maxBullets 属性或字典中的 fire_signal 键是否为假
                            break # 如果满足任一条件，则退出循环

                        mouse_xy_smooth(0, down, gun.interval, start_time) # 调用 mouse_xy 函数移动鼠标

                        # mouse_xy(0, down) # 调用 mouse_xy 函数移动鼠标
                        # elapsed = (round(time.perf_counter(), 3) * 1000 - start_time) # 计算经过的时间（以毫秒为单位）
                        # sleeptime = gun.interval - elapsed # 计算睡眠时间
                        # time.sleep(sleeptime/ 1000) # 睡眠指定时间
                        # start_time = round(time.perf_counter(), 3) * 1000 # 获取当前时间（以毫秒为单位）
                        
                else: # 连狙压枪 如果该枪是单发模式
                    while True: # 进入循环
                        posture_ratio = gun.posture_states[dict['posture']] # 根据字典中的 posture 键获取枪支对象的姿势状态，并计算出姿势比例
                        down = gun.para_range[i] * posture_ratio * gun.k # 根据枪支对象的 para_range 属性、姿势比例和 k 属性计算出下移量
                        i += 1 # 将 i 变量加 1
                        if i == gun.maxBullets or dict['singlebullet'] < 1: # 检查 i 是否等于枪支对象的 maxBullets 属性或字典中的 singlebullet 键是否小于 1
                            dict['singlebullet'] = 0 # 将字典中的 singlebullet 键设置为 0
                            break # 退出循环

                        # mouse_xy_smooth(0, down, gun.interval, start_time) # 调用 mouse_xy 函数移动鼠标

                        mouse_xy(0, down) # 调用 mouse_xy 函数移动鼠标
                        elapsed = (round(time.perf_counter(), 3) * 1000 - start_time) # 计算经过的时间（以毫秒为单位）
                        sleeptime = gun.interval - elapsed # 计算睡眠时间
                        time.sleep(sleeptime / 1000) # 睡眠指定时间
                        click_mouse_button(1) # 调用 click_mouse_button 函数点击鼠标按钮
                        start_time = round(time.perf_counter(), 3) * 1000 # 获取当前时间（以毫秒为单位）