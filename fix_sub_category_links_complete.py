import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 실제 존재하는 sub- 파일 목록
SUB_FILES = [
    'sub-고혈압.html',
    'sub-고지혈증.html',
    'sub-협심증심근경색.html',
    'sub-동맥경화.html',
    'sub-뇌졸중.html',
    'sub-당뇨.html',
    'sub-공복혈당.html',
    'sub-혈당관리.html',
    'sub-인슐린.html',
    'sub-당뇨합병증.html',
    'sub-관절염.html',
    'sub-퇴행성관절염.html',
    'sub-허리디스크.html',
    'sub-골다공증.html',
    'sub-오십견.html',
    'sub-갱년기.html',
    'sub-갑상선.html',
    'sub-대사증후군.html',
    'sub-비만.html',
    'sub-우울증.html',
    'sub-치매.html',
    'sub-수면장애.html',
    'sub-위염.html',
    'sub-역류성식도염.html',
    'sub-지방간.html',
    'sub-과민성대장증후군.html',
    'sub-백내장.html',
    'sub-녹내장.html',
    'sub-치주질환.html',
]

# 카테고리명 -> sub-파일명 매핑
CATEGORY_TO_SUB = {
    '고혈압': 'sub-고혈압.html',
    '고지혈증-콜레스테롤': 'sub-고지혈증.html',
    '고지혈증(콜레스테롤)': 'sub-고지혈증.html',
    '협심증-심근경색': 'sub-협심증심근경색.html',
    '협심증/심근경색': 'sub-협심증심근경색.html',
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


def find_sub_file(category_name):
    """카테고리명으로 sub-파일 찾기"""
    # 직접 매핑 확인
    if category_name in CATEGORY_TO_SUB:
        return CATEGORY_TO_SUB[category_name]
    
    # 부분 매칭
    for key, value in CATEGORY_TO_SUB.items():
        if category_name in key or key in category_name:
            return value
    
    # 기본값: sub-{카테고리명}.html
    return f'sub-{category_name}.html'


def fix_sub_links(filepath):
    """서브 카테고리 링크 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 패턴 1: <a href="#" data-category="고혈압" onclick="loadCategoryPosts('고혈압'); return false;"
        pattern1 = r'<a href="#" data-category="([^"]+)" onclick="loadCategoryPosts\([^)]+\); return false;"'
        
        def replace_link1(match):
            category = match.group(1)
            if category:
                sub_file = find_sub_file(category)
                return f'<a href="{sub_file}"'
            return '<a href="#"'
        
        content = re.sub(pattern1, replace_link1, content)
        
        # 패턴 2: <a href="#" data-category="" onclick="loadCategoryPosts(''); return false;"
        # 이 경우 h3 태그의 텍스트를 사용
        pattern2 = r'<a href="#" data-category="" onclick="loadCategoryPosts\(\'\'\); return false;"([^>]*>.*?<h3>([^<]+)</h3>)'
        
        def replace_link2(match):
            full_match = match.group(0)
            category_text = match.group(2).strip()
            # 괄호 제거
            category_text = re.sub(r'[()]', '', category_text)
            sub_file = find_sub_file(category_text)
            return f'<a href="{sub_file}"{match.group(1)}'
        
        content = re.sub(pattern2, replace_link2, content, flags=re.DOTALL)
        
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
    print("🔧 서브 카테고리 링크 완전 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   data-category 링크를 sub-*.html로 변경\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in CATEGORY_FILES:
        if fix_sub_links(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

