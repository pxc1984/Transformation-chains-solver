from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.service import Service
import time
from bs4 import BeautifulSoup
import re

def _extract_reactions(line):
    soup = BeautifulSoup(line, 'html.parser')
    reactions = []
    for a in soup.find_all('a'):
        href = a.get('href')
        if href is not None and href.startswith('/en/?s='):
            reaction = a.text.strip()
            reactions.append(reaction)
    return reactions

def solve1(unformatted_input):
    """This function inputs a chain of chemical components, seperated with " = " and outputs
    all reactions to go from one product to another.
    Example:
        H2O = NaOH = Na2SO4

    Args:
        unformatted_input (str): chain of chemical reactants, seperated with " = "
    """
    answer = ""

    reactants_list = unformatted_input.strip().split(" = ")
    for i in range(len(reactants_list) - 1):
        reactant = reactants_list[i]
        product = reactants_list[i + 1]
        # I basically steal all reactions from this site :3
        
        start = time.time()
        answer_html = driver.get(f"https://chemequations.com/en/advanced-search/?reactant1={reactant}&product1={product}&submit=")
        end = time.time()
        print("BENCHMARK: " + str(end - start))
        
        time.sleep(0.3)

        lines = driver.page_source.split("\n")
        query = lines[93]
        reactions = _extract_reactions(query)
        
        number_of_reaction = 0
        answer = answer + f"\n{i + 1}. {reactant} → {product}"
        for reaction in reactions:
            number_of_reaction += 1
            answer = answer + f"\n\t{number_of_reaction})\t{reaction}"
    return answer[1:]

if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    reaction = "NaOH = Na2SO4"

    print(solve1(reaction))
