def my_split(in_string, separator):
    separated = []
    word = ""

    if separator == "":
        raise ValueError("separator cannot be empty")

    i = 0
    while i < len(in_string):
        if in_string[i:i + len(separator)] == separator:
            separated.append(word)
            word = ""
            i += len(separator)
            print(f"marhale 1: {word} va {i}")
        else:
            word += in_string[i]
            i += 1
            print(f"marhale 2: {word} va {i}")

    # اضافه کردن آخرین کلمه باقی‌مانده
    separated.append(word)

    return separated


string = "salam quera tina quera tavalodet quera mobarek bashe "
separator = "quera"
print(my_split(string, separator))