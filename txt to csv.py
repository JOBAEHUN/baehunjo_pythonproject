#!/usr/bin/env python
# txt_to_csv_delete_txt.py

from pathlib import Path
import pandas as pd

# ✅ 여기만 네 txt 파일들이 있는 폴더 경로로 바꿔주면 됨
# 예) ROOT_DIR = Path(r"C:\Users\찐\Desktop\coupling_txt")
ROOT_DIR = Path(r"C:\Users\jbh12\OneDrive\Desktop\Data_2\굴절률 스윕")


def convert_txt_to_csv_and_delete(txt_path: Path):
    """공백/탭으로 구분된 2컬럼 숫자 txt -> csv 변환 후 txt 삭제"""
    # 1) txt를 읽어서 DataFrame으로 변환
    df = pd.read_csv(
        txt_path,
        sep=r"\s+",          # 공백/탭 모두 구분자로 인식
        header=None,         # 헤더 없음
        names=["L", "CE"],   # x: coupling length, y: coupling efficiency
        engine="python",
    )

    # 2) 같은 이름으로 확장자만 .csv 로 변경
    csv_path = txt_path.with_suffix(".csv")
    df.to_csv(csv_path, index=False)

    # 3) 여기까지 왔으면 변환 성공이니까 txt 삭제
    txt_path.unlink()

    print(f"[OK] {txt_path.name}  ->  {csv_path.name} (원본 txt 삭제 완료)")


def main():
    if not ROOT_DIR.exists():
        print(f"[ERR] 경로가 존재하지 않습니다: {ROOT_DIR}")
        return

    if ROOT_DIR.is_file():
        # ROOT_DIR에 txt 하나를 직접 넣은 경우도 처리 (옵션용)
        txt_path = ROOT_DIR
        if txt_path.suffix.lower() != ".txt":
            print(f"[ERR] txt 파일이 아닙니다: {txt_path}")
            return
        try:
            convert_txt_to_csv_and_delete(txt_path)
        except Exception as e:
            print(f"[ERR] 변환 실패: {txt_path.name} -> {e}")
        return

    # 폴더인 경우: 폴더 안의 모든 *.txt 변환
    txt_files = sorted(ROOT_DIR.glob("*.txt"))
    if not txt_files:
        print(f"[WARN] {ROOT_DIR} 안에서 *.txt 파일을 찾지 못했습니다.")
        return

    print(f"[INFO] 폴더: {ROOT_DIR}  / txt 파일 개수: {len(txt_files)}")
    for txt_path in txt_files:
        try:
            convert_txt_to_csv_and_delete(txt_path)
        except Exception as e:
            print(f"[ERR] 변환 실패: {txt_path.name} -> {e}")


if __name__ == "__main__":
    main()
