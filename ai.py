from __future__ import print_function
from heapq import * #Hint: Use heappop and heappush
from queue import PriorityQueue

ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)]

class AI:
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    def set_search(self):
        self.final_cost = 0
        self.grid.reset()
        self.finished = False
        self.failed = False
        self.previous = {}

        # Initialization of algorithms goes here
        if self.type == "dfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "ucs":
            self.frontier = [(0,self.grid.start)]
            self.explored = []
        elif self.type == "astar":
            self.frontier = [(abs(self.grid.start[0]-self.grid.goal[0]) + abs(self.grid.start[1]-self.grid.goal[1]),0,self.grid.start)]
            self.explored = []

    def get_result(self):
        total_cost = 0
        current = self.grid.goal
        while not current == self.grid.start:
            total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = True #This turns the color of the node to red
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()

    #DFS: BUGGY, fix it first
    def dfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop()
        if current == self.grid.goal:
            self.finished = True
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    if self.grid.nodes[n].color_checked == False and self.grid.nodes[n].color_frontier == False:
                        self.previous[n] = current
                        self.frontier.append(n)
                        self.grid.nodes[n].color_frontier = True
    
    #Implement BFS here (Don't forget implement initialization at line 23)
    def bfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop(0)
        if current == self.grid.goal:
            self.finished = True
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    if self.grid.nodes[n].color_checked == False and self.grid.nodes[n].color_frontier == False:
                        self.previous[n] = current
                        self.frontier.append(n)
                        self.grid.nodes[n].color_frontier = True

        
    
    #Implement UCS here (Don't forget implement initialization at line 23)
    def ucs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return

        current_buf = heappop(self.frontier)
        current_cos = current_buf[0]
        current = current_buf[1]
        if current == self.grid.goal:
            self.finished = True
            return
            
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.explored.append(current)
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    if any(n in item for item in self.frontier) == False and n not in self.explored:
                        self.previous[n] = current
                        heappush(self.frontier,(current_cos + self.grid.nodes[n].cost(),n))
                        self.grid.nodes[n].color_frontier = True

                    elif any(n in item for item in self.frontier):
                        new_cos = current_cos + self.grid.nodes[n].cost()
                        for i in range(len(self.frontier)):
                            if n == self.frontier[i][1] and new_cos < self.frontier[i][0]:
                                self.frontier.pop(i)
                                heappush(self.frontier,(new_cos,n))
                                self.previous[n] = current
                                break
                    

                    
    
    #Implement Astar here (Don't forget implement initialization at line 23)
    def astar_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return

        current_buf = heappop(self.frontier)
        current_cos = current_buf[1]
        current = current_buf[2]
        if current == self.grid.goal:
            self.finished = True
            return
            
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.explored.append(current)
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    if any(n in item for item in self.frontier) == False and n not in self.explored:
                        self.previous[n] = current
                        heappush(self.frontier,(current_cos + self.grid.nodes[n].cost()+abs(n[0]-self.grid.goal[0]) + abs(n[1]-self.grid.goal[1]),current_cos + self.grid.nodes[n].cost(),n))
                        self.grid.nodes[n].color_frontier = True

                    elif any(n in item for item in self.frontier):
                        new_cos = current_cos + self.grid.nodes[n].cost()
                        new_total_cos = new_cos + abs(n[0]-self.grid.goal[0]) + abs(n[1]-self.grid.goal[1])
                        for i in range(len(self.frontier)):
                            if n == self.frontier[i][2] and new_total_cos < self.frontier[i][0]:
                                self.frontier.pop(i)
                                heappush(self.frontier,(new_total_cos,new_cos,n))
                                self.previous[n] = current
                                break
