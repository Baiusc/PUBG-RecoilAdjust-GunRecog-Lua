# PUBGRecognizeAndGunpress

# 注意
- 本项目的配件识别是基于截取屏幕固定位置识别的，受限于开发条件，只适配于2560*1440的屏幕
- 请先安装好LGS_9.02.65_x64_Logitech.exe。（实测只安装最新版GHUB也可行）因为压枪是基于调用罗技鼠标驱动实现的（即使你的鼠标不是罗技的也没有关系）
- 最好使用简体中文界面，否则有少数枪械无法识别
- 没做图形界面（感觉也不需要）

# 如何打包为可执行程序.exe
1. 执行pyinstaller monitor.py -p dataload.py -p ghub.py -p gun_press.py -p recognize.py -p ghub_device.dll
2. 把“ghub_device.dll”，“枪械数据”文件夹,“picture”文件夹放到上一步生成的dist/monitor目录中

# 如何调试代码
执行monitor.py的if __name__=='__main__'

# 环境
```bash
# powershell开启管理员
Start-Process powershell -Verb runAs
```

```bash
# 将 PUBG 环境导出为.yml文件
conda env export -n PUBG > PUBG.yml

# 使用.yml文件创建 PUBG 环境
conda env create -f ./PUBG.yml

# 激活环境（已配置vscode/config文件，终端自动激活环境）
conda activate PUBG

# 安装py依赖
pip install -r ./requirements.txt

```

# 弹道表调试方向：
方向1：开火时，捕获鼠标位移量（像素） 
方向2：使用士兵76宏进行弹道调试

# 76 弹道表
```lua
pubg["Beryl M762"] = function (gunName)

	return pubg.execOptions(gunName, {
		interval = 86,
		ballistic = {
			{1, 0},
			{2, 44},
			{3, 24},
			{5, 28},
			{10, 33},
			{15, 45},
			{30, 47},
			{40, 51},
		}
	})

end
pubg["AKM"] = function (gunName)

	return pubg.execOptions(gunName, {
		interval = 99,
		ballistic = {
			{1, 0},
			{2, 42},
			{5, 25},
			{10, 32},
			{40, 40},
		}
	})

end

pubg["M416"] = function (gunName)

	return pubg.execOptions(gunName, {
		interval = 85,
		ballistic = {
			{1, 0},
			{2, 35},
			{4, 18},
			{10, 24},
			{15, 32},
			{30, 30},
			{40, 37},
		}
	})

end
```




