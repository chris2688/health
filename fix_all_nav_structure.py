import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
ALL_FILES = [
    "food-main.html",
    "exercise-main.html",
    "lifestyle-main.html",
    "news-main.html",
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
    "food-피해야할과일.html",
    "food-질환별식단.html",
    "food-모르면독이된다.html",
    "exercise-질환별운동가이드.html",
    "exercise-운동팁.html",
    "lifestyle-생활습관.html",
    "lifestyle-생활습관바꾸기팁.html",
]


def fix_nav_structure(filepath):
    """nav 구조 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # nav 안에 mobile-menu-btn이 있으면 밖으로 이동
        # 패턴: <nav>...<button class="mobile-menu-btn">...</button>...</nav>
        # 또는: <nav>...</nav> 없이 <button class="mobile-menu-btn">가 nav 안에 있는 경우
        
        if '<nav class="main-nav" id="mainNav">' in content:
            nav_start = content.find('<nav class="main-nav" id="mainNav">')
            nav_end = content.find('</nav>', nav_start)
            
            if nav_start != -1:
                if nav_end == -1:
                    # </nav> 태그가 없으면 추가
                    # news-main.html 같은 경우를 찾아서 </nav> 추가
                    after_nav = content[nav_start:]
                    # mobile-menu-btn이나 </div>를 찾아서 그 앞에 </nav> 추가
                    btn_pos = after_nav.find('<button class="mobile-menu-btn"')
                    div_pos = after_nav.find('</div>')
                    
                    if btn_pos != -1 and (div_pos == -1 or btn_pos < div_pos):
                        # mobile-menu-btn 앞에 </nav> 추가
                        insert_pos = nav_start + btn_pos
                        content = content[:insert_pos] + '            </nav>\n            ' + content[insert_pos:]
                        nav_end = insert_pos + len('            </nav>\n            ')
                    elif div_pos != -1:
                        # </div> 앞에 </nav> 추가
                        insert_pos = nav_start + div_pos
                        content = content[:insert_pos] + '            </nav>\n            ' + content[insert_pos:]
                        nav_end = insert_pos + len('            </nav>\n            ')
                
                if nav_end != -1:
                    nav_content = content[nav_start:nav_end]
                    
                    # nav 안에 mobile-menu-btn이 있으면
                    if '<button class="mobile-menu-btn"' in nav_content:
                        # nav 안의 mobile-menu-btn 제거
                        nav_content_clean = re.sub(
                            r'\s*<button class="mobile-menu-btn"[^>]*>☰</button>\s*',
                            '',
                            nav_content
                        )
                        
                        # nav 내용 교체
                        content = content[:nav_start] + nav_content_clean + content[nav_end:]
                        
                        # nav_end 위치 재계산
                        nav_end = content.find('</nav>', nav_start)
                        
                        # </nav> 다음에 mobile-menu-btn 추가 (없으면)
                        if nav_end != -1:
                            after_nav = content[nav_end + 6:nav_end + 200]
                            if '<button class="mobile-menu-btn"' not in after_nav:
                                # mobile-menu-btn 찾기
                                btn_match = re.search(r'<button class="mobile-menu-btn"[^>]*>☰</button>', content[nav_end:])
                                if not btn_match:
                                    # 없으면 추가
                                    mobile_btn = '\n            <button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>'
                                    content = content[:nav_end + 6] + mobile_btn + content[nav_end + 6:]
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - nav 구조 수정 완료")
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
    print("🔧 모든 파일 nav 구조 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. nav 안의 mobile-menu-btn을 밖으로 이동")
    print("   2. </nav> 태그 추가 (없는 경우)\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_nav_structure(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

