
class BTNode(object):
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def get_value(self):
        return self.value


# This class is used to provide static values
class Value(object):
    value = 0

    def get_vlaue(self):
        return Value.value

    def set_value(self, item):
        Value.value = item
        return Value.value


class BTree(object):
    def __init__(self, root=None):
        self.root = root
        self.iter_queue = []
        self.deep = 0

    """
    Add a new element
    """

    def add(self, value):
        if self.root is None:
            self.root = BTNode(value)
        else:
            queue = list()
            queue.append(self.root)

            while len(queue) > 0:
                node = queue.pop(0)
                if not node.left:
                    node.left = BTNode(value)
                    return
                else:
                    queue.append(node.left)

                if not node.right:
                    node.right = BTNode(value)
                    return
                else:
                    queue.append(node.right)

    """
    Set an element with specific index / key (lst.set(1, 3))
    if applicable.In this case, I can only convert the bt
    tree into a list type and then modify the value in the list.
    """

    def set_element(self, pos, value):
        tmp_list = self.to_list()
        length = len(tmp_list)
        if pos < 0 or pos > length:
            return False
        else:
            tmp_list[pos] = value
            self.root = None
            self.from_list(tmp_list)
            return self

    """
    Parent method is used in reduce function and
    some of methods using the same idea
    """

    def parent(self, value):
        if self.root.value == value:
            return None
        """Use the stack to iterate all nodes"""
        queue = list()
        queue.append(self.root)
        while len(queue):
            """Get the first element of the tmp stack"""
            tmp = queue.pop(0)
            if tmp.left and tmp.left.value == value:
                return tmp
            if tmp.right and tmp.right.value == value:
                return tmp
            """push the value to stack"""
            if tmp.left is not None:
                queue.append(tmp.left)
            if tmp.right is not None:
                queue.append(tmp.right)
        return None

    """
    Remove an element by
    - value for sets value
    """

    def remove(self, value):
        if self.root is None:
            return False
        if self.root.value == value:
            self.root = None
            return True
        parent_node = self.parent(value)
        # If parent_node is not None
        if parent_node:
            # The parent_node of the deleted node has been found,
            # now just find the side that should be deleted
            if parent_node.left.value == value:
                delete_node = parent_node.left
            else:
                delete_node = parent_node.right
            # If we want to delete the node, we should
            # refactor the binary tree
            if delete_node.left is None:
                if parent_node.left.value == value:
                    parent_node.left = delete_node.right
                else:
                    parent_node.right = delete_node.right
                return True
            elif delete_node.right is None:
                if parent_node.left.value == value:
                    parent_node.left = delete_node.left
                else:
                    parent_node.right = delete_node.left
                return True
            # This is the most complicated case, the deleted
            # node has both left and right children
            else:
                # Previous node and next node are seen as temporary nodes
                pre_node = delete_node
                next_node = delete_node.right

                if next_node.left is None:
                    pre_node.right = next_node.right
                    next_node.left = delete_node.left
                    next_node.right = delete_node.right
                else:
                    while next_node.left:
                        pre_node = next_node
                        next_node = next_node.left
                    pre_node.left = next_node.right
                    next_node.left = delete_node.left
                    next_node.right = delete_node.right

                if parent_node.left.value == value:
                    parent_node.left = next_node
                else:
                    parent_node.right = next_node
                return True
            # Until here the node has been deleted and
            # the tree has been refactored
        else:
            return False

    """
    Access:
    - size (lst.size())
    - is member (lst.member(3))
    - reverse (lst.reverse() (if applicable)
    """

    def size(self):
        if self.root is None:
            return 0
        # Use recursive method
        left_sum = BTree(self.root.left).size()
        right_sum = BTree(self.root.right).size()
        # Exit conditions
        if left_sum == 0 and right_sum == 0:
            return 1
        elif left_sum == 0:
            return 1 + right_sum
        elif right_sum == 0:
            return 1 + left_sum
        else:
            return 1 + left_sum + right_sum

    # consistent with parent function idea
    def is_member(self, value) -> bool:
        if self.root.value == value:
            return True
        node_stack = list()
        node_stack.append(self.root)
        while len(node_stack):
            tmp = node_stack.pop(0)
            if tmp.left and tmp.left.value == value:
                return True
            if tmp.right and tmp.right.value == value:
                return True
            if tmp.left is not None:
                node_stack.append(tmp.left)
            if tmp.right is not None:
                node_stack.append(tmp.right)
        return False

    """
    Conversion from/to built-in list (you should avoid
    # of usage these function into your library):
    - from_list (lst.from_list([12, 99, 37]))
    - to_list (lst.to_list())
    """

    def from_list(self, lst):
        for index in range(len(lst)):
            self.add(lst[index])
        return self

    # consistent with size function idea
    def to_list(self):
        if self.root is None:
            return []
        else:
            left_lst = BTree(self.root.left).to_list()
            right_lst = BTree(self.root.right).to_list()
            # Exit conditions
            if left_lst is None and right_lst is None:
                return [self.root.value]
            if left_lst is None:
                return [self.root.value] + right_lst
            if right_lst is None:
                return left_lst + [self.root.value]
            return left_lst + [self.root.value] + right_lst

    """
    Filter data structure by specific predicate
    """

    def filter(self) -> list:
        lst = self.to_list()
        new_lst = []
        for i in range(len(lst)):
            if type(lst[i]) == int:
                new_lst.append(lst[i])
        return new_lst

    """
    Map structure by specific function
    """

    """
    Q: Can it be a source of undefined behavior?
    If yes — give an example and fix it, if not — proof it.
    """

    """
    A: From 6.15 of python documentation
        Python evaluates expressions from left to right.
        Notice that while evaluating an assignment, the right-hand
        side is evaluated before the left-hand side.

        So here the functions will be called in order from left to right.
        So any of the changes you will see will be due to the functions
        called from left to right.
    """

    def map(self, f):
        if self.root is None:
            return None
        queue = list()
        queue.append(self.root)
        while len(queue):
            tmp = queue.pop(0)
            # It's an undefined behavior here, if it happened in c or c++,
            # different compilers will be very different.
            val = Value()
            val.set_value(tmp.value)

            def h(x):
                x += 1
                val.set_value(x)
                return x

            def g(x):
                x *= 2
                val.set_value(x)
                return x

            # A detailed description is proved in mutable_test.py
            tmp.value = f(val.get_vlaue())
            if tmp.left is not None:
                queue.append(tmp.left)
            if tmp.right is not None:
                queue.append(tmp.right)
        return self

    """
    Reduce–process structure elements to
    build a return value by specific functions
    """

    # I have some doubts about this function,
    # is this to compress the elements?
    def reduce(self, f, initial_state=0):
        state = initial_state
        lst = self.to_list()
        # i = 0
        # while i < len(lst):
        #    state = f(state, lst[i])
        #    i += 1
        # Apparently for is better than while here
        for i in range(len(lst)):
            state = f(state, lst[i])
        return state

    """
    Data structure should be an iterator in Python style
    """

    def __iter__(self):
        if self.root is None:
            self.deep = 0
            return self
        self.iter_queue.append(self.root)
        self.deep += 1
        return self

    """
    An iterator object implements __next__,
    which is expected to return the next element of the
    iterable object that returned it,
    and to raise a StopIteration exception
    when no more elements are available.
    """

    def __next__(self):
        # signals "the end"
        if self.deep == 0:
            raise StopIteration
        # Add left and right subtrees to the queue
        if self.root.left is not None:
            self.iter_queue.append(self.root.left)
        if self.root.right is not None:
            self.iter_queue.append(self.root.right)
        nxt = self.iter_queue[self.deep - 1].value

        if self.deep < len(self.iter_queue):
            self.root = self.iter_queue[self.deep]
            self.deep += 1
        else:
            # iterator the last element
            self.root = self.iter_queue[0]
            self.deep = 0
        return nxt

    """
    Data structure should be a monoid and
    implement empty and concat methods
    """

    def empty(self):
        return None

    # According to my understanding, what this function
    # should return is the sum of two bt trees
    def concat(self, bt1, bt2):
        if not bt1:
            return bt2
        if not bt2:
            return bt1
        # return the new BT tree
        new_root = BTNode(bt1.value + bt2.value)
        new_root.left = self.concat(bt1.left, bt2.left)
        new_root.right = self.concat(bt1.right, bt2.right)
        return new_root