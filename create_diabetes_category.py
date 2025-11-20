import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# category-심혈관질환.html을 템플릿으로 사용하여 category-당뇨병.html 생성
print("=" * 60)
print("🏥 당뇨병 카테고리 페이지 생성")
print("=" * 60)

# 심혈관질환 템플릿 읽기
with open('category-심혈관질환.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 당뇨병용으로 수정
diabetes_content = template

# 제목 변경
diabetes_content = diabetes_content.replace('<title>심혈관 질환 - 9988 건강정보</title>', 
                                           '<title>당뇨병 - 9988 건강정보</title>')

# 섹션 타이틀 변경
diabetes_content = diabetes_content.replace('<div class="main-icon">❤️</div>',
                                           '<div class="main-icon">💉</div>')
diabetes_content = diabetes_content.replace('<h2>심혈관 질환</h2>',
                                           '<h2>당뇨병</h2>')

# 서브 카테고리 카드 변경 (3개)
old_cards = '''<a href="sub-고혈압.html" class="health-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;">
                    <div class="health-card-icon">🩺</div>
                    <h3>고혈압</h3>
                </a>
                
                <a href="sub-고지혈증.html" class="health-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
                    <div class="health-card-icon">💊</div>
                    <h3>고지혈증(콜레스테롤)</h3>
                </a>
                
                <a href="sub-협심증심근경색.html" class="health-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">
                    <div class="health-card-icon">💔</div>
                    <h3>협심증/심근경색</h3>
                </a>
                
                <a href="sub-동맥경화.html" class="health-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
                    <div class="health-card-icon">🫀</div>
                    <h3>동맥경화</h3>
                </a>
                
                <a href="sub-뇌졸중.html" class="health-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
                    <div class="health-card-icon">🧠</div>
                    <h3>뇌졸중</h3>
                </a>'''

new_cards = '''<a href="sub-당뇨.html" class="health-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
                    <div class="health-card-icon">💉</div>
                    <h3>당뇨</h3>
                </a>
                
                <a href="sub-공복혈당장애.html" class="health-card" style="--card-color-1:#FFB84D; --card-color-2:#F77737;">
                    <div class="health-card-icon">🩸</div>
                    <h3>공복혈당장애</h3>
                </a>
                
                <a href="sub-당뇨병합병증.html" class="health-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
                    <div class="health-card-icon">⚕️</div>
                    <h3>당뇨병 합병증<br>(방광, 신장 등)</h3>
                </a>'''

diabetes_content = diabetes_content.replace(old_cards, new_cards)

# 파일 저장
with open('category-당뇨병.html', 'w', encoding='utf-8') as f:
    f.write(diabetes_content)

print("\n✅ category-당뇨병.html 생성 완료!")
print("\n📋 포함된 서브 카테고리:")
print("   1. 💉 당뇨")
print("   2. 🩸 공복혈당장애")
print("   3. ⚕️ 당뇨병 합병증 (방광, 신장 등)")
print("=" * 60)

