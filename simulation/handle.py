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