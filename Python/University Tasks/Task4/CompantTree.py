from CompanyNode import CompanyNode
import CompanyNode as coNo
import copy


# -----------------------      Handy Functions     -----------------------------


def recursively_add_queue(node, tree={}, level=1):
    current_level = []
    for child in node.get_children():
        current_level.append(child)
    if level in tree.keys():
        tree.update({level: list(tree[level]) + current_level})
    else:
        tree.update({level: current_level})
    for child in current_level:
        if child.get_children():
            return recursively_add_queue(child, tree, level + 1)
    return tree


def recursively_add_iterations(node, iterList=[]):
    if node.get_children():
        if len(node.get_children()) % 2 == 0:
            length = (len(node.get_children()) - 1) // 2 + 1
        else:
            length = len(node.get_children()) // 2 + 1
        for i in range(length):
            recursively_add_iterations(node.get_children()[i], iterList)
    iterList.append(node)
    if node.get_children():
        for i in range(length, len(node.get_children())):
            recursively_add_iterations(node.get_children()[i], iterList)
    return iterList

# -----------------------      Handy Functions     -----------------------------


def raise_flag_root_validity(root):
    if root is None:
        return
    if type(root) is not None and type(root) != CompanyNode:
        raise ValueError("Nope!")
    if type(root) == CompanyNode and root.get_parent() is not None:
        raise ValueError("Nope too!")


class CompanyTree:
    def __init__(self, root=None):
        raise_flag_root_validity(root)
        self._root = root

    def set_root(self, root):
        try:
            raise_flag_root_validity(root)
        except ValueError:
            return False
        self._root = root
        return True

    def get_root(self):
        return self._root

    def __str__(self):
        listToPrint = recursively_add_queue(self._root, {})
        listToPrint.update({0: [self._root]})
        string = ""
        for level in range(len(listToPrint)):
            end = len(listToPrint[level]) - 1
            for node_num in range(len(listToPrint[level])):
                string += str(listToPrint[level][node_num])
                if node_num != end:
                    string += " * "
            if level != len(listToPrint) - 1:
                string += "\n"
        return string

    def __iter__(self):
        self.complete_list = iter(recursively_add_iterations(self._root))
        return self.complete_list

    def __next__(self):
        return next(self.complete_list)

    def insert_node(self, node):
        new_parent = next(iter(self))
        if node.get_parent() is not None or node in self.complete_list:
            return False
        return new_parent.add_child(node)

    def is_it_in(self,name):
        for node in self:
            if node.name == name:
                return node
        return None

    def remove_node(self, name):
        node = self.is_it_in(name)
        if node is None:
            return None
        else:
            parent = node.get_parent()
            parent._children = parent._children + node._children
            for child in node.get_children():
                child.set_parent(node.get_parent())
            node._parent.remove_by_index(node)
            node._parent = None
            node._children = []
            return node

