import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 실제 존재하는 sub- 파일 목록 가져오기
def get_sub_files():
    """실제 존재하는 sub- 파일 목록"""
    sub_files = set()
    for file in os.listdir('.'):
        if file.startswith('sub-') and file.endswith('.html'):
            sub_files.add(file)
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


def verify_and_fix_sub_links(filepath):
    """서브 카테고리 링크 확인 및 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        sub_files = get_sub_files()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 모든 sub- 링크 찾기
        pattern = r'href="(sub-[^"]+\.html)"'
        matches = re.findall(pattern, content)
        
        fixed_links = []
        for link in matches:
            if link not in sub_files:
                # 파일이 없으면 가장 유사한 파일 찾기
                # 공백 제거
                clean_link = link.replace(' ', '')
                if clean_link in sub_files:
                    content = content.replace(f'href="{link}"', f'href="{clean_link}"')
                    fixed_links.append(f"{link} -> {clean_link}")
                else:
                    # 부분 매칭
                    found = False
                    for sub_file in sub_files:
                        # 파일명에서 공백과 특수문자 제거 후 비교
                        link_clean = re.sub(r'[()/- ]', '', link.replace('sub-', '').replace('.html', ''))
                        sub_clean = re.sub(r'[()/- ]', '', sub_file.replace('sub-', '').replace('.html', ''))
                        if link_clean == sub_clean or link_clean in sub_clean or sub_clean in link_clean:
                            content = content.replace(f'href="{link}"', f'href="{sub_file}"')
                            fixed_links.append(f"{link} -> {sub_file}")
                            found = True
                            break
                    if not found:
                        print(f"    ⚠️ {filepath}: {link} 파일을 찾을 수 없음")
        
        if fixed_links:
            print(f"  ✅ {filepath} - 링크 수정:")
            for fix in fixed_links:
                print(f"      {fix}")
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 모든 서브 카테고리 링크 확인 및 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   실제 파일명과 일치하도록 링크 수정\n")
    
    print("📝 파일 확인 중...\n")
    fixed_count = 0
    
    for file in CATEGORY_FILES:
        if verify_and_fix_sub_links(file):
            fixed_count += 1
    
    print(f"\n✅ 총 {fixed_count}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

