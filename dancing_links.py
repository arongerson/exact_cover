
class Node():

    """
        - A Dancing Link element holding a numeral 1 of the array.
        - the node has 4 pointers;
        -   the up pointer called v_prev
        -   the down pointer called v_next
        -   the left pointer called h_prev
        -   the right pointer called h_next
        - the node also stores its row, column and the head of the column in which it is attached
        - the previous pointer of the first node in a row or column remains None,


	:ivar head: the reference to the head of the column
	:ivar row: the row index of the node, starting at 0
	:ivar col: the column index of the node, starting at 0
	:ivar h_next: a pointer to the next node in a row
	:ivar h_prev: a pointer to the previous node in a row
    :ivar v_next: a pointer to the next node in a column
	:ivar v_prev: a pointer to the previous node in a column
	"""

    def __init__(self, head, row, col):
        """ Initializes a new node """
        self.h_next = None
        self.h_prev = None
        self.v_next = None
        self.v_prev = None
        self.head = head
        self.row = row
        self.col = col
        # increment the number of nodes in the head
        self.head.nodes += 1

    def __str__(self):
        return str(self.row) + "," + str(self.col)

class Head():
    """
        - A Dancing Link head of the column.
        - the head stores the pointer to the first node (first 1) in the given column,
        - it has extra two pointers, one points to the head in the next column and the other to the head of the previous column
        - another variable stores the number of nodes (1's) in the column, this number is updated whenever the number of nodes changes when rows, columns are deleted or restored
        - the col variable stores the initial column the head is located, it is not updated when a previous column is deleted,
        - to get the true nth index for column when other columns have been deleted we iterate and count the number of times it takes,
        - to reach to the particular head.
        - the last_node variable stores the last node to be added to the column, this is useful during initialization of the dancing links


	:ivar col: the column which this head points to
	:ivar last_node: the current last node in the column, only used during initialization of the dancing link
	:ivar col: the column index of the node, starting at 0
	:ivar nodes: the number of nodes, i.e 1's in the column
	:ivar prev: a pointer to the head in the previous column, the prev pointer of the first column head remains None
    :ivar next: a pointer to the head in the next column, the next pointer of the last column head remains None
	:ivar node: a pointer to the first node i.e 1 in the array
	"""
    def __init__(self, col):
        """ Initializes a new head """
        self.next = None
        self.prev = None
        self.node = None
        self.col = col
        self.last_node = None
        self.nodes = 0

    def __str__(self):
        return str(self.col) + "," + str(self.nodes)


class DancingLink():
    """
        - A dancing link data structure with nodes in the locations with 1's in the given array.
        - the dancing link has a doubly linked list of heads, the size of which equals to the number of columns in the array
        - every head points to the first node in the column forming another doubly linked list vertically,
        - the nodes in the same row are also connected to create another doubly linked list
        - there's no node in the position where there is a zero in the array

	:ivar array: a 2-dimensional array used to create the dancing link
	:ivar head: the head of the dancing link, pointing to the head of the first column
	:ivar rows: the number of rows in the array
	:ivar cols: the number of columns in the array
	:ivar heads: provides a constant time access to the heads of the columns, so far just used during testing, not updated when a row or column is removed from the dancing link
	"""

    def __init__(self, array):
        """ Initializes the dancing link """
        self.array = array
        self.head = None
        self.rows = len(array)
        self.cols = len(array[0])
        self.heads = dict()
        self.__init()

    def __init(self):
        """
            - calls the methods responsible for setting up the data structure
        """
        self.__init_heads()
        self.__init_nodes()

    def __init_heads(self):
        """
            - initializes the column heads, the size of which equals to the number of columns
        """
        current_node = None
        for i in range(self.cols):
            node = Head(i)
            self.heads[i] = node
            if i == 0:
                self.head = node
            else:
                current_node.next = node
                node.prev = current_node
            current_node = node

    def __init_nodes(self):
        """
            - initializes the nodes in locations where a 1 exists in the given array and makes all the required links to the column heads
            - the nodes are created from top left, rowwise to the bottom right
        """
        for row in range(self.rows):
            # this node keeps track of the last node added in the given row, updated to None every time we move to the next row
            last_hor_node = None
            for col in range(self.cols):
                if self.array[row][col] == 1:
                    # get the head of this column
                    head = self.heads[col]
                    # create a new node
                    node = Node(head, row, col)
                    # get the node that precedes this node in the column
                    last_ver_node = head.last_node
                    # save this node in the column head to be used in linking the next node to be created
                    head.last_node = node
                    # connect the nodes
                    if last_ver_node is None:
                        head.node = node
                    else:
                        last_ver_node.v_next = node
                        node.v_prev = last_ver_node
                    if last_hor_node is not None:
                        last_hor_node.h_next = node
                        node.h_prev = last_hor_node
                    # update the last node to be created in this row
                    last_hor_node = node

    def is_empty(self):
        """
            - checks whether dancing link is empty by examing all columns and checking whether they all have no nodes
            - the dancing link is considered empty when all columns still attached to the dancing link have no 1's

            :return: True if the dancing link is empty, False otherwise
            :rtype: bool
        """
        current_head = self.head
        while current_head is not None:
            # current_head.nodes gives you the number of nodes in that column
            if current_head.nodes > 0:
                return False
            current_head = current_head.next
        return True

    def can_not_have_solution(self):
        """
            - checks whether the existing dancing link can have a solution or not
            - if a column exists in the dancing link with zero nodes, the solution does not exist, best time to backtract

            :return: True if the solution cannot be found, False otherwise
            :rtype: bool
        """
        current_head = self.head
        while current_head is not None:
            if current_head.nodes == 0:
                return True
            current_head = current_head.next
        return False

    def get_column_head(self, col):
        """
            - given a column number, the method returns the head at that given column,
            - useful during testing when some of the rows and columns have been detached, from the data structure

            :param col: the column number
            :type col: int
            :return: head of the column if it exists, None otherwise
            :rtype: Head
        """
        current_head = self.head
        index = 0
        while current_head is not None and index < col:
            current_head = current_head.next
            index += 1
        return current_head

    def get_head_column_nodes(self, head):
        """
            - given the head of the column the method returns all the nodes still attached in this column
            - Note: used to simplify testing when rows or columns have been deleted or restored

            :param head: the head of the column
            :type: Head
            :return: a list of nodes in the dancing link still attached to this column
            :rtype: list
        """
        node = head.node
        list = [] # stores the nodes in the column
        while node is not None:
            list.append([node.row, node.col])
            node = node.v_next
        return list

    def detach_column(self, head):
        """
            - given the head of the column, detach this column from the dancing link,
            - the pointers of the deleted column are not altered so it is possible to reattach it in its exact previous location

            :param head: head of the column
            :type head: Head
            :return: a list of nodes in this column that have been detached
            :rtype: list
        """
        # detach head
        if head.prev is None:
            self.head = head.next
        if head.next is not None:
            head.next.prev = head.prev
        if head.prev is not None:
            head.prev.next = head.next

        # detach the nodes
        current_node = head.node
        detached_nodes = []
        while current_node is not None:
            if current_node.h_prev is not None:
                current_node.h_prev.h_next = current_node.h_next
            if current_node.h_next is not None:
                current_node.h_next.h_prev = current_node.h_prev
            detached_nodes.append(current_node)
            current_node = current_node.v_next
        return detached_nodes

    def reattach_column(self, head):
        """
            - given the head of the column, reattach all its nodes in the dancing link in their previous location

            :param head: head of the column
            :type head: Head
        """
        # reattach head
        if head.prev is None:
            self.head = head
        if head.next is not None:
            head.next.prev = head
        if head.prev is not None:
            head.prev.next = head

        # reattach the nodes
        current_node = head.node
        while current_node is not None:
            if current_node.h_prev is not None:
                current_node.h_prev.h_next = current_node
            if current_node.h_next is not None:
                current_node.h_next.h_prev = current_node
            current_node = current_node.v_next

    def detach_row(self, node):
        """
            - given a node detach all nodes in its row,
            - the target node in this case is no longer in the dancing link because row deletion should strictly come after,
            - column deletion

            :param node: the node in the column that has been already detached from the list
            :type node: Node
        """
        # detach the nodes to the left of the target node
        current_node = node.h_prev
        self.__detach_left_right(current_node, True)
        # detach the nodes to the right of the target node
        current_node = node.h_next
        self.__detach_left_right(current_node, False)

    def __detach_left_right(self, current_node, is_left):
        """
            - an auxiliary method that traverses the left and right nodes of the target node and detached them from the list

            :param current_node: the starting node to be detached
            :type current_node: Node
            :param is_left: True if we have to traverse the left nodes and False if we have to traverse the right nodes
            :type is_left: bool
        """
        while current_node is not None:
            if current_node.v_prev is None:
                current_node.head.node = current_node.v_next
            if current_node.v_prev is not None:
                current_node.v_prev.v_next = current_node.v_next
            if current_node.v_next is not None:
                current_node.v_next.v_prev = current_node.v_prev
            # decrement the size of the number of nodes in the column head of this node
            current_node.head.nodes -= 1
            if is_left:
                # move leftwards
                current_node = current_node.h_prev
            else:
                # move rightwards
               current_node = current_node.h_next

    def reattach_row(self, node):
        """
            - given the node, the method reattaches all nodes previously in the given row

            :param node: the node whose row is to be reattached.
            :type node: Node
        """
        # reattach the nodes to the left of the target node
        current_node = node.h_prev
        self.__reattach_left_right(current_node, True)
        # reattach the nodes to the right of the target node
        current_node = node.h_next
        self.__reattach_left_right(current_node, False)

    def __reattach_left_right(self, current_node, is_left):
        """
            - an auxiliary method which traverses all the nodes in the given row and reestablishes the connection

            :param current_node: the starting node to be reattached
            :type current_node: Node
            :param is_left: traverses the list leftwards if true, right otherwise
            :type is_left: bool
        """
        while current_node is not None:
            if current_node.v_prev is None:
                current_node.head.node = current_node
            if current_node.v_prev is not None:
                current_node.v_prev.v_next = current_node
            if current_node.v_next is not None:
                current_node.v_next.v_prev = current_node
            # increment the size of the number of nodes in the column head of this node
            current_node.head.nodes += 1
            if is_left:
                # move leftwards
                current_node = current_node.h_prev
            else:
                # move rightwards
               current_node = current_node.h_next

    def get_all_row_heads(self, node):
        """
            - scans the row in the given node and returns the column heads of the columns where 1 exists

            :param node: the node whose row has to be scanned
            :type node: Node
            :return: a list of column heads
            :rtype: list
        """
        heads = [node.head] # stores all the required heads
        # heads on the left side of the node
        current_node = node.h_prev
        while current_node is not None:
            heads.append(current_node.head)
            current_node = current_node.h_prev
        # heads on the right side of the node
        current_node = node.h_next
        while current_node is not None:
            heads.append(current_node.head)
            current_node = current_node.h_next
        return heads

    def complete_column_row_deletion(self, node):
        """
            - given a node, the method deletes its respective column followed by deleting all rows with a 1 in this column,
            - it then traverses this node's row and deletes all columns with a 1 and their respective rows with a 1 keeping
            - record of all deleted columns and rows to be used in case the deletion is to be undone.

            :param node: the reference node
            :type node: Node
            :return: a 2-dimensional array of the deleted nodes, each entry containing the column head at the zeroth index and a list of the detached nodes in the second index, ex: [[head, [nodes1, node2]], [head3, [node4, node7]]]
            :rtype: list
        """
        heads = self.get_all_row_heads(node)
        restoration_list = []
        for head in heads:
            column_row_deleted = []
            detached_nodes = self.detach_column(head)
            # add the column head in the zeroth index
            column_row_deleted.append(head)
            # add the detached nodes in the second index
            column_row_deleted.append(detached_nodes)
            for node in detached_nodes:
                self.detach_row(node)
            restoration_list.append(column_row_deleted)
        return restoration_list

    def complete_column_row_restoration(self, restoration_list):
        """
            - given the list used in the previous complete deletion, the method reestablishes all the links
            - reataching nodes takes place in the reverse order the nodes rows and columns were deleted, LIFO

            :param restoration_list: a 2-dimensional array used to restore the deleted connections
            :type restoration_list: list
        """

        # reverse the main list so reattaching is done in reverse order
        for item in reversed(restoration_list):
            column_node = item[0]
            # reverse the order the rows were deleted so the row removed last is added first
            for row_node in reversed(item[1]):
                self.reattach_row(row_node)
            self.reattach_column(column_node)

    def get_min_nodes_head(self):
        """
            - finds the column with the minimum number of nodes, i.e 1's and returns its head

            :return: the column head with at least one node and with the minimum number of nodes, if all heads have zero nodes it returns None
            :rtype: Head
        """
        if self.head == None:
            return None
        head = self.head
        current_head = head.next
        while current_head is not None:
            if current_head.nodes > 0:
                if head.nodes == 0 or current_head.nodes < head.nodes:
                    head = current_head
            current_head = current_head.next
        if head.nodes > 0:
            return head
        return None
