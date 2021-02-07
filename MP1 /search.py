# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018


"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "astar": astar,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)


def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    rows,cols = maze.getDimensions()
    visited = [[False]*cols for _ in range(rows)];
    # print(visited)
    # print(rows," ", cols)
    queue = [];
    Dict_list = {}
    start_row, start_col = maze.getStart();
    # print(start_row,start_col)
    answer = []
    final = maze.getObjectives();
    # print(final)
    queue.append(maze.getStart())
    visited[start_row][start_col] = True;
    # print(visited)
    while queue:
        temp = queue.pop(0)
        # print("root",temp)
        neigh = maze.getNeighbors(temp[0],temp[1])
        # print("neighbors",neigh)
        for i in neigh:
            # print("current neighbor",i)
            # print("boolean",visited[i[0]][i[1]])
            if visited[i[0]][i[1]]==False :
                queue.append(i)
                Dict_list[i] = temp;
                visited[i[0]][i[1]] = True;
                # print ("current queue",queue)

            if i in final:
                answer.append(i)
                # print(i)
                # print(temp)
                y = Dict_list[i]
                # print(y)
                while(maze.getStart() != y):
                    # print(y)
                    answer.append(y)
                    y = Dict_list[y]
                # print(answer)
                answer.append(maze.getStart())
                answer.reverse()
                return answer





def dfs(maze):
    """
    Runs DFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    rows,cols = maze.getDimensions()
    visited = [[False]*cols for _ in range(rows)];
    # print(visited)
    # print(rows," ", cols)
    stack = [];
    Dict_list = {}
    start_row, start_col = maze.getStart();
    # print(start_row,start_col)
    answer = []
    final = maze.getObjectives();
    # print(final)
    stack.append(maze.getStart())
    visited[start_row][start_col] = True;
    # print(visited)
    while stack:
        temp = stack.pop(-1)
        # print("root",temp)
        neigh = maze.getNeighbors(temp[0],temp[1])
        # print("neighbors",neigh)
        for i in neigh:
            # print("current neighbor",i)
            # print("boolean",visited[i[0]][i[1]])
            if visited[i[0]][i[1]]==False :
                stack.append(i)
                Dict_list[i] = temp;
                visited[i[0]][i[1]] = True;
                # print ("current queue",queue)

            if i in final:
                answer.append(i)
                # print(i)
                # print(temp)
                y = Dict_list[i]
                # print(y)
                while(maze.getStart() != y):
                    # print(y)
                    answer.append(y)
                    y = Dict_list[y]
                # print(answer)
                answer.append(maze.getStart())
                answer.reverse()
                return answer


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    rows,cols = maze.getDimensions()
    start_row,start_col = maze.getStart()
    fin_row,fin_col = maze.getObjectives()[0];
    g_score = [[float("inf")]*cols for _ in range(rows)]
    h_score = [[float("inf")]*cols for _ in range(rows)]
    f_score = [[float("inf")]*cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            h_score[i][j]= Manhattan(i,j,fin_row,fin_col)
    g_score[start_row][start_col] = 0;
    f_score[start_row][start_col] = h_score[start_row][start_col]
    Dict_list = {}
    answer = []
    open_list = [(f_score[start_row][start_col],maze.getStart())]
    closed_set = []
    val_list = [maze.getStart()]
    while open_list:
        temp = min(open_list)[1]
        open_list.remove(min(open_list))
        val_list.remove(temp)
        neigh = maze.getNeighbors(temp[0],temp[1])
        closed_set.append(temp)
        for i in neigh:
            g_temp = g_score[temp[0]][temp[1]]+1
            if(i not in closed_set):
                if(g_temp < g_score[i[0]][i[1]]):
                    g_score[i[0]][i[1]] = g_temp
                    f_score[i[0]][i[1]] = h_score[i[0]][i[1]] + g_temp
                    Dict_list[i] = temp;
                    if (i not in val_list):
                        val_list.append(i)
                        open_list.append((f_score[i[0]][i[1]],i))
                    if i in maze.getObjectives():
                        answer.append(i)
                        y = Dict_list[i]
                        while(maze.getStart() != y):
                            answer.append(y)
                            y = Dict_list[y]
                        answer.append(maze.getStart())
                        answer.reverse()
                        return answer
    return []

def Manhattan(x,y,goal_x,goal_y):
    h = abs(x-goal_x)+abs(y-goal_y)
    return h

def astar_multi(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    rows,cols = maze.getDimensions()
    fin_answer=[]
    final = maze.getObjectives()
    rows,cols = maze.getDimensions()
    start_row,start_col = maze.getStart()
    # print(start_row, " ",start_col)
    while final:
    # for i in range(5):
        # print("final:",final)
        Manh_dis = []
        for i in final:
            val = Manhattan(i[0],i[1],start_row,start_col)
            Manh_dis.append((val,i))
        # print("Manh_dis:",Manh_dis)
        final_ = min(Manh_dis)
        fin_row,fin_col = final_[1];
        final.remove(final_[1])
        Manh_dis.remove(final_)

        fin_answer = fin_answer + astar_(maze,start_row,start_col,fin_row,fin_col)

        start_row,start_col = final_[1]
    #fin_answer.reverse()
    # print (fin_answer)

    fin_answer.append(maze.getStart())
    fin_answer.reverse()
    return fin_answer

def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    rows,cols = maze.getDimensions()
    fin_answer=[]
    final = maze.getObjectives()
    rows,cols = maze.getDimensions()
    start_row,start_col = maze.getStart()
    # print(start_row, " ",start_col)
    while final:
    # for i in range(5):
        # print("final:",final)
        Manh_dis = []
        for i in final:
            val = Manhattan(i[0],i[1],start_row,start_col)
            Manh_dis.append((val,i))
        # print("Manh_dis:",Manh_dis)
        final_ = min(Manh_dis)
        fin_row,fin_col = final_[1];
        final.remove(final_[1])
        Manh_dis.remove(final_)

        fin_answer = fin_answer + astar_(maze,start_row,start_col,fin_row,fin_col)

        start_row,start_col = final_[1]
    #fin_answer.reverse()
    # print (fin_answer)

    fin_answer.append(maze.getStart())
    fin_answer.reverse()
    return fin_answer

def astar_(maze,start_row,start_col,fin_row,fin_col):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    rows,cols = maze.getDimensions()
    g_score = [[float("inf")]*cols for _ in range(rows)]
    h_score = [[float("inf")]*cols for _ in range(rows)]
    f_score = [[float("inf")]*cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            h_score[i][j]= Manhattan(i,j,fin_row,fin_col)
    g_score[start_row][start_col] = 0;
    f_score[start_row][start_col] = h_score[start_row][start_col]
    Dict_list = {}
    answer = []
    open_list = [(f_score[start_row][start_col],(start_row,start_col))]
    closed_set = []
    val_list = [(start_row,start_col)]
    while open_list:
        temp = min(open_list)[1]
        open_list.remove(min(open_list))
        val_list.remove(temp)
        neigh = maze.getNeighbors(temp[0],temp[1])
        closed_set.append(temp)
        for i in neigh:
            g_temp = g_score[temp[0]][temp[1]]+1
            if(i not in closed_set):
                if(g_temp < g_score[i[0]][i[1]]):
                    g_score[i[0]][i[1]] = g_temp
                    f_score[i[0]][i[1]] = h_score[i[0]][i[1]] + g_temp
                    Dict_list[i] = temp;
                    if (i not in val_list):
                        val_list.append(i)
                        open_list.append((f_score[i[0]][i[1]],i))
                    if i == (fin_row,fin_col):
                        answer.append(i)
                        y = Dict_list[i]
                        while((start_row,start_col) != y):
                            answer.append(y)
                            y = Dict_list[y]
                        # answer.append((start_row,start_col))
                        answer.reverse()
                        return answer
    return []
