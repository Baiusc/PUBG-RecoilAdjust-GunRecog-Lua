from ctypes import CDLL
import time

# --- 初始化 G HUB 或 LGS 驱动 ---
try:
    # 尝试加载 ghub_device.dll 动态链接库
    ghub_lib = CDLL(r'./ghub_device.dll')
    # 尝试打开设备，检查是否成功
    is_ghub_ok = ghub_lib.device_open() == 1
    if not is_ghub_ok:
        print('未安装 G HUB 或 LGS 驱动，或设备未连接！')
    else:
        print('G HUB 驱动初始化成功！')
except FileNotFoundError:
    print('没有找到 ghub_device.dll 文件，请确保文件存在于程序同目录下。')
    is_ghub_ok = False # 如果文件不存在，标记为失败

# --- 鼠标和键盘操作函数 ---

def press_mouse_button(button):
    """
    按下鼠标按键。
    
    Args:
        button (int): 鼠标按键代码，例如左键、右键等。
    """
    if is_ghub_ok:
        ghub_lib.mouse_down(button)

def release_mouse_button(button):
    """
    松开鼠标按键。

    Args:
        button (int): 鼠标按键代码。
    """
    if is_ghub_ok:
        ghub_lib.mouse_up(button)

def click_mouse_button(button):
    """
    点击鼠标按键（按下后立即松开）。

    Args:
        button (int): 鼠标按键代码。
    """
    press_mouse_button(button)
    release_mouse_button(button)

def press_key(key_code):
    """
    按下键盘按键。

    Args:
        key_code (int): 键盘按键代码。
    """
    if is_ghub_ok:
        ghub_lib.key_down(key_code)

def release_key(key_code):
    """
    松开键盘按键。

    Args:
        key_code (int): 键盘按键代码。
    """
    if is_ghub_ok:
        ghub_lib.key_up(key_code)

def click_key(key_code):
    """
    点击键盘按键（按下后立即松开）。

    Args:
        key_code (int): 键盘按键代码。
    """
    press_key(key_code)
    release_key(key_code)

def mouse_xy(x, y, abs_move=False):
    """
    相对移动鼠标。
    
    Args:
        x (int): 鼠标在X轴上的相对移动量。
        y (int): 鼠标在Y轴上的相对移动量。
        abs_move (bool): 如果为True，则执行绝对移动（但此函数通常只用于相对移动）。
    """
    if is_ghub_ok:
        # 使用 moveR 函数实现相对移动
        ghub_lib.moveR(int(x), int(y), abs_move)

def mouse_xy_smooth(x, y, total_time, start_time, abs_move=False):
    """
    平滑地移动鼠标，将总移动量分步完成。

    Args:
        x (int): 鼠标在X轴上的总移动量。
        y (int): 鼠标在Y轴上的总移动量。
        total_time (float): 完成移动所需的总时间（毫秒）。
        start_time (float): 开始移动时的基准时间（毫秒）。
        abs_move (bool): 是否为绝对移动。
    """
    if is_ghub_ok:
        # 定义每次移动的步长，这里以Y轴为例
        step = 1
        if y == 0:
            y = 1
        steps = int(y / step)
        if steps == 0:
            steps = 1
            
        # 计算每步移动需要的时间间隔
        sleep_time = total_time / steps # 毫秒
        
        for _ in range(steps):
            ghub_lib.moveR(int(x / steps), step, abs_move)
            
            # 精确控制时间，等待到下一帧移动的时间点
            while (time.perf_counter() * 1000 - start_time) < sleep_time:
                pass
            
            # 更新下一帧的开始时间
            start_time = time.perf_counter() * 1000

# --- 主程序入口 ---
if __name__ == '__main__':
    # 示例用法
    # 相对移动鼠标，向下移动100像素
    if is_ghub_ok:
        ghub_lib.moveR(0, 100, False)