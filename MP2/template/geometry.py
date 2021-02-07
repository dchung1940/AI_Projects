# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.
        
        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position of the arm link, (x-coordinate, y-coordinate)
    """
    temp_x = math.cos(math.radians(angle))*length
    temp_y = math.sin(math.radians(angle))*length
    end_x = start[0] + temp_x
    end_y = start[1] - temp_y
    end = (end_x, end_y)
    return end

def doesArmTouchObstacles(armPos, obstacles):
    """Determine whether the given arm links touch obstacles

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            obstacles (list): x-, y- coordinate and radius of obstacles [(x, y, r)]

        Return:
            True if touched. False it not.
    """    
    for arm in armPos:
        start = arm[0]
        end = arm[1]
        for i in obstacles:
            C_x = i[0]
            C_y = i[1]

            vect_1 = [C_x - start[0],C_y - start[1]]
            vect_2 = [end[0]-start[0],end[1]-start[1]]
            seg_leng = vect_2[0]**2+vect_2[1]**2
            vect_dot = np.dot(vect_1,vect_2)
            proj_ = float(vect_dot)/seg_leng
            
            if(proj_<0):
                x_ = start[0]
                y_ = start[1]
            elif(proj_>1): 
                x_ = end[0]
                y_ = end[1]
            else:
                x_ = start[0] + float(proj_)*vect_2[0]
                y_ = start[1] + float(proj_)*vect_2[1]
            dist_x = C_x - x_
            dist_y = C_y - y_
            dist = math.sqrt(dist_x**2+dist_y**2)
            if(dist < i[2]):
                return True
    return False

def doesArmTouchGoals(armEnd, goals):
    """Determine whether the given arm links touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]

        Return:
            True if touched. False it not.
    """
    for i in goals:
        dist = (armEnd[0]-i[0])**2 + (armEnd[1]-i[1])**2
        if(dist<= (i[2])**2):
            return True
    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False it not.
    """
    window_x = window[0]
    window_y = window[1]

    for i in armPos:

        if i[1][0] > window_x or i[1][1] > window_y or i[1][0] <0 or i[1][1]<0 or i[0][0] > window_x or i[0][1] >window_y or i[0][0]<0 or i[0][1]<0:
            return False
    return True