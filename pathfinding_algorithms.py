import numpy as np
import math
from typing import Tuple
from data_structures import Node,VisitedNodes,Queue,Stack,PriorityQueue

def a_star(grid:np.array,start:tuple,end:tuple) -> Tuple[list,list]:
    """ A function that searches for the shortest path in a grid using the A* algorithm

        This function searches through a grid searching for the shortest path using the A* algorithm. The function first
        sets up a VisitedNodes object (visited) and a PriorityQueue object (priority_queue) to keep track of checked
        nodes. A Node object for the first starting position is created and pushed into the priority queue.
        While there are still objects in the priority_queue, the function will pull the first item from the
        priority_queue and store it in visited. The function will check that the current node's position is not equal
        to the end position; if it does then a visited list and path list is created by calling the appropriate methods
        from visited. Otherwise, the function iterates on the current node's children, and checks if they are already in
        visited or the priority_queue, and that the child is accessible (accessible > 0). If true, then child of the
        current node is added to the priority_queue along with the child's information.

        Parameters
        ----------
            grid : np.array
                a numpy array detailing the grid
            start : tuple
                a tuple detailing the starting node's position
            end : tuple
                a tuple detailing the ending node's position
        Returns
        -------
            Tuple[list,list]
                A list of visited nodes and a list of nodes that are included in the path

    """

    # heuristics used; diagonal_distance is used by default
    def euclidean_distance(child_node, end):
        return math.sqrt((pow(child_node[0]-end[0],2))+(pow(child_node[1]-end[1],2)))

    def manhattan_distance(child_node,end):
        return (abs(child_node[0] - end[0]) + abs(child_node[1]-end[1])) * 10

    def diagonal_distance(child_node,end):
        dx = abs(child_node[0] - end[0])
        dy = abs(child_node[1] - end[1])

        return 10 * (dx+dy) + (14 - 2 * 10) * min(dx,dy)

    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
        return [None],[None]

    visited = VisitedNodes()
    priority_queue = PriorityQueue()
    priority_queue.push(Node(grid, start, neighbors="8_wind", cost=0, heuristic=diagonal_distance(start, end)))

    while len(priority_queue) > 0:
        node = priority_queue.pop()
        visited._store_node(node)
        if node.pos == end:
            visited_list,path_list = visited.create_path(node.pos, start)
            return visited_list,path_list
        else:
            for child in node.children:
                if child["node"] not in visited.visited_nodes and child["node"] not in priority_queue.queue_list and child["accessibility"]:
                    priority_queue.push(Node(grid, child["node"], parent=node.pos, neighbors="8_wind", cost=child["cost"],
                                             heuristic=diagonal_distance(child["node"], end)))
    return [None],[None]


def dfs(grid:np.array, start:tuple, end:tuple, _stack: Stack = Stack()) -> Tuple[list, list]:
    """ A function that searches for a path in a grid using the Depth-first-search algorithm

        This function searches through a grid searching for a path using the Depth-first-search algorithm. The function
        first pushes the first Node object into the stack. A VisitedNodes object is created (visited). While there are
        objects in the stack, the first node of the stack is removed and appended in visited. The node's position is
        checked to see if it is equal to the end position; if it is, then a list of visited nodes and a path list is
        returned. Otherwise, the function iterates over each child of the current node. The child is checked to see
        if it is in the stack or in visited nodes, and is accessible. If true, the child node is pushed into the stack
        and the process repeats.

        Parameters
        ----------
            grid : np.array
                a numpy array detailing the grid
            start : tuple
                a tuple detailing the starting node's position
            end : tuple
                a tuple detailing the ending node's position
            _stack : Stack = Stack()
                a stack object
        Returns
        -------
            Tuple[list,list]
                A list of visited nodes and a list of nodes that are included in the path
    """

    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
        return [None],[None]

    _stack.push(Node(grid, start))
    visited = VisitedNodes()

    while len(_stack) > 0:
            node = _stack.pop()
            visited._store_node(node)
            if node.pos == end:
                visited_list,path_list = visited.create_path(node.pos, start)
                return visited_list,path_list
            else:
                for child in node.children:
                    if child["node"] not in visited.visited_nodes and child["node"] not in _stack.stacked_nodes and child["accessibility"]:
                            _stack.push(Node(grid, child["node"], parent=node.pos))
    return [None],[None]

def bfs(grid:np.array,start:tuple,end:tuple) -> Tuple[list,list]:
    """ A function that searches for the shortest path in a grid using the Breadth-first-search algorithm

        This function searches through a grid searching for the shortest path using the Breadth-first-search algorithm.
        First a Queue (queue) object is created and the first node is pushed into it. A VisitedNodes (visited) object
        is created after. While there are objects in queue, the first object in the queue is removed and placed in
        visited. If the node's position is equal to the end, then a visited list and a path list is returned. Otherwise,
        each child of the node is iterated upon and checked to see if they are in visited or the queue, and if that
        child is accessible. If true, then that child node is pushed into the queue and the process repeats.

        Parameters
        ----------
            grid : np.array
                a numpy array detailing the grid
            start : tuple
                a tuple detailing the starting node's position
            end : tuple
                a tuple detailing the ending node's position
        Returns
        -------
            Tuple[list,list]
                A list of visited nodes and a list of nodes that are included in the path
    """

    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
        return [None],[None]

    queue = Queue()
    queue.push(Node(grid,start))
    visited= VisitedNodes()

    while len(queue) > 0:
        node = queue.pop()
        visited._store_node(node)
        if node.pos == end:
            visited_list, path_list = visited.create_path(node.pos, start)
            return visited_list, path_list
        else:
            for child in node.children:
                if child["node"] not in visited.visited_nodes and child["node"] not in queue.queue_list and child["accessibility"]:
                    queue.push(Node(grid, child["node"], parent=node.pos))
    return [None],[None]


if __name__ == "__main__":
    grid = np.genfromtxt("data_np.txt", delimiter=",", dtype=np.int)
    print(grid)
    # # print(grid)
    visited_list,path_list = bfs(grid,(4,0),(0,4))
    print(visited_list)
    print(path_list)



    test_nodes = [Node(grid, (4, 0), cost=0, heuristic=12),
                       Node(grid, (3, 0), cost=10, heuristic=10),
                       Node(grid, (4, 1), cost=10, heuristic=8)]

    test_queue = Queue()


    for node in test_nodes:
        test_queue.push(node)

    print(len(test_queue))
    # #
    # # for node in test_queue:
    # #     print(node)

    import sys
    from os.path import dirname

    # print(sys.executable)
    # print("\n".join(sys.path))
    #
    # sys.path.append(dirname(__file__))

    # print("test")