# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
import json
import os
import urllib.request
from pathlib import Path

URL = "https://raw.githubusercontent.com/arkilpatel/SVAMP/main/SVAMP.json"

# Data Format
#
# Required:
#   - question (problem statement)
#
# Optional:
#   - expected_answer (expected answer)
#   - reference_solution (text-based solution)


if __name__ == "__main__":
    data_folder = Path(__file__).absolute().parent
    original_file = str(data_folder / f"original_test.json")
    data_folder.mkdir(exist_ok=True)
    output_file = str(data_folder / f"test.jsonl")

    if not os.path.exists(original_file):
        urllib.request.urlretrieve(URL, original_file)

    data = []
    with open(original_file, "rt", encoding="utf-8") as fin:
        original_data = json.load(fin)
        for original_entry in original_data:
            new_entry = {}
            # fixing formatting issues
            if original_entry["Body"][-1].isalpha():
                original_entry["Body"] += "."
            # mapping to the required naming format
            new_entry["question"] = original_entry["Body"] + " " + original_entry["Question"]
            new_entry["expected_answer"] = original_entry["Answer"]
            # converting to int if able to for cleaner text-only representation
            if int(new_entry["expected_answer"]) == new_entry["expected_answer"]:
                new_entry["expected_answer"] = int(new_entry["expected_answer"])
            new_entry["reference_equation"] = original_entry["Equation"]
            data.append(new_entry)

    with open(output_file, "wt", encoding="utf-8") as fout:
        for entry in data:
            fout.write(json.dumps(entry) + "\n")
