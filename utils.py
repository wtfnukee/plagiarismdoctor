import ast
from collections.abc import Iterable
import re
from typing import Union


def clean_whitespaces(input: str) -> str:
    return re.sub('\s+', '', input)


def clean_linebreaks(input):
    return re.sub('[\n]{2,}', '\n', input)


def levenshtein(a: str, b: str) -> int:
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def parse_import(i: ast.Import, imports: dict):
    i = i.__dict__
    names = i['names']
    modules = [j.__dict__['name'] for j in names]
    for module in modules:
        imports[module] = [module]


def parse_importfrom(i: ast.ImportFrom, imports: dict):
    i = i.__dict__
    module = i['module']
    submodules = [j.__dict__['name'] for j in i['names']]
    imports[module] = imports.get(module, []) + submodules


def parse(x):
    imports = dict()
    other = ''
    for i in ast.parse(x).body:
        if isinstance(i, ast.Import):
            parse_import(i, imports)
        elif isinstance(i, ast.ImportFrom):
            parse_importfrom(i, imports)
        else:
            other += ast.unparse(i) + ' '
    return imports, other


def compare(x, y):
    imports_x, other_x = parse(x)
    imports_y, other_y = parse(y)
    return 1 - dict_size(dict_intersection(imports_x, imports_y)) / (
            max(dict_size(imports_x), dict_size(imports_y)) + 0.01) - levenshtein(other_x, other_y) / min(len(other_x),
                                                                                                          len(other_y))


def single(array: list):
    assert len(array) == 1, 'array contains more the one element'
    return array[0]


def list_intersection(x: list, y: list) -> list:
    return [i for i in x if i in y]


def dict_intersection(x: dict, y: dict) -> dict:
    return {k: list_intersection(x[k], y[k]) for k in x if k in y}
    # return {k: x[k] for k in x if k in y and len(x[k]) == len(y[k])}


def dict_size(x: dict) -> int:
    total = 0
    for k, v in x.items():
        total += len(v)
    return total
