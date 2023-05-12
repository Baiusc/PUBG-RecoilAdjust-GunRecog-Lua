from ctypes import CDLL
import time
try:
    gm = CDLL(r'./ghub_device.dll')
    gmok = gm.device_open() == 1
    if not gmok:
        print('未安装ghub或者lgs驱动!!!')
    else:
        print('初始化成功!')
except FileNotFoundError:
    print('没有找到 ghub_device.dll 文件')

#按下鼠标按键
def press_mouse_button(button):
    if gmok:
        gm.mouse_down(button)

#松开鼠标按键
def release_mouse_button(button):
    if gmok:
        gm.mouse_up(button)

#点击鼠标
def click_mouse_button(button):
    press_mouse_button(button)
    release_mouse_button(button)

#按下键盘按键
def press_key(code):
    if gmok:
        gm.key_down(code)

#松开键盘按键
def release_key(code):
    if gmok:
        gm.key_up(code)

#点击键盘按键
def click_key(code):
    press_key(code)
    release_key(code)

# 鼠标移动
def mouse_xy(x, y, abs_move = False):
    if gmok:
        gm.moveR(int(0), int(y), abs_move)

# 平滑鼠标移动
def mouse_xy_smooth(x, y, time_all, time_start, abs_move=False):
    if gmok:
        step = 1 
        if(y==0): y = 1
        steps = int(y/step)
        sleep_time = time_all/steps # 毫秒
        for i in range(steps):
            gm.moveR(1, step, abs_move)
            while time.perf_counter()* 1000 - time_start < sleep_time: # 若还没到开火间隔时间，则等待
                pass
            time_start = time.perf_counter()* 1000  # 更新开始时间（以毫秒为单位）
           


if __name__=='__main__':
    # mouse_xy(0,100)
    # mouse_xy(100,0)
    # mouse_xy(-100,-100)
     gm.moveR(0, 100, False)
                    
   



