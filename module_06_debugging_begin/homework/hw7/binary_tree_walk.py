"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
import itertools
import logging
import os
import random
import re
from collections import deque
from dataclasses import dataclass
from typing import Optional, List

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def find_walk_logs() -> List[BinaryTreeNode]:
    roots_tree: List[BinaryTreeNode] = []
    path_dir: str = os.path.abspath(os.path.join('.'))
    for obj in os.listdir(path_dir):
        if obj.endswith('.txt'):
            path_to_log: str = os.path.join(path_dir, obj)
            root_binary_tree_node: BinaryTreeNode = restore_tree(path_to_log_file=path_to_log)
            roots_tree.append(root_binary_tree_node)
    return roots_tree


def find_place_for_child(node, parent, log, child):
    if node.val == parent:
        if 'left' in log:
            node.left = BinaryTreeNode(child)
            return
        elif 'right' in log:
            node.right = BinaryTreeNode(child)
            return
    else:
        if node.left:
            find_place_for_child(node.left, parent, log, child)
        if node.right:
            find_place_for_child(node.right, parent, log, child)


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pattern_val = r'\d+'
    root_tree = False
    with open(path_to_log_file, 'r',
              encoding='UTF-8') as logs:
        tex_logs: str = logs.read()

    for log in tex_logs.split('\n'):
        if not log.startswith('INFO'):
            node_branch_str: List[str] = re.findall(pattern=pattern_val, string=log)
            if node_branch_str:
                parent, child = int(node_branch_str[0]), int(node_branch_str[1])
                if not root_tree:
                    root_tree = BinaryTreeNode(parent)
                find_place_for_child(node=root_tree, parent=parent, child=child, log=log)
    return root_tree


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename="walk_log_4.txt",
    )

    root = get_tree(7)
    walk(root)
