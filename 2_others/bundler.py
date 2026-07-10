import os
files_to_merge = [os.path.join("2_others", "logbook.txt")]

for name in os.listdir("1_main"):
    if name.endswith(".py") or name.endswith("sql"):
        files_to_merge.append(os.path.join("1_main", name))

with open(os.path.join("2_others", "context.txt"), "w", encoding="utf-8") as outfile:
    for file_name in files_to_merge:
        outfile.write(f"\n===========ФАЙЛ: {file_name} ===========\n")
        with open(file_name, "r", encoding="utf-8") as infile:
            outfile.write(infile.read())