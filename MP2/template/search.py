# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod, [])(maze)

def bfs(maze):

    rows,cols = maze.getDimensions()
    queue = []
    start = maze.getStart()
    queue.append(start)
    visited = {}
    visited[start] = 0 
    answer = []
    while queue:
        temp = queue.pop(0)
        for i in maze.getNeighbors(temp[0],temp[1]):
            if i not in visited:
                queue.append(i)
                visited[i] = temp
                
        if(temp in maze.getObjectives()):
            while temp != 0:
                answer.append(temp)
                temp = visited[temp]

            answer.reverse()
            return answer,0
    return answer,0

    # rows,cols = maze.getDimensions()
    # visited = [[False]*cols for _ in range(rows)];
    # queue = [];
    # Dict_list = {}
    # start_row, start_col = maze.getStart();
    # answer = []
    # final = maze.getObjectives();
    # queue.append(maze.getStart())
    # visited[start_row][start_col] = True;
    
    #getneighbor function not working... different boundary condition

    # while queue:
    #     temp = queue.pop(0)
    #     neigh = maze.getNeighbors(temp[0],temp[1])
    #     for i in neigh:
    #         if visited[i[0]][i[1]]==False :
    #             queue.append(i)
    #             Dict_list[i] = temp;
    #             visited[i[0]][i[1]] = True;
    #         if i in final:
    #             answer.append(i)
    #             y = Dict_list[i]
    #             while(maze.getStart() != y):
    #                 answer.append(y)
    #                 y = Dict_list[y]
    #             answer.append(maze.getStart())
    #             answer.reverse()
    #             return answer

def dfs(maze):
    # TODO: Write your code here    
    return [], 0

def greedy(maze):
    # TODO: Write your code here    
    return [], 0

def astar(maze):
    # TODO: Write your code here    
    return [], 0

