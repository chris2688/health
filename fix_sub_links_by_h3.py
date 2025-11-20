import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 카테고리명 -> sub-파일명 매핑
CATEGORY_TO_SUB = {
    '고혈압': 'sub-고혈압.html',
    '고지혈증(콜레스테롤)': 'sub-고지혈증.html',
    '고지혈증-콜레스테롤': 'sub-고지혈증.html',
    '협심증/심근경색': 'sub-협심증심근경색.html',
    '협심증-심근경색': 'sub-협심증심근경색.html',
    '동맥경화': 'sub-동맥경화.html',
    '뇌졸중': 'sub-뇌졸중.html',
    '당뇨병': 'sub-당뇨.html',
    '공복혈당': 'sub-공복혈당.html',
    '혈당관리': 'sub-혈당관리.html',
    '인슐린': 'sub-인슐린.html',
    '당뇨합병증': 'sub-당뇨합병증.html',
    '관절염': 'sub-관절염.html',
    '퇴행성관절염': 'sub-퇴행성관절염.html',
    '허리디스크': 'sub-허리디스크.html',
    '골다공증': 'sub-골다공증.html',
    '오십견': 'sub-오십견.html',
    '갱년기': 'sub-갱년기.html',
    '갑상선': 'sub-갑상선.html',
    '대사증후군': 'sub-대사증후군.html',
    '비만': 'sub-비만.html',
    '우울증': 'sub-우울증.html',
    '치매': 'sub-치매.html',
    '수면장애': 'sub-수면장애.html',
    '위염': 'sub-위염.html',
    '역류성식도염': 'sub-역류성식도염.html',
    '지방간': 'sub-지방간.html',
    '과민성대장증후군': 'sub-과민성대장증후군.html',
    '백내장': 'sub-백내장.html',
    '녹내장': 'sub-녹내장.html',
    '치주질환': 'sub-치주질환.html',
}

# 수정할 파일 목록
CATEGORY_FILES = [
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
]


def find_sub_file(category_text):
    """카테고리 텍스트로 sub-파일 찾기"""
    # 직접 매핑 확인
    if category_text in CATEGORY_TO_SUB:
        return CATEGORY_TO_SUB[category_text]
    
    # 괄호 제거 후 매핑
    clean_text = re.sub(r'[()]', '', category_text)
    if clean_text in CATEGORY_TO_SUB:
        return CATEGORY_TO_SUB[clean_text]
    
    # 부분 매칭
    for key, value in CATEGORY_TO_SUB.items():
        key_clean = re.sub(r'[()/-]', '', key)
        text_clean = re.sub(r'[()/-]', '', category_text)
        if key_clean in text_clean or text_clean in key_clean:
            return value
    
    # 기본값: sub-{카테고리명}.html (괄호 제거)
    clean_name = re.sub(r'[()]', '', category_text)
    return f'sub-{clean_name}.html'


def fix_sub_links_by_h3(filepath):
    """h3 태그 텍스트를 기반으로 서브 카테고리 링크 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 패턴: <a href="#" ... > ... <h3>카테고리명</h3> ... </a>
        # health-card 클래스를 가진 링크 찾기
        pattern = r'(<a href="#"[^>]*class="health-card"[^>]*>.*?<h3>([^<]+)</h3>.*?</a>)'
        
        def replace_link(match):
            full_link = match.group(1)
            category_text = match.group(2).strip()
            
            # sub-파일 찾기
            sub_file = find_sub_file(category_text)
            
            # href="#"를 href="sub-파일"로 변경
            new_link = re.sub(r'href="#"', f'href="{sub_file}"', full_link)
            
            return new_link
        
        content = re.sub(pattern, replace_link, content, flags=re.DOTALL)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 서브 카테고리 링크 수정 완료")
            return True
        else:
            print(f"  ℹ️ {filepath} - 변경사항 없음")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 h3 텍스트 기반 서브 카테고리 링크 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   h3 태그의 텍스트를 기반으로 sub-*.html 링크 생성\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in CATEGORY_FILES:
        if fix_sub_links_by_h3(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

