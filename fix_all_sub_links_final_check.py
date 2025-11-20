import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 실제 존재하는 sub- 파일 목록 가져오기
def get_sub_files():
    """실제 존재하는 sub- 파일 목록"""
    sub_files = {}
    for file in os.listdir('.'):
        if file.startswith('sub-') and file.endswith('.html'):
            # 파일명에서 키워드 추출
            key = file.replace('sub-', '').replace('.html', '')
            sub_files[key] = file
    return sub_files

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

# 특정 매핑 (h3 텍스트 -> 실제 파일명)
SPECIFIC_MAPPINGS = {
    '공복혈당장애': 'sub-공복혈당장애.html',
    '공복혈당': 'sub-공복혈당.html',
    '당뇨병 합병증 (망막,신장 등)': 'sub-당뇨병합병증.html',
    '당뇨합병증': 'sub-당뇨합병증.html',
    '허리디스크/목디스크': 'sub-허리디스크목디스크.html',
    '오십견(유착성 관절낭염)': 'sub-오십견.html',
    '갑상선 기능 저하/항진': 'sub-갑상선.html',
    '갱년기 증후군': 'sub-갱년기증후군.html',
    '우울증/번아웃 증후군': 'sub-우울증번아웃.html',
    '수면장애/불면증': 'sub-수면장애불면증.html',
    '치매/경도인지장애': 'sub-치매경도인지장애.html',
    '이명/어지럼증': 'sub-이명어지럼증.html',
    '위염/위궤양': 'sub-위염위궤양.html',
    '지방간/간기능 저하': 'sub-지방간.html',
    '백내장/녹내장': 'sub-백내장녹내장.html',
    '치주염/치아손실': 'sub-치주염치아손실.html',
    '비만/체형변화': 'sub-비만체형변화.html',
}


def find_matching_file(h3_text, current_link, sub_files):
    """h3 텍스트와 현재 링크를 기반으로 올바른 파일 찾기"""
    # 특정 매핑 확인
    if h3_text in SPECIFIC_MAPPINGS:
        return SPECIFIC_MAPPINGS[h3_text]
    
    # 현재 링크에서 파일명 추출
    current_file = current_link.replace('sub-', '').replace('.html', '')
    
    # 현재 파일명이 실제 파일 목록에 있는지 확인
    if current_file in sub_files:
        return sub_files[current_file]
    
    # h3 텍스트를 기반으로 파일 찾기
    h3_clean = re.sub(r'[()/- ]', '', h3_text)
    
    for key, file in sub_files.items():
        key_clean = re.sub(r'[()/- ]', '', key)
        if h3_clean == key_clean or h3_clean in key_clean or key_clean in h3_clean:
            return file
    
    # 기본값: 현재 링크 유지
    return current_link


def fix_all_sub_links_final(filepath):
    """모든 서브 카테고리 링크 확인 및 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        sub_files = get_sub_files()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 패턴: <a href="sub-*.html" ... > ... <h3>텍스트</h3> ... </a>
        pattern = r'(<a href="(sub-[^"]+\.html)"([^>]*class="health-card"[^>]*>.*?<h3>([^<]+)</h3>.*?</a>))'
        
        def replace_link(match):
            full_link = match.group(1)
            current_link = match.group(2)
            h3_text = match.group(4).strip()
            
            # 올바른 파일 찾기
            correct_file = find_matching_file(h3_text, current_link, sub_files)
            
            # 파일이 실제로 존재하는지 확인
            if not os.path.exists(correct_file):
                # 파일이 없으면 현재 링크 유지
                return full_link
            
            # 링크 교체
            new_link = full_link.replace(f'href="{current_link}"', f'href="{correct_file}"')
            return new_link
        
        content = re.sub(pattern, replace_link, content, flags=re.DOTALL)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 서브 링크 수정 완료")
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
    print("🔧 모든 서브 카테고리 링크 최종 확인 및 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   h3 텍스트와 실제 파일명을 비교하여 링크 수정\n")
    
    print("📝 파일 확인 중...\n")
    fixed_count = 0
    
    for file in CATEGORY_FILES:
        if fix_all_sub_links_final(file):
            fixed_count += 1
    
    print(f"\n✅ 총 {fixed_count}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

