import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === 설정 ===
TXT_PATH = r"C:\baehunjo_pythonproject\(1310nm) GC PDE Sweep.txt"
E_FIXED = 0.18

P_MIN, P_MAX = 0.86, 1.00   # <-- 여기서 Pitch 범위 지정
LEVELS = 25

pat = re.compile(
    r"\(E\s*([0-9.]+)\s*um\)\s*"
    r"\(P\s*([0-9.]+)\s*um\)\s*"
    r"\(D\s*([0-9.]+)\)\s*"
    r"([-+0-9.eE]+)"
)

rows = []
with open(TXT_PATH, "r", encoding="utf-8") as f:
    for line in f:
        m = pat.search(line)
        if m:
            e, p, d, val = map(float, m.groups())
            rows.append((e, p, d, val))

df = pd.DataFrame(rows, columns=["E", "Pitch", "Duty", "Value"])

# E 고정 필터(옵션)
df = df[np.isclose(df["E"], E_FIXED)]

# ✅ Pitch 스윕 범위 필터는 df 만든 다음에!
df = df[df["Pitch"].between(P_MIN - 1e-9, P_MAX + 1e-9)]

# (혹시 필터 후 데이터가 0개면 바로 알리기)
if df.empty:
    raise ValueError("Pitch 범위 필터 후 데이터가 비었습니다. P_MIN/P_MAX 또는 txt 데이터 범위를 확인하세요.")

grid = df.pivot(index="Duty", columns="Pitch", values="Value").sort_index().sort_index(axis=1)

P = grid.columns.to_numpy()
D = grid.index.to_numpy()
PP, DD = np.meshgrid(P, D)
Z = np.ma.masked_invalid(grid.to_numpy())

fig, ax = plt.subplots(figsize=(7, 4.5), constrained_layout=True)
cf = ax.contourf(PP, DD, Z, levels=LEVELS, cmap="turbo")
ax.contour(PP, DD, Z, levels=LEVELS, colors="k", linewidths=0.4)

ax.set_xlabel("Pitch (um)")
ax.set_ylabel("Duty Cycle")
ax.set_xlim(P_MIN, P_MAX)   # ✅ 표시도 0.85~1.00로 고정

cb = fig.colorbar(cf, ax=ax)
cb.set_label("Value")

plt.show()