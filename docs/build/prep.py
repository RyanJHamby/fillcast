import re, sys
src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8").read().split("\n")
sep = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")
out, i = [], 0
def cells(l): return [c.strip() for c in l.strip().strip("|").split("|")]
while i < len(lines):
    if lines[i].startswith("|") and i + 1 < len(lines) and sep.match(lines[i + 1]):
        j = i
        while j < len(lines) and lines[j].startswith("|"): j += 1
        block = lines[i:j]
        rows = [cells(l) for k, l in enumerate(block) if k != 1]
        n = len(cells(block[0]))
        if all(len(r) == n for r in rows):
            means = [max(8, sum(len(r[c]) for r in rows) / len(rows), 1.25 * max(len(w) for r in rows for w in r[c].split() or [''])) for c in range(n)]
            tot = sum(means)
            w = [max(4, round(100 * m / tot)) for m in means]
            block[1] = "|" + "|".join("-" * x for x in w) + "|"
        out += block
        i = j
    else:
        out.append(lines[i]); i += 1
t = "\n".join(out)
t = t.replace("Items marked ✔ were read", "Items marked [read] were read").replace("* ✔ ", "* [read] ")
open(dst, "w", encoding="utf-8").write(t)
