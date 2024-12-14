import websocket
import json
import rel
import threading
import time
import socket
import re
import requests



class LinkHouWebSocketClient:
    def __init__(self, url, debug=False):
        self.subscription_events = {}
        self.subscription_data = {}
        self.subscription_lock = threading.Lock()
        self.thread = None
        self.url = url
        self.ws_request = None
        self.ws_subscribe = None
        self.subscriptions = {}
        self.debug = debug
        # websocket.enableTrace(self.debug)

    @staticmethod
    def on_open(ws):
        print("WebSocket connection opened")

    def on_message(self, ws, message):
        message = json.loads(message)
        sn_num = message.get("sn")
        if sn_num is not None:
            with self.subscription_lock:
                self.subscription_data[sn_num] = message
                self.subscription_events[sn_num].set()
        else:
            self.exec_callback(message["type"], message)

    def exec_callback(self, message_type, message):
        """执行回调函数
        """
        with self.subscription_lock:
            if message_type in self.subscriptions:
                try:
                    self.subscriptions[message_type](message)
                except Exception as e:
                    print(f"Error executing callback for {message_type}: {e}")

    @staticmethod
    def on_error(ws, error):
        print(f"WebSocket error: {error}")

    @staticmethod
    def on_close(ws, close_status, close_msg):
        print("WebSocket connection closed")

    def connect(self):
        self.close()
        self.ws_subscribe = websocket.WebSocketApp(self.url,
                                                   on_open=self.on_open,
                                                   on_message=self.on_message,
                                                   on_error=self.on_error,
                                                   on_close=self.on_close)

        self.ws_request = websocket.WebSocketApp(self.url,
                                                 on_open=self.on_open,
                                                 on_message=self.on_message,
                                                 on_error=self.on_error,
                                                 on_close=self.on_close)

        # 后台 rel 调度执行
        self.ws_subscribe.run_forever(dispatcher=rel, reconnect=10)
        self.ws_request.run_forever(dispatcher=rel, reconnect=10)
        self.thread = threading.Thread(target=rel.dispatch)
        self.thread.start()

    def close(self):
        if self.ws_subscribe:
            self.ws_subscribe.close()
        if self.ws_request:
            self.ws_request.close()
        if self.thread:
            rel.abort()
            self.thread.join()

    def reconnect_test(self):
        match = re.match(r'ws://(\d+\.\d+\.\d+\.\d+):(\d+)/', self.url)
        ip_address = match.group(1)
        port = int(match.group(2))
        try:
            s = socket.create_connection((ip_address, port), timeout=5)
            s.close()
            print(f"Connection to {ip_address}:{port} successful.")
            return True
        except socket.error as e:
            print(f"Error connecting to {ip_address}:{port}: {e}")
            return False

    def add_topic_callback(self, message_type: str, cb_func):
        """添加话题回调函数
        """
        with self.subscription_lock:
            self.subscriptions[message_type] = cb_func

    def submit_subscriptions(self):
        """发送订阅请求
        """
        msg = {
            "type": "woosh.Subscription",
            "body": {
                "sub": True,
                "topics": list(self.subscriptions.keys())
            }
        }
        self.ws_subscribe.send(json.dumps(msg))

    def remove_topic_callback(self, message_type):
        """移除话题回调函数
        """
        with self.subscription_lock:
            if message_type in self.subscriptions:
                del self.subscriptions[message_type]

class LinkHouApi(LinkHouWebSocketClient):
    def __init__(self, url, debug=False):
        super().__init__(url, debug)
        self.connect()

    # =================================================
    # 机器人信息相关
    # =================================================

    #获取机器人状态
    def GetState(self):
        url = "http://192.168.16.216:6002/api/AMR/GetState"
        payload = json.dumps({
            "id": 5
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #获取地图信息
    def GetFloorMap(self):
        url = "http://192.168.16.216:6002/api/Map/GetFloorMap"

        payload = json.dumps({
            "id": 5,
            "floorId": 1,
            "mapType": 0
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
    #暂停行走
    def PauseWalk(self):
        url = "http://192.168.16.216:6002/api/AMR/PauseWalk"

        payload = json.dumps({
            "id": 5
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #继续行走
    def ContinueWalk(self):
        url = "http://192.168.16.216:6002/api/AMR/ContinueWalk"
        payload = json.dumps({
            "id": 5
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #设置为自动模式
    def SetAutoMode(self):
        url = "http://192.168.16.216:6002/api/AMR/SetAutoMode"
        payload = json.dumps({
            "id": 5
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #设置为手动模式
    def SetManualMode(self):
        url = "http://192.168.16.216:6002/api/AMR/SetManualMode"
        payload = json.dumps({
            "id": 5
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #复位
    def Reset(self):
        url = "http://192.168.16.216:6002/api/AMR/Reset"
        payload = json.dumps({
            "id": 5
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #设置灯光
    def SetLighting(self):
        url = "http://192.168.16.216:6002/api/AMR/SetLighting"
        payload = json.dumps({
            "id": 212,
            "mode": 2,
            "frequency": 5,
            "color": [
               255,
               0,
               0
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #获取音乐列表
    def GetAllMusic(self):
        url = "http://192.168.16.216:6002/api/AMR/GetAllMusic"
        payload = json.dumps({
            "id": 5
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #AMR传感器校准
    def Calibration(self):
        url = "http://192.168.16.216:6002/api/AMR/Calibration"
        payload = json.dumps({
            "id": 5
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #播报指定音乐
    def PlayMusic(self):
        url = "http://192.168.16.216:6002/api/AMR/PlayMusic"
        payload = json.dumps({
            "id": 5
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #重定位接口
    def Relocation(self):
        url = "http://192.168.16.216:6002/api/AMR/Relocation"
        payload = json.dumps({
            "id": 0,
            "x": 0,
            "y": 0,
            "z": 0,
            "angle": 0
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #语音播报接口
    def TextSpeach(self):
        url = "http://192.168.16.216:6002/api/AMR/TextSpeach"
        payload = json.dumps({
            "id": 5 ,
            "text": "你好"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #取消任务接口
    def CancelTask(self):
        url = "http://192.168.16.216:6002/api/Task/CancelTask"
        payload = json.dumps({
            "id": 10058
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    #创建任务接口
    def CreateTask(self):
        url = "http://192.168.16.216:6002/api/Task/CreateTask"
        payload = json.dumps({
            "sourceId": "string",
            "taskNum": "string",
            "mapId": 0,
            "agvTypeId": 0,
            "agvId": 0,
            "stationList": [
                {
                    "stationId": 10012,
                    "actionType": 0,
                    "agvBufferIndex": 1,
                    "stationBufferIndex": 1,
                    "actionParam": 0,
                    "stationName": "charge_area_2F"
                }

            ],
            "priority": 0,
            "maxLoopTimes": 1
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)