print("Hello, to the chemistry world!")
molecule = input("Enter the formula of your element: ")

import re
from typing import Dict, List, Tuple
import numpy as np
from mendeleev import element

class ChemFormulaParser:
    # Parsing chemical formulas including brackets
    @staticmethod
    def parseformula(formula: str) -> Dict[str, int]:
        """ AIM:-
        Parsing chemical formula into element counts. 
        Ex:- ChemFormulaParser.parseform("K4[Fe(CN)6]") -> {'K': 4, 'Fe': 1, 'C': 6, 'N': 6}
        """

        # Step 1:- Convert sq. brackets into standard parentheses
        formula = formula.replace('[','(')
        formula = formula.replace(']',')')

        #Step 2:- Convert curly brackets into standard parentheses
        formula = formula.replace('{','(')
        formula = formula.replace('}',')')

        #Step 3:- Start with an empty dict
        stack = [{}]

        i = 0 # start tracking indice of string compound
        length = len(formula)

        while i < length:
            char = formula[i]

            #Case 1:- Opening brackets
            if char == '(':
                stack.append({})
                i += 1

            #Case 2:- Closing brackets tell closed section Fe2(SO4)3, meaning S->3 and O->4*3
            elif char == ')':
                if len(stack) <= 1: #In the case of showing error
                    raise ValueError("invalid closing of bracket at index number", i)

                i += 1
                start_num = i 

                #while loop is applying for numbers having 2 or 3 digits like C6H12O6
                while i<length and formula[i].isdigit(): 
                    i += 1

                """in chemistry, molecules sometimes have assigned value of them (liek H20, where H has 2)
                but then oxygen doesn't have any number behind it, doesn't mean its invalid, just means it has one atom"""
                if start_num < i:
                    multiplier = int(formula[start_num:i])
                else:
                    multiplier = 1

                inner_grp = stack.pop() # converting it into it's own dict
                parents_grp = stack[len(stack)-1]
                for element, count in inner_grp.items():
                    currcount = parents_grp.get(element,0)
                    parents_grp[element] = currcount + count * multiplier

            elif char.isupper(): # Upper letter means we found an element's symbol (O)
                start_element = i
                i += 1
                

                while i<length and formula[i].islower(): # the lowercase letter will be merged witht the element
                    i += 1
                element_symbol = formula[start_element:i]

                start_num = i
                while i < length and formula[i].isdigit():
                    i += 1

                if start_num < i:
                    element_count = int(formula[start_num:i])# FIX start_element -> start_num as python tries to slice the letter and converts it to a int which crashes it
                else:
                    element_count = 1

                # Add this element's count to the top of the stack
                current_group = stack[-1]
                current_group[element_symbol] = current_group.get(element_symbol, 0) + element_count

            else:
                i += 1

        return stack[0]


print(ChemFormulaParser.parseformula(molecule))

class moleSolver:
    @staticmethod
    def molar_mass(formula: str) -> float:
        elements = ChemFormulaParser.parseformula(formula)
        total_mass = 0.0

        # Look up the mass using mendeleev library
        for symbol, count in elements.items():
            el = element(symbol)
            total_mass += el.mass * count

        # FIXED: Un-indented return statement so it calculates the full molecule mass AFTER the loop finishes
        return total_mass

    @staticmethod
    def atomic_no(formula: str) -> list[int]:
        elements = ChemFormulaParser.parseformula(formula)
        atomic_no = []
        for symbol in elements.keys():
            el = element(symbol)
            atomic_no.append(el.atomic_number)

        return atomic_no

# Define a sample molecule variable so Python knows what it is
molecule = "K4[Fe(CN)6]"

# FIXED: Changed calculate_molar_mass to molar_mass to match your function definition above
print(f"Molar mass of {molecule}: {moleSolver.molar_mass(molecule)} g/mol")
print("Atomic numbers", molecule, ":", moleSolver.atomic_no(molecule))