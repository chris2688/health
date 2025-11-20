import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔧 모든 페이지의 뒤로가기 버튼 스타일 통일")
print("=" * 70)

# 표준 뒤로가기 버튼 스타일 (sub-hypertension.html 기준)
STANDARD_BACK_BUTTON_CSS = """.back-button {
            display: inline-block;
            margin: 30px 0 30px 0;
            padding: 12px 24px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }
        
        .back-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        
        .back-button::before {
            content: '← ';
            font-weight: bold;
        }"""

# 수정할 파일 목록
files_to_fix = []

# 모든 HTML 파일 찾기
for filename in os.listdir('.'):
    if filename.endswith('.html') and not filename.startswith('backup'):
        # category-, sub-, food-, exercise-, lifestyle-, news- 파일들만
        if any(filename.startswith(prefix) for prefix in ['category-', 'sub-', 'food-', 'exercise-', 'lifestyle-', 'news-']):
            files_to_fix.append(filename)

print(f"\n📝 {len(files_to_fix)}개 파일 검사 중...\n")

fixed_count = 0
skipped_count = 0

for filename in files_to_fix:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 기존 .back-button 스타일을 찾아서 교체
        # 여러 패턴을 시도
        patterns = [
            # 패턴 1: .back-button { ... } (단일 블록)
            r'\.back-button\s*\{[^}]*?\}',
            # 패턴 2: .back-button:hover { ... } 포함
            r'\.back-button\s*\{[^}]*?\}\s*\.back-button:hover\s*\{[^}]*?\}',
            # 패턴 3: .back-button::before 포함
            r'\.back-button\s*\{[^}]*?\}\s*\.back-button:hover\s*\{[^}]*?\}\s*\.back-button::before\s*\{[^}]*?\}',
        ]
        
        replaced = False
        for pattern in patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, STANDARD_BACK_BUTTON_CSS, content, count=1, flags=re.DOTALL)
                replaced = True
                break
        
        # 변경사항이 있으면 저장
        if replaced and content != original_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename}")
            fixed_count += 1
        else:
            # 이미 표준 스타일이거나 뒤로가기 버튼이 없는 경우
            if '.back-button' not in content:
                pass  # 뒤로가기 버튼 없음 (정상)
            else:
                print(f"ℹ️  {filename} - 이미 표준 스타일")
                skipped_count += 1
    
    except Exception as e:
        print(f"❌ {filename} - 오류: {e}")

print(f"\n✅ {fixed_count}개 파일 수정 완료!")
print(f"ℹ️  {skipped_count}개 파일은 이미 표준 스타일")

print("\n" + "=" * 70)
print("🎉 뒤로가기 버튼 스타일 통일 완료!")
print("=" * 70)
print("\n표준 스타일:")
print("  - 흰색 배경, 보라색 텍스트")
print("  - 둥근 모서리 (50px)")
print("  - 그림자 효과")
print("  - 호버 시 위로 이동")
print("  - '← ' 화살표 자동 추가")
print("=" * 70)

