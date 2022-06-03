1，新增文件GetUESenseImg.m、straightRoadVideoRecording.slx、straightRoadVideoRecording.slxc 放到ueGUI.mlapp 同级目录下
2，目前在GUI界面里加了一个“Render”按钮，看其回调函数即可知道传参方式，目前是用getParam获得的参数。其中图像尺寸2048是参考原有图片的。
3，Render读取编辑框中参数，并生成DriverSide.png 和 PassengerSide.png 两张图像。注意首次运行时间较长需要耐心等待一会儿，之后会快一些，速度与性能有关。
PS：请确认已经正确安装了UE4、Matlab Automated Driving Toolbox 、Matlab Computer Vision Toolbox（在附加功能->获取附加功能里下载）。