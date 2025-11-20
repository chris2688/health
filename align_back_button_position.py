import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_category_back_button(filepath):
    """카테고리 페이지의 뒤로가기 버튼 위치를 서브 페이지와 동일하게"""
    print(f"Fixing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # .health-card-container 스타일 수정
        old_container = r'\.health-card-container \{[^}]+\}'
        new_container = '''.health-card-container {
            padding: 0;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: calc(100vh - 80px);
        }
        
        .container-inner {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px 60px;
        }'''
        
        content = re.sub(old_container, new_container, content)
        
        # HTML 구조 수정: 뒤로가기와 콘텐츠를 container-inner로 감싸기
        # 현재: <div class="health-card-container"><a href="..." class="back-button">...</a><div class="section-title">...
        # 원하는: <div class="health-card-container"><div class="container-inner"><a href="..." class="back-button">...</a><div class="section-title">...
        
        pattern = r'(<div class="health-card-container">)\s*(<a href="[^"]*" class="back-button">뒤로가기</a>)\s*(<div class="section-title">)'
        replacement = r'\1\n        <div class="container-inner">\n            \2\n\n            \3'
        
        content = re.sub(pattern, replacement, content)
        
        # 닫는 태그 수정: </div></div> 전에 </div> 추가
        # health-cards-grid의 닫는 태그 후 container-inner 닫기
        pattern2 = r'(</div>\s*</div>\s*</div>\s*<script>)'
        replacement2 = r'</div>\n        </div>\n    </div>\n\n    <script>'
        
        content = re.sub(pattern2, replacement2, content)
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 위치 조정 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def fix_sub_back_button(filepath):
    """서브 페이지의 뒤로가기 버튼은 이미 올바른 위치"""
    print(f"Checking: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # .site-main이 이미 max-width: 1200px이므로 일관성 확인만
        if 'max-width: 1200px' in content and '.site-main' in content:
            print(f"  ✅ 이미 올바른 구조!")
            return True
        
        # 만약 없다면 추가
        old_style = r'\.site-main \{[^}]+\}'
        new_style = '''.site-main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }'''
        
        content = re.sub(old_style, new_style, content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 위치 확인 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return False

def main():
    print("=" * 60)
    print("📐 뒤로가기 버튼 위치 완전 통일")
    print("=" * 60)
    
    # 카테고리 파일
    category_files = glob.glob("category-*.html")
    print(f"\n📁 카테고리 페이지: {len(category_files)}개")
    
    success_count = 0
    for file in category_files:
        if fix_category_back_button(file):
            success_count += 1
    
    # 서브 파일
    sub_files = glob.glob("sub-*.html")
    print(f"\n📁 서브 페이지: {len(sub_files)}개")
    
    for file in sub_files:
        if fix_sub_back_button(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(category_files) + len(sub_files)}개 파일")
    print("=" * 60)
    print("\n🎯 통일된 구조:")
    print("  - 최대 너비: 1200px (중앙 정렬)")
    print("  - 좌우 패딩: 20px")
    print("  - 뒤로가기 위치: 모든 페이지 동일")

if __name__ == "__main__":
    main()

