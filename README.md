# 项目介绍
    本项目是对灵猴底盘API调用所建立的。
    可以通过WebSocket协议对底盘进行操控
 
# 环境依赖
    见requirement.txt文件
 
# 目录结构描述
    ├── ReadMe.md           // 帮助文档
    
    ├── example.py    // 测试底盘的python文件
    
    ├── linkhouWebSocketClient.py    // 包含WebSocket连接以及底盘API调用的接口
 
# 使用说明
使用pip安装

pip install AGVlinkhou

主要功能

 CreateTask(self,stationnumber) // 用于创建导航任务，stationnumber 需要前往的站台数量，之后根据提示输入站台编号
 
 CancelTask(self,id) //取消任务，id = 任务编号
 
 GetState(self,id) // 获取机器人状态，id = 机器人编号

 仅适用于内部的机器人
# 版本内容更新
###### v1.0.1:
1.增加了输入了机器人ID，便于调用不同机器人
###### v1.0.3:
1.修改了创建导航任务的逻辑，现在可以前往多个导航点，并且选择是否需要循环操作

    
