import pytesseract
from PIL import Image
import os
import re
from PyPDF2 import PdfMerger
import io

# 1. Tesseract 설치 경로 설정 (윈도우 사용자 필수 확인)
# 설치 경로가 다르다면 아래 경로를 실제 설치된 위치로 수정해주세요.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def convert_to_high_quality_pdf():
    # 사용자 폴더 경로
    folder_path = r'C:\Users\Baehun Jo\OneDrive\Desktop\ASDL\대학원 영어시험\지텔프 문법'
    output_filename = "지텔프_문법_합본.pdf"

    # 2. 파일 목록 가져오기 및 숫자 순서대로 정렬
    files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

    # 파일명에서 숫자 부분만 추출하여 정렬 (스크린샷 (10) -> 10)
    def extract_number(filename):
        numbers = re.findall(r'\d+', filename)
        return int(numbers[-1]) if numbers else 0

    files.sort(key=extract_number)
    print(f"발견된 파일 순서: {files}")

    merger = PdfMerger()

    for file in files:
        img_path = os.path.join(folder_path, file)

        # 3. 고화질 처리를 위한 이미지 열기
        img = Image.open(img_path)

        # OCR 수행 (한글+영어) 및 PDF 데이터 생성
        # extension='pdf'로 설정하면 텍스트 레이어가 포함된 PDF 바이트가 생성됨
        print(f"처리 중: {file}...")
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, lang='kor+eng', extension='pdf')

        # 메모리 상에서 바로 병합
        merger.append(io.BytesIO(pdf_bytes))

    # 4. 최종 결과 저장
    save_path = os.path.join(folder_path, output_filename)
    merger.write(save_path)
    merger.close()

    print("-" * 30)
    print(f"최종 고화질 OCR PDF 생성 완료!")
    print(f"경로: {save_path}")


if __name__ == "__main__":
    convert_to_high_quality_pdf()