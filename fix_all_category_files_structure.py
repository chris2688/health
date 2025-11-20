import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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


def fix_category_file_structure(filepath):
    """카테고리 파일의 구조 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. health-cards-grid가 제대로 닫혀있는지 확인
        # 마지막 health-card 다음에 </div>가 있는지 확인
        # 패턴: </a> 다음에 빈 줄들이 있고, 그 다음에 </div>가 없으면 추가
        
        # health-cards-grid 닫기 확인
        if '<div class="health-cards-grid">' in content:
            # 마지막 health-card를 찾고, 그 다음에 </div>가 있는지 확인
            pattern = r'(</a>\s*\n\s*\n\s*)(</div>|</style>|<style>)'
            match = re.search(pattern, content)
            if match and match.group(2) != '</div>':
                # </div> 추가
                content = re.sub(
                    r'(</a>\s*\n\s*\n\s*)(</style>|<style>)',
                    r'\1</div>\n\n        </div>\n\n    </div>\n\n    \2',
                    content,
                    count=1
                )
        
        # 2. </style> 태그 확인 (style 태그 안에 HTML이 있으면 수정)
        # 패턴: } 다음에 <h3> 또는 <div>가 있으면 </style> 추가
        pattern = r'(\}\s*\n\s*)(<h3>|<div class="posts-section">)'
        if re.search(pattern, content):
            content = re.sub(
                r'(\}\s*\n\s*)(<h3>|<div class="posts-section">)',
                r'\1</style>\n\n    \2',
                content,
                count=1
            )
        
        # 3. posts-section div가 없으면 추가
        if '<h3>📝 관련 글</h3>' in content and '<div class="posts-section">' not in content:
            content = re.sub(
                r'(</style>\s*\n\s*)(<h3>📝 관련 글</h3>)',
                r'\1<div class="posts-section">\n\n        \2',
                content
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
    print("🔧 모든 카테고리 파일 구조 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. health-cards-grid 닫는 태그 확인")
    print("   2. </style> 태그 확인")
    print("   3. posts-section div 확인\n")
    
    print("📝 파일 수정 중...\n")
    fixed_count = 0
    
    for file in CATEGORY_FILES:
        if fix_category_file_structure(file):
            print(f"  ✅ {file} - 구조 수정 완료")
            fixed_count += 1
        else:
            print(f"  ℹ️ {file} - 변경사항 없음")
    
    print(f"\n✅ 총 {fixed_count}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

