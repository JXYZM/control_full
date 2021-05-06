#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from copy import deepcopy

def handle_flight_control(input, todo_list):
    for i in range(len(input["flights"])):
        flight_id = int(input["flights"][i]["flight_id"][4:])
        point_id = int(input["flights"][i]["point_id"])
        action = input["flights"][i]["action"]
        insert = int(input["flights"][i]["insert"])
        if len(todo_list[flight_id]) == 0:
            todo_list[flight_id].append({"point" : point_id, "action" : [action]})
        elif insert >= len(todo_list[flight_id]):
            if point_id != todo_list[flight_id][-1]["point"]:
                todo_list[flight_id].append({"point" : point_id, "action" : [action]})
            else:
                if "action" not in todo_list[flight_id][-1].keys():
                    todo_list[flight_id][-1]["action"] = [action]
                else:
                    todo_list[flight_id][-1]["action"].append(action)
        elif insert == 0:
            if point_id != todo_list[flight_id][0]["point"]:
                todo_list[flight_id] = todo_list[flight_id][0:insert] + [{"point" : point_id, "action" : [action]}] + todo_list[flight_id][insert:]
            else:
                if "action" not in todo_list[flight_id][0].keys():
                    todo_list[flight_id][0]["action"] = [action]
                else:
                    todo_list[flight_id][0]["action"].append(action)
        else:
            if point_id == todo_list[flight_id][insert-1]["point"]:
                if "action" not in todo_list[flight_id][insert-1].keys():
                    todo_list[flight_id][insert-1]["action"] = [action]
                else:
                    todo_list[flight_id][insert-1]["action"].append(action)
            elif point_id == todo_list[flight_id][insert]["point"]:
                if "action" not in todo_list[flight_id][insert].keys():
                    todo_list[flight_id][insert]["action"] = [action]
                else:
                    todo_list[flight_id][insert]["action"].append(action)
            else:
                todo_list[flight_id] = todo_list[flight_id][0:insert] + [{"point": point_id, "action": [action]}] + todo_list[flight_id][insert:]

    return deepcopy(todo_list)



def handle_mission_control(input, tdl, mb, mall, cost):
    for i in range(len(input["missions"])):
        mission_id = int(input["missions"][i]["mission_id"][2:])
        mission = mall[mission_id]
        pt = -1
        for j in range(len(mb)):
            if mission in mb[j]:
                pt = j
                break
        mb[pt].remove(mission)
        for j in range(len(tdl[pt])):
            if tdl[pt][j]["point"] == mission[1]:
                if "get" in tdl[pt][j].keys():
                    if mission_id in tdl[pt][j]["get"]:
                        tdl[pt][j]["get"].remove(mission_id)
                        if len(tdl[pt][j]["get"]) == 0:
                            tdl[pt][j].pop("get")
            elif tdl[pt][j]["point"] == mission[2]:
                if "put" in tdl[pt][j].keys():
                    if mission_id in tdl[pt][j]["put"]:
                        tdl[pt][j]["put"].remove(mission_id)
                        if len(tdl[pt][j]["put"]) == 0:
                            tdl[pt][j].pop("put")

    return deepcopy(tdl), deepcopy(mb)