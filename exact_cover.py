import dancing_links

class ExactCover():
    """
    - a class containing the implementation of the backtracking algorithm for solving an exact cover problem

	:ivar array: a 2-dimensional array for generating the dancing link
	:ivar __solution: a list for storing different solutions of the exact cover problem
	:ivar __sub_solution: a list for storing the rows of a single solution of the exact cover problem
	"""
    def __init__(self, array):
        """ initializes the ExactCover object"""
        self.array = array
        self.__solution = []
        self.__sub_solution = []

    def is_empty(self, M, all_solutions):
        """
            - checks if M is empty, saves the solution and returns True, returns False if M is not empty,
            - refactored from the backtracking algorithm to reduce clatter
            :param M: the dancing link object to be checked
            :type M: dancing_links.DancingLink
            :param all_solutions: True if all solutions are to be found, False otherwise
            :type all_solutions: bool
            :return:True if M is empty, False otherwise
            :rtype: bool
        """
        if M.is_empty():
            if all_solutions:
                self.__solution.append(sorted(self.__sub_solution))
                return True
            self.__solution = sorted(self.__sub_solution)
            return True
        return False

    def __get_solution(self, all_solutions):
        """
            - encapsulates the backtracking recursive algorithm for solving the exact cover problem
            :param all_solutions: True when all solutions are to be found, False if the program should stop after getting a single solutions
            :type: bool
            :return: a 2-dimensional array of individual solutions if all solutions are to be found, a one dimensional array of the single solution otherwise
            :rtype: list
        """
        link = dancing_links.DancingLink(self.array)
        self.__solution = []
        self.__sub_solution = []
        def solve(M):
            """
                - a backtracking recursive algorithm for solving the exact cover problem

                :param M: a DancingLink object
                :type M: dancing_links.DancingLink
            """
            if self.is_empty(M, all_solutions):
                return True
            # choose a column
            column_head = M.get_min_nodes_head()
            # get the first node from the column
            node = column_head.node
            while node is not None:
                # include the row in the solution
                self.__sub_solution.append(node.row)
                restoration_list = M.complete_column_row_deletion(node)
                if not M.can_not_have_solution() and solve(M) and not all_solutions:
                    return True
                # the row does not give the solution, backtrack
                self.__sub_solution = self.__sub_solution[:-1]
                # restore the dancing link to a previous version
                M.complete_column_row_restoration(restoration_list)
                # move to the next node
                node = node.v_next
            return False
        solve(link)
        return self.__solution

    def get_single_solution(self):
        """ an auxiliary method to find a single solution """
        return self.__get_solution(False)

    def get_all_solutions(self):
        """ an auxiliary method to find all solutions """
        return self.__get_solution(True)
