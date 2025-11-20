import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 메인 카테고리 -> 첫 번째 서브 카테고리 매핑
CATEGORY_TO_FIRST_SUB = {
    '심혈관 질환': 'sub-고혈압.html',
    '당뇨병': 'sub-당뇨.html',
    '관절/근골격계': 'sub-관절염.html',
    '호르몬/내분비': 'sub-갑상선.html',
    '정신건강/신경계': 'sub-우울증번아웃.html',
    '소화기 질환': 'sub-위염위궤양.html',
    '안과/치과/기타': 'sub-백내장녹내장.html',
}


def fix_index_v2_links(filepath):
    """index-v2.html의 카테고리 링크를 첫 번째 서브 카테고리로 변경"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 각 카테고리 카드의 링크 수정
        for category_name, sub_file in CATEGORY_TO_FIRST_SUB.items():
            # 패턴: <a href="..." ...> ... <h2 class="card-title">카테고리명</h2> ... </a>
            pattern = rf'(<a href="[^"]*"[^>]*>.*?<h2 class="card-title">){re.escape(category_name)}(</h2>.*?</a>)'
            
            def replace_link(match):
                before = match.group(1)
                after = match.group(2)
                return f'{before}{category_name}{after}'.replace(
                    re.search(r'href="[^"]*"', match.group(0)).group(0),
                    f'href="{sub_file}"'
                )
            
            # 더 정확한 패턴: href와 card-title 사이의 내용 찾기
            pattern2 = rf'(<a href=")([^"]*)("[^>]*>.*?<h2 class="card-title">){re.escape(category_name)}(</h2>)'
            content = re.sub(
                pattern2,
                rf'\1{sub_file}\3{category_name}\4',
                content,
                flags=re.DOTALL
            )
        
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
    print("🔧 index-v2.html 메인 카테고리를 서브 카테고리로 연결")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   각 메인 카테고리 카드를 첫 번째 서브 카테고리로 연결\n")
    
    for category, sub in CATEGORY_TO_FIRST_SUB.items():
        print(f"   {category} → {sub}")
    
    print("\n📝 파일 수정 중...\n")
    
    if fix_index_v2_links("index-v2.html"):
        print("  ✅ index-v2.html - 링크 수정 완료")
        print("\n✅ 수정 완료!")
    else:
        print("  ⚠️ 변경사항이 없거나 오류가 발생했습니다.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
