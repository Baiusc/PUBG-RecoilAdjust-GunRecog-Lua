import codecs
import json

class FireState:
    """
    存储游戏角色的开火状态。
    """
    def __init__(self, posture, firetype, has_bullet):
        """
        初始化 FireState 对象。

        Args:
            posture (int): 玩家姿势，0 代表站立，1 代表蹲下，2 代表卧倒。
            firetype (int): 开火模式，0 代表单发，1 代表三连发，2 代表两连发，3 代表全自动。
            has_bullet (bool): 弹匣中是否有子弹，True 为有，False 为无。
        """
        self.posture = posture
        self.firetype = firetype
        self.has_bullet = has_bullet


class Gun:
    """
    表示游戏中的一把枪械及其相关属性和配件影响。
    """
    def __init__(self, name='None', mirror='', muzzle='', grip='', butt=''):
        """
        初始化 Gun 对象，并从配置文件加载枪械数据。

        Args:
            name (str): 枪械名称。
            mirror (str): 瞄准镜名称。
            muzzle (str): 枪口配件名称。
            grip (str): 握把名称。
            butt (str): 枪托名称。
        """
        self.name = name
        self.para_range = []  # 记录每发子弹的下压幅度
        self.posture_states = [1.0]  # 姿势对压枪的系数，站立默认为1.0
        self.parts = [mirror, muzzle, grip, butt]  # 配件列表
        self.k = 1.0  # 配件压枪的总系数，由所有配件系数累乘得到
        self.interval = 0  # 每发射击的间隔时间（毫秒）
        self.maxBullets = 0  # 弹匣最大子弹数量
        self.single = False  # 是否为单发模式的枪械

        # 如果枪械名称有效，则从配置文件加载数据
        if name and name != 'None':
            try:
                # 使用 codecs 打开文件以支持中文编码
                with codecs.open("./枪械数据/game.json", "r", "utf-8") as f:
                    game_data = json.load(f)
                    gun_data = game_data['list'][name]

                    self.name = gun_data['name']
                    self.maxBullets = gun_data['maxBullets']
                    self.single = gun_data['single']
                    self.interval = gun_data['speed']
                    self.para_range = gun_data['ballistic']
                    
                    # 特殊处理M762，因为它可能有独特的压枪数据
                    if self.name == 'M762':
                        self.m762_zl = gun_data['m762_zl']

                    # 加载不同姿势下的压枪系数
                    self.posture_states.append(gun_data['posture']['squat'])
                    self.posture_states.append(gun_data['posture']['down'])

                    # 根据已装备的配件计算总的压枪系数k
                    if mirror and mirror != 'None':
                        self.k *= gun_data['mirror'].get(mirror, 1.0)
                    if muzzle and muzzle != 'None':
                        self.k *= gun_data['muzzle'].get(muzzle, 1.0)
                    if grip and grip != 'None':
                        self.k *= gun_data['grip'].get(grip, 1.0)
                    if butt and butt != 'None':
                        self.k *= gun_data['butt'].get(butt, 1.0)

            except (FileNotFoundError, KeyError, Exception) as e:
                print(f"加载枪械数据时出错：{type(e)} - {e}")

if __name__ == '__main__':
    # 示例用法
    # 创建一个 Gun 对象
    # akm = Gun(name='AKM', mirror='reddot', muzzle='compensator', grip='half', butt='none')
    # print(f"枪械名称: {akm.name}")
    # print(f"压枪系数: {akm.k}")
    pass