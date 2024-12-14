from linkhouWebSocketClient import LinkHouApi
import time

amr = LinkHouApi("ws://192.168.16.216:6001")
#print(amr.GetState())
#amr.CreateTask()
amr.CancelTask()
amr.close()
