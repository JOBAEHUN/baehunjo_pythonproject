import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import AutoMinorLocator
from matplotlib.lines import Line2D


def use_cambria_math_if_possible() -> str:
    candidates = [
        Path(r"C:\Windows\Fonts\cambriamath.ttf"),
        Path.home() / r"AppData\Local\Microsoft\Windows\Fonts\cambriamath.ttf",
    ]

    for fp in candidates:
        if fp.exists():
            fm.fontManager.addfont(str(fp))
            name = fm.FontProperties(fname=str(fp)).get_name()  # Matplotlib이 인식하는 실제 이름
            mpl.rcParams["font.family"] = name
            return name

    # 없으면 논문풍 대체(수식 포함 깔끔)
    mpl.rcParams["font.family"] = "STIXGeneral"
    mpl.rcParams["mathtext.fontset"] = "stix"
    return "STIXGeneral"


# =======================
# 0) 폰트 먼저 결정
# =======================
chosen_font = use_cambria_math_if_possible()
print("Using font:", chosen_font)

# =======================
# 1) 설정
# =======================
DATA_DIR = Path(r"C:\Users\jbh12\OneDrive\Desktop\Data")
GLOB_PATTERNS = ["*.txt", "*"]  # 필요하면 좁히세요
LSPACER_FILTER = 0.1  # 전체면 None

RE_TIP = re.compile(r"Tip_first(?P<val>[0-9]*\.?[0-9]+)")
RE_LSP = re.compile(r"Lspacer(?P<val>[0-9]*\.?[0-9]+)")

# =======================
# 2) Matplotlib 스타일 (논문풍)
# =======================
plt.rcParams.update({
    "font.family": chosen_font,   # <- 여기서 "Cambria Math"로 덮어쓰지 않게!
    "font.size": 12,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "legend.fontsize": 11,
    "axes.linewidth": 1.0,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 6,
    "ytick.major.size": 6,
    "xtick.minor.size": 3,
    "ytick.minor.size": 3,
    "xtick.top": True,
    "ytick.right": True,
})

def extract_param(pattern, text):
    m = pattern.search(text)
    return float(m.group("val")) if m else None

# =======================
# 3) 파일 로드
# =======================
files = []
for pat in GLOB_PATTERNS:
    for p in DATA_DIR.glob(pat):
        if not p.is_file():
            continue
        if p.suffix.lower() not in (".txt", ""):
            continue

        name = p.name
        tip = extract_param(RE_TIP, name)
        lsp = extract_param(RE_LSP, name)

        if tip is None:
            continue

        if LSPACER_FILTER is not None:
            if lsp is None or abs(lsp - float(LSPACER_FILTER)) > 1e-12:
                continue

        files.append((p, tip, lsp))

if not files:
    raise FileNotFoundError(
        f"조건에 맞는 파일을 못 찾았어요.\n"
        f"- 폴더: {DATA_DIR}\n"
        f"- LSPACER_FILTER={LSPACER_FILTER}\n"
        f"- 패턴: {GLOB_PATTERNS}\n"
        f"파일 확장자(.txt) 유무와 파일명에 'Tip_first'가 있는지 확인해 주세요."
    )

files.sort(key=lambda x: (x[1], x[2] if x[2] is not None else -np.inf))

# =======================
# 4) Plot
# =======================
fig, ax = plt.subplots(figsize=(7.2, 4.6))

# Tip_first 값별로 색을 고정
tips = sorted({round(tip, 6) for _, tip, _ in files})
base_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]  # 기본 컬러 사이클
tip_to_color = {tip: base_colors[i % len(base_colors)] for i, tip in enumerate(tips)}

labeled = set()

for path, tip, lsp in files:
    tip_key = round(tip, 6)
    df = pd.read_csv(path, sep=r"\s+", header=None, names=["L", "eta"], engine="python")

    x = df["L"].to_numpy()
    y = df["eta"].to_numpy()

    # 같은 Tip_first 여러 개 파일이 있어도 색은 동일, 범례는 1번만
    label = f"Tip_first = {tip_key:g}" if tip_key not in labeled else "_nolegend_"
    if tip_key not in labeled:
        labeled.add(tip_key)

    ax.plot(x, y, linewidth=1.8, color=tip_to_color[tip_key], label=label)

ax.set_xlabel("Coupling Length")
ax.set_ylabel("Coupling Efficiency")
ax.margins(x=0.02, y=0.05)

ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.grid(True, which="major", linewidth=0.6, alpha=0.35)
ax.grid(True, which="minor", linewidth=0.4, alpha=0.18)

ax.legend(frameon=False, loc="best")

if LSPACER_FILTER is not None:
    ax.set_title(f"Lspacer = {float(LSPACER_FILTER):g}")

fig.tight_layout()
plt.show()
