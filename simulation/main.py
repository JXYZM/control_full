#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
main.py
simulation module
'''
# import socket
import json
# from multiprocessing import Process
from flask import Flask
from flask import request
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources=r'/*')

from copy import deepcopy
from flight import Flight
import math

NUM_OF_FLIGHT = 3
SPEED_OF_FLIGHT = 7.5
NUM_OF_POINT = 30

POINT = {}
DIST = []
FLIGHT = {}

MISSION_ALL = []
MISSION_A = []
MISSION_B = []
TODO_LIST = []
POSITION = []
CURRENT_COST = []

def init_center():
    global MISSION_ALL
    global MISSION_A
    global MISSION_B
    global TODO_LIST
    global POSITION
    global CURRENT_COST
    # global PATH
    # for i in range(NUM_OF_FLIGHT):
    #     MISSION_A.append([])
    #     MISSION_B.append([])
    #     TODO_LIST.append([])
    #     POSITION.append([118958877.0, 32114745.0])
    #     CURRENT_COST.append(0.0)
    MISSION_ALL.append([0, 3, 10, 42])
    MISSION_ALL.append([1, 22, 5, 39])
    MISSION_ALL.append([2, 10, 5, 60])
    MISSION_ALL.append([3, 17, 14, 37])
    MISSION_ALL.append([4, 4, 24, 44])
    MISSION_ALL.append([5, 14, 24, 53])
    MISSION_ALL.append([6, 6, 13, 51])
    MISSION_ALL.append([7, 27, 20, 46])
    MISSION_ALL.append([8, 13, 20, 56])
    MISSION_A.append([[0, 3, 10, 42], [1, 22, 5, 39]])
    MISSION_A.append([[3, 17, 14, 37], [4, 4, 24, 44]])
    MISSION_A.append([[6, 6, 13, 51], [7, 27, 20, 46]])
    MISSION_B.append([[2, 10, 5, 60]])
    MISSION_B.append([[5, 14, 24, 53]])
    MISSION_B.append([[8, 13, 20, 56]])
    TODO_LIST.append([{"point": 10, "todo": {"put": [0], "get": [2]}}, {"point": 5, "todo": {"put": [1, 2]}}])
    TODO_LIST.append([{"point": 14, "todo": {"put": [3], "get": [5]}}, {"point": 24, "todo": {"put": [4, 5]}}])
    TODO_LIST.append([{"point": 13, "todo": {"put": [6], "get": [8]}}, {"point": 20, "todo": {"put": [7, 8]}}])
    for i in range(NUM_OF_FLIGHT):
        POSITION.append([118958877.0, 32114745.0])
        CURRENT_COST.append(0.0)

def initialize_point():
    global POINT
    f = open("data/point.txt")
    lines = f.read().splitlines()
    for line in lines:
        temp = line.split(" ")
        POINT[int(temp[0])] = [float(temp[1]), float(temp[2])]
    f.close()

def initialize_dist():
    global DIST
    DIST = [[float(0) for i in range(NUM_OF_POINT)] for j in range(NUM_OF_POINT)]
    f = open("data/route.txt")
    lines = f.read().splitlines()
    for line in lines:
        temp = line.split(" ")
        DIST[int(temp[0])][int(temp[1])] = float(temp[2])
        DIST[int(temp[1])][int(temp[0])] = float(temp[2])
    f.close()

def initialize_flight():
    global FLIGHT
    for i in range(NUM_OF_FLIGHT):
        FLIGHT[i] = Flight(deepcopy(POINT), deepcopy(DIST), deepcopy(MISSION_A[i]))
        FLIGHT[i].update_from_center(deepcopy(MISSION_B[i]), deepcopy(TODO_LIST[i]))

def load_file():
    initialize_point()
    initialize_dist()
    initialize_flight()

def generate_distance(position):
    cost = {}
    # current point & N points --> N+1 * N+1
    len_of_content = NUM_OF_POINT + 1
    for i in range(NUM_OF_FLIGHT):
        content = [[float(0) for j in range(len_of_content)] for k in range(len_of_content)]
        # 0 vs 1-N
        for j in range(1, len_of_content):
            c = math.sqrt(pow(position[i][0] - POINT[j-1][0], 2) + pow(position[i][1] - POINT[j-1][1], 2)) / SPEED_OF_FLIGHT
            content[0][j] = c
            content[j][0] = c
        # 1-N * 1-N
        for j in range(1, len_of_content):
            for k in range(j+1, len_of_content):
                c = DIST[j-1][k-1] / SPEED_OF_FLIGHT
                content[j][k] = c
                content[k][j] = c
        cost[i] = content
    return deepcopy(cost)

def generate_cost_current(content, flight_id):
    # current todo_list = []
    if len(TODO_LIST[flight_id]) == 0:
        return 0.0
    else:
        # route time
        time_all = 0
        # mission time
        cost_all = 0
        for i in range(len(TODO_LIST[flight_id])):
            point_id = TODO_LIST[flight_id][i]["point"]
            if i == 0:
                # current position to point 0
                time_all += content[0][point_id + 1]
            else:
                # point i-1 to point i
                time_all += content[TODO_LIST[flight_id][i - 1]["point"] + 1][point_id + 1]
            # cost += flight_time * num_of_mission(finished now)
            if "put" in TODO_LIST[flight_id][i]["todo"].keys():
                cost_all += time_all * len(TODO_LIST[flight_id][i]["todo"]["put"])
        return cost_all

@app.route('/dev/', methods=['POST'])
def handle_client():
    tmp = request.get_data()
    tmp = tmp.decode("utf-8")
    if tmp[0] == "-":
        pass
    else:
        input_from_ui = json.loads(tmp)
        print(input_from_ui)
        if input_from_ui["type"] == 0:
            for i in range(NUM_OF_FLIGHT):
                POSITION[i] = FLIGHT[i].get_position(1)
                MISSION_A[i], MISSION_B[i], TODO_LIST[i] = FLIGHT[i].update_mission_todolist()
                FLIGHT[i].update_from_center(deepcopy(MISSION_B[i]), deepcopy(TODO_LIST[i]))
            cost = generate_distance(deepcopy(POSITION))
            for i in range(NUM_OF_FLIGHT):
                CURRENT_COST[i] = generate_cost_current(deepcopy(cost[i]), i)
                #print("n: {} | p: {} | a: {} | b: {} | t: {} | c: {}".format(n, POSITION[i], MISSION_A[i], MISSION_B[i], TODO_LIST[i], CURRENT_COST[i]))
            flight_info = []
            for i in range(NUM_OF_FLIGHT):
                tmp = {}
                tmp["header"] = str(i) + "号无人机状态"
                tmp["key"] = str(i)
                tmp["id"] = "uav " + str(i)
                tmp["position"] = "{:.4f} , {:.4f}".format(POSITION[i][0] / 1000000, POSITION[i][1] / 1000000)
                if (len(MISSION_A[i]) + len(MISSION_B[i])) > 0:
                    tmp["status"] = ["running", "processing"]
                else:
                    tmp["status"] = ["finished", "success"]
                tmp["battery"] = "100 %"
                tmp["ma"] = ""
                for j in range(len(MISSION_A[i])):
                    tmp["ma"] += str(MISSION_A[i][j][0])
                    if j < len(MISSION_A[i]) - 1:
                        tmp["ma"] += " , "
                tmp["mb"] = ""
                for j in range(len(MISSION_B[i])):
                    tmp["mb"] += str(MISSION_B[i][j][0])
                    if j < len(MISSION_B[i]) - 1:
                        tmp["mb"] += " , "
                tmp["list"] = ""
                for j in range(len(TODO_LIST[i])):
                    tmp["list"] += " -> " + str(TODO_LIST[i][j]["point"]) + " : "
                    tmp["list"] += "( "
                    if "put" in TODO_LIST[i][j]["todo"].keys():
                        tmp["list"] += "put : "
                        for k in range(len(TODO_LIST[i][j]["todo"]["put"])):
                            tmp["list"] += str(TODO_LIST[i][j]["todo"]["put"][k]) + " "
                    if "get" in TODO_LIST[i][j]["todo"].keys():
                        tmp["list"] += "get : "
                        for k in range(len(TODO_LIST[i][j]["todo"]["get"])):
                            tmp["list"] += str(TODO_LIST[i][j]["todo"]["get"][k]) + " "
                    tmp["list"] += ")"
                tmp["load"] = str(len(MISSION_A[i]) + len(MISSION_B[i]))
                tmp["cost"] = "{:.2f}".format(CURRENT_COST[i])
                flight_info.append(deepcopy(tmp))
            #print(flight_info)
            mi_tf = {}
            mi_ts = {}
            for i in range(NUM_OF_FLIGHT):
                for j in range(len(MISSION_A[i])):
                    mi_tf[MISSION_A[i][j][0]] = i
                for j in range(len(MISSION_B[i])):
                    mi_ts[MISSION_B[i][j][0]] = i
            mission_info = []
            for i in range(len(MISSION_ALL)):
                tmp = {}
                tmp["header"] = str(MISSION_ALL[i][0]) + "号任务状态"
                tmp["key"] = str(i)
                tmp["id"] = "m " + str(MISSION_ALL[i][0])
                tmp["des"] = "time_stamp : " + str(MISSION_ALL[i][3]) + "  |  "
                tmp["des"] += "from " + str(MISSION_ALL[i][1]) + " to " + str(MISSION_ALL[i][2])
                tmp["status"] = ["", ""]
                if MISSION_ALL[i][0] in mi_tf.keys():
                    tmp["status"][0] = " to_finish" + " | " + "taken by uav " + str(mi_tf[MISSION_ALL[i][0]])
                    tmp["status"][1] = "processing"
                elif MISSION_ALL[i][0] in mi_ts.keys():
                    tmp["status"][0] = " to_start" + " | " + "taken by uav " + str(mi_ts[MISSION_ALL[i][0]])
                    tmp["status"][1] = "processing"
                else:
                    tmp["status"][0] = " finished "
                    tmp["status"][1] = "success"
                mission_info.append(tmp)
            print(mission_info)
            response_body = json.dumps({"todo_list": TODO_LIST, "position": POSITION, "flight_info": flight_info, "mission_info": mission_info})
            return response_body
        if input_from_ui["type"] == 1:
            message = ""
            for i in range(len(input_from_ui["flights"])):
                message += input_from_ui["flights"][i]["flight_id"]
                if i < len(input_from_ui["flights"]) - 1:
                    message += ", "
            message += " 的动作配置信息已送达"
            response_body = json.dumps({"message": message})
            return response_body
        if input_from_ui["type"] == 2:
            message = ""
            for i in range(len(input_from_ui["missions"])):
                message += input_from_ui["missions"][i]["mission_id"]
                if i < len(input_from_ui["missions"]) - 1:
                    message += ", "
            message += " 的调整信息已送达"
            response_body = json.dumps({"message": message})
            return response_body

if __name__ == '__main__':
    init_center()
    load_file()
    app.run(host='0.0.0.0', port=7000, debug=False)
