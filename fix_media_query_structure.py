import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
ALL_FILES = [
    "index-v2.html",
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
    "food-main.html",
    "exercise-main.html",
    "lifestyle-main.html",
    "news-main.html",
    "food-피해야할과일.html",
    "food-질환별식단.html",
    "food-모르면독이된다.html",
    "exercise-질환별운동가이드.html",
    "exercise-운동팁.html",
    "lifestyle-생활습관.html",
    "lifestyle-생활습관바꾸기팁.html",
]


def fix_file(filepath):
    """미디어 쿼리 구조 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 미디어 쿼리 구조 수정
        # 패턴: @media (max-width: 768px) { ... } 다음에 또 스타일이 있는 경우
        # .main-nav.active .mobile-close-btn { ... } 다음에 미디어 쿼리가 닫히고, 그 다음에 또 스타일이 있는 경우
        
        # 미디어 쿼리 안에 .hero-heading과 .cards-grid가 들어가도록 수정
        pattern = r'(@media\s*\(max-width:\s*768px\)[^}]*?\.main-nav\.active\s*\.mobile-close-btn[^}]*?display:\s*block;[^}]*?\})\s*\}\s*(\.hero-heading[^}]*?font-size:\s*32px;[^}]*?\}\s*\.cards-grid[^}]*?grid-template-columns:\s*1fr;[^}]*?gap:\s*20px;[^}]*?\})\s*\}'
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(
                pattern,
                r'''@media (max-width: 768px) {
            .header-content {
                min-height: 70px;
            }
            
            .logo-image {
                height: 40px;
            }
            
            .main-nav {
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                flex-direction: column;
                padding: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                z-index: 1000;
            }
            
            .main-nav.active {
                display: flex;
            }
            
            .nav-item {
                padding: 15px 20px;
                text-align: center;
            }
            
            .mobile-menu-btn {
                display: block;
            }
            
            .main-nav.active .mobile-close-btn {
                display: block;
            }
            
            .hero-heading {
                font-size: 32px;
            }
            
            .cards-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
        }''',
                content,
                flags=re.DOTALL
            )
        
        # 2. 기본 스타일 확인 (PC에서 정상 작동)
        # .main-nav가 display: flex인지 확인
        if '.main-nav {' in content:
            nav_style = re.search(r'\.main-nav\s*\{[^}]*?\}', content, re.DOTALL)
            if nav_style and 'display: flex' not in nav_style.group(0):
                # display: flex 추가
                content = re.sub(
                    r'(\.main-nav\s*\{)',
                    r'\1\n            display: flex;\n            gap: 0;',
                    content
                )
        
        # 3. 헤더 링크 확인
        # 링크가 상대 경로인지 확인
        if 'href="index-v2.html"' in content and 'href="food-main.html"' in content:
            # 링크는 이미 상대 경로로 되어 있음
            pass
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 수정 완료")
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
    print("🔧 미디어 쿼리 구조 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 미디어 쿼리 구조 정리")
    print("   2. PC에서 정상 작동 확인")
    print("   3. 헤더 링크 확인\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

