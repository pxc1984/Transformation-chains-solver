import pytest
import numpy as numpy
from sympy import Matrix
import re

# Im putting → just in case

def split_formula(formula, all_atoms: set):
    # Use a regular expression to split the formula into individual elements
    elements = re.findall('[A-Z][a-z]?\d*', formula)

    # Loop over the elements and extract the element symbol and count
    answer = {}
    for element in elements:
        # Extract the element symbol by finding the first uppercase letter
        element_symbol = re.findall('[A-Z][a-z]?', element)[0]
        
        all_atoms.add(element_symbol)

        # Extract the count by finding any digits at the end of the element string
        count = int(re.findall('\d+', element)[0]) if re.findall('\d+', element) else 1

        # Add the element symbol and count to the dictionary
        try:
            answer[element_symbol] += count
        except KeyError:
            answer[element_symbol] = count
    return answer

def solve_integer_linear_equations(A, b):
    # Convert the input arrays to SymPy matrices
    A = Matrix(A)
    b = Matrix(b)

    # Augment the matrix A with the vector b
    M = A.row_join(b)

    # Use Gauss-Jordan elimination to solve the system of linear equations
    M_rref, _ = M.rref()
    if M_rref[-1, -1] == 0:
        # The matrix M is singular, so there are infinitely many solutions
        x = M.nullspace()[0]
    else:
        # The matrix M has a unique solution
        x = M_rref[:, -1]

    # Convert the solution to a list of integers
    x = [int(x[i]) for i in range(len(x))]

    return x

def autobalance(equation):
    # Split equation into components
    reactants, products = equation.split(" → ")
    reactants = reactants.split(" + ")
    products = products.split(" + ")

    all_atoms = set()
    
    atoms_count_reactants = []
    atoms_count_products = []
    
    for formula in reactants:
        atoms_count_reactants.append(split_formula(formula, all_atoms))
    
    for formula in products:
        atoms_count_products.append(split_formula(formula, all_atoms))
    
    print(atoms_count_reactants, "=", atoms_count_products)
    
    m = []
    # Loop over all atoms
    for atom in list(all_atoms):
        n = []
        for formula in atoms_count_reactants:
            try:
                n.append(formula[atom])
            except KeyError:
                n.append(0)
        for formula in atoms_count_products:
            try:
                n.append(0 - formula[atom])
            except KeyError:
                n.append(0)
        m.append(n)
    print(m)
    print()
    coefficients = solve_integer_linear_equations(m, ["1" for i in range(len(all_atoms))])
    
    coefficients = list(map(lambda x: str(abs(x)), coefficients))

    for i in range(len(coefficients)):
        if coefficients[i] == '1':
            coefficients[i] = ''

    coefficients_reactants = coefficients[::len(reactants)]
    coefficients_products = coefficients[len(reactants)::]
    answer = " + ".join(map(lambda x, c: str(c) + str(x), reactants, coefficients_reactants)), " → ", " + ".join(map(lambda x, c: str(c) + str(x), products, reversed(coefficients_products)))
    print()
    print(answer)
    print()
    return ''.join(answer)


def test_autobalance():
    assert autobalance("NaOH + H2SO4 → Na2SO4 + H2O") == "2NaOH + H2SO4 → Na2SO4 + 2H2O"
    assert autobalance("CuO + H2 → H2O + Cu") == "CuO + H2 → H2O + Cu"
    assert autobalance("Fe2O3 + CO → Fe + CO2") == "2Fe2O3 + 3CO → 4Fe + 3CO2"
    assert autobalance("H2 + SiO2 → H2O + Si") == "2H2 + SiO2 → 2H2O + Si"

test_autobalance()
