print("Hello, to the chemistry world!")

import re
from typing import Dict, List, Tuple
import numpy as np

class ChemFormulaParser:
    # Parsing chemical formulas including brackets
    @staticmethod
    def parseform(formula: str) -> Dict[str, int]:
        """ 
        Parsing chemical formula into element counts. 
        Ex:- ChemFormulaParser.parseform("K4[Fe(CN)6]") ==> {'K': 4, 'Fe': 1, 'C': 6, 'N': 6}
        """
        
        def parseSUBform(sub_form: str) -> Dict[str, int]:
            element_counts: Dict[str, int] = {}
            pattern = r'([A-Z][a-z]*)(\d*)'
            for element, count in re.findall(pattern, sub_form):
                if element:
                    num = int(count) if count else 1
                    element_counts[element] = element_counts.get(element, 0) + num
            return element_counts  # FIX: Unindented so it returns after the loop finishes

        def multiply_counts(
                    counts: Dict[str, int], factor: int) -> Dict[str, int]:  # FIX: factor type hint changed to int
            return {elem: cnt * factor for elem, cnt in counts.items()}

        def merge_counts(c1: Dict[str, int], c2: Dict[str, int]) -> Dict[str, int]:  # FIX: 'Dist' corrected to 'Dict'
            merged = c1.copy()
            for elem, cnt in c2.items():
                merged[elem] = merged.get(elem, 0) + cnt
            return merged

        # Normalize brackets types
        formula = formula.replace('[','(').replace(']',')')

        # Regex to process inner nested brackets
        bracket_pattern = r'\(([^()]+)\)(\d*)'  # FIX: Added the missing backslash to properly match the closing parenthesis
        
        while '(' in formula:
            match = re.search(bracket_pattern, formula)
            if not match:
                break
            sub_content = match.group(1)
            multiplier = int(match.group(2)) if match.group(2) else 1

            # FIX: Everything below here must be indented to run INSIDE the while loop!
            sub_content = parseSUBform(sub_content) 
            scaled_counts = multiply_counts(sub_content, multiplier)  # FIX: Corrected function name 'multiplier_counnts' and matched variable name 'scaled_counts'

            placeholder_parts = []
            for elem, cnt in scaled_counts.items():
                placeholder_parts.append(f"{elem}{cnt}")

            replacement = "".join(placeholder_parts)
            formula = formula[:match.start()] + replacement + formula[match.end():]

        return parseSUBform(formula)  # FIX: Changed from parseform() to parseSUBform() to avoid infinite recursion