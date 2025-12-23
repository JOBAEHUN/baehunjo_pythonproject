from pathlib import Path
import re

#오케이

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -------------------------------------------------
# 1) 파일 이름에서 파라미터 뽑기
#    예) (TE)1.31um 메쉬0.04 셀40 Lspacer0.2 Nominal0.9 Tip0.1 SMF_diameter4 Y_misalignment0.csv
# -------------------------------------------------
def parse_params(path: Path):
    name = path.stem  # 확장자(.csv) 제거
    params = {}

    def grab(key, pattern):
        m = re.search(pattern, name)
        if m:
            try:
                params[key] = float(m.group(1))
            except ValueError:
                pass

    grab("Lspacer",       r"Lspacer([0-9.]+)")
    grab("Nominal",       r"Nominal([0-9.]+)")
    grab("Tip",           r"Tip([0-9.]+)")
    grab("SMF_diameter",  r"SMF_diameter([0-9.]+)")
    grab("Y_misalignment", r"Y_misalignment(-?[0-9.]+)")

    # 편의상 편광 / 파장도 필요하면 쓸 수 있게
    m = re.search(r"\((TE|TM)\)", name)
    if m:
        params["pol"] = m.group(1)

    m = re.search(r"([0-9.]+)um", name)
    if m:
        try:
            params["lambda_um"] = float(m.group(1))
        except ValueError:
            pass

    return params


# -------------------------------------------------
# 2) CSV 한 개에서 L, CE 읽어서 (L[µm], C.L[dB])로 반환
#    CSV 형식: 컬럼 이름이 L, CE 라고 가정
# -------------------------------------------------
def read_ce_data(csv_path: Path):
    df = pd.read_csv(csv_path)

    if not {"L", "CE"}.issubset(df.columns):
        raise ValueError(f"{csv_path.name} 에 L, CE 컬럼이 없음")

    # L: m 단위라고 가정 → µm로 변환
    L_m = pd.to_numeric(df["L"], errors="coerce").to_numpy(dtype=float)
    CE  = pd.to_numeric(df["CE"], errors="coerce").to_numpy(dtype=float)

    # CE: 0 < CE <= 1 인 것만 사용 (그 외는 NaN/0/쓰레기 값이라 생각)
    valid = np.isfinite(L_m) & np.isfinite(CE) & (CE > 0) & (CE <= 1)

    L_um  = L_m[valid] * 1e6  # m → µm
    CE_ok = CE[valid]

    # Coupling loss [dB]
    CL_dB = -10 * np.log10(CE_ok)

    return L_um, CL_dB


# -------------------------------------------------
# 3) 전체 폴더(하위폴더 포함)에서 하나의 DataFrame 만들기
#    각 row: (Lspacer, L_um, CL_dB, Nominal, Tip, SMF_diameter, Y_misalignment, file)
# -------------------------------------------------
def build_dataframe(base_dir: str):
    base = Path(base_dir)
    records = []

    # **하위 폴더까지 전부 탐색**
    for csv in base.rglob("*.csv"):
        params = parse_params(csv)

        try:
            L_um, CL_dB = read_ce_data(csv)
        except Exception as e:
            print(f"스킵: {csv.name} -> {e}")
            continue

        for L_val, cl in zip(L_um, CL_dB):
            records.append(
                {
                    "file": csv.name,
                    "L_um": L_val,          # x축
                    "CL_dB": cl,           # 색
                    "Lspacer": params.get("Lspacer"),
                    "Nominal": params.get("Nominal"),
                    "Tip": params.get("Tip"),
                    "SMF_diameter": params.get("SMF_diameter"),
                    "Y_misalignment": params.get("Y_misalignment"),
                }
            )

    return pd.DataFrame(records)


# -------------------------------------------------
# 4) Lspacer–L 히트맵 그리기
#    x축: coupling length L (µm)
#    y축: Lspacer (µm)
#    색: C.L. (dB)
#    나머지(Nominal, Tip, SMF_diameter, Y_mis)는 필터로 고정
# -------------------------------------------------
def plot_heatmap_Lspacer_vs_L(
    base_dir,
    nominal_filter=None,
    tip_filter=None,
    smf_filter=None,
    y_mis_filter=None,
):
    df = build_dataframe(base_dir)

    if df.empty:
        print("읽어온 데이터가 없음 ㅠㅠ")
        return

    # 전체에서 시작해서 조건별로 좁혀가는 마스크
    mask = np.ones(len(df), dtype=bool)

    # 숫자 필드 필터 도우미
    def apply_filter(col_name, value):
        nonlocal mask, df
        if value is None:
            return
        col = pd.to_numeric(df[col_name], errors="coerce")
        mask &= np.isclose(col, value, atol=1e-9)

    if nominal_filter is not None:
        apply_filter("Nominal", nominal_filter)
    if tip_filter is not None:
        apply_filter("Tip", tip_filter)
    if smf_filter is not None:
        apply_filter("SMF_diameter", smf_filter)
    if y_mis_filter is not None:
        apply_filter("Y_misalignment", y_mis_filter)

    df_sel = df[mask].copy()

    if df_sel.empty:
        print("조건에 맞는 데이터가 없음 ㅠㅠ")
        return

    # 피벗: 행=Lspacer, 열=L, 값=CL_dB
    pivot = df_sel.pivot_table(
        index="Lspacer",
        columns="L_um",
        values="CL_dB",
        aggfunc="mean",   # 동일 좌표가 여러 번 있으면 평균
    )

    pivot = pivot.sort_index().sort_index(axis=1)

    X, Y = np.meshgrid(pivot.columns.values, pivot.index.values)
    Z = pivot.to_numpy()

    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.pcolormesh(X, Y, Z, shading="auto")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("C.L. (dB)")

    ax.set_xlabel("Coupling length L (µm)")
    ax.set_ylabel("Lspacer (µm)")

    title = []
    if nominal_filter is not None:
        title.append(f"Nominal = {nominal_filter} µm")
    if tip_filter is not None:
        title.append(f"Tip = {tip_filter} µm")
    if smf_filter is not None:
        title.append(f"SMF_d = {smf_filter} µm")
    if y_mis_filter is not None:
        title.append(f"Y_mis = {y_mis_filter} µm")

    ax.set_title(", ".join(title) if title else "Lspacer vs L heatmap")

    plt.tight_layout()
    plt.show()


# -------------------------------------------------
# 5) 실행 예시
# -------------------------------------------------
if __name__ == "__main__":
    base_dir = r"C:\MyPythonProject\data\TE Mode 400nm"

    plot_heatmap_Lspacer_vs_L(
        base_dir=base_dir,
        nominal_filter=0.9,   # Nominal0.9
        tip_filter=0.05,      # Tip0.05 (원하면 다른 값으로)
        smf_filter=4.0,       # SMF_diameter4
        y_mis_filter=0.0,     # Y_misalignment0
    )
