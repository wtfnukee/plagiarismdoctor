# Plagiarism Doctor
## Yes, it is like Plague Doctor
<img src="https://user-images.githubusercontent.com/45035322/209869937-2937a4e6-73fb-4f36-aacf-c9b5c34f3b58.png" width="256">

*Credits to Midjourney for this beautiful picture*

-----

Run this to compare files and write similarity score to file
```
python3 compare.py input.txt scores.txt
```

Example of input.txt
```
files/main.py plagiat1/main.py
files/loss.py plagiat2/loss.py
files/loss.py files/loss.py
```

Example of scores.txt
```
0.75
0.75
1.0
```
