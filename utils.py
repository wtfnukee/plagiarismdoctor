import ast


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
            add, delete, change = (
                previous_row[j] + 1,
                current_row[j - 1] + 1,
                previous_row[j - 1],
            )
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def parse_import(i: ast.Import, imports: dict) -> dict:
    i = i.__dict__
    names = i["names"]
    modules = [j.__dict__["name"] for j in names]
    for module in modules:
        imports[module] = [module]
    return imports


def parse_importfrom(i: ast.ImportFrom, imports: dict) -> dict:
    i = i.__dict__
    module = i["module"]
    submodules = [j.__dict__["name"] for j in i["names"]]
    imports[module] = imports.get(module, []) + submodules
    return imports


def parse(x):
    imports = dict()
    other = ""
    for i in ast.parse(x).body:
        if isinstance(i, ast.Import):
            imports.update(parse_import(i, imports))
        elif isinstance(i, ast.ImportFrom):
            imports.update(parse_import(i, imports))
        else:
            other += ast.unparse(i) + " "
    return imports, other.lower()


def clip(x):
    return 0 if x == 1 else x


def compare(x: str, y: str) -> float:
    imports_x, other_x = parse(x)
    imports_y, other_y = parse(y)
    return (
            + dict_size(dict_intersection(imports_x, imports_y)) / max(dict_size(imports_x), dict_size(imports_y))
            - levenshtein(other_x, other_y) / max(len(other_x), len(other_y))
    )


def list_intersection(x: list, y: list) -> list:
    return [i for i in x if i in y]


def dict_intersection(x: dict, y: dict) -> dict:
    return {k: list_intersection(x[k], y[k]) for k in x if k in y}


def dict_size(x: dict) -> int:
    total = 0
    for v in x.values():
        total += len(v)
    return total
