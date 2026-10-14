# Review Lab - Quiz Prep
#
# Complete the functions and classes below as described in review_lab.md (Part E).
# Do not change the required public function/method names or signatures.
# You may add your own helper functions or methods.
#
# Rules:
#   - Don't use Python's built-in searching or sorting: no list.index(), `in` on the
#     list, sorted(), list.sort(), min()/max() to search, or the bisect module.
#   - Linked lists must not use sentinel nodes, and must not store data in a Python list.
#   - Recursive problems must actually be recursive.
#
# Run the tests with:  python test_review_lab.py


# =====================================================================================
# Part E1 - Searching
# =====================================================================================


# Problem 1
def linear_search(my_list, key):
    """Iterative. Return the index of the first occurrence of key in my_list, or -1."""
    pass


# Problem 2
def recursive_linear_search(my_list, key):
    """Recursive. Return the index of the first occurrence of key in my_list, or -1.

    Write a recursive helper that takes an index parameter, and call it from here.
    """
    pass


# Problem 3
def binary_search(my_list, key):
    """Iterative. my_list is sorted ascending. Return an index of key, or -1.

    Must be O(log n).
    """
    pass


# Problem 4
def recursive_binary_search(my_list, key):
    """Recursive. my_list is sorted ascending. Return an index of key, or -1.

    Write a recursive helper that takes low_index and high_index, and call it
    from here. Don't slice the list.
    """
    pass


# Problem 5 (Challenge)
def binary_search_first(my_list, key):
    """my_list is sorted ascending and may contain duplicates.

    Return the index of the FIRST occurrence of key, or -1.
    Must be O(log n), even when every element in my_list equals key.
    """
    pass


# =====================================================================================
# Part E2 - Sorting
# =====================================================================================


# Problem 6a
def merge(my_list, a_first_index, b_first_index, b_last_index, empty_list):
    """Merge two sorted runs of my_list into one sorted run.

    Run a is my_list[a_first_index .. b_first_index - 1] (inclusive).
    Run b is my_list[b_first_index .. b_last_index] (inclusive).

    Use empty_list as temporary storage, then copy the merged result back into
    my_list[a_first_index .. b_last_index]. Nothing outside that range may change.
    Must be stable: when two values are equal, the one from run a comes first.
    """
    pass


# Problem 6b
def recursive_merge_sort(my_list, first_index, last_index, empty_list):
    """Sort my_list[first_index .. last_index] (inclusive) in place.

    Nothing outside that range may change.
    """
    pass


# Problem 6c
def merge_sort(my_list):
    """Sort my_list in place.

    Create the temporary list ONCE here, then call recursive_merge_sort.
    """
    pass


# =====================================================================================
# Part E3 - Singly linked list (front and back references, no sentinels)
# =====================================================================================


class SinglyLinked:

    class Node:
        def __init__(self, data, next=None):
            self.data = data
            self.next = next

        def get_data(self):
            return self.data

        def get_next(self):
            return self.next

    def __init__(self):
        self.front = None
        self.back = None

    def get_front(self):
        return self.front

    def get_back(self):
        return self.back

    # Problem 7a
    def push_front(self, data):
        """Add data to the front of the list. O(1)."""
        pass

    # Problem 7b
    def push_back(self, data):
        """Add data to the back of the list. O(1)."""
        pass

    # Problem 7c
    def pop_front(self):
        """Remove and return the front value. O(1).

        On an empty list, raise IndexError("pop_front() used on empty list").
        """
        pass

    # Problem 7d
    def pop_back(self):
        """Remove and return the back value.

        On an empty list, raise IndexError("pop_back() used on empty list").
        """
        pass

    # Problem 7e
    def search(self, key):
        """Return the node holding the first occurrence of key, or None."""
        pass

    # Problem 7f
    def remove(self, key):
        """Remove the first node holding key.

        Return True if a node was removed, False otherwise.
        Keep front and back correct.
        """
        pass

    # Problem 7g
    def reverse(self):
        """Reverse the list in place by relinking the existing nodes.

        Don't create new nodes or copy data between nodes.
        """
        pass

    # Problem 7h
    def __len__(self):
        """Return the number of nodes in the list."""
        pass


# =====================================================================================
# Part E4 - Doubly linked list (front and back references, no sentinels)
# =====================================================================================


class DoublyLinked:

    class Node:
        def __init__(self, data, next=None, prev=None):
            self.data = data
            self.next = next
            self.prev = prev

        def get_data(self):
            return self.data

        def get_next(self):
            return self.next

        def get_previous(self):
            return self.prev

    def __init__(self):
        self.front = None
        self.back = None

    def get_front(self):
        return self.front

    def get_back(self):
        return self.back

    # Problem 8a
    def push_front(self, data):
        """Add data to the front of the list. O(1)."""
        pass

    # Problem 8b
    def push_back(self, data):
        """Add data to the back of the list. O(1)."""
        pass

    # Problem 8c
    def pop_front(self):
        """Remove and return the front value. O(1).

        On an empty list, raise IndexError("pop_front() used on empty list").
        """
        pass

    # Problem 8d
    def pop_back(self):
        """Remove and return the back value. O(1).

        On an empty list, raise IndexError("pop_back() used on empty list").
        """
        pass

    # Problem 8e
    def search(self, key):
        """Return the node holding the first occurrence of key, or None."""
        pass

    # Problem 8f
    def insert_after(self, node, data):
        """Insert a new node holding data directly after node. O(1).

        node is guaranteed to be a node that is currently in this list.
        """
        pass

    # Problem 8g
    def remove_node(self, node):
        """Unlink node from the list and return its data. O(1).

        node is guaranteed to be a node that is currently in this list.
        """
        pass

    # Problem 8h
    def reverse(self):
        """Reverse the list in place by relinking the existing nodes.

        Don't create new nodes or copy data between nodes.
        """
        pass

    # Problem 8i
    def __len__(self):
        """Return the number of nodes in the list."""
        pass


# =====================================================================================
# Part E5 - Putting it together
# =====================================================================================


# Problem 9
def merge_sorted_lists(list_a, list_b):
    """list_a and list_b are SinglyLinked lists with values sorted ascending.

    Return a NEW SinglyLinked list holding every value from both lists, sorted
    ascending. Don't modify list_a or list_b.
    Must be O(n + m): walk both lists once, like merge. Don't copy the values
    into a Python list and sort them.
    """
    pass
