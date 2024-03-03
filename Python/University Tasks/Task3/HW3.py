# ----------------- Question 1 ---------------------------------------------------------
def question1(num: int) -> bool:

    def question1_recursion(num: int, divisor: int, current_sum: int) -> bool:
        if divisor >= num or current_sum >= num:
            if num != current_sum:
                return False
            else:
                return True
        elif num % divisor == 0:
            current_sum = current_sum + divisor
        return question1_recursion(num, divisor+1, current_sum)

    return question1_recursion(num, 1, 0)

# ----------------- Question 2 ---------------------------------------------------------


def question2_recursion(lst: list, current_index: int, current_sum: int, number_of_subsets:int) -> int:
    if current_sum == 0:
        return number_of_subsets+1
    if len(lst) - current_index <= 1:
        if lst[current_index] == current_sum:
            return number_of_subsets+1
        else:
            return number_of_subsets

    included = question2_recursion(lst, current_index+1, current_sum - lst[current_index], number_of_subsets)
    excluded = question2_recursion(lst, current_index+1, current_sum, number_of_subsets)
    return included + excluded

def question2(lst: list, x: int) -> int:
    return question2_recursion(lst, 0, x, 0)


# ----------------- Question 3_a -------------------------------------------------------

def question3_a(mat: list,indices: tuple,epidemic: int)-> None:
    global question3_healthy_amount
    question3_healthy_amount = 0
    if mat[indices[0]][indices[1]] != 0 and mat[indices[0]][indices[1]] != epidemic:
        mat[indices[0]][indices[1]] = epidemic
        return
    question3_a_recursion(mat,indices[1],indices[0],epidemic)
    return


def isFree(mat:list ,col_index: int, row_index: int) -> bool:
    if mat[row_index][col_index] != 0:
        return False
    return True


def question3_a_recursion(mat: list, col_index: int, row_index: int, epidemic: int) -> None:
    global question3_healthy_amount
    mat[row_index][col_index] = epidemic
    question3_healthy_amount += 1
    # Infect Left
    if col_index < len(mat[row_index])-1 and isFree(mat,col_index+1,row_index):
        question3_a_recursion(mat,col_index+1,row_index,epidemic)
    # Infect Down
    if row_index < len(mat)-1 and isFree(mat,col_index,row_index+1):
        question3_a_recursion(mat,col_index,row_index+1,epidemic)
    # Infect Right
    if col_index > 0 and isFree(mat,col_index-1,row_index):
        question3_a_recursion(mat,col_index-1,row_index,epidemic)
    #infect Up:
    if row_index > 0 and isFree(mat,col_index,row_index-1):
        question3_a_recursion(mat,col_index,row_index-1,epidemic)
    return

# ----------------- Question 3_b -------------------------------------------------------


def question3_b_recursion(mat: list, indices: tuple, current_max: int) -> int:
    global question3_healthy_amount
    question3_healthy_amount = 0
    if indices[0] >= len(mat):
        return current_max
    if indices[1] >= len(mat[indices[0]]):
        return question3_b_recursion(mat,(indices[0]+1,0), current_max)
    if mat[indices[0]][indices[1]] == 0:
        question3_a_recursion(mat, indices[1], indices[0], -1)
    if question3_healthy_amount > current_max:
        return question3_b_recursion(mat,(indices[0],indices[1]+1),question3_healthy_amount)
    else:
        return question3_b_recursion(mat,(indices[0],indices[1]+1),current_max)


def question3_b(mat: list) -> int:
    global question3_healthy_amount
    modified_mat = mat.copy()
    return question3_b_recursion(modified_mat, (0, 0), 0)