from pathlib import Path
import matplotlib.font_manager as fm

# (A) 윈도우 폰트 파일 존재 여부
p = Path(r"C:\Windows\Fonts\cambriamath.ttf")
print("cambriamath.ttf exists:", p.exists())

# (B) Matplotlib이 인식하는 폰트 이름 목록에서 Cambria 관련만
names = sorted({f.name for f in fm.fontManager.ttflist})
print([n for n in names if "Cambria" in n])
