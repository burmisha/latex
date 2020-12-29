#!/usr/bin/env python3

import collections

variants = [2, 3, 4, 5]
deltas = collections.Counter()
deltas_half = collections.Counter()
for a in variants:
    for b in variants:
        for c in variants:
            for d in variants:
                r1 = (a + b + 1) // 2
                r2 = (c + d + 1) // 2
                r = (a + b + c + d + r1 + r2 + 3) // 6
                delta = r - (a + b + c + d) / 4
                delta_half = (r1 + r2 + 1) // 2 - (a + b + c + d) / 4
                deltas[delta] += 1
                deltas_half[delta_half] += 1
                if delta_half == 1:
                    print(f'{a},{b} → {r1}  {c},{d} → {r2}  →  {r} (delta: {delta} for [{a}{b}{c}{d}]) delta_half: {delta_half})')

print(deltas)
print(deltas_half)
