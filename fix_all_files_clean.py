import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
ALL_FILES = [
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
    """파일 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 깨진 mobile-close-btn 수정
        content = re.sub(
            r'\.mobile-close-btn\s*\{[^}]*?ppx;[^}]*?\}',
            '''        .mobile-close-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 8px 12px;
            position: absolute;
            top: 15px;
            right: 15px;
            z-index: 1001;
            line-height: 1;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            transition: all 0.3s;
        }''',
            content,
            flags=re.DOTALL
        )
        
        # 2. 중복된 모바일 미디어 쿼리 제거 및 애니메이션 제거
        # 패턴: 두 번째 @media (max-width: 768px) 블록 제거
        pattern = r'(@media\s*\(max-width:\s*768px\)[^}]*?\.header-content[^}]*?\}[^}]*?\.logo-image[^}]*?\}[^}]*?\.main-nav[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\}[^}]*?\.nav-item[^}]*?\}[^}]*?\.mobile-menu-btn[^}]*?\}[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\})\s*@media\s*\(max-width:\s*768px\)\s*\{[^}]*?\.header-content[^}]*?\}[^}]*?\.logo-image[^}]*?\}[^}]*?\.main-nav[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\}[^}]*?\.nav-item[^}]*?\}[^}]*?\.mobile-menu-btn[^}]*?\}[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\}'
        
        content = re.sub(
            pattern,
            r'''        @media (max-width: 768px) {
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
        }''',
            content,
            flags=re.DOTALL
        )
        
        # 3. 애니메이션 속성 제거
        content = re.sub(
            r'opacity:\s*0;[^}]*?transform:\s*translateY\([^)]*\);[^}]*?transition:[^}]*?max-height:\s*0;[^}]*?overflow:\s*hidden;',
            '',
            content
        )
        content = re.sub(
            r'opacity:\s*1;[^}]*?transform:\s*translateY\([^)]*\);[^}]*?max-height:\s*\d+px;',
            '',
            content
        )
        content = re.sub(
            r'opacity:\s*0;[^}]*?transform:\s*translateY\([^)]*\);[^}]*?transition:[^}]*?',
            '',
            content
        )
        content = re.sub(
            r'opacity:\s*1;[^}]*?transform:\s*translateY\([^)]*\);',
            '',
            content
        )
        content = re.sub(
            r'opacity:\s*1;[^}]*?transform:\s*scale\([^)]*\);',
            '',
            content
        )
        
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
    print("🔧 모든 파일 정리")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 깨진 CSS 수정")
    print("   2. 중복 미디어 쿼리 제거")
    print("   3. 애니메이션 제거\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

