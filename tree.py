import random
from collections import deque
from time import sleep  # For animation delays (simulated)

class AVLNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1
        self.visited = False  # Animation highlight

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y

    def insert(self, node, val):
        if not node:
            return AVLNode(val)
        
        if val < node.val:
            node.left = self.insert(node.left, val)
        else:
            node.right = self.insert(node.right, val)

        self.update_height(node)
        balance = self.get_balance(node)

        # Left Left
        if balance > 1 and val < node.left.val:
            return self.right_rotate(node)
        # Right Right
        if balance < -1 and val > node.right.val:
            return self.left_rotate(node)
        # Left Right
        if balance > 1 and val > node.left.val:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # Right Left
        if balance < -1 and val < node.right.val:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def insert_node(self, val):
        self.root = self.insert(self.root, val)

    def search(self, node, val, path=[]):
        if not node:
            return False, path
        path.append(node.val)
        node.visited = True  # Highlight for animation
        if node.val == val:
            return True, path
        if val < node.val:
            return self.search(node.left, val, path)
        return self.search(node.right, val, path)

    def search_node(self, val):
        found, path = self.search(self.root, val)
        return found, path

    def clear_visited(self, node):
        if node:
            node.visited = False
            self.clear_visited(node.left)
            self.clear_visited(node.right)

    def inorder(self):
        def _inorder(node, result):
            if node:
                _inorder(node.left, result)
                result.append(node.val)
                _inorder(node.right, result)
        result = []
        _inorder(self.root, result)
        return result

    def height(self):
        return self.get_height(self.root)

    def generate_random(self, size=20):
        self.root = None
        for _ in range(size):
            self.insert_node(random.randint(1, 99))