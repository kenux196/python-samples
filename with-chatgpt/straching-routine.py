from fpdf import FPDF
import os
import platform

# 한글 스트레칭 루틴
korean_routine = [
    {
        "title": "1. 고개 천천히 돌리기 (1분)",
        "steps": [
            "오른쪽으로 천천히 돌려 5초 유지 → 반대 방향으로도",
            "고개를 아래로 숙이고 턱을 당긴 채 10초 유지 (C자형 교정)"
        ]
    },
    {
        "title": "2. 어깨 으쓱 & 돌리기 (1분)",
        "steps": [
            "어깨 으쓱으쓱 10회 → 앞→뒤로 크게 원 그리듯 돌리기 10회",
            "왼쪽 어깨 위에 오른손 얹고, 고개는 오른쪽으로 돌려 10초 → 반대쪽도"
        ]
    },
    {
        "title": "3. 가슴 열기 & 팔 뒤로 뻗기 (1분)",
        "steps": [
            "양손을 뒤로 깍지 끼고, 가슴을 쫙 편 채로 15초 유지 x 2세트",
            "팔꿈치 굽힌 상태에서 벽에 팔 대고 가슴 열기 10초씩"
        ]
    },
    {
        "title": "4. 허리 & 척추 스트레칭 (1분)",
        "steps": [
            "양손을 허벅지 위에 두고, 고양이 자세 / 소 자세 의자 버전으로!",
            "등을 둥글게 말아주기 (고양이) → 허리를 뒤로 젖혀 열어주기 (소) 10회"
        ]
    },
    {
        "title": "5. 다리 쭉 뻗고 숙이기 (1분)",
        "steps": [
            "의자에서 살짝 내려앉아 다리 쭉 뻗고, 허리 굽히지 말고 앞으로 숙이기",
            "햄스트링, 허리 근육 이완 효과 굿!"
        ]
    }
]

# PDF 생성
pdf = FPDF()
pdf.add_page()

# ⬇️ 여기에 너의 나눔고딕 폰트 경로를 넣어줘!
if platform.system() == "Darwin":  # macOS
  font_path = os.path.expanduser("~/Library/Fonts/NanumGothic.ttf")
elif platform.system() == "Windows":  # Windows
  font_path = "C:/Windows/Fonts/NanumGothic.ttf"
elif platform.system() == "Linux":  # Linux
  font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
else:
  raise RuntimeError("Unsupported OS")
pdf.add_font("Nanum", "", font_path, uni=True)
pdf.set_font("Nanum", size=14)

pdf.cell(0, 10, "목 · 어깨 · 허리 통합 스트레칭 루틴 (5분 루틴)", ln=True)

for routine in korean_routine:
    pdf.ln(5)
    pdf.set_font("Nanum", size=12)
    pdf.multi_cell(0, 10, f"[{routine['title']}]")
    for step in routine["steps"]:
        pdf.multi_cell(0, 8, f"- {step}")

# 저장
pdf.output("스트레칭_루틴_한글버전.pdf")