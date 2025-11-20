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

def unify_back_button_style(filepath):
    """모든 파일의 뒤로가기 버튼 스타일 통일"""
    print(f"Unifying: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 기존 .back-button 스타일 모두 제거 (중복 포함)
        # 패턴 1: .back-button { ... } 부터 다음 } 까지
        content = re.sub(
            r'\.back-button\s*\{[^}]+\}\s*\.back-button:hover\s*\{[^}]+\}\s*\.back-button::before\s*\{[^}]+\}',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 패턴 2: 남아있는 개별 .back-button 관련 스타일 제거
        content = re.sub(
            r'\.back-button(?::hover|::before)?\s*\{[^}]+\}',
            '',
            content
        )
        
        # 미디어 쿼리 안의 .back-button 스타일도 제거
        content = re.sub(
            r'@media[^{]*\{[^}]*\.back-button\s*\{[^}]+\}[^}]*\}',
            lambda m: re.sub(r'\.back-button\s*\{[^}]+\}', '', m.group(0)),
            content,
            flags=re.DOTALL
        )
        
        # 콘텐츠 영역 스타일 전에 통일된 버튼 CSS 삽입
        # "/* ========== 콘텐츠 영역 ========== */" 또는 ".health-card-container" 또는 ".site-main" 전에 삽입
        
        if '/* ========== 콘텐츠 영역 ========== */' in content:
            content = content.replace(
                '/* ========== 콘텐츠 영역 ========== */',
                f'''/* ========== 뒤로가기 버튼 ========== */
{UNIFIED_BACK_BUTTON_CSS}
        
        /* ========== 콘텐츠 영역 ========== */'''
            )
        elif '.health-card-container {' in content:
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
        
        print(f"  ✅ 스타일 통일 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🎨 뒤로가기 버튼 스타일 완전 통일")
    print("=" * 60)
    
    all_files = glob.glob("category-*.html") + glob.glob("sub-*.html")
    print(f"\n📁 총 {len(all_files)}개 파일")
    
    success_count = 0
    for file in all_files:
        if unify_back_button_style(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(all_files)}개 파일")
    print("=" * 60)
    print("\n🎯 통일된 스타일:")
    print("  - 배경: 보라색 반투명 (rgba(102, 126, 234, 0.1))")
    print("  - 텍스트: 보라색 (#667eea)")
    print("  - 위치: 동일 (margin: 0 0 30px 0)")
    print("  - 호버: 배경 진하게 + 좌측 이동")

if __name__ == "__main__":
    main()

