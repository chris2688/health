import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# sub 파일 정보: (파일명, 페이지제목, 뒤로가기링크, 아이콘)
SUB_FILES_INFO = [
    # 심혈관
    ('sub-고혈압.html', '고혈압', 'category-심혈관질환.html', '🩺'),
    ('sub-고지혈증.html', '고지혈증(콜레스테롤)', 'category-심혈관질환.html', '💊'),
    ('sub-협심증심근경색.html', '협심증/심근경색', 'category-심혈관질환.html', '💔'),
    ('sub-동맥경화.html', '동맥경화', 'category-심혈관질환.html', '🫀'),
    ('sub-뇌졸중.html', '뇌졸중', 'category-심혈관질환.html', '🧠'),
    # 당뇨
    ('sub-당뇨.html', '당뇨병', 'category-당뇨병.html', '💉'),
    ('sub-공복혈당장애.html', '공복혈당장애', 'category-당뇨병.html', '📊'),
    ('sub-당뇨병합병증.html', '당뇨병 합병증 (망막,신장 등)', 'category-당뇨병.html', '👁️'),
    # 관절
    ('sub-허리디스크목디스크.html', '허리디스크/목디스크', 'category-관절근골격계.html', '🔴'),
    ('sub-골다공증.html', '골다공증', 'category-관절근골격계.html', '🦴'),
    ('sub-오십견.html', '오십견(유착성 관절낭염)', 'category-관절근골격계.html', '💪'),
    # 호르몬
    ('sub-갑상선.html', '갑상선 기능 저하/항진', 'category-호르몬내분비.html', '🦋'),
    ('sub-갱년기증후군.html', '갱년기 증후군', 'category-호르몬내분비.html', '🌸'),
    ('sub-대사증후군.html', '대사증후군', 'category-호르몬내분비.html', '⚖️'),
    # 정신건강
    ('sub-우울증번아웃.html', '우울증/번아웃 증후군', 'category-정신건강신경계.html', '😔'),
    ('sub-수면장애불면증.html', '수면장애/불면증', 'category-정신건강신경계.html', '😴'),
    ('sub-치매경도인지장애.html', '치매/경도인지장애', 'category-정신건강신경계.html', '🧩'),
    ('sub-이명어지럼증.html', '이명/어지럼증', 'category-정신건강신경계.html', '👂'),
    # 소화기
    ('sub-위염위궤양.html', '위염/위궤양', 'category-소화기질환.html', '🔴'),
    ('sub-역류성식도염.html', '역류성 식도염', 'category-소화기질환.html', '🔥'),
    ('sub-과민성대장증후군.html', '과민성 대장증후군', 'category-소화기질환.html', '💫'),
    ('sub-지방간.html', '지방간/간기능 저하', 'category-소화기질환.html', '🫀'),
    # 안과/치과
    ('sub-백내장녹내장.html', '백내장/녹내장', 'category-안과치과기타.html', '👓'),
    ('sub-치주염치아손실.html', '치주염/치아손실', 'category-안과치과기타.html', '🦷'),
    ('sub-비만체형변화.html', '비만/체형변화', 'category-안과치과기타.html', '⚖️'),
]

# sub-관절염.html을 템플릿으로 읽기
TEMPLATE_FILE = 'sub-관절염.html'


def generate_sub_file(filename, page_title, back_link, icon):
    """sub 파일 생성"""
    try:
        # 템플릿 읽기
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # 제목 변경
        template = re.sub(
            r'<title>.*?</title>',
            f'<title>{page_title} - 9988 건강정보</title>',
            template
        )
        
        # 페이지 제목 변경
        template = re.sub(
            r'<h1 class="page-title">.*?</h1>',
            f'<h1 class="page-title">{page_title}</h1>',
            template
        )
        
        # 뒤로가기 링크 변경
        template = re.sub(
            r'href="category-관절근골격계\.html"',
            f'href="{back_link}"',
            template
        )
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(template)
        
        return True
        
    except Exception as e:
        print(f"  ❌ {filename} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 모든 sub-*.html 파일 생성")
    print("=" * 60)
    print(f"\n📝 템플릿: {TEMPLATE_FILE}\n")
    
    if not os.path.exists(TEMPLATE_FILE):
        print(f"❌ 템플릿 파일이 없습니다: {TEMPLATE_FILE}")
        return
    
    print("📝 파일 생성 중...\n")
    created_count = 0
    skipped_count = 0
    
    for filename, page_title, back_link, icon in SUB_FILES_INFO:
        if os.path.exists(filename):
            # 파일이 이미 있으면 내용 확인
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content.strip()) > 100:  # 내용이 있으면
                    print(f"  ℹ️ {filename} - 이미 존재 (내용 있음, 재생성)")
                else:
                    print(f"  ⚠️ {filename} - 내용 없음, 재생성")
        
        if generate_sub_file(filename, page_title, back_link, icon):
            print(f"  ✅ {filename} - 생성 완료")
            created_count += 1
        else:
            skipped_count += 1
    
    print(f"\n✅ 총 {created_count}개 파일 생성 완료!")
    if skipped_count > 0:
        print(f"⚠️ {skipped_count}개 파일 생성 실패")
    print("=" * 60)


if __name__ == "__main__":
    main()

