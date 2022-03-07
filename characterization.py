#! /usr/bin/env python3
# Compare converted texts of RFCs against reference HTML files

import os
import difflib, pprint
from pathlib import Path
from rfc2html import markup

generate_references = False
show_diff = True

def print_diff(a, b):
    d = difflib.Differ()
    result = list(d.compare(a.splitlines(keepends = True),
                            b.splitlines(keepends = True)
    ))
    for line in result:
        print(line, end = "")
    print()

def get_input(input_file):
    with open(os.path.join("characterization/inputs", input_file)) as f:
        return f.read()    

passed = 0
failed = 0
skipped = 0

for input_file in os.listdir("characterization/inputs"):
    reference_html = Path(input_file).with_suffix(".html")
    reference_path = os.path.join("characterization/references",reference_html)
    print(f"{input_file} <-> {reference_html}", end = "")
    try:
        input_text = get_input(input_file)
    except UnicodeDecodeError:
        print(" SKIP")
        skipped += 1
        continue
    converted_text = markup(input_text)
    
    if generate_references:
        with open(reference_path, "w") as f:
            f.write(converted_text)
            print()
            continue
    with open(reference_path) as f:
        reference_text = f.read()
    
    if reference_text != converted_text:
        print(" FAIL")
        failed += 1
        if show_diff:
            print_diff(reference_text, converted_text)
    else:
        print(" PASS")
        passed += 1

total = passed + failed + skipped
print("-"* 80)
print(f"Total {total}, passed {passed}, failed {failed}, skipped {skipped}")

