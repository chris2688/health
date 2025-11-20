import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 실제 존재하는 sub- 파일 목록 (공백 제거)
SUB_FILES = {
    'sub-역류성식도염.html': 'sub-역류성식도염.html',
    'sub-과민성대장증후군.html': 'sub-과민성대장증후군.html',
    'sub-역류성 식도염.html': 'sub-역류성식도염.html',
    'sub-과민성 대장증후군.html': 'sub-과민성대장증후군.html',
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


def fix_sub_links_spaces(filepath):
    """서브 카테고리 링크의 공백 제거 및 파일명 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 공백이 있는 sub- 파일명 수정
        content = re.sub(
            r'href="sub-역류성 식도염\.html"',
            'href="sub-역류성식도염.html"',
            content
        )
        content = re.sub(
            r'href="sub-과민성 대장증후군\.html"',
            'href="sub-과민성대장증후군.html"',
            content
        )
        
        # 모든 sub- 링크에서 공백 제거 (일반적인 경우)
        # 패턴: href="sub-파일명.html"에서 파일명의 공백 제거
        def remove_spaces_in_sub(match):
            full_href = match.group(0)
            # 공백 제거
            new_href = full_href.replace(' ', '')
            return new_href
        
        content = re.sub(
            r'href="sub-[^"]*\.html"',
            remove_spaces_in_sub,
            content
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 서브 링크 공백 제거 완료")
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
    print("🔧 서브 카테고리 링크 공백 제거")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   sub-*.html 링크에서 공백 제거\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in CATEGORY_FILES:
        if fix_sub_links_spaces(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

