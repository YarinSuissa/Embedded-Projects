import copy

# ----------------------- Block of Validity Checks -----------------------------


def validity_check_string(given_string: str) -> bool:
    # Type check
    if type(given_string) != str:
        return False
    # Capital letter check
    if given_string[0].islower() or not given_string[0].isalpha():
        return False
    # Length Check
    if len(given_string) < 2:
        return False
    # Duplicate spacing and numerical check
    new_collection = given_string.split()
    new_collection.sort(key=len)
    for word in new_collection:
        if len(word) < 2:
            return False
        if not (word.isalpha() and word.isascii()):
            return False
    if not duplicate_Spacing_Validity(given_string):
        return False
    return True


def validity_check_stocks(stock: int, canBeFloat=False) -> bool:
    if not canBeFloat:
        if type(stock) != int:
            return False
    else:
        if not xor_bool(type(stock) != int, type(stock) != float):
            return False
    if stock <= 0:
        return False
    return True


def check_validity(name: str, stocks_num: int, stock_price: int, comp_type: str) -> bool:
    # --------------- Check name & comp_type:
    if not validity_check_string(name) or not validity_check_string(comp_type):
        return False
    # --------------- Check stock_num & stock_price:
    if not validity_check_stocks(stocks_num) or not validity_check_stocks(stock_price, True):
        return False
    return True


# ----------------------- Block of Validity Checks -----------------------------
# -----------------------      Handy Functions     -----------------------------


def findIndexes(string: str, char: str) -> list:
    known_indexes = []
    for index in range(len(string)):
        if string[index] == char:
            known_indexes.append(index)
    return known_indexes


def duplicate_Spacing_Validity(string: str, char=" ") -> bool:
    list_of_indexes = findIndexes(string, char)
    for i in list_of_indexes:
        for j in list_of_indexes:
            if i == j:
                continue
            elif abs(i - j) <= 1:
                return False
    return True


def xor_bool(statement1: bool, statement2: bool) -> bool:
    # XOR = (┐A ^ B) v (A ^ ┐B)
    return (statement1 and not statement2) or (not statement1 and statement2)


def compare(num1, num2, operator):
    # Find the right operator and return the needed value
    if operator == "<":
        return num1 < num2
    elif operator == "<=":
        return num1 <= num2
    elif operator == ">":
        return num1 > num2
    elif operator == ">=":
        return num1 >= num2
    elif operator == "!=":
        return num1 != num2
    elif operator == "==":
        return num1 == num2
    else:
        return False


# -----------------------      Handy Functions     -----------------------------


class Company:
    _comparison_type = "net worth"

    def __init__(self, name, stocks_num, stock_price, comp_type):

        if not check_validity(name, stocks_num, stock_price, comp_type):
            raise ValueError("Input is not valid!\nTry again!")

        self.name = name
        self.stock_num = stocks_num
        self.stock_price = stock_price
        self.comp_type = comp_type

    def net_worth(self):
        return self.stock_num * self.stock_price

    def set_stock_market(self, stock_market):
        # DO NOT TOUCH
        pass

    def set_name(self, name):
        if not validity_check_string(name):
            return False
        self.name = name
        return True

    def set_stocks_num(self, stocks_num):
        if not validity_check_stocks(stocks_num):
            return False
        previous_cap = self.net_worth()
        self.stock_num = stocks_num
        self.stock_price = previous_cap / self.stock_num
        return True

    def set_stock_price(self, stock_price):
        if not validity_check_stocks(stock_price, True) or stock_price > self.net_worth():
            return False
        previous_cap = self.net_worth()
        self.stock_price = stock_price
        # ??????????????
        self.stock_num = int(previous_cap // self.stock_price)
        return True

    def set_comp_type(self, comp_type):
        if not validity_check_string(comp_type):
            return False
        self.comp_type = comp_type
        return True

    def update_net_worth(self, net_worth):
        if not validity_check_stocks(net_worth, True):
            return False
        self.stock_price = net_worth / self.stock_num
        return True

    def add_stocks(self, number):
        num_of_stocks = int(self.stock_num + number)
        if not validity_check_stocks(num_of_stocks):
            return False
        self.stock_num = num_of_stocks
        return True

    def start_compare(self, other, operator):
        if type(other) != Company:
            return False
        return self.compare_type(other, operator)

    def compare_type(self, other, operator):
        if self._comparison_type == "net worth":
            return compare(self.net_worth(), other.net_worth(), operator)
        elif self._comparison_type == "stock num":
            return compare(self.stock_num, other.stock_num, operator)
        elif self._comparison_type == "stock price":
            return compare(self.stock_price, other.stock_price, operator)
        return False

    @classmethod
    def change_comparison_type(cls, comparison_type):
        known_values = ["net worth", "stock num", "stock price"]
        if comparison_type.lower() in known_values:
            cls._comparison_type = comparison_type
            return True
        return False

    def __str__(self):
        return "(" + self.name + ", " + str(self.stock_num) + " stocks, Price: " + str(
            self.stock_price) + ", " + self.comp_type + ", Net Worth: " + str(self.net_worth()) + ")"

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.start_compare(other, "<")

    def __gt__(self, other):
        return self.start_compare(other, ">")

    def __eq__(self, other):
        return self.start_compare(other, "==")

    def __ge__(self, other):
        return self.start_compare(other, ">=")

    def __le__(self, other):
        return self.start_compare(other, "<=")

    def __ne__(self, other):
        return self.start_compare(other, "!=")

    def __add__(self, other):
        if other.name == self.name:
            return self
        new_stock_num = self.stock_num + other.stock_num
        new_market_cap = self.net_worth() + other.net_worth()
        new_stock_price = new_market_cap / new_stock_num
        return Company(self.name, new_stock_num, new_stock_price, self.comp_type)
