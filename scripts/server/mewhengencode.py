'''Code that generated my very bad, hardcoded c code'''
text = "Vec3([%lf, %lf, %lf])"

for i in range(1,12):
    x = ("Vec3(%lf, %lf, %lf), "*i)[:-2]
    results = []
    for j in range(i):
        for k in range(3):
            results.append(f"&result[{j}][{k}]")

    string = f"""if (amount == {i}) {{
    matched = sscanf(str, "[{x}]", {", ".join(results)});
    if (matched != {3*i}) {{
        printf("%d Matched\\n", matched);
        return -1;
    }}
}}"""
    print(string)
