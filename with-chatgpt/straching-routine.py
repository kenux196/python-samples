from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
import platform
from typing import List, Dict

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

# 상수 정의
PDF_TITLE = "목 · 어깨 · 허리 통합 스트레칭 루틴 (5분 루틴)"
OUTPUT_FILE = "스트레칭_루틴_한글버전.pdf"
FONT_NAME = "Nanum"
TITLE_FONT_SIZE = 14
CONTENT_FONT_SIZE = 12

def get_font_path() -> str:
    """운영체제별 폰트 경로를 반환합니다."""
    font_paths = {
        "Darwin": os.path.expanduser("~/Library/Fonts/NanumGothic.ttf"),
        "Windows": "C:/Windows/Fonts/NanumGothic.ttf",
        "Linux": "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    }
    
    system = platform.system()
    if system not in font_paths:
        raise RuntimeError(f"지원하지 않는 운영체제입니다: {system}")
    
    font_path = font_paths[system]
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"나눔고딕 폰트 파일을 찾을 수 없습니다: {font_path}")
    
    return font_path

def create_pdf(routine_data: List[Dict]) -> None:
    """PDF를 생성합니다."""
    # 폰트 등록
    font_path = get_font_path()
    pdfmetrics.registerFont(TTFont(FONT_NAME, font_path))
    
    # PDF 문서 생성
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # 스타일 설정
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Korean',
        fontName=FONT_NAME,
        fontSize=12,
        leading=16
    ))
    
    # 내용 작성
    story = []
    story.append(Paragraph(PDF_TITLE, ParagraphStyle(
        'Title',
        fontName=FONT_NAME,
        fontSize=16,
        spaceAfter=30
    )))
    
    for routine in routine_data:
        story.append(Paragraph(routine['title'], styles['Korean']))
        for step in routine['steps']:
            story.append(Paragraph(f"• {step}", styles['Korean']))
        story.append(Spacer(1, 12))
    
    # PDF 생성
    doc.build(story)

def main():
    """메인 함수"""
    try:
        create_pdf(korean_routine)
        print(f"PDF가 성공적으로 생성되었습니다: {OUTPUT_FILE}")
    except Exception as e:
        print(f"PDF 생성 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()