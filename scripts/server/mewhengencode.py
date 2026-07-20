text = "Vec3([%lf, %lf, %lf])"

for i in range(1,12):
    x = ("Vec3(%lf, %lf, %lf), "*i)[:-3]
    string = f"""if (amount == {i}) {{
    matched = sscanf(str, "{x}", {"result"+i});
    if (matched != 3) {{
        printf("%d Matched\\n", matched);
        return -1;
    }}
}}"""
    print(string)
