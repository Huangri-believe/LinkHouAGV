from linkhouWebSocketClient import LinkHouApi
import time

amr = LinkHouApi("ws://192.168.16.216:6001")

#print(amr.GetState(id = 5))
amr.CreateTask(stationnumber=2)
#amr.GetAllTask()
#amr.CancelTask()
amr.close()

