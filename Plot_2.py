import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import AutoMinorLocator


# =======================
# 0) 폰트 설정 (가능하면 Cambria Math)
# =======================
def use_cambria_math_if_possible() -> str:
    candidates = [
        Path(r"C:\Windows\Fonts\cambriamath.ttf"),
        Path.home() / r"AppData\Local\Microsoft\Windows\Fonts\cambriamath.ttf",
    ]

    for fp in candidates:
        if fp.exists():
            fm.fontManager.addfont(str(fp))
            name = fm.FontProperties(fname=str(fp)).get_name()
            mpl.rcParams["font.family"] = name
            return name

    mpl.rcParams["font.family"] = "STIXGeneral"
    mpl.rcParams["mathtext.fontset"] = "stix"
    return "STIXGeneral"


chosen_font = use_cambria_math_if_possible()
print("Using font:", chosen_font)


# =======================
# 1) 사용자 설정
# =======================
DATA_DIR = Path(r"C:\Users\jbh12\OneDrive\Desktop\Data")

# txt 확장자 있을 때만 보고 싶으면 ["*.txt"] 로 두세요.
GLOB_PATTERNS = ["*.txt", "*"]

# 특정 Lspacer만 보고 싶으면 숫자 입력 (예: 0.5). 전체면 None
LSPACER_FILTER = 0.5

# (100um)/(200um) 선택:
# - None이면 실행 시 물어봄(추천)
# - 100 또는 200처럼 숫자 넣으면 고정
CORE_UM_FILTER = None   # 예: 100 / 200 / None(ask)

# 파일명 파라미터 정규식
RE_TIP = re.compile(r"Tip_first(?P<val>[0-9]*\.?[0-9]+)")
RE_LSP = re.compile(r"Lspacer(?P<val>[0-9]*\.?[0-9]+)")


# =======================
# 2) Matplotlib 스타일
# =======================
plt.rcParams.update({
    "font.family": chosen_font,
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


def extract_core_um(filename: str):
    # "(TE)" 같은 괄호도 있으니 "(숫자um)"만 찾기
    m = re.search(r"\((\d+)um\)", filename)
    return int(m.group(1)) if m else None


# =======================
# 3) 파일 로드 (메타데이터 추출)
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
        core_um = extract_core_um(name)

        # 최소 조건: Tip_first 있어야 플롯 가능
        if tip is None:
            continue

        # Lspacer 필터
        if LSPACER_FILTER is not None:
            if lsp is None or abs(lsp - float(LSPACER_FILTER)) > 1e-12:
                continue

        files.append((p, tip, lsp, core_um))

if not files:
    raise FileNotFoundError(
        f"조건에 맞는 파일을 못 찾았어요.\n"
        f"- 폴더: {DATA_DIR}\n"
        f"- LSPACER_FILTER={LSPACER_FILTER}\n"
        f"- 패턴: {GLOB_PATTERNS}\n"
    )

# =======================
# 3.5) (100um)/(200um) 선택
# =======================
available_cores = sorted({c for _, _, _, c in files if c is not None})

if CORE_UM_FILTER is None:
    # 콘솔에서 선택하게
    if available_cores:
        print("Available core sizes (um):", available_cores)
        choice = input("Select core size (e.g. 100 / 200 / all): ").strip().lower()
        if choice != "all":
            try:
                CORE_UM_FILTER = int(choice)
            except ValueError:
                raise ValueError("입력이 잘못됐어요. 100, 200 또는 all 로 입력해 주세요.")
    else:
        print("No '(xxxum)' pattern found in filenames. Core filtering will be skipped.")
        CORE_UM_FILTER = "all"

if CORE_UM_FILTER != "all" and CORE_UM_FILTER is not None:
    files = [t for t in files if t[3] == CORE_UM_FILTER]

if not files:
    raise FileNotFoundError(
        f"선택한 core_um={CORE_UM_FILTER} 조건에 맞는 파일이 없어요.\n"
        f"사용 가능한 core_um: {available_cores}"
    )

# Tip_first 기준 정렬(범례 정돈)
files.sort(key=lambda x: (x[1], x[2] if x[2] is not None else -np.inf))


# =======================
# 4) Plot (Tip_first별 색 고정)
# =======================
fig, ax = plt.subplots(figsize=(7.2, 4.6))

tips = sorted({round(tip, 6) for _, tip, _, _ in files})
base_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
tip_to_color = {tip: base_colors[i % len(base_colors)] for i, tip in enumerate(tips)}

labeled = set()

for path, tip, lsp, core_um in files:
    tip_key = round(tip, 6)
    df = pd.read_csv(path, sep=r"\s+", header=None, names=["L", "eta"], engine="python")

    x = df["L"].to_numpy()
    y = df["eta"].to_numpy()

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

# 타이틀에 core/Lspacer 표시
title_parts = []
if CORE_UM_FILTER not in (None, "all"):
    title_parts.append(f"Core = {CORE_UM_FILTER} um")
if LSPACER_FILTER is not None:
    title_parts.append(f"Lspacer = {float(LSPACER_FILTER):g}")
if title_parts:
    ax.set_title(" | ".join(title_parts))

fig.tight_layout()
plt.show(block=True)
