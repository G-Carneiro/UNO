from typing import List, Optional
from random import shuffle

from .Node import DoublyLinkedListNode as Node, T


class DoublyCircularList:
    def __init__(self, start_list: Optional[List[T]] = None) -> None:
        self._head: Optional[Node] = None
        self._size: int = 0
        if start_list:
            self._insert_values(values=start_list)

    def head(self) -> Optional[Node]:
        return self._head

    def size(self) -> int:
        return self._size

    def empty(self) -> bool:
        return (self._size == 0)

    def push_back(self, data: T) -> None:
        if self.empty():
            self._head = Node(data)
        elif (self._size == 1):
            new_node: Node = Node(data)
            new_node.set_previous(self._head)
            new_node.set_next(self._head)
            self._head.set_previous(new_node)
            self._head.set_next(new_node)
        else:
            new_node: Node = Node(data)
            tail: Node = self._head.previous()
            new_node.set_previous(tail)
            new_node.set_next(self._head)
            tail.set_next(new_node)
            self._head.set_previous(new_node)

        self._size += 1

        return None

    def push_front(self, data: T) -> None:
        if self.empty():
            self._head = Node(data)
            self._size += 1
        else:
            self.push_back(data)
            self._head = self._head.previous()

        return None

    def insert(self, data: T, index: Optional[int] = None) -> None:
        if ((index is None) or (index > self._size)):
            index = self._size
        elif (index < 0):
            index = 0

        if (index == self._size):
            self.push_back(data=data)
        elif (index == 0):
            self.push_front(data=data)
        else:
            actual_node: Node = self._head
            new_node = Node(data)

            for _ in range(index):
                actual_node = actual_node.next()

            previous_node: Node = actual_node.previous()
            new_node.set_previous(previous_node)
            new_node.set_next(actual_node)
            previous_node.set_next(new_node)
            actual_node.set_previous(new_node)

            self._size += 1

        return None

    def _insert_values(self, values: List[T]) -> None:
        for value in values:
            self.push_back(value)

        return None

    def pop_back(self) -> Optional[T]:
        if (self.empty()):
            return None

        tail: Node = self._head.previous()
        if (self._size == 1):
            tail = self._head
            self._head = None
        elif (self._size == 2):
            self._head.set_previous(None)
            self._head.set_next(None)
        else:
            new_tail: Node = tail.previous()
            new_tail.set_next(self._head)
            self._head.set_previous(new_tail)

        self._size -= 1

        return (tail.data())

    def pop_front(self) -> Optional[T]:
        if (self.empty()):
            return None

        head: Node = self._head
        if (self._size == 1):
            self._head = None
        elif (self._size == 2):
            new_head: Node = self._head.previous()
            new_head.set_previous(None)
            new_head.set_next(None)
            self._head = new_head
        else:
            new_head: Node = self._head.next()
            tail: Node = self._head.previous()
            new_head.set_previous(tail)
            tail.set_next(new_head)
            self._head = new_head

        self._size -= 1

        return (head.data())

    def pop(self, index: Optional[int] = None) -> Optional[T]:
        if ((index is None) or (index > self._size - 1)):
            index = self._size - 1
        elif (index < 0):
            index = 0

        if (index == self._size - 1):
            return self.pop_back()
        elif (index == 0):
            return self.pop_front()
        else:
            removed_node: Node = self._head
            for _ in range(index):
                removed_node = removed_node.next()

            previous_node: Node = removed_node.previous()
            next_node: Node = removed_node.next()
            previous_node.set_next(next_node)
            next_node.set_previous(previous_node)

            self._size -= 1

            return (removed_node.data())

    def remove(self, data: T) -> None:
        index: int = self.find(data)
        if (index is not None):
            self.pop(index)

        return None

    def find(self, data: T) -> Optional[int]:
        index: int = 0
        actual_node: Node = self._head
        while (index < self._size):
            if (actual_node.data() == data):
                return index

            actual_node = actual_node.next()
            index += 1

        return None

    def contains(self, data: T) -> bool:
        index: Optional[int] = self.find(data)
        if (index is not None):
            return True

        return False

    def clear(self) -> None:
        self._head = None
        self._size = 0
        return None

    def shuffle(self) -> None:
        if (self._size < 3):
            return None

        nodes: List[Node] = [self._head]
        actual_node: Node = self._head
        tail: Node = self._head.previous()
        while (actual_node != tail):
            actual_node = actual_node.next()
            nodes.append(actual_node)

        shuffle(nodes)
        for i in range(self._size - 1):
            nodes[i].set_previous(nodes[i - 1])
            nodes[i].set_next(nodes[i + 1])

        self._head = nodes[0]
        nodes[-1].set_previous(nodes[-2])
        nodes[-1].set_next(self._head)

        return None
