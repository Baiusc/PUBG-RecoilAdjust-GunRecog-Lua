import multiprocessing
from multiprocessing import Process
from threading import Thread
from pynput import mouse,keyboard
from win32gui import GetWindowText, GetForegroundWindow
from gun_press import *


def start_mouse_listen(dict):    # 定义一个函数，用于监听鼠标事件
    def on_button_click(x, y, button, pressed):        # 定义一个内部函数，用于处理鼠标点击事件
        nonlocal dict # 声明 dict 变量为非局部变量
        if button == button.left: # 如果点击的是鼠标左键
            if pressed and '绝地求生' in GetWindowText(GetForegroundWindow()): # 如果鼠标左键被按下且当前窗口标题包含 '绝地求生'
                dict['fire_signal'] = True # 将字典中的 'fire_signal' 键的值设置为 True
                dict['singlebullet'] += 1 # 将字典中的 'singlebullet' 键的值加 1
            elif not pressed and '绝地求生' in GetWindowText(GetForegroundWindow()): # 如果鼠标左键被释放且当前窗口标题包含 '绝地求生'
                dict['fire_signal'] = False # 将字典中的 'fire_signal' 键的值设置为 False
                dict['singlebullet'] -= 1 # 将字典中的 'singlebullet' 键的值减 1
            else: # 其他情况
                dict['fire_signal'] = False # 将字典中的 'fire_signal' 键的值设置为 False
        else: # 如果点击的不是鼠标左键
            pass # 不执行任何操作
        return True # 返回 True，表示继续监听鼠标事件

    # 仅调试时用到
    def on_move(x, y):
        if dict['fire_signal']: 
            # 在开火时记录鼠标的位置
            print('鼠标位置： {0}'.format((x, y)))

    with mouse.Listener(on_click=on_button_click) as listener: # ,on_move=on_move
        # 创建一个鼠标监听器对象，指定 on_click 参数为 on_button_click 函数
        listener.join() # 等待监听器完成

def start_key_listen(dict):
    # 定义一个函数，用于监听键盘事件
    def on_key_press(key):
        # 定义一个内部函数，用于处理键盘按下事件
        nonlocal dict # 声明 dict 变量为非局部变量
        windowName = GetWindowText(GetForegroundWindow()) 
        if '绝地求生' in GetWindowText(GetForegroundWindow()): # 如果当前窗口标题包含 '绝地求生'
            if key == keyboard.Key.tab: # 如果按下的是 Tab 键
                if dict['key_pressed']: # 如果字典中的 'key_pressed' 键的值为 True
                    return True # 返回 True，表示继续监听键盘事件
                dict['key_pressed'] = True # 将字典中的 'key_pressed' 键的值设置为 True
                dict['bag_signal'] = True # 将字典中的 'bag_signal' 键的值设置为 True
            elif key == keyboard.KeyCode.from_char('1'): # 如果按下的是 '1' 键
                dict['switch'] = 0 # 将字典中的 'switch' 键的值设置为 0
            elif key == keyboard.KeyCode.from_char('2'): # 如果按下的是 '2' 键
                dict['switch'] = 1 # 将字典中的 'switch' 键的值设置为 1
            if dict['fire_signal']: # 如果字典中的 'fire_signal' 键的值为 True
                # 开火过程中才对卧(z)，蹲（c/ctrl），切换开火模式(b)的按键进行检测，检测到则更新当前开火状态
                if key == keyboard.KeyCode.from_char(
                        'z') or key == keyboard.Key.ctrl or key == keyboard.KeyCode.from_char(
                    'b') or key == keyboard.KeyCode.from_char('c'):
                    firestate_struct = get_firestate() # 调用 get_firestate 函数获取当前开火状态
                    dict['posture'] = firestate_struct.posture # 将字典中的 'posture' 键的值设置为 firestate_struct 的 posture 属性值
                    dict['firemode'] = firestate_struct.firetype # 将字典中的 'firemode' 键的值设置为 firestate_struct 的 firetype 属性值

    def on_key_release(key):
        # 定义一个内部函数，用于处理键盘释放事件
        nonlocal dict # 声明 dict 变量为非局部变量
        dict['key_pressed'] = False # 将字典中的 'key_pressed' 键的值设置为 False

    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        # 创建一个键盘监听器对象，指定 on_press 和 on_release 参数分别为 on_key_press 和 on_key_release 函数
        listener.join() # 等待监听器完成

def start_listen(dict):
    t1 = Thread(target=start_mouse_listen,args=(dict,)) # 创建一个新线程对象，目标函数是 start_mouse_listen，将共享字典作为参数传递给该函数
    t2 = Thread(target=start_key_listen,args=(dict,)) # 创建另一个新线程对象，目标函数是 start_key_listen，将共享字典作为参数传递给该函数
    t1.start() # 启动鼠标监听线程
    t2.start() # 启动键盘监听线程
    t1.join() # 等待鼠标监听线程完成
    t2.join() # 等待键盘监听线程完成

# 请在下面的代码中添加功能：在程序退出时，关闭p_listen和p_fire进程。
if __name__=='__main__':
    multiprocessing.freeze_support() # 在 Windows 上支持冻结可执行文件
    mgr = multiprocessing.Manager() # 创建一个管理器对象，用于在多个进程之间共享数据
    dict = mgr.dict() # 使用管理器对象创建一个可在多个进程之间共享的字典
    dict['key_pressed'] = False # 在字典中添加一个名为 'key_pressed' 的键，并将其值设置为 False
    dict['fire_signal'] = False # 在字典中添加一个名为 'fire_signal' 的键，并将其值设置为 False
    dict['firestate_inspect'] = False # 在字典中添加一个名为 'firestate_inspect' 的键，并将其值设置为 False
    dict['bag_signal'] = False # 在字典中添加一个名为 'bag_signal' 的键，并将其值设置为 False
    dict['switch'] = 0 # 在字典中添加一个名为 'switch' 的键，并将其值设置为 0
    dict['posture'] = 0 # 在字典中添加一个名为 'posture' 的键，并将其值设置为 0
    dict['singlebullet'] = 0 # 在字典中添加一个名为 'singlebullet' 的键，并将其值设置为 0
    dict['firemode'] = 3 # 在字典中添加一个名为 'firemode' 的键，并将其值设置为 3
    p_fire = Process(target=fire,args=(dict,)) # 创建一个新的进程对象，目标函数是 fire，将共享字典作为参数传递给该函数
    p_listen = Process(target=start_listen,args=(dict,)) # 创建另一个新的进程对象，目标函数是 start_listen，将共享字典作为参数传递给该函数
    p_listen.start() # 启动监听进程
    p_fire.start() # 启动发射进程
    p_listen.join() # 等待监听进程完成
    p_fire.join() # 等待发射进程完成

