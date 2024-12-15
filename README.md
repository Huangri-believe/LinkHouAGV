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

pip install AGVlinhou

主要功能

 CreateTask(self,stationId,stationName,actionType = 0,) // 用于创建导航任务，stationId = 站台编号，stationName = 站台名称 actionType = 动作类型
 
 CancelTask(self,id) //取消任务，id = 任务编号
 
 GetState(self,id) // 获取机器人状态，id = 机器人编号
# 版本内容更新
###### v1.0.1:
1.增加了输入了机器人ID，便于调用不同机器人

    
