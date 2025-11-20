import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 모든 서브 카테고리 정보
SUB_CATEGORIES = {
    # 심혈관질환
    'sub-고혈압.html': {
        'title': '고혈압 - 9988 건강정보',
        'page_title': '고혈압',
        'back_link': 'category-심혈관질환.html',
        'category_slug': 'cardiovascular'
    },
    'sub-고지혈증.html': {
        'title': '고지혈증 - 9988 건강정보',
        'page_title': '고지혈증',
        'back_link': 'category-심혈관질환.html',
        'category_slug': 'cardiovascular'
    },
    'sub-협심증심근경색.html': {
        'title': '협심증/심근경색 - 9988 건강정보',
        'page_title': '협심증/심근경색',
        'back_link': 'category-심혈관질환.html',
        'category_slug': 'cardiovascular'
    },
    'sub-동맥경화.html': {
        'title': '동맥경화 - 9988 건강정보',
        'page_title': '동맥경화',
        'back_link': 'category-심혈관질환.html',
        'category_slug': 'cardiovascular'
    },
    'sub-뇌졸중.html': {
        'title': '뇌졸중 - 9988 건강정보',
        'page_title': '뇌졸중',
        'back_link': 'category-심혈관질환.html',
        'category_slug': 'cardiovascular'
    },
    # 당뇨병
    'sub-당뇨.html': {
        'title': '당뇨병 - 9988 건강정보',
        'page_title': '당뇨병',
        'back_link': 'category-당뇨병.html',
        'category_slug': 'diabetes'
    },
    'sub-공복혈당장애.html': {
        'title': '공복혈당장애 - 9988 건강정보',
        'page_title': '공복혈당장애',
        'back_link': 'category-당뇨병.html',
        'category_slug': 'diabetes'
    },
    'sub-당뇨병합병증.html': {
        'title': '당뇨병 합병증 - 9988 건강정보',
        'page_title': '당뇨병 합병증',
        'back_link': 'category-당뇨병.html',
        'category_slug': 'diabetes'
    },
    # 관절근골격계
    'sub-관절염.html': {
        'title': '관절염 - 9988 건강정보',
        'page_title': '관절염',
        'back_link': 'category-관절근골격계.html',
        'category_slug': 'joint'
    },
    'sub-허리디스크목디스크.html': {
        'title': '허리디스크/목디스크 - 9988 건강정보',
        'page_title': '허리디스크/목디스크',
        'back_link': 'category-관절근골격계.html',
        'category_slug': 'joint'
    },
    'sub-골다공증.html': {
        'title': '골다공증 - 9988 건강정보',
        'page_title': '골다공증',
        'back_link': 'category-관절근골격계.html',
        'category_slug': 'joint'
    },
    'sub-오십견.html': {
        'title': '오십견 - 9988 건강정보',
        'page_title': '오십견',
        'back_link': 'category-관절근골격계.html',
        'category_slug': 'joint'
    },
    # 호르몬내분비
    'sub-갑상선.html': {
        'title': '갑상선 - 9988 건강정보',
        'page_title': '갑상선',
        'back_link': 'category-호르몬내분비.html',
        'category_slug': 'endocrine'
    },
    'sub-갱년기증후군.html': {
        'title': '갱년기 증후군 - 9988 건강정보',
        'page_title': '갱년기 증후군',
        'back_link': 'category-호르몬내분비.html',
        'category_slug': 'endocrine'
    },
    'sub-대사증후군.html': {
        'title': '대사증후군 - 9988 건강정보',
        'page_title': '대사증후군',
        'back_link': 'category-호르몬내분비.html',
        'category_slug': 'endocrine'
    },
    # 정신건강신경계
    'sub-우울증번아웃.html': {
        'title': '우울증/번아웃 - 9988 건강정보',
        'page_title': '우울증/번아웃',
        'back_link': 'category-정신건강신경계.html',
        'category_slug': 'mental-health'
    },
    'sub-수면장애불면증.html': {
        'title': '수면장애/불면증 - 9988 건강정보',
        'page_title': '수면장애/불면증',
        'back_link': 'category-정신건강신경계.html',
        'category_slug': 'mental-health'
    },
    'sub-치매경도인지장애.html': {
        'title': '치매/경도인지장애 - 9988 건강정보',
        'page_title': '치매/경도인지장애',
        'back_link': 'category-정신건강신경계.html',
        'category_slug': 'mental-health'
    },
    'sub-이명어지럼증.html': {
        'title': '이명/어지럼증 - 9988 건강정보',
        'page_title': '이명/어지럼증',
        'back_link': 'category-정신건강신경계.html',
        'category_slug': 'mental-health'
    },
    # 소화기질환
    'sub-위염위궤양.html': {
        'title': '위염/위궤양 - 9988 건강정보',
        'page_title': '위염/위궤양',
        'back_link': 'category-소화기질환.html',
        'category_slug': 'digestive'
    },
    'sub-역류성식도염.html': {
        'title': '역류성 식도염 - 9988 건강정보',
        'page_title': '역류성 식도염',
        'back_link': 'category-소화기질환.html',
        'category_slug': 'digestive'
    },
    'sub-과민성대장증후군.html': {
        'title': '과민성 대장증후군 - 9988 건강정보',
        'page_title': '과민성 대장증후군',
        'back_link': 'category-소화기질환.html',
        'category_slug': 'digestive'
    },
    'sub-지방간.html': {
        'title': '지방간 - 9988 건강정보',
        'page_title': '지방간',
        'back_link': 'category-소화기질환.html',
        'category_slug': 'digestive'
    },
    # 안과치과기타
    'sub-백내장녹내장.html': {
        'title': '백내장/녹내장 - 9988 건강정보',
        'page_title': '백내장/녹내장',
        'back_link': 'category-안과치과기타.html',
        'category_slug': 'eye-dental'
    },
    'sub-치주염치아손실.html': {
        'title': '치주염/치아손실 - 9988 건강정보',
        'page_title': '치주염/치아손실',
        'back_link': 'category-안과치과기타.html',
        'category_slug': 'eye-dental'
    },
    'sub-비만체형변화.html': {
        'title': '비만/체형변화 - 9988 건강정보',
        'page_title': '비만/체형변화',
        'back_link': 'category-안과치과기타.html',
        'category_slug': 'eye-dental'
    },
}

# sub-갑상선.html을 템플릿으로 읽기
TEMPLATE_FILE = 'sub-갑상선.html'


def generate_sub_page(filename, data):
    """서브 페이지 생성"""
    try:
        # 템플릿 읽기
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # 제목 교체
        template = re.sub(
            r'<title>.*?</title>',
            f'<title>{data["title"]}</title>',
            template
        )
        
        # 페이지 제목 교체
        template = re.sub(
            r'<h1 class="page-title">.*?</h1>',
            f'<h1 class="page-title">{data["page_title"]}</h1>',
            template
        )
        
        # 뒤로가기 링크 교체
        template = re.sub(
            r'href="category-[^"]+\.html" class="back-button"',
            f'href="{data["back_link"]}" class="back-button"',
            template
        )
        
        # 카테고리 슬러그 교체 (JavaScript 부분)
        template = re.sub(
            r"'sub-갑상선\.html': 'endocrine'",
            f"'{filename}': '{data[\"category_slug\"]}'",
            template
        )
        
        # 페이지 제목 기반 카테고리 매핑 추가
        page_title_escaped = data["page_title"].replace("'", "\\'")
        template = re.sub(
            r"const pageToCategory = \{",
            f"const pageToCategory = {{\n                    '{filename}': '{data[\"category_slug\"]}',",
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
    print("🔧 모든 sub-*.html 파일 재생성")
    print("=" * 60)
    print("\n💡 템플릿: sub-갑상선.html\n")
    
    if not os.path.exists(TEMPLATE_FILE):
        print(f"❌ 템플릿 파일을 찾을 수 없습니다: {TEMPLATE_FILE}")
        return
    
    print("📝 파일 생성 중...\n")
    created_count = 0
    
    for filename, data in SUB_CATEGORIES.items():
        if generate_sub_page(filename, data):
            print(f"  ✅ {filename} - 생성 완료")
            created_count += 1
        else:
            print(f"  ❌ {filename} - 생성 실패")
    
    print(f"\n✅ 총 {created_count}개 파일 생성 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

