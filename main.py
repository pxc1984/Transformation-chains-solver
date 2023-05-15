from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.service import Service
import time
from bs4 import BeautifulSoup
import re

# Im putting → just in case

def autobalance(equation):
    # Split the equation into reactants and products
    reactants, products = equation.split(" → ")

    # Create a set of all unique elements in the equation
    elements = set()
    for molecule in reactants.split(" + ") + products.split(" + "):
        for element in re.findall("[A-Z][a-z]*", molecule):
            elements.add(element)

    # Initialize a matrix to represent the coefficients of each element in each molecule
    matrix = []
    for element in elements:
        row = []
        for molecule in reactants.split(" + "):
            count = 0
            for e, c in re.findall("([A-Z][a-z]*)(\d*)", molecule):
                if e == element:
                    count = int(c) if c else 1
                    break
            row.append(count)
        for molecule in products.split(" + "):
            count = 0
            for e, c in re.findall("([A-Z][a-z]*)(\d*)", molecule):
                if e == element:
                    count = -int(c) if c else -1
                    break
            row.append(count)
        matrix.append(row)

    # Convert the matrix to row echelon form using Gaussian elimination
    num_rows, num_cols = len(matrix), len(matrix[0])
    for i in range(num_rows):
        # Find the pivot element
        pivot_row = i
        while pivot_row < num_rows and matrix[pivot_row][i] == 0:
            pivot_row += 1
        if pivot_row == num_rows:
            # No pivot element in this column, equation cannot be balanced
            return None
        if pivot_row != i:
            # Swap the rows to make the pivot element the first non-zero element in the column
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]

        # Eliminate the other non-zero elements in this column
        pivot = matrix[i][i]
        for j in range(i+1, num_rows):
            factor = matrix[j][i] // pivot
            for k in range(i, num_cols):
                matrix[j][k] -= factor * matrix[i][k]

    # Convert the matrix to reduced row echelon form
    for i in range(num_rows-1, -1, -1):
        # Find the pivot element
        pivot_col = None
        for j in range(num_cols):
            if matrix[i][j] != 0:
                pivot_col = j
                break
        if pivot_col is None:
            # This row is all zeros, move on to the next row
            continue

        # Divide the pivot row by the pivot element to make the pivot element equal to 1
        pivot = matrix[i][pivot_col]
        for j in range(pivot_col, num_cols):
            matrix[i][j] //= pivot

        # Use the pivot row to eliminate the other non-zero elements in this column
        for j in range(i):
            factor = matrix[j][pivot_col]
            for k in range(pivot_col, num_cols):
                matrix[j][k] -= factor * matrix[i][k]

    # Extract the coefficients of the balanced equation
    coefficients = matrix[-1]

    # Build the balanced equation from the reactants, products, and coefficients
    balanced_equation = ""
    for i, molecule in enumerate(reactants.split(" + ")):
        count = coefficients[i]
        if count == 1:
            balanced_equation += molecule
        else:
            balanced_equation += str(count) + molecule
        if i < len(reactants.split(" + ")) - 1:
            balanced_equation += " + "
    balanced_equation += " → "
    for i, molecule in enumerate(products.split(" + ")):
        count = coefficients[i+len(reactants.split(" + "))]
        if count == 1:
            balanced_equation += molecule
        else:
            balanced_equation += str(count) + molecule
        if i < len(products.split(" + ")) - 1:
            balanced_equation += " + "

    return balanced_equation


def extract_reactions(line):
    soup = BeautifulSoup(line, 'html.parser')
    reactions = []
    for a in soup.find_all('a'):
        href = a.get('href')
        if href is not None and href.startswith('/en/?s='):
            reaction = a.text.strip()
            reactions.append(reaction)
    return reactions


chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


print("Введите цепочку реакций разделяя реагенты с помощью \" = \"")
unformatted_input = input("Цепочка реакций: ")
reactants_list = unformatted_input.split(" = ")
for i in range(len(reactants_list) - 1):
    reactant = reactants_list[i]
    product = reactants_list[i + 1]
    answer_html = driver.get(f"https://chemequations.com/en/advanced-search/?reactant1={reactant}&product1={product}&submit=")
    time.sleep(0.3)

    lines = driver.page_source.split("\n")
    query = lines[93]
    reactions = extract_reactions(query)
    
    number_of_reaction = 0
    print(f"{i + 1}. {reactant} → {product}")
    for reaction in reactions:
        number_of_reaction += 1
        print(f"\t{number_of_reaction})\t{reaction}")
