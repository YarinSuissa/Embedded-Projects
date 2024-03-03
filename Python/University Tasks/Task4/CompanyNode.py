from Company import Company
import Company as co
import copy


# -----------------------      Handy Functions     -----------------------------


def is_ancestor_recursive(self, other, currentState=False):
    if other in self._children or currentState:
        return True
    for child in self._children:
        currentState = currentState or is_ancestor_recursive(child, other, currentState)
        if currentState:
            return True


def test_node_validity_down(node, currentState=True):
    if not node._children:
        return node.NodesRule(node._parent, "<=")
    for child in node._children:
        currentState = currentState and test_node_validity_down(child)
        if not currentState:
            break
    return currentState


def test_node_validity_up(node, child, currentState=True):
    if node._parent is None:
        return currentState and node.NodesRule(child)
    return test_node_validity_up(node._parent, node, currentState)

# -----------------------      Handy Functions     -----------------------------

class CompanyNode(Company):
    _comparison_type = Company._comparison_type

    def __init__(self, name, stocks_num, stock_price, comp_type):
        Company.__init__(self, name, stocks_num, stock_price, comp_type)
        self._children = []
        self._parent = None

    def set_parent(self, new_parent):
        if type(new_parent) != CompanyNode:
            return False
        if self._parent is not None:
            old_parent = self._parent
        self._parent = new_parent
        return True

    def get_parent(self):
        return self._parent

    def get_children(self):
        return self._children

    def is_leaf(self):
        if not self.get_children():
            return True
        return False

    def NodesRule(self, other, operator=">=") -> bool:
        if type(other) != CompanyNode:
            return False
        if self._comparison_type == "total sum":
            return co.compare(self.total_net_worth(), other.total_net_worth(), operator)
        else:
            return self.compare_type(other, operator)

    def add_child(self, child) -> bool:
        if type(child) != CompanyNode:
            return False
        if child.get_parent() is not None:
            old_parent = child._parent
            old_parent_children = old_parent.get_parent()
            old_parent_children.remove_by_index(child)
        if self.NodesRule(child):
            self._children.append(child)
            child._parent = self
            return True

    def total_net_recursion(self, market_sum=0):
        if self.is_leaf():
            return self.net_worth()
        for child in self._children:
            market_sum += child.total_net_recursion(market_sum)
        return market_sum + self.net_worth()

    def total_net_worth(self):
        return self.total_net_recursion()

    def test_node_order_validity(self):
        return test_node_validity_down(self) and test_node_validity_up(self._parent, self)

    def is_ancestor(self, other):
        if is_ancestor_recursive(self, other) is None:
            return False
        else:
            return True


    @classmethod
    def change_comparison_type(cls, comparison_type):
        if comparison_type.lower() == "total num":
            cls._comparison_type = comparison_type
            return True
        else:
            return super().change_comparison_type(comparison_type)

    def remove_by_index(self, other):
        for index in range(len(self._children)):
            if other == self._children[index] and other.name == self._children[index].name:
                del self._children[index]
                return
        return

    def set_stock_price(self, stock_price) -> bool:
        original_node = copy.deepcopy(self)
        super().set_stock_price(stock_price)
        if not self.NodesRule(self._parent,"<="):
            super().set_stock_price(original_node.stock_price)
            return False
        for child in self._children:
            if not self.NodesRule(child):
                return False
        return True

    def set_stocks_num(self, stocks_num) -> bool:
        original_node = copy.deepcopy(self)
        super().set_stocks_num(stocks_num)
        if not self.NodesRule(self._parent,"<="):
            super().set_stocks_num(original_node.stock_num)
            return False
        for child in self._children:
            if not self.NodesRule(child):
                return False
        return True

    def update_net_worth(self, net_worth) -> bool:
        original_node = copy.deepcopy(self)
        super().update_net_worth(net_worth)
        if not self.NodesRule(self._parent,"<="):
            super().update_net_worth(original_node.net_worth())
            return False
        for child in self._children:
            if not self.NodesRule(child):
                return False
        return True
    
    def add_stocks(self, number) -> bool:
        original_node = copy.deepcopy(self)
        super().add_stocks(number)
        if not self.NodesRule(self._parent,"<="):
            super().add_stocks(-1*number)
            return False
        for child in self._children:
            if not self.NodesRule(child):
                return False
        return True
        
    def __add__(self, other):
        if other.is_ancestor(self):
            raise ValueError("oops! you silly")
        new_stock_num = copy.deepcopy(self.stock_num + other.stock_num)
        new_market_cap = copy.deepcopy(self.net_worth() + other.net_worth())
        new_stock_price = copy.deepcopy(new_market_cap / new_stock_num)
        new_node = CompanyNode(self.name, new_stock_num, new_stock_price, self.comp_type)
        other._parent.remove_by_index(other)
        other._parent = None
        new_node._children = copy.deepcopy(self.get_children() + other.get_children())
        new_node._parent = copy.deepcopy(self._parent)
        for child in other.get_children():
            if not new_node.NodesRule(child):
                raise ValueError("oops! you are silly too!")
            child.set_parent(new_node)
        return new_node

    def __lt__(self, other):
        return self.NodesRule(other, "<")

    def __gt__(self, other):
        return self.NodesRule(other, ">")

    def __eq__(self, other):
        return self.NodesRule(other, "==")

    def __ge__(self, other):
        return self.NodesRule(other, ">=")

    def __le__(self, other):
        return self.NodesRule(other, "<=")

    def __ne__(self, other):
        return self.NodesRule(other, "!=")

    def __len__(self):
        return len(self._children)

    def __repr__(self):
        return "[" + str(self) + ", " + str(self._children) + "]"


