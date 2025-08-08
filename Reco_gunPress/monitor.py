# 导入所需的库
import multiprocessing
from multiprocessing import Process
from threading import Thread
from pynput import mouse, keyboard
from win32gui import GetWindowText, GetForegroundWindow
from Reco_gunPress.gun_press_myself import *
import atexit

def start_mouse_listen(shared_data):
    """
    启动鼠标监听器，用于监测鼠标点击事件。
    """
    def on_click(x, y, button, pressed):
        """
        处理鼠标点击事件的回调函数。
        """
        # 声明 shared_data 为非局部变量，以便修改共享字典
        nonlocal shared_data
        
        # 检查当前窗口是否为“绝地求生”
        is_pubg_window = '绝地求生' in GetWindowText(GetForegroundWindow())

        if button == mouse.Button.left and is_pubg_window:
            if pressed:
                # 鼠标左键按下，表示开火
                shared_data['fire_signal'] = True
                shared_data['singlebullet'] += 1
            else:
                # 鼠标左键释放，停止开火
                shared_data['fire_signal'] = False
                shared_data['singlebullet'] -= 1
        else:
            # 如果不在游戏窗口，则确保开火信号为 False
            shared_data['fire_signal'] = False
            
        return True

    # 启动鼠标监听器
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def start_key_listen(shared_data):
    """
    启动键盘监听器，用于监测键盘事件。
    """
    def on_press(key):
        """
        处理键盘按下事件的回调函数。
        """
        nonlocal shared_data

        # 检查当前窗口是否为“绝地求生”
        if '绝地求生' in GetWindowText(GetForegroundWindow()):
            if key == keyboard.Key.tab:
                # 按下 Tab 键打开背包
                if not shared_data['key_pressed']:
                    shared_data['key_pressed'] = True
                    shared_data['bag_signal'] = True
            elif key == keyboard.KeyCode.from_char('1'):
                # 按下 '1' 键切换到主武器
                shared_data['switch'] = 0
            elif key == keyboard.KeyCode.from_char('2'):
                # 按下 '2' 键切换到副武器
                shared_data['switch'] = 1

            # 如果正在开火，检测姿势和开火模式变化
            if shared_data['fire_signal']:
                if key in [keyboard.KeyCode.from_char('z'),
                           keyboard.Key.ctrl,
                           keyboard.KeyCode.from_char('c'),
                           keyboard.KeyCode.from_char('b')]:
                    firestate_struct = get_firestate()
                    shared_data['posture'] = firestate_struct.posture
                    shared_data['firemode'] = firestate_struct.firetype

    def on_release(key):
        """
        处理键盘释放事件的回调函数。
        """
        nonlocal shared_data
        shared_data['key_pressed'] = False

    # 启动键盘监听器
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def start_listen(shared_data):
    """
    启动一个包含鼠标和键盘监听器的线程，用于并行监听。
    """
    mouse_thread = Thread(target=start_mouse_listen, args=(shared_data,))
    key_thread = Thread(target=start_key_listen, args=(shared_data,))
    
    mouse_thread.start()
    key_thread.start()
    
    mouse_thread.join()
    key_thread.join()

def exit_handler(p_listen, p_fire):
    """
    程序退出时，终止子进程。
    """
    print("程序退出，正在关闭子进程...")
    if p_listen.is_alive():
        p_listen.terminate()
        p_listen.join()
    if p_fire.is_alive():
        p_fire.terminate()
        p_fire.join()
    print("子进程已关闭。")

if __name__ == '__main__':
    # 启用对可执行文件冻结的支持
    multiprocessing.freeze_support()
    
    # 创建一个管理器，用于在进程间共享数据
    manager = multiprocessing.Manager()
    shared_data = manager.dict()
    
    # 初始化共享字典中的键值
    shared_data['key_pressed'] = False
    shared_data['fire_signal'] = False
    shared_data['firestate_inspect'] = False
    shared_data['bag_signal'] = False
    shared_data['switch'] = 0
    shared_data['posture'] = 0
    shared_data['singlebullet'] = 0
    shared_data['firemode'] = 3
    
    # 创建并启动用于开火和监听的两个进程
    p_fire = Process(target=fire, args=(shared_data,))
    p_listen = Process(target=start_listen, args=(shared_data,))
    
    p_listen.start()
    p_fire.start()

    # 注册退出处理函数，确保程序退出时子进程被正确关闭
    atexit.register(exit_handler, p_listen, p_fire)
    
    # 等待进程完成（通常不会执行到这里，因为监听进程会一直运行）
    p_listen.join()
    p_fire.join()