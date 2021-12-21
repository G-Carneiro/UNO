from __future__ import annotations
from typing import Optional

from .Player import Player

T = Player


class Node:
    def __init__(self, data: T) -> None:
        self._data: T = data

    def data(self) -> T:
        return self._data

    def __repr__(self) -> str:
        return str(self._data)


class LinkedListNode(Node):
    def __init__(self, data: T) -> None:
        super().__init__(data)
        self._next: Optional[LinkedListNode] = None

    def next(self) -> Optional[LinkedListNode]:
        return self._next

    def set_next(self, node: Optional[LinkedListNode] = None) -> None:
        self._next = node
        return None


class DoublyLinkedListNode(Node):
    def __init__(self, data: T) -> None:
        super().__init__(data)
        self._next: Optional[DoublyLinkedListNode] = None
        self._previous: Optional[DoublyLinkedListNode] = None

    def next(self) -> Optional[DoublyLinkedListNode]:
        return self._next

    def set_next(self, node: Optional[DoublyLinkedListNode] = None) -> None:
        self._next = node
        return None

    def previous(self) -> Optional[DoublyLinkedListNode]:
        return self._previous

    def set_previous(self, node: Optional[DoublyLinkedListNode] = None) -> None:
        self._previous = node
        return None


class BinaryTreeNode(Node):
    def __init__(self, data: T) -> None:
        super().__init__(data)
        self._left: Optional[BinaryTreeNode] = None
        self._right: Optional[BinaryTreeNode] = None

    def left(self) -> Optional[BinaryTreeNode]:
        return self._left

    def set_left(self, node: Optional[BinaryTreeNode] = None) -> None:
        self._left = node
        return None

    def right(self) -> Optional[BinaryTreeNode]:
        return self._right

    def set_right(self, node: Optional[BinaryTreeNode] = None) -> None:
        self._right = node
        return None
