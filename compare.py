import argparse
from utils import *

parser = argparse.ArgumentParser(
    prog="Plagiarism Doctor", description="Yes, it is like Plague Doctor"
)
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()
input_path, output_path = args.input, args.output

with open(input_path, encoding="UTF-8") as inp, open(
    output_path, encoding="UTF-8", mode="w"
) as out:
    for i in inp.readlines():
        x, y = i.split()
        score = compare(x, y)
        out.write(f"{score}\n")
