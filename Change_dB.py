import pandas as pd
import numpy as np
import os
import glob

# ==========================================
# 1. 폴더 경로 설정 (여기에 실제 경로를 복사해서 넣으세요)
# 예시: r"C:\Users\Name\Desktop\MyData"
# 문자열 앞에 r을 붙이면 윈도우 경로(\) 오류를 방지할 수 있습니다.
folder_path = r"C:\MyPythonProject\data\TE Mode 400nm\4"
# ==========================================

# 해당 폴더 내의 모든 .csv 파일 경로를 리스트로 가져옵니다.
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

print(f"총 {len(csv_files)}개의 CSV 파일을 찾았습니다.\n")

for file_path in csv_files:
    try:
        # 이미 변환된 파일(_dB.csv)은 건너뛰기 (중복 실행 방지)
        if "_dB.csv" in file_path:
            continue

        # 파일 읽기
        df = pd.read_csv(file_path)

        # 파일 이름만 추출 (출력용)
        file_name = os.path.basename(file_path)
        print(f"처리 중: {file_name} ...", end=" ")

        # 컬럼 이름 변경 ('CE' -> 'C.E')
        if 'CE' in df.columns:
            df.rename(columns={'CE': 'C.E'}, inplace=True)

        # 'C.E' 컬럼이 있는지 확인 후 계산
        if 'C.E' in df.columns:
            # dB 계산: 10 * log10(C.E)
            df['C.E(dB)'] = - 10 * np.log10(df['C.E'])

            # 저장할 파일 이름 생성 (원본이름_dB.csv)
            new_file_path = file_path.replace(".csv", "_dB.csv")

            # 저장
            df.to_csv(new_file_path, index=False)
            print("완료! -> 저장됨")
        else:
            print("실패 (C.E 또는 CE 열이 없음)")

    except Exception as e:
        print(f"\n에러 발생 ({file_name}): {e}")

print("\n모든 작업이 끝났습니다.")