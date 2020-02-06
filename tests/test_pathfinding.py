import unittest
import numpy as np
from pathfinding_algorithms import bfs,dfs,a_star
from data_structures import Maze, Node,VisitedNodes,Queue,Stack,PriorityQueue
from hypothesis import given,settings, Verbosity
import hypothesis.strategies as st
from hypothesis.extra.numpy import arrays as hypo_array

class PathfindingTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    def setUp(self):
        pass

        # self.grid = np.genfromtxt("data_np.txt", delimiter=",", dtype=np.int)
        # self.start = (4,0)
        # self.end = (0,4)
        #
        # self.dfs_correct_returns = {
        #     "visited_list":[(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (3, 4), (3, 3), (3, 2), (2, 3), (2, 4), (1, 4), (0, 4)],
        #     "path_list":[(0, 4), (1, 4), (2, 4), (2, 3), (3, 3), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1), (4, 0)]
        # }
        # self.bfs_correct_returns = {
        #     "visited_list": [(4, 0), (3, 0), (4, 1), (4, 2), (3, 2), (4, 3), (3, 3), (4, 4), (2, 3), (3, 4), (2, 4), (1, 4), (0, 4)],
        #     "path_list": [(0, 4), (1, 4), (2, 4), (2, 3), (3, 3), (3, 2), (4, 2), (4, 1), (4, 0)]
        # }
        #
        # self.test_nodes = [Node(self.grid, (4,0), cost=0, heuristic=12),
        #                    Node(self.grid, (3,0), cost=10, heuristic=10),
        #                    Node(self.grid, (4,1), cost=10, heuristic=8)]
        #
        # self.maze = Maze(self.grid)
        # self.priority_queue = PriorityQueue()
        # self.stack = Stack()
        # self.queue = Queue()


    def tearDown(self):
        self.priority_queue = PriorityQueue()
        self.stack = Stack()
        self.queue = Queue()


    ###############
    #### tests ####
    ###############

    #### Algorithm Testing ####

    # settings decorator with verbosity to show inputs and errors in terminal
    @settings(verbosity=Verbosity.verbose)
    # given decorater to set up the inputs, we use hypo array (imported above) to create a mock numpy array for the grid
    # st.tuples(st.integer(),st.integer()) is creating a tuple with two integers set between 0 to 4
    @given(hypo_array(dtype=np.int,shape=(5,5),elements=st.integers(0,1)),
           st.tuples(st.integers(0,4),st.integers(0,4)),
           st.tuples(st.integers(0,4),st.integers(0,4)))
    # the above will paramaterize the function and for this particular test we assert that the function will return
    # two lists.
    def test_dfs_assert_return_lists(self,grid,start,end):
        visited_list,path_list = dfs(grid,start,end,_stack=Stack())
        # self.assertEqual(visited_list,self.dfs_correct_returns["visited_list"],"tested visited_list is not equal to correct visited list")
        # self.assertEqual(path_list,self.dfs_correct_returns["path_list"],"tested path_list is not equal to correct path list")
        assert visited_list
        assert path_list

    # def test_bfs_assert_equal_return_lists(self):
    #     visited_list, path_list = bfs(self.grid, self.start, self.end)
    #     self.assertEqual(visited_list, self.bfs_correct_returns["visited_list"],
    #                      "tested visited_list is not equal to correct visited list")
    #     self.assertEqual(path_list, self.bfs_correct_returns["path_list"],
    #                      "tested path_list is not equal to correct path list")

    # def test_a_star_assert_equal_return_lists(self):
    #     pass
    #
    #
    # #### Class Testing ####
    #
    # def test_stack_push_assert_in(self):
    #     self.stack.push(self.test_nodes[0])
    #     self.assertIn(self.test_nodes[0],self.stack.nodes,"Was not able to push node into stack")
    #
    #     pass
    #
    # def test_stack_pop_assert_sequence_equal(self):
    #     pass
    #
    # def test_queue_push_assert_in(self):
    #     pass
    #
    # def test_queue_pop_assert_sequence_equal(self):
    #     pass
    #
    # def test_priority_queue_push(self):
    #     self.priority_queue.push(self.test_nodes[0])
    #     self.assertIn(self.test_nodes[0], self.priority_queue.queued_nodes, "Was not able to push Node into priority queue.")
    #
    # def test_priority_queue_prioritize(self):
    #     for node in self.test_nodes[1:]:
    #         self.priority_queue.push(node)
    #     self.assertEqual(self.priority_queue.queued_nodes[0], self.test_nodes[2], "prioritize failed with test nodes.")
    #
    # def test_priority_queue_pop(self):
    #     for node in self.test_nodes:
    #         self.priority_queue.push(node)
    #     self.priority_queue.pop()
    #     self.assertSequenceEqual(self.priority_queue.queued_nodes, [self.test_nodes[1], self.test_nodes[2]], "pop failed with test nodes.")
    #
    # def test_visited_nodes_create_path(self):
    #     pass

if __name__ == "__main__":

    unittest.main()