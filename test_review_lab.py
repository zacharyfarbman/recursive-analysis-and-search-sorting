#
#   Unit tests for review_lab.py (quiz review: searching, merge sort, linked lists).
#   Run with Python 3:
#       python test_review_lab.py
#       python -m unittest -v test_review_lab
#       python -m unittest -v test_review_lab.SinglyLinkedTestCase
#

import math
import os
import random
import sys
import unittest

import review_lab
from review_lab import (
    linear_search,
    recursive_linear_search,
    binary_search,
    recursive_binary_search,
    binary_search_first,
    merge,
    recursive_merge_sort,
    merge_sort,
    SinglyLinked,
    DoublyLinked,
    merge_sorted_lists,
)


# =====================================================================================
# Helpers
# =====================================================================================

MAX_NODES = 10000
LAB_FILE = os.path.abspath(review_lab.__file__)


class CountingList(list):
    """A Python list that counts how many elements are read from it.

    Used to check that binary searches really are O(log n). It also stops a
    search that is stuck in an infinite loop, so the test fails instead of hanging.
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.reads = 0
        self.max_reads = 20 * len(self) + 100

    def _count(self, amount):
        self.reads += amount
        if self.reads > self.max_reads:
            raise AssertionError(
                "Read the list more than {} times: is your search stuck in an infinite loop?".format(
                    self.max_reads))

    def __getitem__(self, index):
        if isinstance(index, slice):
            self._count(len(range(*index.indices(len(self)))))
        else:
            self._count(1)
        return super().__getitem__(index)

    def __iter__(self):
        for i in range(len(self)):
            self._count(1)
            yield super().__getitem__(i)

    def __contains__(self, item):
        self._count(len(self))
        return super().__contains__(item)

    def index(self, *args):
        self._count(len(self))
        return super().index(*args)

    def count(self, item):
        self._count(len(self))
        return super().count(item)


def read_limit(n):
    """A generous number of reads for an O(log n) search on n elements."""
    if n <= 1:
        return 4
    return 4 * (int(math.log2(n)) + 1) + 4


def max_call_depth(func, *args):
    """Call func(*args) and return (result, deepest stack of review_lab.py calls)."""
    depth = 0
    deepest = 0
    known = {}

    def profiler(frame, event, arg):
        nonlocal depth, deepest
        filename = frame.f_code.co_filename
        if filename not in known:
            known[filename] = os.path.abspath(filename) == LAB_FILE
        if not known[filename]:
            return
        if event == "call":
            depth += 1
            deepest = max(deepest, depth)
        elif event == "return":
            depth -= 1

    old_profiler = sys.getprofile()
    sys.setprofile(profiler)
    try:
        result = func(*args)
    finally:
        sys.setprofile(old_profiler)
    return result, deepest


class Record:
    """A value compared only by key. tag records the original position (for stability)."""

    def __init__(self, key, tag):
        self.key = key
        self.tag = tag

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key

    def __gt__(self, other):
        return self.key > other.key

    def __ge__(self, other):
        return self.key >= other.key

    def __eq__(self, other):
        return self.key == other.key

    __hash__ = None

    def __repr__(self):
        return "Record({}, {})".format(self.key, self.tag)


def make_singly(values):
    """Build a SinglyLinked list directly from nodes (doesn't depend on your push methods)."""
    lst = SinglyLinked()
    prev = None
    for value in values:
        node = SinglyLinked.Node(value)
        if prev is None:
            lst.front = node
        else:
            prev.next = node
        prev = node
    lst.back = prev
    return lst


def make_doubly(values):
    """Build a DoublyLinked list directly from nodes (doesn't depend on your push methods)."""
    lst = DoublyLinked()
    prev = None
    for value in values:
        node = DoublyLinked.Node(value, None, prev)
        if prev is None:
            lst.front = node
        else:
            prev.next = node
        prev = node
    lst.back = prev
    return lst


def forward_nodes(lst):
    """Walk from front following next links. Returns the list of nodes."""
    nodes = []
    curr = lst.get_front()
    while curr is not None:
        nodes.append(curr)
        if len(nodes) > MAX_NODES:
            raise AssertionError(
                "Walked more than {} nodes from front: is there a cycle in your next links?".format(MAX_NODES))
        curr = curr.get_next()
    return nodes


def backward_nodes(lst):
    """Walk from back following prev links. Returns the list of nodes."""
    nodes = []
    curr = lst.get_back()
    while curr is not None:
        nodes.append(curr)
        if len(nodes) > MAX_NODES:
            raise AssertionError(
                "Walked more than {} nodes from back: is there a cycle in your prev links?".format(MAX_NODES))
        curr = curr.get_previous()
    return nodes


def values_of(nodes):
    return [node.get_data() for node in nodes]


class LinkedListAssertions(unittest.TestCase):
    """Shared checks that the whole structure of a list is valid, not just its values."""

    def check_singly(self, lst, expected):
        nodes = forward_nodes(lst)
        self.assertEqual(values_of(nodes), expected, "values walking front to back")
        if not expected:
            self.assertIsNone(lst.get_front(), "front should be None for an empty list")
            self.assertIsNone(lst.get_back(), "back should be None for an empty list")
        else:
            self.assertIs(lst.get_back(), nodes[-1], "back should be the last node reached from front")
            self.assertIsNone(lst.get_back().get_next(), "back.next should be None")

    def check_doubly(self, lst, expected):
        forward = forward_nodes(lst)
        self.assertEqual(values_of(forward), expected, "values walking front to back (next links)")
        backward = backward_nodes(lst)
        self.assertEqual(values_of(backward), list(reversed(expected)),
                         "values walking back to front (prev links)")
        if not expected:
            self.assertIsNone(lst.get_front(), "front should be None for an empty list")
            self.assertIsNone(lst.get_back(), "back should be None for an empty list")
        else:
            self.assertIsNone(lst.get_front().get_previous(), "front.prev should be None")
            self.assertIsNone(lst.get_back().get_next(), "back.next should be None")
            self.assertIs(lst.get_back(), forward[-1], "back should be the last node reached from front")
            self.assertIs(lst.get_front(), backward[-1], "front should be the last node reached from back")
            for node in forward[:-1]:
                self.assertIs(node.get_next().get_previous(), node,
                              "node.next.prev should be node (data {})".format(node.get_data()))


# =====================================================================================
# Part E1 - Searching
# =====================================================================================

class LinearSearchTestCase(unittest.TestCase):

    def setUp(self):
        self.data = [5, 3, 9, 3, 1, 12, 9]

    def test_linear_search_found(self):
        self.assertEqual(linear_search(self.data, 5), 0)
        self.assertEqual(linear_search(self.data, 3), 1)   # first occurrence
        self.assertEqual(linear_search(self.data, 9), 2)   # first occurrence
        self.assertEqual(linear_search(self.data, 1), 4)
        self.assertEqual(linear_search(self.data, 12), 5)

    def test_linear_search_not_found(self):
        self.assertEqual(linear_search(self.data, 7), -1)
        self.assertEqual(linear_search(self.data, 0), -1)
        self.assertEqual(linear_search([], 7), -1)

    def test_linear_search_other_types(self):
        words = ["pear", "apple", "fig", "apple"]
        self.assertEqual(linear_search(words, "apple"), 1)
        self.assertEqual(linear_search(words, "kiwi"), -1)

    def test_recursive_linear_search_found(self):
        self.assertEqual(recursive_linear_search(self.data, 5), 0)
        self.assertEqual(recursive_linear_search(self.data, 3), 1)
        self.assertEqual(recursive_linear_search(self.data, 9), 2)
        self.assertEqual(recursive_linear_search(self.data, 1), 4)
        self.assertEqual(recursive_linear_search(self.data, 12), 5)

    def test_recursive_linear_search_not_found(self):
        self.assertEqual(recursive_linear_search(self.data, 7), -1)
        self.assertEqual(recursive_linear_search([], 7), -1)
        self.assertEqual(recursive_linear_search([4], 7), -1)
        self.assertEqual(recursive_linear_search([4], 4), 0)

    def test_recursive_linear_search_is_recursive(self):
        data = list(range(50))
        result, depth = max_call_depth(recursive_linear_search, data, -1)
        self.assertEqual(result, -1)
        self.assertGreaterEqual(depth, 50,
                                "recursive_linear_search should make one recursive call per element")


class BinarySearchTestCase(unittest.TestCase):

    def setUp(self):
        self.data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

    def check_finds_every_element(self, search):
        for i, value in enumerate(self.data):
            self.assertEqual(search(CountingList(self.data), value), i, "searching for {}".format(value))

    def check_not_found(self, search):
        for key in [0, 1, 3, 13, 50, 60, 92, 1000]:
            self.assertEqual(search(CountingList(self.data), key), -1, "searching for {}".format(key))
        self.assertEqual(search(CountingList([]), 5), -1)
        self.assertEqual(search(CountingList([5]), 5), 0)
        self.assertEqual(search(CountingList([5]), 4), -1)
        self.assertEqual(search(CountingList([5]), 6), -1)
        self.assertEqual(search(CountingList([3, 7]), 3), 0)
        self.assertEqual(search(CountingList([3, 7]), 7), 1)
        self.assertEqual(search(CountingList([3, 7]), 5), -1)

    def check_duplicates(self, search):
        data = [1, 2, 2, 2, 3, 5, 5, 8]
        for key in [2, 5]:
            index = search(CountingList(data), key)
            self.assertNotEqual(index, -1, "searching for {}".format(key))
            self.assertEqual(data[index], key, "searching for {}".format(key))

    def check_log_reads(self, search):
        n = 1000
        data = CountingList(range(0, 2 * n, 2))   # 0, 2, 4, ..., 1998
        keys = [0, 2, 998, 1000, 1996, 1998, -1, 1, 999, 1999, 5000]
        for key in keys:
            data.reads = 0
            expected = key // 2 if 0 <= key < 2 * n and key % 2 == 0 else -1
            self.assertEqual(search(data, key), expected, "searching for {}".format(key))
            self.assertLessEqual(data.reads, read_limit(n),
                                 "searching for {} read the list {} times: that isn't O(log n)".format(
                                     key, data.reads))

    def test_binary_search_found(self):
        self.check_finds_every_element(binary_search)

    def test_binary_search_not_found(self):
        self.check_not_found(binary_search)

    def test_binary_search_duplicates(self):
        self.check_duplicates(binary_search)

    def test_binary_search_is_log_n(self):
        self.check_log_reads(binary_search)

    def test_recursive_binary_search_found(self):
        self.check_finds_every_element(recursive_binary_search)

    def test_recursive_binary_search_not_found(self):
        self.check_not_found(recursive_binary_search)

    def test_recursive_binary_search_duplicates(self):
        self.check_duplicates(recursive_binary_search)

    def test_recursive_binary_search_is_log_n(self):
        self.check_log_reads(recursive_binary_search)

    def test_recursive_binary_search_is_recursive(self):
        data = list(range(1024))
        result, depth = max_call_depth(recursive_binary_search, data, -5)
        self.assertEqual(result, -1)
        self.assertGreaterEqual(depth, 8,
                                "recursive_binary_search should recurse about log2(n) levels deep")

    def test_binary_search_first_duplicates(self):
        data = [1, 2, 2, 2, 3, 5, 5, 8]
        self.assertEqual(binary_search_first(CountingList(data), 1), 0)
        self.assertEqual(binary_search_first(CountingList(data), 2), 1)
        self.assertEqual(binary_search_first(CountingList(data), 3), 4)
        self.assertEqual(binary_search_first(CountingList(data), 5), 5)
        self.assertEqual(binary_search_first(CountingList(data), 8), 7)

    def test_binary_search_first_not_found(self):
        data = [1, 2, 2, 2, 3, 5, 5, 8]
        for key in [0, 4, 6, 9]:
            self.assertEqual(binary_search_first(CountingList(data), key), -1, "searching for {}".format(key))
        self.assertEqual(binary_search_first(CountingList([]), 3), -1)
        self.assertEqual(binary_search_first(CountingList([3]), 3), 0)
        self.assertEqual(binary_search_first(CountingList([3]), 4), -1)

    def test_binary_search_first_no_duplicates(self):
        self.check_finds_every_element(binary_search_first)

    def test_binary_search_first_all_same_is_log_n(self):
        n = 1000
        cases = [
            ([7] * n, 7, 0),
            ([7] * (n - 1) + [8], 8, n - 1),
            ([1] + [7] * (n - 1), 7, 1),
            ([1] * (n // 2) + [7] * (n // 2), 7, n // 2),
            ([7] * n, 8, -1),
        ]
        for values, key, expected in cases:
            data = CountingList(values)
            self.assertEqual(binary_search_first(data, key), expected)
            self.assertLessEqual(data.reads, read_limit(n),
                                 "binary_search_first read the list {} times: that isn't O(log n)".format(
                                     data.reads))


# =====================================================================================
# Part E2 - Sorting
# =====================================================================================

class MergeSortTestCase(unittest.TestCase):

    def test_merge_basic(self):
        data = [1, 4, 7, 2, 3, 9]
        merge(data, 0, 3, 5, [None] * len(data))
        self.assertEqual(data, [1, 2, 3, 4, 7, 9])

    def test_merge_one_run_runs_out_first(self):
        data = [1, 2, 3, 10, 11]
        merge(data, 0, 3, 4, [None] * len(data))
        self.assertEqual(data, [1, 2, 3, 10, 11])

        data = [10, 11, 1, 2, 3]
        merge(data, 0, 2, 4, [None] * len(data))
        self.assertEqual(data, [1, 2, 3, 10, 11])

    def test_merge_single_elements(self):
        data = [9, 4]
        merge(data, 0, 1, 1, [None] * len(data))
        self.assertEqual(data, [4, 9])

    def test_merge_only_touches_its_range(self):
        data = [99, 3, 8, 1, 5, -1]
        merge(data, 1, 3, 4, [None] * len(data))
        self.assertEqual(data, [99, 1, 3, 5, 8, -1])

    def test_merge_is_stable(self):
        data = [Record(1, "a0"), Record(2, "a1"), Record(2, "a2"),
                Record(1, "b0"), Record(2, "b1"), Record(3, "b2")]
        merge(data, 0, 3, 5, [None] * len(data))
        self.assertEqual([r.tag for r in data], ["a0", "b0", "a1", "a2", "b1", "b2"])

    def test_recursive_merge_sort_only_touches_its_range(self):
        data = [9, 7, 5, 3, 1, 0]
        recursive_merge_sort(data, 1, 4, [None] * len(data))
        self.assertEqual(data, [9, 1, 3, 5, 7, 0])

    def test_merge_sort_small_cases(self):
        for values in [[], [1], [2, 1], [1, 2], [3, 3, 3], [3, 1, 2]]:
            data = list(values)
            merge_sort(data)
            self.assertEqual(data, sorted(values), "sorting {}".format(values))

    def test_merge_sort_trace_example(self):
        data = [38, 27, 43, 3, 9, 82, 10]
        merge_sort(data)
        self.assertEqual(data, [3, 9, 10, 27, 38, 43, 82])

    def test_merge_sort_sorted_and_reversed(self):
        data = list(range(20))
        merge_sort(data)
        self.assertEqual(data, list(range(20)))

        data = list(range(20, 0, -1))
        merge_sort(data)
        self.assertEqual(data, list(range(1, 21)))

    def test_merge_sort_random(self):
        rng = random.Random(1337)
        for size in [5, 16, 17, 100, 501]:
            values = [rng.randint(-50, 50) for _ in range(size)]
            data = list(values)
            merge_sort(data)
            self.assertEqual(data, sorted(values), "sorting a random list of size {}".format(size))

    def test_merge_sort_strings(self):
        data = ["pear", "apple", "fig", "banana", "apple"]
        merge_sort(data)
        self.assertEqual(data, ["apple", "apple", "banana", "fig", "pear"])

    def test_merge_sort_is_in_place(self):
        data = [5, 2, 4, 1, 3]
        same_object = data
        merge_sort(data)
        self.assertIs(data, same_object)
        self.assertEqual(same_object, [1, 2, 3, 4, 5])

    def test_merge_sort_is_stable(self):
        rng = random.Random(42)
        keys = [rng.randint(0, 5) for _ in range(60)]
        data = [Record(key, i) for i, key in enumerate(keys)]
        merge_sort(data)
        self.assertEqual([r.key for r in data], sorted(keys))
        for left, right in zip(data, data[1:]):
            if left.key == right.key:
                self.assertLess(left.tag, right.tag,
                                "equal keys changed order: merge sort should be stable")

    def test_merge_sort_is_recursive(self):
        data = list(range(64, 0, -1))
        _, depth = max_call_depth(merge_sort, data)
        self.assertEqual(data, list(range(1, 65)))
        self.assertGreaterEqual(depth, 6, "merge_sort should recurse about log2(n) levels deep")


# =====================================================================================
# Part E3 - Singly linked list
# =====================================================================================

class SinglyLinkedTestCase(LinkedListAssertions):

    def test_init(self):
        lst = SinglyLinked()
        self.assertIsNone(lst.get_front())
        self.assertIsNone(lst.get_back())

    def test_push_front(self):
        lst = SinglyLinked()
        lst.push_front(1)
        self.check_singly(lst, [1])
        self.assertIs(lst.get_front(), lst.get_back())
        lst.push_front(5)
        self.check_singly(lst, [5, 1])
        lst.push_front(3)
        self.check_singly(lst, [3, 5, 1])

    def test_push_back(self):
        lst = SinglyLinked()
        lst.push_back(1)
        self.check_singly(lst, [1])
        self.assertIs(lst.get_front(), lst.get_back())
        lst.push_back(5)
        self.check_singly(lst, [1, 5])
        lst.push_back(3)
        self.check_singly(lst, [1, 5, 3])

    def test_push_mixed(self):
        lst = SinglyLinked()
        lst.push_back(2)
        lst.push_front(1)
        lst.push_back(3)
        lst.push_front(0)
        self.check_singly(lst, [0, 1, 2, 3])

    def test_pop_front(self):
        lst = make_singly([31, 15, 24, 9])
        self.assertEqual(lst.pop_front(), 31)
        self.check_singly(lst, [15, 24, 9])
        self.assertEqual(lst.pop_front(), 15)
        self.check_singly(lst, [24, 9])
        self.assertEqual(lst.pop_front(), 24)
        self.check_singly(lst, [9])
        self.assertEqual(lst.pop_front(), 9)
        self.check_singly(lst, [])
        with self.assertRaises(IndexError) as cm:
            lst.pop_front()
        self.assertEqual(str(cm.exception), "pop_front() used on empty list")

    def test_pop_back(self):
        lst = make_singly([31, 15, 24, 9])
        self.assertEqual(lst.pop_back(), 9)
        self.check_singly(lst, [31, 15, 24])
        self.assertEqual(lst.pop_back(), 24)
        self.check_singly(lst, [31, 15])
        self.assertEqual(lst.pop_back(), 15)
        self.check_singly(lst, [31])
        self.assertEqual(lst.pop_back(), 31)
        self.check_singly(lst, [])
        with self.assertRaises(IndexError) as cm:
            lst.pop_back()
        self.assertEqual(str(cm.exception), "pop_back() used on empty list")

    def test_reuse_after_emptying(self):
        lst = SinglyLinked()
        lst.push_back(1)
        lst.pop_back()
        lst.push_back(2)
        self.check_singly(lst, [2])
        lst.pop_front()
        lst.push_front(3)
        lst.push_back(4)
        self.check_singly(lst, [3, 4])

    def test_search(self):
        lst = make_singly([4, 8, 15, 8, 23])
        node = lst.search(8)
        self.assertIsNotNone(node)
        self.assertEqual(node.get_data(), 8)
        self.assertIs(node, lst.get_front().get_next(), "search should return the first matching node")
        self.assertIs(lst.search(4), lst.get_front())
        self.assertIs(lst.search(23), lst.get_back())
        self.assertIsNone(lst.search(42))
        self.assertIsNone(SinglyLinked().search(1))

    def test_remove_front_middle_back(self):
        lst = make_singly([1, 2, 3, 4, 5])
        self.assertIs(lst.remove(1), True)
        self.check_singly(lst, [2, 3, 4, 5])
        self.assertIs(lst.remove(4), True)
        self.check_singly(lst, [2, 3, 5])
        self.assertIs(lst.remove(5), True)
        self.check_singly(lst, [2, 3])

    def test_remove_only_node(self):
        lst = make_singly([7])
        self.assertIs(lst.remove(7), True)
        self.check_singly(lst, [])

    def test_remove_not_found(self):
        lst = make_singly([1, 2, 3])
        self.assertIs(lst.remove(9), False)
        self.check_singly(lst, [1, 2, 3])
        self.assertIs(SinglyLinked().remove(9), False)

    def test_remove_first_occurrence_only(self):
        lst = make_singly([6, 1, 6, 2, 6])
        self.assertIs(lst.remove(6), True)
        self.check_singly(lst, [1, 6, 2, 6])
        self.assertIs(lst.remove(6), True)
        self.check_singly(lst, [1, 2, 6])
        self.assertIs(lst.remove(6), True)
        self.check_singly(lst, [1, 2])
        self.assertIs(lst.remove(6), False)

    def test_reverse(self):
        lst = SinglyLinked()
        lst.reverse()
        self.check_singly(lst, [])

        lst = make_singly([1])
        lst.reverse()
        self.check_singly(lst, [1])

        lst = make_singly([1, 2])
        lst.reverse()
        self.check_singly(lst, [2, 1])

        lst = make_singly([1, 2, 3, 4, 5])
        lst.reverse()
        self.check_singly(lst, [5, 4, 3, 2, 1])
        lst.reverse()
        self.check_singly(lst, [1, 2, 3, 4, 5])

    def test_reverse_relinks_nodes(self):
        lst = make_singly(["a", "b", "c", "d"])
        before = forward_nodes(lst)
        lst.reverse()
        after = forward_nodes(lst)
        self.assertEqual(len(after), len(before))
        for old, new in zip(reversed(before), after):
            self.assertIs(old, new, "reverse should relink the same node objects, not copy data")

    def test_len(self):
        self.assertEqual(len(SinglyLinked()), 0)
        self.assertEqual(len(make_singly([1])), 1)
        self.assertEqual(len(make_singly([1, 2, 3, 4, 5])), 5)


# =====================================================================================
# Part E4 - Doubly linked list
# =====================================================================================

class DoublyLinkedTestCase(LinkedListAssertions):

    def test_init(self):
        lst = DoublyLinked()
        self.assertIsNone(lst.get_front())
        self.assertIsNone(lst.get_back())

    def test_push_front(self):
        lst = DoublyLinked()
        lst.push_front(1)
        self.check_doubly(lst, [1])
        self.assertIs(lst.get_front(), lst.get_back())
        lst.push_front(5)
        self.check_doubly(lst, [5, 1])
        lst.push_front(3)
        self.check_doubly(lst, [3, 5, 1])
        lst.push_front(15)
        self.check_doubly(lst, [15, 3, 5, 1])

    def test_push_back(self):
        lst = DoublyLinked()
        lst.push_back(1)
        self.check_doubly(lst, [1])
        self.assertIs(lst.get_front(), lst.get_back())
        lst.push_back(5)
        self.check_doubly(lst, [1, 5])
        lst.push_back(3)
        self.check_doubly(lst, [1, 5, 3])
        lst.push_back(15)
        self.check_doubly(lst, [1, 5, 3, 15])

    def test_push_mixed(self):
        lst = DoublyLinked()
        lst.push_back(2)
        lst.push_front(1)
        lst.push_back(3)
        lst.push_front(0)
        self.check_doubly(lst, [0, 1, 2, 3])

    def test_pop_front(self):
        lst = make_doubly([31, 15, 24, 9])
        self.assertEqual(lst.pop_front(), 31)
        self.check_doubly(lst, [15, 24, 9])
        self.assertEqual(lst.pop_front(), 15)
        self.check_doubly(lst, [24, 9])
        self.assertEqual(lst.pop_front(), 24)
        self.check_doubly(lst, [9])
        self.assertEqual(lst.pop_front(), 9)
        self.check_doubly(lst, [])
        with self.assertRaises(IndexError) as cm:
            lst.pop_front()
        self.assertEqual(str(cm.exception), "pop_front() used on empty list")

    def test_pop_back(self):
        lst = make_doubly([31, 15, 24, 9])
        self.assertEqual(lst.pop_back(), 9)
        self.check_doubly(lst, [31, 15, 24])
        self.assertEqual(lst.pop_back(), 24)
        self.check_doubly(lst, [31, 15])
        self.assertEqual(lst.pop_back(), 15)
        self.check_doubly(lst, [31])
        self.assertEqual(lst.pop_back(), 31)
        self.check_doubly(lst, [])
        with self.assertRaises(IndexError) as cm:
            lst.pop_back()
        self.assertEqual(str(cm.exception), "pop_back() used on empty list")

    def test_trace_example(self):
        # The sequence from Part C3 of the worksheet.
        lst = DoublyLinked()
        lst.push_front(4)
        lst.push_back(7)
        lst.push_front(1)
        a = lst.pop_back()
        lst.push_back(9)
        lst.push_front(6)
        b = lst.pop_front()
        self.assertEqual(a, 7)
        self.assertEqual(b, 6)
        self.check_doubly(lst, [1, 4, 9])

    def test_reuse_after_emptying(self):
        lst = DoublyLinked()
        lst.push_back(1)
        lst.pop_front()
        lst.push_back(2)
        self.check_doubly(lst, [2])
        lst.pop_back()
        lst.push_front(3)
        lst.push_back(4)
        self.check_doubly(lst, [3, 4])

    def test_search(self):
        lst = make_doubly([4, 8, 15, 8, 23])
        node = lst.search(8)
        self.assertIsNotNone(node)
        self.assertEqual(node.get_data(), 8)
        self.assertIs(node, lst.get_front().get_next(), "search should return the first matching node")
        self.assertIs(lst.search(4), lst.get_front())
        self.assertIs(lst.search(23), lst.get_back())
        self.assertIsNone(lst.search(42))
        self.assertIsNone(DoublyLinked().search(1))

    def test_insert_after_middle(self):
        lst = make_doubly([1, 2, 4])
        lst.insert_after(lst.search(2), 3)
        self.check_doubly(lst, [1, 2, 3, 4])

    def test_insert_after_front(self):
        lst = make_doubly([1, 3])
        lst.insert_after(lst.get_front(), 2)
        self.check_doubly(lst, [1, 2, 3])

    def test_insert_after_back(self):
        lst = make_doubly([1, 2])
        lst.insert_after(lst.get_back(), 3)
        self.check_doubly(lst, [1, 2, 3])
        lst.insert_after(lst.get_back(), 4)
        self.check_doubly(lst, [1, 2, 3, 4])

    def test_insert_after_only_node(self):
        lst = make_doubly([1])
        lst.insert_after(lst.get_front(), 2)
        self.check_doubly(lst, [1, 2])

    def test_remove_node_middle(self):
        lst = make_doubly([1, 2, 3, 4])
        self.assertEqual(lst.remove_node(lst.search(3)), 3)
        self.check_doubly(lst, [1, 2, 4])

    def test_remove_node_front(self):
        lst = make_doubly([1, 2, 3])
        self.assertEqual(lst.remove_node(lst.get_front()), 1)
        self.check_doubly(lst, [2, 3])

    def test_remove_node_back(self):
        lst = make_doubly([1, 2, 3])
        self.assertEqual(lst.remove_node(lst.get_back()), 3)
        self.check_doubly(lst, [1, 2])

    def test_remove_node_only(self):
        lst = make_doubly([7])
        self.assertEqual(lst.remove_node(lst.get_front()), 7)
        self.check_doubly(lst, [])

    def test_remove_node_until_empty(self):
        lst = make_doubly([1, 2, 3, 4, 5])
        self.assertEqual(lst.remove_node(lst.search(3)), 3)
        self.assertEqual(lst.remove_node(lst.get_back()), 5)
        self.assertEqual(lst.remove_node(lst.get_front()), 1)
        self.check_doubly(lst, [2, 4])
        self.assertEqual(lst.remove_node(lst.get_front()), 2)
        self.assertEqual(lst.remove_node(lst.get_front()), 4)
        self.check_doubly(lst, [])

    def test_reverse(self):
        lst = DoublyLinked()
        lst.reverse()
        self.check_doubly(lst, [])

        lst = make_doubly([1])
        lst.reverse()
        self.check_doubly(lst, [1])

        lst = make_doubly([1, 2])
        lst.reverse()
        self.check_doubly(lst, [2, 1])

        lst = make_doubly([1, 2, 3, 4, 5])
        lst.reverse()
        self.check_doubly(lst, [5, 4, 3, 2, 1])
        lst.reverse()
        self.check_doubly(lst, [1, 2, 3, 4, 5])

    def test_reverse_relinks_nodes(self):
        lst = make_doubly(["a", "b", "c", "d"])
        before = forward_nodes(lst)
        lst.reverse()
        after = forward_nodes(lst)
        self.assertEqual(len(after), len(before))
        for old, new in zip(reversed(before), after):
            self.assertIs(old, new, "reverse should relink the same node objects, not copy data")

    def test_len(self):
        self.assertEqual(len(DoublyLinked()), 0)
        self.assertEqual(len(make_doubly([1])), 1)
        self.assertEqual(len(make_doubly([1, 2, 3, 4, 5])), 5)


# =====================================================================================
# Part E5 - Putting it together
# =====================================================================================

class MergeSortedListsTestCase(LinkedListAssertions):

    def check_merge(self, a_values, b_values):
        list_a = make_singly(a_values)
        list_b = make_singly(b_values)
        a_nodes = forward_nodes(list_a)
        b_nodes = forward_nodes(list_b)

        result = merge_sorted_lists(list_a, list_b)

        self.assertIsInstance(result, SinglyLinked, "merge_sorted_lists should return a SinglyLinked list")
        self.assertIsNot(result, list_a)
        self.assertIsNot(result, list_b)
        self.check_singly(result, sorted(a_values + b_values))

        # The input lists must be unchanged, node for node.
        self.check_singly(list_a, a_values)
        self.check_singly(list_b, b_values)
        for old, now in zip(a_nodes, forward_nodes(list_a)):
            self.assertIs(old, now, "list_a was modified")
        for old, now in zip(b_nodes, forward_nodes(list_b)):
            self.assertIs(old, now, "list_b was modified")

    def test_interleaved(self):
        self.check_merge([1, 4, 7, 10], [2, 3, 8, 12])

    def test_different_lengths(self):
        self.check_merge([5], [1, 2, 3, 9, 11])
        self.check_merge([1, 2, 3, 9, 11], [5])

    def test_one_after_the_other(self):
        self.check_merge([1, 2, 3], [10, 20, 30])
        self.check_merge([10, 20, 30], [1, 2, 3])

    def test_duplicates(self):
        self.check_merge([1, 3, 3, 5], [3, 3, 4])

    def test_empty_inputs(self):
        self.check_merge([], [1, 2, 3])
        self.check_merge([1, 2, 3], [])
        self.check_merge([], [])


if __name__ == "__main__":
    unittest.main()
