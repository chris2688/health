import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔧 news-main.html 수정")
print("=" * 70)

# food-main.html을 템플릿으로 사용
try:
    with open('food-main.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 불필요한 빈 줄 제거
    content = re.sub(r'\n\n+', '\n', content)
    
    # 타이틀 및 아이콘 변경
    content = content.replace('<title>식단/음식 - 9988 건강정보</title>', '<title>건강News - 9988 건강정보</title>')
    content = content.replace('식단/음식', '건강News')
    content = content.replace('🍽️', '📰')
    content = content.replace('건강한 식단 가이드', '최신 건강 뉴스')
    content = content.replace('관심있는 주제를 선택하세요', '최신 건강 정보를 확인하세요')
    
    # 카테고리 카드를 뉴스 관련으로 변경
    news_cards = '''            <div class="health-cards-grid">
                <!-- 뉴스는 동적으로 WordPress에서 로드됨 -->
                <div class="news-placeholder">
                    <p style="text-align: center; padding: 60px 20px; color: #999; font-size: 18px;">
                        📰 최신 건강 뉴스를 불러오는 중...
                    </p>
                </div>
            </div>'''
    
    # health-cards-grid 부분을 뉴스 플레이스홀더로 교체
    content = re.sub(
        r'<div class="health-cards-grid">.*?</div>\s*</div>',
        news_cards + '\n        </div>',
        content,
        flags=re.DOTALL
    )
    
    # WordPress 카테고리를 news로 변경
    content = re.sub(
        r"const categorySlug = '.*?';",
        "const categorySlug = 'news';  // 뉴스 카테고리",
        content
    )
    
    # news-main.html로 저장
    with open('news-main.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ news-main.html 재생성 완료!")
    print("\n변경사항:")
    print("  - 불필요한 빈 줄 제거")
    print("  - 타이틀 및 아이콘 변경")
    print("  - 뉴스 플레이스홀더 추가")
    print("  - WordPress news 카테고리 연동")
    
    # 파일 크기 확인
    import os
    size = os.path.getsize('news-main.html') / 1024
    print(f"\n파일 크기: {size:.1f} KB")
    
    print("\n" + "=" * 70)
    print("🎉 완료!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ 오류: {e}")
    import traceback
    traceback.print_exc()

