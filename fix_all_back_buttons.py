import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 통일된 뒤로가기 버튼 CSS
UNIFIED_BACK_BUTTON_CSS = '''        .back-button {
            display: inline-block;
            margin: 0 0 30px 0;
            margin-left: max(20px, calc((100% - 1200px) / 2 + 20px));
            padding: 12px 24px;
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.3s;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .back-button:hover {
            background: rgba(102, 126, 234, 0.2);
            transform: translateX(-5px);
        }
        
        .back-button::before {
            content: '← ';
            font-weight: bold;
        }'''

def update_back_button_style(filepath):
    """뒤로가기 버튼 스타일 업데이트"""
    print(f"Updating: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 기존 .back-button 스타일 제거
        content = re.sub(
            r'\/\* ========== 뒤로가기 버튼 ========== \*\/\s*\.back-button\s*\{[^}]+\}\s*\.back-button:hover\s*\{[^}]+\}\s*\.back-button::before\s*\{[^}]+\}',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 새로운 스타일 삽입
        if '/* ========== 콘텐츠 영역 ========== */' in content:
            content = content.replace(
                '/* ========== 콘텐츠 영역 ========== */',
                f'''/* ========== 뒤로가기 버튼 ========== */
{UNIFIED_BACK_BUTTON_CSS}
        
        /* ========== 콘텐츠 영역 ========== */'''
            )
        else:
            # .health-card-container 또는 .site-main 전에 삽입
            if '.health-card-container {' in content:
                content = re.sub(
                    r'(\.health-card-container\s*\{)',
                    f'''/* ========== 뒤로가기 버튼 ========== */
{UNIFIED_BACK_BUTTON_CSS}
        
        \\1''',
                    content,
                    count=1
                )
            elif '.site-main {' in content:
                content = re.sub(
                    r'(\.site-main\s*\{)',
                    f'''/* ========== 뒤로가기 버튼 ========== */
{UNIFIED_BACK_BUTTON_CSS}
        
        \\1''',
                    content,
                    count=1
                )
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 업데이트 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("📐 모든 페이지 뒤로가기 버튼 위치 통일")
    print("=" * 60)
    
    # 모든 HTML 파일 (category, sub, food)
    all_files = glob.glob("category-*.html") + glob.glob("sub-*.html") + glob.glob("food-*.html")
    print(f"\n📁 총 {len(all_files)}개 파일")
    
    success_count = 0
    for file in all_files:
        if update_back_button_style(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(all_files)}개 파일")
    print("=" * 60)
    print("\n🎯 적용된 스타일:")
    print("  - 좌측 여백: calc((100% - 1200px) / 2 + 20px)")
    print("  - 최소 여백: 20px")
    print("  - 결과: 모든 페이지에서 동일한 좌측 위치")

if __name__ == "__main__":
    main()

