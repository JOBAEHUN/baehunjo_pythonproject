import math

# GC 길이(µm) = 700 + 150·π
L_GC = 400 + (200 * math.pi)         # ≈ 1 171.238 µm

def snake_total_length(i: int, with_gc: bool = True) -> float:
    """
    Propagation-loss 트랙의 총 길이(µm)를 반환.
    i : 루프 인덱스 (0, 2, 4, …)   — 2씩 증가할 때마다 루프 2개 추가
    with_gc : GC 연결부 길이를 포함할지 여부
    """
    # 1) 밴딩 구간
    loops = i                         # 밴드 개수
    L_bend = (1+loops) * 2 * math.pi * 200    # 2πD

    # 2) 직경 보정
    L_corr = 600                          # 300 × 2

    # 3) 수직(Y) 직선
    Ly = 2 * (0 * (i + 1) + 16 * i * (i + 1) / 2)

    # 4) 수평(X) 직선
    Lx = 2 * (8 * (i + 1) + 8 * i * (i + 1) / 2)

    # 5) 총합
    L_total = L_bend + L_corr + Ly + Lx
    if with_gc:
        L_total += L_GC
    return L_total

# 예시: i = 0, 2, 4  (단위 µm)
for i in (1,4,8,12,16,20,24):
    print(f"i={i:>2}:  L_total = {snake_total_length(i):.2f} µm")