#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

"""
Construct and return Tenner Grid CSP models.
"""

from cspbase import *
import itertools

import time

def tenner_csp_model_1(initial_tenner_board):
    """ Return a CSP object representing a Tenner Grid CSP problem along
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from
       (0,0) to (n,9)) where n can be 3 to 8.

       The input board is specified as a pair (n_grid, last_row).
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid.
       If a -1 is in the list it represents an empty cell.
       Otherwise if a number between 0--9 is in the list then this represents a
       pre-set board position. E.g., the board

       ---------------------
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists

       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]


       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a -1 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.

       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each
       column.
    """

    n_grid = initial_tenner_board[0]
    last_row = initial_tenner_board[1]

    # Create all of the variables
    variable_array = generate_variable_array(n_grid)

    stime = time.process_time()

    # Create the constraints:
    ##### The digits in the same row must be different - Use BINARY
    ##### The digits in the adjacent cells (even diagonally) must be different - Use BINARY

    csp = CSP("model1", [x for sublist in variable_array for x in sublist])
    sums = [[] for k in range(len(variable_array[0]))]
    for i in range(len(variable_array)):
        previous_vars = []
        for j in range(len(variable_array[i])):
            curr_var = variable_array[i][j]
            curr_name = "C_" + str(i) + str(j)
            generate_adjacency_constraints(csp, variable_array, i, j)
            if len(previous_vars) > 0:
                for m in range(len(previous_vars) - 1):
                    (var, row, col) = previous_vars[m]
                    name = curr_name + "_" + str(row) + str(col)
                    c = Constraint(name, [curr_var, var])
                    c.add_satisfying_tuples(generate_bin_sat_tuples_diff(curr_var, var))
                    csp.add_constraint(c)

            previous_vars.append((curr_var, i, j))
            sums[j].append(curr_var)

    ##### The digits in the same column need to add up to the sum in the corresponding
    ##### column in the (n+1)th row - USE N-ARY

    for i in range(len(sums)):
        name = "C_col_" + str(i)
        c = Constraint(name, sums[i])
        c.add_satisfying_tuples(generate_nary_sat_tuples_sum(sums[i], last_row[i]))
        csp.add_constraint(c)

    return csp, variable_array

def generate_bin_sat_tuples_diff(var1, var2):
    """
    Generates satisfying typles for Variables var1 and var2 (in order).
    """
    dom1 = tuple(var1.domain())
    dom2 = tuple(var2.domain())
    result = list(itertools.product(dom1, dom2))

    return [(x, y) for (x, y) in result if x != y]

def generate_nary_sat_tuples_sum(vars, value):
    """ Generates satifying tuples for variables in vars whose sum gives the value"""

    list_perm = [(v.domain()) for v in vars]

    result = [tup for tup in itertools.product(*list_perm) if sum(tup) == value]

    return result

def generate_nary_sat_tuples_diff(variables):
    """ Generates satifying tuples for variables in vars whose sum gives the value"""

    result = []
    list_perm = [(v.cur_domain()) for v in variables]

    for perm in itertools.product(*list_perm):
        if sum(perm) == 45:
            result.append(perm)
    return result

def generate_variable_array(n_grid):
    """
    Generates a variable array corresponding to the Tenner grid n_grid.
    """
    variable_array = []
    init_domain = list(range(0, 10))

    for i in range(len(n_grid)):
        variable_array.append([])
        for j in range(len(n_grid[i])):
            value = n_grid[i][j]
            name = "V_" + str(i) + str(j)
            if value == -1:
                domain = init_domain
            else:
                domain = [value]
            variable = Variable(name, domain)
            variable_array[i].append(variable)

    return variable_array


def generate_adjacency_constraints(csp, variable_array, i, j):
    """ Generates contraints for variable_array[i][j] and its adjacent neighbours."""

    curr_var = variable_array[i][j]
    curr_name = "C_" + str(i) + str(j)

    if (0 < j) and (i < len(variable_array) - 1):
        bl = variable_array[i + 1][j - 1]  # bottom left
        bl_name = curr_name + "_" + str(i + 1) + str(j - 1)
        c = Constraint(bl_name, [curr_var, bl])
        c.add_satisfying_tuples(generate_bin_sat_tuples_diff(curr_var, bl))
        csp.add_constraint(c)

    if (j < len(variable_array[i]) - 1) and (i < len(variable_array) - 1):
        br = variable_array[i + 1][j + 1]  # bottom right
        br_name = curr_name + "_" + str(i + 1) + str(j + 1)
        c = Constraint(br_name, [curr_var, br])
        c.add_satisfying_tuples(generate_bin_sat_tuples_diff(curr_var, br))
        csp.add_constraint(c)

    if j < len(variable_array[i]) - 1:
        r = variable_array[i][j + 1]  # right
        r_name = curr_name + "_" + str(i) + str(j - 1)
        c = Constraint(r_name, [curr_var, r])
        c.add_satisfying_tuples(generate_bin_sat_tuples_diff(curr_var, r))
        csp.add_constraint(c)

    if i < len(variable_array) - 1:
        b = variable_array[i + 1][j]  # bottom
        b_name = curr_name + "_" + str(i - 1) + str(j)
        c = Constraint(b_name, [curr_var, b])
        c.add_satisfying_tuples(generate_bin_sat_tuples_diff(curr_var, b))
        csp.add_constraint(c)


##############################

def tenner_csp_model_2(initial_tenner_board):
    """Return a CSP object representing a Tenner Grid CSP problem along
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from
       (0,0) to (n,9)) where n can be 3 to 8.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.

       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular,
       model_2 has a combination of n-nary
       all-different constraints and binary not-equal constraints: all-different
       constraints for the variables in each row, binary constraints for
       contiguous cells (including diagonally contiguous cells), and n-nary sum
       constraints for each column.
       Each n-ary all-different constraint has more than two variables (some of
       these variables will have a single value in their domain).
       model_2 should create these all-different constraints between the relevant
       variables.
    """
    n_grid = initial_tenner_board[0]
    last_row = initial_tenner_board[1]

    # Create all of the variables
    variable_array = generate_variable_array(n_grid)

    # Create the constraints:
    ##### The digits in the adjacent cells (even diagonally) must be different - Use BINARY

    csp = CSP("model2", [x for sublist in variable_array for x in sublist])
    sums = [[] for k in range(len(variable_array[0]))]

    for i in range(len(variable_array)):
        previous_vars = []
        for j in range(len(variable_array[i])):
            curr_var = variable_array[i][j]
            generate_adjacency_constraints(csp, variable_array, i, j)
            previous_vars.append((curr_var, i, j))
            sums[j].append(curr_var)


    # ROW CONSTRAINTS

    for i in range(len(variable_array)):
        curr_row = variable_array[i]

        variables_fixed = [(curr_row[j].domain()[0], j) for j in range(len(curr_row)) if len(curr_row[j].domain()) == 1]
        true_domain = list(range(10))
        [true_domain.remove(v[0]) for v in variables_fixed]
        sat_tup = [list(x) for x in itertools.permutations(true_domain)]

        for k in range(len(sat_tup)):
            for val in variables_fixed:
                sat_tup[k].insert(val[1], val[0])

        constraint = Constraint("C_row_{}".format(i), curr_row)
        constraint.add_satisfying_tuples(sat_tup)

        csp.add_constraint(constraint)


    ##### The digits in the same column need to add up to the sum in the corresponding
    ##### column in the (n+1)th row - USE N-ARY


    # COLUMN CONSTRAINTS
    for i in range(len(sums)):
        name = "C_col_" + str(i)
        c = Constraint(name, sums[i])
        c.add_satisfying_tuples(generate_nary_sat_tuples_sum(sums[i], last_row[i]))
        csp.add_constraint(c)


    return csp, variable_array
