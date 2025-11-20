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


def fix_back_button_margin(filepath):
    """뒤로가기 버튼의 margin 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 뒤로가기 버튼의 margin-top을 제거 (떨어지지 않도록)
        content = re.sub(
            r'\.back-button\s*\{[^}]*margin:[^}]*margin-left:[^}]*\}',
            '.back-button {\n            display: inline-block;\n            margin: 0 0 20px 0;\n            padding: 12px 24px;\n            background: rgba(102, 126, 234, 0.1);\n            color: #667eea;\n            text-decoration: none;\n            border-radius: 50px;\n            font-weight: 600;\n            font-size: 15px;\n            transition: all 0.3s;\n            box-shadow: 0 2px 10px rgba(0,0,0,0.05);\n        }',
            content,
            flags=re.DOTALL
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 뒤로가기 버튼 margin 수정 완료")
            return True
        else:
            print(f"  ℹ️ {filepath} - 변경사항 없음")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 뒤로가기 버튼 margin 수정")
    print("=" * 60)
    print("\n💡 뒤로가기 버튼이 떨어지지 않도록 margin-top 제거\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in SUBCATEGORY_FILES:
        if fix_back_button_margin(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()
