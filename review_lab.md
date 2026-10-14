# Review Lab - Quiz Prep

**Topics:** analysis of recursive functions, linear search, binary search, recursive merge sort, singly linked lists (no sentinels), doubly linked lists (no sentinels).

**Course resources:**

- Analysis of recursive functions: https://seneca-ictoer.github.io/data-structures-and-algorithms/C-Recursion/analysis-of-recursive-functions
- Searching: https://seneca-ictoer.github.io/data-structures-and-algorithms/D-Searching-And-Sorting/searching
- Merge sort: https://seneca-ictoer.github.io/data-structures-and-algorithms/D-Searching-And-Sorting/merge_sort
- Linked lists: https://seneca-ictoer.github.io/data-structures-and-algorithms/E-Lists/implementation-push-and-pop-front

**Files:**

| File | What it is |
| --- | --- |
| `review_lab.md` | This worksheet. Write your analysis, tables, traces, and answers here. |
| `review_lab.py` | Boilerplate for the coding problems (Part E). |
| `test_review_lab.py` | Unit tests for `review_lab.py`. |

Try to do everything without notes first, then check against the course pages. That is closest to quiz conditions.

---

## Part A - Recursive Analysis

Complete your analysis for each function below. Analyze the code exactly as provided, using the same method as the course notes:

1. Say what $n$ represents and what $T(n)$ represents.
2. Count operations line by line, writing each recursive call as $T(\text{smaller size})$.
3. Write the base case(s) and the recurrence.
4. Expand the recurrence until a pattern shows up, and figure out how many steps it takes to reach the base case.
5. Write the closed form and the Big-O.

State which case (best or worst) you are analyzing and why.

---

### Function 1 - Recursive linear search

Analyze `recursive_linear_search` with respect to the length of `my_list`.

```python
def recursive_linear_search(my_list, key, i):
    if i == len(my_list):
        return -1
    elif my_list[i] == key:
        return i
    else:
        return recursive_linear_search(my_list, key, i + 1)


def linear_search(my_list, key):
    return recursive_linear_search(my_list, key, 0)
```

> Things to decide: `i` changes on every call but `my_list` does not, so what should $n$ actually measure? What input makes the function do the most work?

### Your analysis

Let $n$ represent the length of `my_list`.

Let $T(n)$ represent the number of operations needed to return the index of `key` in `my_list`.

```python
def recursive_linear_search(my_list, key, i):
    if i == len(my_list):                                      # 2
        return -1                                              # 1
    elif my_list[i] == key:                                    # 2
        return i                                               # 1
    else:
        return recursive_linear_search(my_list, key, i + 1)    # 1 + T(n-1)


def linear_search(my_list, key):
    return recursive_linear_search(my_list, key, 0)            # T(n)
```

**Base case(s):**
If `my_list` is empty or the first value in `my_list` is the `key` or the only value in `my_list` is the `key`, then we do at most 3 operations:

```python
    if i == len(my_list):                                      # 2
        return -1                                              # 1
or
    elif my_list[i] == key:                                    # 2
        return i                                               # 1
```

Therefore, we have:

$$
\begin{aligned}
T(0) &= 2 + 1 = 3 \\ 
T(1) &= 2 + 1 = 3 
\end{aligned}
$$

**Recursive case:**
For our recursive case, we have $2 + 2 + 1 + T(n-1)$ operations:

```python
    if i == len(my_list):                                      # 2
        return -1                                              # 1
    elif my_list[i] == key:                                    # 2
        return i                                               # 1
    else:
        return recursive_linear_search(my_list, key, i + 1)    # 1 + T(n-1)
```

Therefore, we have:

$$
\begin{aligned}
T(n) &= 2 + 2 + 1 + T(n-1) \\
T(n) &= 5 + T(n-1)
\end{aligned}
$$

**Expansion:**
Since, $T(n) &= 5 + T(n-1)$, we have:

$$
\begin{aligned}
T(n) &= 5 + T(n-1) \\
T(n-1) &= 5 + T(n-2) \\
T(n-2) &= 5 + T(n-3) \\
... \\
T(1) &= 3
\end{aligned}
$$

There are a total of $(n-1)$ 5's. We know this because we need to reach $T(1)$ to get the 3.

**Closed form:**
Thus:

$$
\begin{aligned}
T(n) &= 5(n-1) + 3 \\
T(n) &= 5n - 2
\end{aligned}
$$

**Big-O:**
Therefore, $T(n)$ is $O(n)$.

---

### Function 2 - Recursive binary search

Analyze `recursive_binary_search` with respect to the length of `my_list`.

```python
def recursive_binary_search(my_list, key, low_index, high_index):
    if low_index > high_index:
        return -1
    mid_index = (low_index + high_index) // 2
    if key == my_list[mid_index]:
        return mid_index
    elif key < my_list[mid_index]:
        return recursive_binary_search(my_list, key, low_index, mid_index - 1)
    else:
        return recursive_binary_search(my_list, key, mid_index + 1, high_index)


def binary_search(my_list, key):
    return recursive_binary_search(my_list, key, 0, len(my_list) - 1)
```

> Things to decide: What is the size of the range still being searched, in terms of `low_index` and `high_index`? Which branch is the worst case: going left (one comparison) or going right (two comparisons)? When the key is not in the list, does the range shrink to size 1 or to size 0 before the function stops?

### Your analysis

Let $n$ represent

Let $T(n)$ represent

```python
def recursive_binary_search(my_list, key, low_index, high_index):
    if low_index > high_index:                                                    #
        return -1                                                                 #
    mid_index = (low_index + high_index) // 2                                     #
    if key == my_list[mid_index]:                                                 #
        return mid_index                                                          #
    elif key < my_list[mid_index]:                                                #
        return recursive_binary_search(my_list, key, low_index, mid_index - 1)    #
    else:
        return recursive_binary_search(my_list, key, mid_index + 1, high_index)   #


def binary_search(my_list, key):
    return recursive_binary_search(my_list, key, 0, len(my_list) - 1)             #
```

**Base case(s):**

**Recursive case:**

**Expansion:**

**Closed form:**

**Big-O:**

---

### Function 3 - The merge function (not recursive)

This is the course's `merge` function. Analyze it with respect to the total number of elements being merged, from `a_first_index` to `b_last_index` inclusive. You need this result for Function 4.

```python
def merge(mylist, a_first_index, b_first_index, b_last_index, empty_list):
    a_ptr = a_first_index
    b_ptr = b_first_index
    empty_list_index = a_ptr

    while (a_ptr < b_first_index) and (b_ptr <= b_last_index):
        if mylist[a_ptr] <= mylist[b_ptr]:
            empty_list[empty_list_index] = mylist[a_ptr]
            empty_list_index += 1
            a_ptr += 1
        else:
            empty_list[empty_list_index] = mylist[b_ptr]
            empty_list_index += 1
            b_ptr += 1

    while a_ptr < b_first_index:
        empty_list[empty_list_index] = mylist[a_ptr]
        empty_list_index += 1
        a_ptr += 1

    while b_ptr <= b_last_index:
        empty_list[empty_list_index] = mylist[b_ptr]
        empty_list_index += 1
        b_ptr += 1

    for i in range(a_first_index, b_last_index + 1):
        mylist[i] = empty_list[i]
```

> Things to decide: You don't know how many times each individual `while` loop runs, since it depends on the data. But every pass through any of the three loop bodies copies exactly one element into `empty_list`. So how many loop-body passes are there in total, across all three loops? How many times does the `for` loop run?

### Your analysis

Let $n$ represent

Let $T(n)$ represent

```python
def merge(mylist, a_first_index, b_first_index, b_last_index, empty_list):
    a_ptr = a_first_index                                            #
    b_ptr = b_first_index                                            #
    empty_list_index = a_ptr                                         #

    while (a_ptr < b_first_index) and (b_ptr <= b_last_index):       #
        if mylist[a_ptr] <= mylist[b_ptr]:                           #
            empty_list[empty_list_index] = mylist[a_ptr]             #
            empty_list_index += 1                                    #
            a_ptr += 1                                               #
        else:
            empty_list[empty_list_index] = mylist[b_ptr]             #
            empty_list_index += 1                                    #
            b_ptr += 1                                               #

    while a_ptr < b_first_index:                                     #
        empty_list[empty_list_index] = mylist[a_ptr]                 #
        empty_list_index += 1                                        #
        a_ptr += 1                                                   #

    while b_ptr <= b_last_index:                                     #
        empty_list[empty_list_index] = mylist[b_ptr]                 #
        empty_list_index += 1                                        #
        b_ptr += 1                                                   #

    for i in range(a_first_index, b_last_index + 1):                 #
        mylist[i] = empty_list[i]                                    #
```

**Total cost of the loops:**

**Formula for $T(n)$:**

**Big-O:**

---

### Function 4 - Recursive merge sort

Analyze `recursive_merge_sort` with respect to the number of elements from `first_index` to `last_index` inclusive. Use your result from Function 3 for the cost of the `merge` call. Then say what `merge_sort` adds on top.

```python
def recursive_merge_sort(mylist, first_index, last_index, empty_list):
    if first_index < last_index:
        mid_index = (first_index + last_index) // 2
        recursive_merge_sort(mylist, first_index, mid_index, empty_list)
        recursive_merge_sort(mylist, mid_index + 1, last_index, empty_list)
        merge(mylist, first_index, mid_index + 1, last_index, empty_list)


def merge_sort(mylist):
    empty_list = [0] * len(mylist)
    recursive_merge_sort(mylist, 0, len(mylist) - 1, empty_list)
```

> Things to decide: This function makes **two** recursive calls, each on about half the elements. When you expand, keep the coefficient in front of $T$ and track how much merge work is done in total at each level. For simplicity, you may assume $n$ is a power of 2. A recursion tree sketch (one row per level) is a good way to check your expansion.

### Your analysis

Let $n$ represent

Let $T(n)$ represent

```python
def recursive_merge_sort(mylist, first_index, last_index, empty_list):
    if first_index < last_index:                                              #
        mid_index = (first_index + last_index) // 2                           #
        recursive_merge_sort(mylist, first_index, mid_index, empty_list)      #
        recursive_merge_sort(mylist, mid_index + 1, last_index, empty_list)   #
        merge(mylist, first_index, mid_index + 1, last_index, empty_list)     #


def merge_sort(mylist):
    empty_list = [0] * len(mylist)                                            #
    recursive_merge_sort(mylist, 0, len(mylist) - 1, empty_list)              #
```

**Base case(s):**

**Recursive case:**

**Expansion:**

| Level | Number of calls | Size of each call | Total merge work at this level |
| --- | --- | --- | --- |
| 0 | | | |
| 1 | | | |
| 2 | | | |
| $k$ | | | |

**How many levels until the base case:**

**Closed form:**

**Big-O of `recursive_merge_sort`:**

**What `merge_sort` adds, and its overall Big-O:**

**Extra memory used (not counting the input list):**

---

### Function 5 - Recursion on a linked list

`node` is a node from a singly linked list (it has `get_data()` and `get_next()`). Analyze `count_matches` with respect to the number of nodes from `node` to the end of the list.

```python
def count_matches(node, key):
    if node is None:
        return 0
    elif node.get_data() == key:
        return 1 + count_matches(node.get_next(), key)
    else:
        return count_matches(node.get_next(), key)
```

> Things to decide: Unlike linear search, this function never stops early. So what makes one input worse than another?

### Your analysis

Let $n$ represent

Let $T(n)$ represent

```python
def count_matches(node, key):
    if node is None:                                      #
        return 0                                          #
    elif node.get_data() == key:                          #
        return 1 + count_matches(node.get_next(), key)    #
    else:
        return count_matches(node.get_next(), key)        #
```

**Base case(s):**

**Recursive case:**

**Expansion:**

**Closed form:**

**Big-O:**

---

### Function 6 (Challenge) - Two calls that don't halve

Analyze `double_trouble` with respect to `n`. Compare your answer to merge sort, which also makes two recursive calls.

```python
def double_trouble(n):
    if n <= 1:
        return 1
    else:
        return double_trouble(n - 1) + double_trouble(n - 1)
```

> Hint: $1 + 2 + 4 + \dots + 2^{k} = 2^{k+1} - 1$.

### Your analysis

Let $n$ represent

Let $T(n)$ represent

```python
def double_trouble(n):
    if n <= 1:                                                 #
        return 1                                               #
    else:
        return double_trouble(n - 1) + double_trouble(n - 1)   #
```

**Base case(s):**

**Recursive case:**

**Expansion:**

**Closed form:**

**Big-O:**

**Why is this so much worse than merge sort, even though both make two recursive calls?**

---

## Part B - Big-O Tables

Fill in each cell from memory, then check your answers.

### Table 1 - Searching and sorting

$n$ is the number of elements in the list.

| Algorithm | Best case | Worst case | Average case | Extra memory | Precondition on the list |
| --- | --- | --- | --- | --- | --- |
| Linear search (iterative) | | | | | |
| Linear search (recursive, Function 1) | | | | | |
| Binary search (iterative) | | | | | |
| Binary search (recursive, Function 2) | | | | | |
| Merge sort | | | | | |

### Table 2 - List operations

$n$ is the number of items. None of the linked lists use sentinel nodes. "Given node" means you already have a reference to the node.

| Operation | Singly linked (`front` only) | Singly linked (`front` and `back`) | Doubly linked (`front` and `back`) | Python list (array based) |
| --- | --- | --- | --- | --- |
| `push_front` | | | | |
| `push_back` | | | | |
| `pop_front` | | | | |
| `pop_back` | | | | |
| Search for a value | | | | |
| Insert after a given node / index | | | | |
| Remove a given node / index | | | | |
| Access the item at position $i$ | | | | |
| Binary search possible in $O(\log n)$? | | | | |

**Explain your answer for `pop_back` on a singly linked list with a `back` reference:**

**Explain your answer for "remove a given node" on a singly linked list vs a doubly linked list:**

---

## Part C - Tracing and Bug Hunting

### C1 - Binary search trace

Trace the course's iterative `binary_search` on this sorted list:

```python
my_list = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
#  index:  0  1  2   3   4   5   6   7   8   9
```

**Search for `key = 23`:**

| Iteration | `low_index` | `high_index` | `mid_index` | `my_list[mid_index]` | Result of comparison / what changes |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |

Return value:

**Search for `key = 60`:**

| Iteration | `low_index` | `high_index` | `mid_index` | `my_list[mid_index]` | Result of comparison / what changes |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |

Return value:

**What is the maximum number of iterations for a list of 10 elements? For a list of 1,000,000 elements? Show how you got it.**

---

### C2 - Merge sort trace

Trace the course's `merge_sort` on:

```python
mylist = [38, 27, 43, 3, 9, 82, 10]
#  index:   0   1   2  3  4   5   6
```

**(a)** List every call to `recursive_merge_sort` in the order it happens, as `(first_index, last_index)`. Mark which ones are base cases.

```text

```

**(b)** Every time `merge` runs, record its arguments and the full list right after it finishes. Add rows as needed.

| Merge # | `a_first_index` | `b_first_index` | `b_last_index` | `mylist` after this merge |
| --- | --- | --- | --- | --- |
| 1 | | | | |
| 2 | | | | |
| | | | | |

**(c)** How many times does `merge` run for a list of $n$ elements? Why?

**(d)** How deep does the recursion go for $n = 7$? For $n = 1{,}000{,}000$?

---

### C3 - Linked list trace

Start with an empty **doubly** linked list and run:

```python
dl = DoublyLinked()
dl.push_front(4)
dl.push_back(7)
dl.push_front(1)
a = dl.pop_back()
dl.push_back(9)
dl.push_front(6)
b = dl.pop_front()
```

Draw the list after **each** line. Show `front`, `back`, and every `next` and `prev` link (`None` included).

```text
after push_front(4):

after push_back(7):

after push_front(1):

after pop_back():

after push_back(9):

after push_front(6):

after pop_front():
```

Values of `a` and `b`:

Final list front to back:

Final list back to front:

---

### C4 - Bug hunt

Each function below has at least one bug. For each one:

- give a specific input or list state that breaks it, and say what goes wrong (wrong answer, crash, or infinite loop/recursion)
- write the fix

**Bug 1 - binary search**

```python
def binary_search(my_list, key):
    low_index = 0
    high_index = len(my_list) - 1
    while low_index < high_index:
        mid_index = high_index // 2
        if key == my_list[mid_index]:
            return mid_index
        elif key < my_list[mid_index]:
            high_index = mid_index - 1
        else:
            low_index = mid_index + 1
    return -1
```

Breaking input(s) and what happens:

Fix:

**Bug 2 - recursive merge sort**

```python
def recursive_merge_sort(mylist, first_index, last_index, empty_list):
    if first_index <= last_index:
        mid_index = (first_index + last_index) // 2
        recursive_merge_sort(mylist, first_index, mid_index, empty_list)
        recursive_merge_sort(mylist, mid_index + 1, last_index, empty_list)
        merge(mylist, first_index, mid_index + 1, last_index, empty_list)
```

Breaking input and what happens:

Fix:

**Bug 3 - `pop_back` on a singly linked list (with `front` and `back`)**

```python
def pop_back(self):
    if self.back is None:
        raise IndexError("pop_back() used on empty list")
    curr = self.front
    while curr.next is not self.back:
        curr = curr.next
    data = self.back.data
    curr.next = None
    self.back = curr
    return data
```

Breaking list state and what happens:

Fix:

**Bug 4 - `push_back` on a doubly linked list**

```python
def push_back(self, data):
    nn = self.Node(data, None, self.back)
    self.back.next = nn
    self.back = nn
```

Breaking list state and what happens:

Fix:

**Bug 5 - `pop_front` on a doubly linked list**

```python
def pop_front(self):
    if self.front is None:
        raise IndexError("pop_front() used on empty list")
    removed = self.front
    self.front = removed.next
    self.front.prev = None
    return removed.data
```

Breaking list state and what happens:

Fix:

---

## Part D - Concept Questions

Answer in a few sentences each.

1. Binary search has two preconditions. What are they, and why does each one matter? Why can't you get $O(\log n)$ binary search on a linked list?

2. You need to search an unsorted list of $n$ items $k$ times. When is it worth sorting it first with merge sort and then using binary search, versus doing $k$ linear searches? Give the total cost of each approach.

3. The course's `merge_sort` creates `empty_list` once and passes it down, instead of creating a temporary list inside `merge`. Why? What is the extra memory merge sort uses?

4. Is the course's merge sort stable? Which exact line decides this? What changes if `<=` becomes `<`?

5. Does merge sort have a different best case and worst case? Why or why not? Compare this to binary search.

6. Recursive and iterative binary search have the same time complexity. Do they use the same amount of memory? Explain.

7. Python's default recursion limit is about 1000 calls. What happens if you call the recursive linear search (Function 1) on a list of 5,000 items? Why is recursive merge sort on 5,000 items fine?

8. Without sentinel nodes, what special cases does every insert or remove need to handle? List them, and say which `front` / `back` updates each one needs.

9. In a doubly linked list, every change to a `next` link usually needs a matching change to a `prev` link. Using `insert_after(node, data)` as the example, list every link that has to change, and the order that keeps you from losing part of the list.

10. Why does a doubly linked list's `pop_back` run in $O(1)$ while a singly linked list's `pop_back` runs in $O(n)$, even when both have a `back` reference?

---

## Part E - Coding Problems

Complete the code in `review_lab.py`. Do not change the required function/method names or signatures. You may add your own helper functions or methods.

**Rules:**

- Don't use Python's built-in searching or sorting: no `list.index()`, `in` on the list, `sorted()`, `list.sort()`, `min()`/`max()` to search, or the `bisect` module.
- Linked lists must not use sentinel nodes, and must not store their data in a Python list.
- Recursive problems must actually be recursive.

**Run the tests:**

```bash
python test_review_lab.py            # all tests
python -m unittest -v test_review_lab # all tests, one line per test
python -m unittest -v test_review_lab.SinglyLinkedTestCase   # one group
```

Test groups: `LinearSearchTestCase`, `BinarySearchTestCase`, `MergeSortTestCase`, `SinglyLinkedTestCase`, `DoublyLinkedTestCase`, `MergeSortedListsTestCase`.

### Part E1 - Searching

| Problem | Function | Requirements |
| --- | --- | --- |
| 1 | `linear_search(my_list, key)` | Iterative. Return the index of the **first** occurrence of `key`, or `-1`. |
| 2 | `recursive_linear_search(my_list, key)` | Same result as Problem 1, but recursive. Use a helper with an index parameter. |
| 3 | `binary_search(my_list, key)` | Iterative. `my_list` is sorted ascending. Return an index of `key`, or `-1`. Must be $O(\log n)$. |
| 4 | `recursive_binary_search(my_list, key)` | Same as Problem 3, but recursive. Use a helper with `low_index` and `high_index`. Don't slice the list. |
| 5 (Challenge) | `binary_search_first(my_list, key)` | `my_list` is sorted ascending and **may contain duplicates**. Return the index of the **first** occurrence of `key`, or `-1`. Must be $O(\log n)$ even if every element equals `key`. |

The binary search tests count how many times your code reads from the list, so a linear search disguised as a binary search will fail.

### Part E2 - Sorting

| Problem | Function | Requirements |
| --- | --- | --- |
| 6a | `merge(my_list, a_first_index, b_first_index, b_last_index, empty_list)` | Merge the sorted run `my_list[a_first_index .. b_first_index-1]` with the sorted run `my_list[b_first_index .. b_last_index]` (inclusive), using `empty_list` as temporary storage. The merged result goes back into `my_list` at the same positions. Nothing outside that range may change. Must be **stable**. |
| 6b | `recursive_merge_sort(my_list, first_index, last_index, empty_list)` | Sort `my_list[first_index .. last_index]` (inclusive) in place. Nothing outside that range may change. |
| 6c | `merge_sort(my_list)` | Sort the whole list in place. Create the temporary list **once** and call `recursive_merge_sort`. |

### Part E3 - Singly linked list (`SinglyLinked`)

Keeps `front` and `back` references. `Node`, `__init__`, `get_front`, and `get_back` are provided.

| Problem | Method | Requirements |
| --- | --- | --- |
| 7a | `push_front(data)` | Add to the front. $O(1)$. |
| 7b | `push_back(data)` | Add to the back. $O(1)$. |
| 7c | `pop_front()` | Remove and return the front value. On an empty list, raise `IndexError("pop_front() used on empty list")`. $O(1)$. |
| 7d | `pop_back()` | Remove and return the back value. On an empty list, raise `IndexError("pop_back() used on empty list")`. |
| 7e | `search(key)` | Return the **node** holding the first occurrence of `key`, or `None`. |
| 7f | `remove(key)` | Remove the first node holding `key`. Return `True` if a node was removed, `False` otherwise. Keep `front` and `back` correct. |
| 7g | `reverse()` | Reverse the list in place by relinking the existing nodes. Don't create new nodes or copy data. |
| 7h | `__len__()` | Return the number of nodes. |

### Part E4 - Doubly linked list (`DoublyLinked`)

Keeps `front` and `back` references. `Node`, `__init__`, `get_front`, and `get_back` are provided. Re-implement the push/pop methods from memory, without looking at Lab 3.

| Problem | Method | Requirements |
| --- | --- | --- |
| 8a | `push_front(data)` | Add to the front. $O(1)$. |
| 8b | `push_back(data)` | Add to the back. $O(1)$. |
| 8c | `pop_front()` | Remove and return the front value. On an empty list, raise `IndexError("pop_front() used on empty list")`. $O(1)$. |
| 8d | `pop_back()` | Remove and return the back value. On an empty list, raise `IndexError("pop_back() used on empty list")`. $O(1)$. |
| 8e | `search(key)` | Return the **node** holding the first occurrence of `key`, or `None`. |
| 8f | `insert_after(node, data)` | Insert a new node holding `data` directly after `node` (a node already in this list). $O(1)$. |
| 8g | `remove_node(node)` | Unlink `node` (a node already in this list) and return its data. $O(1)$. |
| 8h | `reverse()` | Reverse the list in place by relinking the existing nodes. Don't create new nodes or copy data. |
| 8i | `__len__()` | Return the number of nodes. |

### Part E5 - Putting it together

| Problem | Function | Requirements |
| --- | --- | --- |
| 9 | `merge_sorted_lists(list_a, list_b)` | `list_a` and `list_b` are `SinglyLinked` lists whose values are sorted ascending. Return a **new** `SinglyLinked` holding every value from both, sorted ascending. Don't modify the input lists. Must be $O(n + m)$: walk both lists once, like `merge`. Don't copy into a Python list and sort. |

---

## Part F - Reflection

1. Which coding problem took you the longest, and what was the bug? Which of the special cases from Part D, question 8 was involved?

2. Look back at your Part A answers. Write the general rule you noticed: what kind of recurrence gives $O(n)$, $O(\log n)$, $O(n \log n)$, and $O(2^n)$?

3. For `binary_search_first`, explain how you made it $O(\log n)$ even when the list is full of duplicates. Why does "find the key, then walk left" not work?
