import argparse

from transformers import pipeline

# Yes, you can build your own neural network, handwritten TF IDF or whatever, but why?
# Just search through hugging face and get what you want
pipe = pipeline(model="Lazyhope/python-clone-detection", trust_remote_code=True)
# https://huggingface.co/Lazyhope/python-clone-detection

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
    for line in inp.readlines():
        first_file, second_file = line.split()
        try:
            with open(first_file, encoding="UTF-8") as x, open(
                second_file, encoding="UTF-8"
            ) as y:
                x = x.read()
                y = y.read()
                is_clone = pipe((x, y))
                score = round(is_clone[True], 2)
                out.write(f"{score}\n")
        except FileNotFoundError:
            out.write(
                f"It appears the files {first_file} or {second_file} are missing.\n"
            )
        except BaseException as e:
            out.write(
                f"There's been a problem (namely {e}) with analyzing {first_file} and {second_file} files.\n"
            )
