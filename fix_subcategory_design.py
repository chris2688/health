import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 서브카테고리 파일 목록
SUBCATEGORY_FILES = [
    "food-피해야할과일.html",
    "food-질환별식단.html",
    "food-모르면독이된다.html",
    "exercise-질환별운동가이드.html",
    "exercise-운동팁.html",
    "lifestyle-생활습관.html",
    "lifestyle-생활습관바꾸기팁.html",
]


def fix_subcategory_design(filepath):
    """서브카테고리 파일의 디자인을 질환별 정보 페이지와 동일하게 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. health-card-container 스타일 수정
        # padding을 질환별 정보 페이지와 동일하게: padding: 20px 0 0 0;
        content = re.sub(
            r'\.health-card-container\s*\{[^}]*padding:[^}]*\}',
            '.health-card-container {\n            padding: 20px 0 0 0;\n            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);\n            min-height: calc(100vh - 80px);\n        }',
            content,
            flags=re.DOTALL
        )
        
        # 2. container-content 스타일 수정
        # padding을 질환별 정보 페이지와 동일하게: padding: 0 20px 60px;
        content = re.sub(
            r'\.container-content\s*\{[^}]*padding:[^}]*max-width:\s*1200px;[^}]*\}',
            '.container-content {\n            padding: 0 20px 60px;\n            max-width: 1200px;\n            margin: 0 auto;\n        }',
            content,
            flags=re.DOTALL
        )
        
        # 3. section-title의 margin-bottom 수정 (50px -> 30px)
        content = re.sub(
            r'\.section-title\s*\{[^}]*margin-bottom:\s*50px;',
            '.section-title {\n            text-align: center;\n            margin-bottom: 30px;',
            content
        )
        
        # 4. 뒤로가기 버튼 스타일 수정 (margin-top을 줄여서 떨어지지 않도록)
        content = re.sub(
            r'\.back-button\s*\{[^}]*margin:[^}]*\}',
            '.back-button {\n            display: inline-block;\n            margin: 0 0 20px 0;\n            margin-left: 0;\n            padding: 12px 24px;\n            background: rgba(102, 126, 234, 0.1);\n            color: #667eea;\n            text-decoration: none;\n            border-radius: 50px;\n            font-weight: 600;\n            font-size: 15px;\n            transition: all 0.3s;\n            box-shadow: 0 2px 10px rgba(0,0,0,0.05);\n        }',
            content,
            flags=re.DOTALL
        )
        
        # 5. health-cards-grid의 max-width와 padding 확인 및 수정
        # 이미 max-width: 1200px이 있지만, container-content 안에 있으므로 중복 제거
        content = re.sub(
            r'\.health-cards-grid\s*\{[^}]*max-width:\s*1200px;[^}]*padding:\s*0\s+20px;[^}]*\}',
            '.health-cards-grid {\n            display: grid;\n            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n            gap: 30px;\n            max-width: 1200px;\n            margin: 0 auto;\n            padding: 0 20px;\n        }',
            content,
            flags=re.DOTALL
        )
        
        # 6. 뒤로가기 버튼이 container-content 안에 제대로 들어가 있는지 확인
        # HTML 구조 확인: container-content 안에 뒤로가기 버튼이 있어야 함
        if '<div class="container-content">' in content:
            # 뒤로가기 버튼이 container-content 바로 다음에 오도록 확인
            if not re.search(r'<div class="container-content">\s*<a href="[^"]*" class="back-button">', content):
                # 뒤로가기 버튼을 container-content 안으로 이동
                content = re.sub(
                    r'(<div class="container-content">)\s*(<div class="section-title">)',
                    r'\1\n            <a href="[BACK_LINK]" class="back-button">뒤로가기</a>\n\n            \2',
                    content
                )
                # [BACK_LINK]를 적절한 링크로 교체
                if 'food-' in filepath:
                    content = content.replace('[BACK_LINK]', 'food-main.html')
                elif 'exercise-' in filepath:
                    content = content.replace('[BACK_LINK]', 'exercise-main.html')
                elif 'lifestyle-' in filepath:
                    content = content.replace('[BACK_LINK]', 'lifestyle-main.html')
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 디자인 수정 완료")
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
    print("🔧 서브카테고리 페이지 디자인 통일")
    print("=" * 60)
    print("\n💡 질환별 정보 페이지와 동일한 디자인으로")
    print("   모든 서브카테고리 페이지를 수정합니다.\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in SUBCATEGORY_FILES:
        if fix_subcategory_design(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    
    print("\n" + "=" * 60)
    print("✅ 수정 완료!")
    print("=" * 60)
    print("\n💡 수정된 내용:")
    print("   - health-card-container: padding: 20px 0 0 0")
    print("   - container-content: padding: 0 20px 60px, max-width: 1200px")
    print("   - section-title: margin-bottom: 30px")
    print("   - 뒤로가기 버튼: margin-top 제거 (떨어지지 않도록)")
    print("   - 전체 페이지 가로 폭: 질환별 정보 페이지와 동일")
    print("=" * 60)


if __name__ == "__main__":
    main()

