import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 카테고리명 -> category 파일명 매핑
CATEGORY_MAPPING = {
    '심혈관 질환': 'category-심혈관질환.html',
    '당뇨병': 'category-당뇨병.html',
    '관절/근골격계': 'category-관절근골격계.html',
    '호르몬/내분비': 'category-호르몬내분비.html',
    '정신건강/신경계': 'category-정신건강신경계.html',
    '소화기 질환': 'category-소화기질환.html',
    '안과/치과/기타': 'category-안과치과기타.html',
}


def fix_index_v2_links(filepath):
    """index-v2.html의 카테고리 링크를 category-*.html로 변경"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 각 카테고리 카드의 링크 수정
        for category_name, category_file in CATEGORY_MAPPING.items():
            # 패턴: <a href="sub-*.html" ... > ... <h2 class="card-title">카테고리명</h2> ...
            pattern = rf'(<a href="[^"]*" class="health-card"[^>]*>.*?<h2 class="card-title">){re.escape(category_name)}(</h2>.*?</a>)'
            
            def replace_link(match):
                return f'{match.group(1)}{category_name}{match.group(2)}'.replace(
                    re.search(r'href="[^"]*"', match.group(0)).group(0),
                    f'href="{category_file}"'
                )
            
            # 더 정확한 패턴 사용
            pattern2 = rf'(<a href=")[^"]*("[^>]*class="health-card"[^>]*>.*?<h2 class="card-title">){re.escape(category_name)}(</h2>)'
            content = re.sub(pattern2, rf'\1{category_file}\2{category_name}\3', content, flags=re.DOTALL)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 index-v2.html 카테고리 링크 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   메인 화면 카테고리 카드를 category-*.html로 연결\n")
    
    print("📝 파일 수정 중...\n")
    
    if fix_index_v2_links("index-v2.html"):
        print("  ✅ index-v2.html - 카테고리 링크 수정 완료")
        print("\n✅ 수정 완료!")
    else:
        print("  ℹ️ index-v2.html - 변경사항 없음")
    
    print("=" * 60)


if __name__ == "__main__":
    main()

