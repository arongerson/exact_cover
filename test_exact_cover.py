import unittest
import exact_cover as ec
import dancing_links as dl

class HeadTest(unittest.TestCase):

    def test_column_head_creation_1(self):
        """ test whether the Head is initialized correctly """
        head = dl.Head(0)
        self.assertEqual(head.next, None)
        self.assertEqual(head.prev, None)
        self.assertEqual(head.node, None)
        self.assertEqual(head.col, 0)
        self.assertEqual(head.last_node, None)
        self.assertEqual(head.nodes, 0)

    def test_column_head_creation_2(self):
        """ test whether the Head is initialized correctly """
        head = dl.Head(3)
        self.assertEqual(head.next, None)
        self.assertEqual(head.prev, None)
        self.assertEqual(head.node, None)
        self.assertEqual(head.col, 3)
        self.assertEqual(head.last_node, None)
        self.assertEqual(head.nodes, 0)

class NodeTest(unittest.TestCase):

    def test_node_creation_1(self):
        """ test whether the Node is initialized correctly """
        head = dl.Head(0)
        node = dl.Node(head, 0, 1)
        self.assertEqual(node.h_next, None)
        self.assertEqual(node.h_prev, None)
        self.assertEqual(node.v_next, None)
        self.assertEqual(node.v_prev, None)
        self.assertEqual(node.head, head)
        self.assertEqual(node.col, 1)
        self.assertEqual(node.row, 0)

    def test_node_creation_number_of_nodes(self):
        """test whether the number of nodes is correctly updated when the node is added to the column"""
        head = dl.Head(3)
        self.assertEqual(head.nodes, 0)
        node = dl.Node(head, 0, 1)
        self.assertEqual(head.nodes, 1)

class DancingLinkTest(unittest.TestCase):

    def setUp(self):
        """ initialize the dataset """
        array_1 = [
            [0,0,1,0,1,1,0],
            [1,0,0,1,0,0,1],
            [0,1,1,0,0,1,0],
            [1,0,0,1,0,0,0],
            [0,1,0,0,0,0,1],
            [0,0,0,1,1,0,1]
            ]
        self.link_mixed_1 = dl.DancingLink(array_1)

        array_2 = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]
            ]
        self.link_zeros = dl.DancingLink(array_2)

        array_3 = [
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1]
            ]
        self.link_ones = dl.DancingLink(array_3)

        array_4 = [
            [0,1,1,1,0,0,1],
            [0,1,0,1,1,1,0],
            [0,0,1,0,0,1,1],
            [1,1,0,1,1,0,1],
            [0,0,0,0,1,0,0],
            [1,0,0,0,0,0,0],
            [1,1,0,1,0,0,0]
            ]
        self.link_mixed_2 = dl.DancingLink(array_4)

        array_5 = [
            [0,1,0,0,1,1,1,0],
            [0,1,1,1,0,0,0,1],
            [1,0,1,0,0,0,0,0],
            [0,0,1,1,1,0,0,1],
            [0,1,1,0,1,1,1,0],
            [0,1,0,0,0,1,0,0],
            [1,0,0,1,0,0,0,1],
            [0,1,1,0,0,0,1,1]
            ]
        self.link_mixed_3 = dl.DancingLink(array_5)

        array_6 = [
            [1,1,1,0,0,0,0],
            [0,0,0,1,1,1,1],
            [1,1,1,0,0,0,0],
            [0,0,0,1,1,1,1],
            [1,1,1,0,0,0,0],
            [0,0,0,1,1,1,1],
            [1,1,1,0,0,0,0]
            ]
        self.link_alternating = dl.DancingLink(array_6)
        self.link_empty = dl.DancingLink([[]])
        array_7 = [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,1,0]
            ]
        self.link_single_1 = dl.DancingLink(array_7)
        array_8 = [
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            ]
        self.link_single_zero_column = dl.DancingLink(array_8)

    def tearDown(self):
        pass

    def test_dancing_link_head_initialization_1(self):
        """ test whether all the column heads are initialized correctly """
        link = self.link_mixed_1
        # check the main head
        self.assertNotEqual(link.head, None)
        self.assertEqual(link.head.col, 0)
        # check rows and columns
        self.assertEqual(link.rows, 6)
        self.assertEqual(link.cols, 7)
        # check whether nodes in the expected positions
        self.assertEqual(link.heads[0].node.row, 1)
        self.assertEqual(link.heads[0].node.col, 0)
        # check the last head next and prev pointers
        self.assertEqual(link.heads[6].next, None)
        self.assertEqual(link.heads[6].prev.nodes, 2)
        self.assertEqual(link.heads[6].prev.col, 5)
        self.assertEqual(link.heads[6].prev.node.row, 0)
        # check the first head next and prev pointers
        self.assertEqual(link.heads[0].prev, None)
        self.assertEqual(link.heads[0].next.col, 1)
        # check the mid head next and prev pointers
        self.assertEqual(link.heads[3].prev.col, 2)
        self.assertEqual(link.heads[3].next.col, 4)

    def test_dancing_link_initialization_empty_array(self):
        """ test whether initializing the dancing link with an empty array gives the expected result """
        link = self.link_empty
        self.assertEqual(link.head, None)

    def test_dancing_link_nodes_initialization(self):
        """ test whether all node initialization works correctly """
        link = self.link_mixed_2
        # test top left node
        node = link.heads[0].node
        self.assertEqual(node.row, 3)
        self.assertEqual(node.col, 0)
        self.assertEqual(node.v_prev, None)
        self.assertEqual(node.v_next.row, 5)
        self.assertEqual(node.h_prev, None)
        self.assertEqual(node.h_next.col, 1)
        self.assertEqual(node.head.nodes, 3)
        # test bottom right node
        node = link.heads[3].node.v_next.v_next.v_next
        self.assertEqual(node.row, 6)
        self.assertEqual(node.col, 3)
        self.assertEqual(node.v_next, None)
        self.assertEqual(node.v_prev.h_next.col, 4)
        self.assertEqual(node.h_next, None)
        self.assertEqual(node.h_prev.col, 1)

    def test_is_empty(self):
        """ testing the is_empty() method with an empty array, an array with a mixture of zeros and ones, all ones and all zeros"""
        self.assertTrue(self.link_zeros.is_empty())
        self.assertFalse(self.link_mixed_3.is_empty())
        self.assertFalse(self.link_single_1.is_empty())
        self.assertTrue(self.link_empty.is_empty())

    def test_can_not_have_solution(self):
        """ testing the can_not_have_solution method with different sets of arrays """
        self.assertTrue(self.link_zeros.can_not_have_solution())
        self.assertFalse(self.link_ones.can_not_have_solution())
        self.assertTrue(self.link_single_zero_column.can_not_have_solution())
        # Tricky: because in the backtracking algorithm the condition for having the solution is to check whether
        # the dancing link is empty, an empty dancing link is considered to have a solution of [], therefore,
        # no_slution method should return False
        self.assertFalse(self.link_empty.can_not_have_solution())

    def test_get_column_head(self):
        """ testing the get_column_head by passing the column number and checking whether the head has the expected number of nodes"""
        link = self.link_mixed_1
        first_head = link.get_column_head(0)
        third_head = link.get_column_head(2)
        fourth_head = link.get_column_head(3)
        seventh_head = link.get_column_head(6)
        self.assertEqual(first_head.nodes, 2)
        self.assertEqual(third_head.nodes, 2)
        self.assertEqual(fourth_head.nodes, 3)
        self.assertEqual(seventh_head.nodes, 3)

    def test_get_column_nodes(self):
        """ checking whether the heads contain the nodes in the expected rows and columns """
        link = self.link_mixed_1
        self.assertEqual(link.get_head_column_nodes(link.get_column_head(0)), [[1,0], [3,0]])
        self.assertEqual(link.get_head_column_nodes(link.get_column_head(1)), [[2,1], [4,1]])
        self.assertEqual(link.get_head_column_nodes(link.get_column_head(2)), [[0,2], [2,2]])
        self.assertEqual(link.get_head_column_nodes(link.get_column_head(3)), [[1,3], [3,3],[5,3]])
        self.assertEqual(link.get_head_column_nodes(link.get_column_head(6)), [[1,6], [4,6],[5,6]])
        self.assertEqual(link.heads[6].nodes, 3)

    def test_detach_column_first_column(self):
        """ testing detaching the first column of the dancing link and checking whether all pointers are updated correctly"""
        # detaching the first column
        link = self.link_mixed_1
        head_0 = link.get_column_head(0)
        # checking the first column before deletion
        self.assertEqual(head_0.col, 0)
        self.assertEqual(link.get_head_column_nodes(head_0), [[1,0], [3,0]])
        self.assertNotEqual(link.get_column_head(6), None)
        link.detach_column(head_0)
        new_head_0 = link.get_column_head(0)
        # checking the first column after deletion
        self.assertEqual(new_head_0.col, 1)
        self.assertEqual(link.get_head_column_nodes(new_head_0), [[2,1], [4,1]])
        # checking the 6th column is None
        self.assertEqual(link.get_column_head(6), None)

    def test_detach_column_central_column(self):
        """ testing detaching a column in the center and checking whether all pointers are updated correctly """
        # detaching the second column
        link = self.link_ones
        head_2 = link.get_column_head(2)
        link.detach_column(head_2)
        new_head_2 = link.get_column_head(2)
        self.assertEqual(new_head_2.col, 3)
        self.assertEqual(new_head_2.next.col, 4)
        self.assertEqual(new_head_2.prev.col, 1)
        self.assertEqual(new_head_2.node.h_next.col, 4)
        self.assertEqual(new_head_2.last_node.h_prev.col, 1)

    def test_detach_column_last_column(self):
        """ testing detaching the last column of the dancing link and checking whether all pointers are updated correctly """
        link = self.link_ones
        head_6 = link.get_column_head(6)
        link.detach_column(head_6)
        self.assertEqual(link.get_column_head(6), None)
        self.assertEqual(link.get_column_head(5).next, None)
        self.assertEqual(link.get_column_head(5).node.h_next, None)

    def test_reattach_column_1(self):
        """ testing reattaching the detached first column and checking whether all pointers are restored correctly """
        link = self.link_mixed_1
        head_0 = link.get_column_head(0)
        link.detach_column(head_0)
        link.reattach_column(head_0)
        head_3 = link.get_column_head(3)
        reattached_head_1 = link.get_column_head(0)
        self.assertEqual(link.get_head_column_nodes(reattached_head_1), [[1,0], [3,0]])
        self.assertEqual(head_3.node.h_prev.col, 0)

    def test_reattach_column_central_column(self):
        """ testing reattaching the central column and checking whether all pointers are restored correctly """
        link = self.link_ones
        head_3 = link.get_column_head(3)
        link.detach_column(head_3)
        link.reattach_column(head_3)
        self.assertEqual(link.get_column_head(2).next.col, 3)
        self.assertEqual(link.get_column_head(4).prev.col, 3)
        self.assertEqual(link.get_column_head(2).node.h_next.col, 3)
        self.assertEqual(link.get_column_head(4).node.h_prev.col, 3)

    def test_reattach_last_column(self):
        """ testing reattaching the last column and checking whether all  nodes are restored correctly """
        link = self.link_ones
        head_6 = link.get_column_head(6)
        link.detach_column(head_6)
        self.assertEqual(link.get_column_head(6), None)
        link.reattach_column(head_6)
        self.assertNotEqual(link.get_column_head(6), None)
        self.assertEqual(link.get_column_head(5).node.h_next.col, 6)

    def test_detach_row(self):
        """
            - testing detaching a row and checking whether all pointers are updated correctly including
            - test whether the number of nodes in the column is correctly updated when the row is deleted

        """
        link = self.link_mixed_1
        head_1 = link.get_column_head(0)
        detached_columns = link.detach_column(head_1)
        for detached_node in detached_columns:
            link.detach_row(detached_node)
        new_head_3 = link.get_column_head(2)
        self.assertEqual(link.get_head_column_nodes(new_head_3), [[5,3]])
        self.assertEqual(new_head_3.nodes, 1)

    def test_reattach_row(self):
        """
            - test reattaching a row restores all the pointers correctly,
            - test whether the number of nodes in the column is correctly updated when the row is reattached
        """
        link = self.link_mixed_1
        head_1 = link.get_column_head(1)
        detached_columns = link.detach_column(head_1)
        for detached_node in detached_columns:
            link.detach_row(detached_node)
        new_head_1 = link.get_column_head(1)
        self.assertEqual(link.get_head_column_nodes(new_head_1), [[0,2]])
        self.assertEqual(new_head_1.nodes, 1)
        for detached_node in reversed(detached_columns):
            link.reattach_row(detached_node)
        link.reattach_column(head_1)
        self.assertEqual(link.get_column_head(1).nodes, 2)
        self.assertEqual(link.get_column_head(2).nodes, 2)
        self.assertEqual(link.get_column_head(5).nodes, 2)

    def test_get_all_row_heads(self):
        """
        - testing the get_all_row_heads method by checking whether all heads returned are in the expected columns by passing a node in the first column
        """
        link = self.link_mixed_1
        head_0 = link.get_column_head(0)
        node = head_0.node
        self.assertNotEqual(node, None)
        heads = link.get_all_row_heads(node)
        self.assertEqual(len(heads), 3)
        self.assertEqual(heads[0].col, 0)
        self.assertEqual(heads[1].col, 3)
        self.assertEqual(heads[2].col, 6)

    def test_get_all_row_heads_from_central_column(self):
        """
        - testing the get_all_row_heads method by checking whether all heads returned are in the expected columns by passing a node in the central column
        """
        link = self.link_mixed_1
        head_4 = link.get_column_head(4)
        node = head_4.node
        self.assertNotEqual(node, None)
        heads = link.get_all_row_heads(node)
        self.assertEqual(len(heads), 3)
        self.assertEqual(heads[0].col, 4)
        self.assertEqual(heads[1].col, 2)
        self.assertEqual(heads[2].col, 5)

    def test_complete_delete_operation(self):
        """
            - given a node in a particular row and column,
            - test deleting all columns with 1's in the given row followed by all the conflicting rows by
            - checking whether the nodes in the reduced matrix are in the expected positions
        """
        link = self.link_mixed_1
        head_1 = link.get_column_head(0)
        # first node in the column
        node = head_1.node
        deleted = link.complete_column_row_deletion(node)
        new_head_0 = link.get_column_head(0)
        self.assertEqual(link.get_head_column_nodes(new_head_0), [[2,1]])
        new_head_1 = link.get_column_head(1)
        self.assertEqual(link.get_head_column_nodes(new_head_1), [[0,2],[2,2]])
        new_head_4 = link.get_column_head(4)
        self.assertEqual(new_head_4, None)
        new_head_3 = link.get_column_head(3)
        self.assertNotEqual(new_head_3, None)

    def test_complete_delete_restoration(self):
        """
            - test restoring all the rows and columns deleted in the complete_column_row_deletion by
            - checking that the nodes are in the expected locations
        """
        link = self.link_mixed_1
        head_1 = link.get_column_head(0)
        node = head_1.node
        restoration_list = link.complete_column_row_deletion(node)
        link.complete_column_row_restoration(restoration_list)
        self.assertEqual(link.get_head_column_nodes(link.get_column_head(0)), [[1,0],[3,0]])
        self.assertEqual(link.get_head_column_nodes(link.get_column_head(3)), [[1,3],[3,3],[5,3]])
        self.assertEqual(link.get_head_column_nodes(link.get_column_head(6)), [[1,6],[4,6],[5,6]])

    def test_get_min_nodes_head(self):
        """ test the get_min_nodes_head by checking whether the returned head is the one with the minimum number of heads"""
        link = self.link_mixed_1
        head = link.get_min_nodes_head()
        self.assertEqual(head.col, 0)
        self.assertEqual(head.nodes, 2)
        # testing with an array with a single one 
        link = self.link_single_1
        head = link.get_min_nodes_head()
        self.assertEqual(head.col, 3)
        self.assertEqual(head.nodes, 1)

    def test_get_min_nodes_head_not_all_zeros(self):
        """ test the get_min_nodes_head does not return the head with all zeros """
        link = self.link_single_zero_column
        head = link.get_min_nodes_head()
        self.assertEqual(head.col, 0)
        self.assertEqual(head.nodes, 3)

class ExactCoverTest(unittest.TestCase):

    def test_exact_cover_1(self):
        array = [
            [0,0,1,0,1,1,0],
            [1,0,0,1,0,0,1],
            [0,1,1,0,0,1,0],
            [1,0,0,1,0,0,0],
            [0,1,0,0,0,0,1],
            [0,0,0,1,1,0,1]
            ]
        exact_cover = ec.ExactCover(array)
        single_solution = exact_cover.get_single_solution()
        self.assertEqual(single_solution, [0,3,4])
        solutions = exact_cover.get_all_solutions()
        for solution in solutions:
            self.assertIn(solution, [[0,3,4]])

    def test_exact_cover_2(self):
        array = [
            [0,1,1,1,0,0,1],
            [0,1,0,1,1,1,0],
            [0,0,1,0,0,1,1],
            [1,1,0,1,1,0,1],
            [0,0,0,0,1,0,0],
            [1,0,0,0,0,0,0],
            [1,1,0,1,0,0,0]
        ]
        exact_cover = ec.ExactCover(array)
        single_solution = exact_cover.get_single_solution()
        self.assertEqual(single_solution, [2,4,6])
        solutions = exact_cover.get_all_solutions()
        for solution in solutions:
            self.assertIn(solution, [[2,4,6]])

    def test_exact_cover_3(self):
        array = [
            [0,1,0,0,1,1,1,0],
            [0,1,1,1,0,0,0,1],
            [1,0,1,0,0,0,0,0],
            [0,0,1,1,1,0,0,1],
            [0,1,1,0,1,1,1,0],
            [0,1,0,0,0,1,0,0],
            [1,0,0,1,0,0,0,1],
            [0,1,1,0,0,0,1,1]
        ]
        exact_cover = ec.ExactCover(array)
        single_solution = exact_cover.get_single_solution()
        self.assertEqual(single_solution, [4,6])
        solutions = exact_cover.get_all_solutions()
        for solution in solutions:
            self.assertIn(solution, [[4,6]])

    def test_exact_cover_4(self):
        array = [
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1]
        ]
        exact_cover = ec.ExactCover(array)
        single_solution = exact_cover.get_single_solution()
        self.assertEqual(single_solution, [0])
        solutions = exact_cover.get_all_solutions()
        for solution in solutions:
            self.assertIn(solution, [[0], [1], [2], [3], [4], [5], [6]])

    def test_exact_cover_5(self):
        array = [
            [1,1,1,0,0,0,0],
            [0,0,0,1,1,1,1],
            [1,1,1,0,0,0,0],
            [0,0,0,1,1,1,1],
            [1,1,1,0,0,0,0],
            [0,0,0,1,1,1,1],
            [1,1,1,0,0,0,0]
        ]
        exact_cover = ec.ExactCover(array)
        single_solution = exact_cover.get_single_solution()
        self.assertEqual(single_solution, [0, 1])
        solutions = exact_cover.get_all_solutions()
        for solution in solutions:
            self.assertIn(solution, [[0, 1], [1, 2], [1, 4], [1, 6], [0, 3], [2, 3], [3, 4], [3, 6], [0, 5], [2, 5], [4, 5], [5, 6]])

    def test_exact_cover_6(self):
        array = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]
        ]
        exact_cover = ec.ExactCover(array)
        single_solution = exact_cover.get_single_solution()
        self.assertEqual(single_solution, [])
        solutions = exact_cover.get_all_solutions()
        for solution in solutions:
            self.assertIn(solution, [[]])

    def test_exact_cover_6(self):
        array = [
            [1,0,0,0,0,0,0],
            [0,1,0,0,0,0,0],
            [0,0,1,0,0,0,1],
            [0,0,0,1,0,1,0],
            [0,0,0,0,1,0,0]
        ]
        exact_cover = ec.ExactCover(array)
        single_solution = exact_cover.get_single_solution()
        self.assertEqual(single_solution, [0, 1, 2, 3, 4])
        solutions = exact_cover.get_all_solutions()
        for solution in solutions:
            self.assertIn(solution, [[0, 1, 2, 3, 4]])


def main():
       unittest.main()

if __name__ == '__main__':
       pass
       main()
