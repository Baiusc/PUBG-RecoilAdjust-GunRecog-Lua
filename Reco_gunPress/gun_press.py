# 导入所需的库
from ghub import * # 假设 ghub 库包含了鼠标操作函数
import time
from recognize import * # 假设 recognize 库包含了识别函数

def fire(shared_data):
    """
    负责处理游戏中的开火和压枪逻辑。
    该函数在一个无限循环中运行，根据共享字典中的信号执行相应操作。
    """
    guns = []  # 存储识别到的枪械信息，Gun 对象列表
    
    while True:
        # --- 1. 背包和装备识别逻辑 ---
        # 检查是否需要识别装备（通过键盘按下Tab键触发）
        if shared_data['bag_signal']:
            # 只有当背包真正打开时才进行识别，防止误操作
            if is_bag_open():
                # 调用 recognize_equipment 函数识别装备，并将结果存储在 guns 列表中
                guns = recognize_equiment()
            # 识别完成后，重置背包信号，等待下一次触发
            shared_data['bag_signal'] = False

        # --- 2. 开火和压枪逻辑 ---
        # 检查开火信号（通过鼠标左键按下触发）
        if shared_data['fire_signal']:
            # 检查当前弹匣是否有子弹
            if not bullet_check():
                continue  # 如果没有子弹，跳过本次循环，不执行压枪

            # 获取当前开火状态（姿势、开火模式等）
            firestate_struct = get_firestate()
            shared_data['posture'] = firestate_struct.posture
            shared_data['firemode'] = firestate_struct.firetype

            # 确保 guns 列表不为空，且当前切换的武器索引有效
            current_gun_index = shared_data['switch']
            if len(guns) > current_gun_index:
                gun = guns[current_gun_index]
                
                # 如果当前武器是“空”，则不执行压枪
                if gun.name == 'None':
                    continue

                i = 0  # 计数器，记录已发射的子弹数
                start_time = time.perf_counter() * 1000  # 记录开火开始时间（毫秒）

                # 根据枪械类型执行不同的压枪逻辑
                if not gun.single:  # 全自动/连发枪械压枪
                    while True:
                        # 根据姿势获取压枪比例
                        posture_ratio = gun.posture_states[shared_data['posture']]
                        
                        # 计算当前子弹的下移量
                        down = gun.para_range[i] * posture_ratio * gun.k
                        
                        i += 1
                        
                        # 检查是否达到最大子弹数或开火信号已停止
                        if i >= gun.maxBullets or not shared_data['fire_signal']:
                            break
                        
                        # 移动鼠标进行压枪
                        mouse_xy(0, down)
                        
                        # 精确控制开火间隔时间
                        elapsed_time = (time.perf_counter() * 1000 - start_time)
                        sleep_time = gun.interval - elapsed_time
                        if sleep_time > 0:
                            time.sleep(sleep_time / 1000)
                        
                        # 更新开始时间为下一次压枪的基准时间
                        start_time = time.perf_counter() * 1000

                else:  # 单发/连狙压枪
                    while True:
                        # 根据姿势获取压枪比例
                        posture_ratio = gun.posture_states[shared_data['posture']]
                        
                        # 计算当前子弹的下移量
                        down = gun.para_range[i] * posture_ratio * gun.k
                        
                        i += 1
                        
                        # 检查是否达到最大子弹数或单发开火信号已停止
                        if i >= gun.maxBullets or shared_data['singlebullet'] < 1:
                            shared_data['singlebullet'] = 0  # 重置单发计数器
                            break
                            
                        # 移动鼠标进行压枪
                        mouse_xy(0, down)
                        
                        # 计算需要等待的时间
                        elapsed_time = (time.perf_counter() * 1000 - start_time)
                        sleep_time = gun.interval - elapsed_time
                        if sleep_time > 0:
                            time.sleep(sleep_time / 1000)
                        
                        # 模拟鼠标点击（连狙模式下）
                        click_mouse_button(1)
                        
                        # 更新开始时间为下一次点击的基准时间
                        start_time = time.perf_counter() * 1000