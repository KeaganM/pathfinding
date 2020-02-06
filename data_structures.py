import numpy as np
import math
from typing import Tuple,Union

class Maze:
    """ A class to hold maze data.

    This is a class to hold information about the state of a grid and its shape.

    Attributes
    ----------
        grid : numpy.array
            a numpy.array object with integer values.
        grid_shape : tuple
            a tuple detailing the bounds of the array.

    Parameters
    ----------
        grid : numpy.array
            a numpy.array object with integer values.

    """
    def __init__(self,grid:np.array) -> None:
        self.grid = grid
        self.grid_shape = grid.shape

    def __repr__(self) -> str:
        return f"grid: {self.grid} \n bounds: {self.grid_shape}"

class Node(Maze):
    """ A class to hold node data.

    This is a class to hold information about a node, and is a child class to the Maze class. Currently designed to work
    with a 2d grid.

    Attributes
    ----------
        grid : numpy.array
            a numpy.array object with integer values.
        current : tuple
            a tuple containing the location of the current node in the grid.
        parent : tuple/None
            a tuple containing the location of the parent node in the grid.
        neighbors : str
            a string that represents which neighbors within the grid to consider.
        cost : int/None
            an integer that represents the cost to get to the cell in the grid.
        heuristic : int/None
            an integer that represents the value from the current node to the end node.
        total_cost : int/None
            an integer that represents the total cost of getting to the current cell.
        children : list
            a list of dictionaries that contains info on the surrounding child nodes.
        info_dict : dict
            a dictionary that contains info on the current cell.

    Parameters
    ----------
    grid : numpy.array
        a numpy.array object with integer values.
    current : tuple
        a tuple containing the location of the current node in the grid.
    parent : tuple/None
        a tuple containing the location of the parent node in the grid.
    neighbors : str
        a string that represents which neighbors within the grid to consider.
    cost : int/None
        a integer that represents the cost to get to the cell in the grid.
    heuristic : int/None
        a integer that represents the value from the current node to the end node.


    Methods
    -------
        get_children_grid(self, neighbors:str)
            a method that gets the children nodes around the current nodes.
        get_total_cost (self)
            a method to calculate the total cost to get to the current cell.
    """
    def __init__(self, grid:np.array, current:tuple, parent:Union[tuple,None] = None, neighbors:str= "4_wind", cost:Union[int,None] = None,
                 heuristic:Union[int,None] = None) -> None:
        Maze.__init__(self,grid=grid)

        self.parent = parent
        self.pos = current
        self.cost = cost
        self.heuristic = heuristic
        self.total_cost = self._get_total_cost()
        self.children = self._get_children_grid(neighbors)
        self.info_dict = {"current":self.pos, "parent":self.parent, "children": self.children}

    def _get_total_cost(self) -> int:
        """ A function to get the total cost to get to a cell.

        This is a function that will take the cost and heuristic if they are not none, and return the total cost to get
        to a cell.

        Returns
        -------
        total_cost : int
            an integer that is the total cost evaluated by adding the cost and the heuristic of a cell.
        """
        if self.cost is not None and self.heuristic is not None:
            return self.cost + self.heuristic


    def _get_children_grid(self, neighbors:str) -> list:
        """ A function to find child cells.

        This is a function that will find child cells of the current cells. The function uses a nested function to
        assure certain parameters of the child cell are met.

        Parameters
        ----------
        neighbors : str
            a string that dictates which cells to be consider; n,w,s,e or ne,n,nw,w,sw,s,se

        Returns
        -------
        iterate_over_directions : function
            a function that will iterate over the desired directions adjacent to the cell.
        """

        def _iterate_over_directions(neighbors_dict:dict) -> list:
            """ A function to iterate over cell directions.

            This is a function that will iterate over desired directions adjacent to the current cell. The function
            considers the grid with respect to

            Parameters
            ----------
            neighbors_dict : dict
                a dictionary of directions and the calculation values need to

            Returns
            -------
            childern : list
                a list of dictionaries with information pertaining to child cells of the current node.

            """

            children = list()
            for key,value in neighbors_dict.items():
                child_node = (self.pos[0] + value["calc"][0], self.pos[1] + value["calc"][1])
                if child_node == self.parent or child_node[0] < 0 or child_node[1] < 0 or child_node[0] >= self.grid_shape[0] or child_node[1] >= self.grid_shape[1]:
                    pass
                else:
                    if self.grid[child_node[0]][child_node[1]] == 0:
                        access = True
                    else:
                        access = False
                    children.append({"node":child_node,"accessibility":access,"cost":value["cost"]})
            return children

        diagonal_line_cost = 14
        straight_line_cost = 10

        # help visualize directions
        four_wind = {
            "north": {
                "calc": [-1, 0],
                "cost": straight_line_cost
            },
            "east": {
                "calc": [0, 1],
                "cost": straight_line_cost
            },
            "south": {
                "calc": [1, 0],
                "cost": straight_line_cost
            },
            "west": {
                "calc": [0, -1],
                "cost": straight_line_cost
            }
        }

        eight_wind = {
            "north_west": {
                "calc": [-1, -1],
                "cost": diagonal_line_cost
            },
            "north": {
                "calc": [-1, 0],
                "cost": straight_line_cost
            },
            "north_east": {
                "calc": [-1, 1],
                "cost": diagonal_line_cost
            },

            "west": {
                "calc": [0, -1],
                "cost": straight_line_cost
            },
            "east": {
                "calc": [0, 1],
                "cost": straight_line_cost
            },
            "south_west": {
                "calc": [1, -1],
                "cost": diagonal_line_cost
            },
            "south": {
                "calc": [1, 0],
                "cost": straight_line_cost
            },
            "south_east": {
                "calc": [1, 1],
                "cost": diagonal_line_cost
            },
        }

        if neighbors == "4_wind":
            return _iterate_over_directions(four_wind)
        if neighbors == "8_wind":
            return  _iterate_over_directions(eight_wind)

    def __repr__(self):
        return f"Node{self.pos}"

class Stack:
    """ A class to act as a stack data structure.

    This is a class to hold information about a stack, and what is put into it ore taken out of it. Methods are designed
    to insert a new object into the stack, and then remove and return an object in the first position of the stack.

    Attributes
    ----------
    stacked_nodes : list
        a list of Node objects

    Methods
    -------
    push(node:Node)
        a function to add a node to the stack
    pop()
        a function to remove the most recent addition from the stack

    """
    def __init__(self) -> None:
        self.stacked_nodes = list()

    def push(self,node: Node) -> None:
        """ A function to insert a new object.

        This is a function that will insert a new object into the first index of a list.

        Parameters
        ----------
        node : Node
            a Node object

        """
        self.stacked_nodes.insert(0, node)

    def pop(self) -> Node:
        """ A function to remove and return the first object.

        This is a function that will remove and return an object that is found in the first position of the list.

        Returns
        -------
            a Node object

        """
        return self.stacked_nodes.pop(0)

    def __repr__(self):
        return f"current stack is: {self.stacked_nodes}"

    def __len__(self):
        return len(self.stacked_nodes)

class Queue:
    """A class to act as a queue data structure

    This is a class to hold information about a queue, what goes into the queue and what is taken out. Methods are
    designed to insert a new object into a queue, and remove the oldest object currently in the queue.

    Attributes
    ----------
        queued_nodes : list
            a list of Node objects
        queue_list : list
            a list of positions

    Methods
    -------
        push(node:Node)
            a function to insert a new object into the queue
        pop()
            a function to remove the oldest object from the queue


    """
    def __init__(self) -> None:
        self.queued_nodes = list()
        self.queue_list = list()

    def push(self, node: Node) -> None:
        """ A function to insert a new object into the queue.

        This is a function that will insert a new object into the last place of the list. The node object is appended
        to the queued_nodes list while the node's position is appended to the queue_list.

        Parameters
        ----------
            node : Node
                a Node object

        """
        self.queued_nodes.append(node)
        self.queue_list.append(node.pos)

    def pop(self) -> Node:
        """ A function to remove and return a popped object.

        This is a function that will remove and return an object that is found in the first position of the list.

        Returns
        -------
            self.queued_nodes.pop(0) : Node
                a Node object

        """
        self.queue_list.pop(0)
        return self.queued_nodes.pop(0)

    def __repr__(self):
        return f"current queue is: {self.queued_nodes}"

    # for educational and testing purposes vvvv
    def __iter__(self):
        return self

    def __next__(self):
        self._iter_queued_nodes = self.queued_nodes
        if self._iter_queued_nodes:
            return self._iter_queued_nodes.pop(0)
        raise StopIteration()
    # ^^^^ for educational and testing purposes

    def __len__(self):
        return len(self.queued_nodes)

class PriorityQueue(Queue):
    """ A class to act as a priority queue data structure.

    This is a class to hold information pertaining to a priority queue. The class is a child of the Queue class.
    Methods are designed to insert objects into a list, rearrange the list according to a heuristic, and remove and
    return the object in the first position of the list.

    Methods
    -------
        push(node:Node)
            a method to insert an object into the priority queue
        _prioritize()
            a method to rearrange the queue based on heuristic
    """
    def __init__(self) -> None:
        super().__init__()

    def push(self,node:Node) -> None:
        """ A function to insert a new object into the queue.

        This is a function that will insert a new object into the last place of the list. The node object is appended
        to the queued_nodes list while the node's position is appended to the queue_list. The _prioritize function is
        called to rearrange the lists.

        Parameters
        ----------
            node : Node
                a Node object

        """
        self.queued_nodes.append(node)
        self.queue_list.append(node.pos)
        self._prioritize()

    def _prioritize(self) -> None:
        """ A function to rearrange the priority list

        This is a function that will rearrange a priority queue based on a given heuristic. It will iterate through
        each node in the list, checking for a value that details the total cost of moving on to the next cell. Nodes
        with the lowest cost are moved to the first position of the list.

        """
        least_total_cost = None
        for node in self.queued_nodes:
            if least_total_cost == None or node.total_cost < least_total_cost:
                self.queued_nodes.remove(node)
                self.queued_nodes.insert(0, node)
                least_total_cost = node.total_cost

    def __repr__(self):
        return f"Queue is {self.queued_nodes}"

class VisitedNodes:
    """ This is a class to house information about visited nodes

    This is a class that contains all the nodes a search function may iterate through. The class keeps track of each
    node that was visited.

    Attributes
    ----------
        nodes : list
            a list of Node objects
        visited_nodes : list
            a list of the Node object's position
        node_info : dict
            a dictionary of node dictionaries

    Methods
    -------
        store_node(node:Node)
            a method to store node information in a series of lists
        create_path(current_node_position,start_position)
            a method to recreate a path through the stored nodes
    """
    def __init__(self) -> None:
        self.nodes = list()
        self.visited_nodes = list()
        self.node_info = dict()

    def _store_node(self, node:Node) -> None:
        """ A function to store a new Node object

            This is a function that will insert a several objects into various lists. A Node object is inserted into
            the nodes list and the Node object's position is inserted into the visited_nodes list. A the info_dict of
            the Node object is inserted into the node_info dictionary, where the key is set to the Node object's
            position.

            Parameters
            ----------
                node : Node
                    a Node object

        """
        self.nodes.append(node)
        self.visited_nodes.append(node.pos)
        self.node_info[node.pos] = node.info_dict

    def create_path(self,current_node_position,start_position) -> Tuple[list,list]:
        """ A function to create a path through the stored nodes

            While the current node's position is not equal to the starting position, the current node is appended to a
            path list. The current node's position is updated to the parent of the current node's position and the
            process repeats. Once the current node's position is equal ot the starting position, the final node's
            information is appended to the path list.

            Parameters
            ----------
                current_node_position : tuple
                    a tuple that describes the position of the current node within a grid
                start_position : tuple
                    a tuple that describes the position of the starting node
            Returns
            -------
                Tuple[list,list]
                    A list of visited nodes and a list of nodes that are included in the path

        """
        path_list = list()
        while current_node_position != start_position:
            path_list.append(self.node_info[current_node_position]["current"])
            current_node_position = self.node_info[current_node_position]["parent"]

        path_list.append(self.node_info[current_node_position]["current"])

        return self.visited_nodes,path_list

    def __repr__(self):
        return f"visited nodes are: {self.nodes}"