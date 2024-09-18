import os
import sys
print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from socket_config import *
from vehicleControl import *
from sceneInfo import *
import config

sceneInfoOutputGap = config.sceneInfoOutputGap

def algorithm(apiList, vehicleControl1):
    control_velocity = 0
    control_steer = 0
    # 自动驾驶模式
    # pos_x, pos_y, pos_yaw, pose_v = LqrController.lqrControl(4, [curPose['posX']], [curPose['posY']])
    # for i in range(len(pos_x)): # 判断路径列表中与当前位置最近的元素
    #     if i < len(pos_x) - 1: # 防止溢出
    #         if math.sqrt(math.pow(pos_x[i] - curPose['posX'] ,2) +
    #                               math.pow(pos_y[i] - curPose['posY'], 2)) < \
    #                 math.sqrt(math.pow(pos_x[i + 1] - curPose['posX'] , 2) +
    #                                    math.pow((pos_y[i + 1] -curPose['posY']), 2)):
    #             control_steer = pos_yaw[i]
    #             control_brake = pose_v[i]
    #     else: # 最后一位
    #         control_steer = pos_yaw[-1]
    #         control_brake = pose_v[-1]
    # vehicleControl1.__steeringSet__(control_steer, yaw=curPose['oriZ'])
    # vehicleControl1.__throttleSet__(control_brake, speed=math.sqrt(
    #     math.pow(curPose['posX'], 2) + math.pow(curPose['posY'], 2)))
    # vehicleControl1.__brakeSet__(control_brake, speed=math.sqrt(
    #     math.pow(curPose['posX'], 2) + math.pow(curPose['posY'], 2)))

    # 手操模式
    vehicleControl1.__keyboardControl__()

    control_dict_demo = json_encoder(vehicleControl1)
    control_dict_demo = json.dumps(control_dict_demo)

    return control_dict_demo


def main():
    loop_counter = 0
    vehicleControl1 = vehicleControlAPI(0, 0, 0)  # 控制初始化
    socketServer = SocketServer()
    socketServer.socket_connect()

    while True:
        dataState, apiList = socketServer.socket_launch()
        if dataState:
            if apiList != None:
                if loop_counter % sceneInfoOutputGap == 1:
                    print("\n\nInfo begin:")
                    apiList.showAllState()
                    print("gear mode: ", vehicleControl1.gear)

        if dataState and loop_counter == 0:
            socketServer.socket_respond()

        elif dataState and apiList != None and apiList.messageState() and loop_counter != 0:

            roadLine = RoadLine()
            roadLineList = roadLine.trajvisualization(apiList.trajListAPI())
            vehicleControl1.__pathVisualizationSet__(roadLineList[1], roadLineList[2],
                                                     roadLineList[1], roadLineList[2])

            control_dict_demo = algorithm(apiList, vehicleControl1)
            control_dict_demo += "|end"
            socketServer.socket_send(control_dict_demo)
        loop_counter += 1


if __name__ == "__main__":
    main()

