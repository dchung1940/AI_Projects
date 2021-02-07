
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    alpha = arm.getArmLimit()[0]
    beta = arm.getArmLimit()[1]
    
    # print("alpha:",alpha)
    # print("beta:",beta)

    rows = int((alpha[1]-alpha[0])/granularity+1)
    cols = int((beta[1]-beta[0])/granularity+1)
    
    # print("rows:",rows)
    # print("cols:",cols)
    curr_map = [[SPACE_CHAR]*cols for _ in range(rows)]    
    offsets = [alpha[0],beta[0]]
    start_angle = arm.getArmAngle()
    start_index = angleToIdx(start_angle, offsets, granularity)
    curr_map[start_index[0]][start_index[1]] = START_CHAR
    
    for i in range(rows):
        for j in range(cols):
            if(i==start_index[0] and j == start_index[1]):
                continue
            angle_set = idxToAngle([i,j],offsets,granularity)
            arm.setArmAngle(angle_set)
            curr_pos = arm.getArmPos()
            end_pos = arm.getEnd()
            
            if(not(isArmWithinWindow(curr_pos,window))):
                curr_map[i][j] = WALL_CHAR
            elif(doesArmTouchObstacles(curr_pos,obstacles)):
                curr_map[i][j] = WALL_CHAR
            elif(doesArmTouchGoals(end_pos,goals)):
                curr_map[i][j] = OBJECTIVE_CHAR
            elif(doesArmTouchObstacles(curr_pos,goals)):
                curr_map[i][j] = WALL_CHAR
            
            
    # print(curr_map)
    return Maze(curr_map,offsets,granularity)


# (70, 50, 15),
#                 (140, 30, 17),     
#                 (115, 75, 17)


