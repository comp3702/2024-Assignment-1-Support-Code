import sys
from constants import *
from environment import *
from state import State

"""
solution.py

This file is a template you should use to implement your solution.

You should implement 

COMP3702 2024 Assignment 1 Support Code
"""


class Solver:

    def __init__(self, environment, loop_counter):
        self.environment = environment
        self.loop_counter = loop_counter
        #
        # TODO: Define any class instance variables you require here.
        # NOTE: avoid performing any computationally expensive heuristic preprocessing operations here - use the preprocess_heuristic method below for this purpose
        #

    # === Uniform Cost Search ==========================================================================================
    def solve_ucs(self):
        """
        Find a path which solves the environment using Uniform Cost Search (UCS).
        :return: path (list of actions, where each action is an element of BEE_ACTIONS)
        """

        #
        #
        # TODO: Implement your UCS code here
        #
        # === Important ================================================================================================
        # To ensure your code works correctly with tester, you should include the following line of code in your main
        # search loop:
        #
        # self.loop_counter.inc()
        #
        # e.g.
        # while loop_condition(): // (While exploring frontier)
        #   self.loop_counter.inc()
        #   ...
        #
        # ==============================================================================================================
        #
        #

        pass

    # === A* Search ====================================================================================================

    def preprocess_heuristic(self):
        """
        Perform pre-processing (e.g. pre-computing repeatedly used values) necessary for your heuristic,
        """

        #
        #
        # TODO: (Optional) Implement code for any preprocessing required by your heuristic here (if your heuristic
        #  requires preprocessing).
        #
        # If you choose to implement code here, you should call this method from your solve_a_star method (e.g. once at
        # the beginning of your search).
        #
        #

        pass

    def compute_heuristic(self, state):
        """
        Compute a heuristic value h(n) for the given state.
        :param state: given state (GameState object)
        :return a real number h(n)
        """

        #
        #
        # TODO: Implement your heuristic function for A* search here.
        #
        # You should call this method from your solve_a_star method (e.g. every time you need to compute a heuristic
        # value for a state).
        #

        pass

    def solve_a_star(self):
        """
        Find a path which solves the environment using A* search.
        :return: path (list of actions, where each action is an element of BEE_ACTIONS)
        """

        #
        #
        # TODO: Implement your A* search code here
        #
        # === Important ================================================================================================
        # To ensure your code works correctly with tester, you should include the following line of code in your main
        # search loop:
        #
        # self.loop_counter.inc()
        #
        # e.g.
        # while loop_condition(): //
        #   self.loop_counter.inc()
        #   ...
        #
        # ==============================================================================================================
        #
        #

        pass

    #
    #
    # TODO: Add any additional methods here
    #
    #
