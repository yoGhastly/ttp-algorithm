import numpy as np
import re


def load(name):

    file_name=name
    file_path = 'data/'
    file_path += file_name
    file_object  = open(file_path,'r')
    file_lines = file_object.readlines()

    basic_info ={
      "problem name": "problem",
      "KNP data type": "data type",
      "dimensions": 0,
      "number of items": 0,
      "KNP cap": 0,
      "min speed": 0,
      "max speed": 0,
      "renting ratio": 0,
      "edge weight": 0,

    }
    #Merge list items into one string
    def appender(list):
        result=""
        for x in range(list.__len__()-1):
            result+= list[x] +" "
        result+=list[list.__len__()-1]
        return result


    # Basic data
    for x in range(9):
        if re.search("PROBLEM NAME:", file_lines[x]):
            basic_info["problem name"]=file_lines[x].split()[2]
        elif re.search("KNAPSACK DATA TYPE:",file_lines[x]):
            basic_info["KNP data type"]= appender(file_lines[x].split()[3:])
        elif re.search("DIMENSION:", file_lines[x]):
            basic_info["dimensions"] = float(file_lines[x].split()[1])
        elif re.search("NUMBER OF ITEMS:", file_lines[x]):
            basic_info["number of items"] = float(file_lines[x].split()[3])
        elif re.search("CAPACITY OF KNAPSACK:", file_lines[x]):
            basic_info["KNP cap"] = float(file_lines[x].split()[3])
        elif re.search("MIN SPEED:", file_lines[x]):
            basic_info["min speed"] = float(file_lines[x].split()[2])
        elif re.search("MAX SPEED:", file_lines[x]):
            basic_info["max speed"] = float(file_lines[x].split()[2])
        elif re.search("RENTING RATIO:", file_lines[x]):
            basic_info["renting ratio"] = float(file_lines[x].split()[2])
        elif re.search("EDGE_WEIGHT_TYPE:", file_lines[x]):
            basic_info["edge weight"] = file_lines[x].split()[1]


    # Node cords
    nodes=[]
    last_node_index=10
    for x in range(10,file_lines.__len__()):
        if(re.search("ITEMS SECTION",file_lines[x])):
            break
        nodes.append(file_lines[x])
        last_node_index +=1

    # Item info
    items=[]
    for x in range(last_node_index+1,file_lines.__len__()):
        items.append(file_lines[x])

    #Transforming into np array:

    #Nodes
    nodes_arr=np.zeros(shape=[nodes.__len__(),3])
    for x in range(0,nodes.__len__()):
       node_data=(re.sub('/t',' ', nodes[x]).split())
       for y in range(node_data.__len__()):
                node_data[y]=float(node_data[y])
       nodes_arr[x]=node_data

    #Items
    items_arr=np.zeros(shape=[items.__len__(),4])
    for x in range(0,items.__len__()):
        item_data=items[x].split()
        for y in range(item_data.__len__()):
           item_data[y]=int(item_data[y])
        items_arr[x]=item_data

    return (basic_info,nodes_arr.astype(int),items_arr.astype(int))