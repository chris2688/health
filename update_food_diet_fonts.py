import os
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def update_food_diet_fonts():
    """질환별 식단 페이지의 폰트 굵기 차별화"""
    print("Updating: food-질환별식단.html")
    
    try:
        with open('food-질환별식단.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. CSS 추가 (이미 있을 수도 있지만 확인)
        if '.health-card h3 strong' not in content:
            css_addition = '''        
        .health-card h3 strong {
            font-weight: 800;
        }
        
        .health-card h3 .light {
            font-weight: 400;
            opacity: 0.95;
        }'''
            
            # .health-card h3 스타일 뒤에 추가
            content = re.sub(
                r'(\.health-card h3 \{[^}]+\})',
                r'\1' + css_addition,
                content
            )
        
        # 2. HTML 텍스트 수정: "질환명 식단" -> "<strong>질환명</strong> <span class="light">식단</span>"
        
        # 고혈압 식단
        content = content.replace(
            '<h3>고혈압 식단</h3>',
            '<h3><strong>고혈압</strong> <span class="light">식단</span></h3>'
        )
        
        # 당뇨 식단
        content = content.replace(
            '<h3>당뇨 식단</h3>',
            '<h3><strong>당뇨</strong> <span class="light">식단</span></h3>'
        )
        
        # 지방간 식단
        content = content.replace(
            '<h3>지방간 식단</h3>',
            '<h3><strong>지방간</strong> <span class="light">식단</span></h3>'
        )
        
        # 갱년기 식단
        content = content.replace(
            '<h3>갱년기 식단</h3>',
            '<h3><strong>갱년기</strong> <span class="light">식단</span></h3>'
        )
        
        # 우울증 식단
        content = content.replace(
            '<h3>우울증 식단</h3>',
            '<h3><strong>우울증</strong> <span class="light">식단</span></h3>'
        )
        
        # 협심증/심근경색 식단
        content = content.replace(
            '<h3>협심증/심근경색 식단</h3>',
            '<h3><strong>협심증/심근경색</strong> <span class="light">식단</span></h3>'
        )
        
        # 퇴행성 관절염/오십견 식단
        content = content.replace(
            '<h3>퇴행성 관절염/오십견 식단</h3>',
            '<h3><strong>퇴행성 관절염/오십견</strong> <span class="light">식단</span></h3>'
        )
        
        # 골다공증 식단
        content = content.replace(
            '<h3>골다공증 식단</h3>',
            '<h3><strong>골다공증</strong> <span class="light">식단</span></h3>'
        )
        
        # 역류성 식도염 식단
        content = content.replace(
            '<h3>역류성 식도염 식단</h3>',
            '<h3><strong>역류성 식도염</strong> <span class="light">식단</span></h3>'
        )
        
        # 고지혈증(콜레스테롤) 식단
        content = content.replace(
            '<h3>고지혈증(콜레스테롤) 식단</h3>',
            '<h3><strong>고지혈증(콜레스테롤)</strong> <span class="light">식단</span></h3>'
        )
        
        # 파일 저장
        with open('food-질환별식단.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 폰트 차별화 완료!")
        print(f"     - 질환명: 굵게 (font-weight: 800)")
        print(f"     - 식단: 얇게 (font-weight: 400)")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🍽️ 질환별 식단 폰트 굵기 차별화")
    print("=" * 60)
    
    update_food_diet_fonts()
    
    print("\n" + "=" * 60)
    print("✅ 완료!")
    print("=" * 60)

if __name__ == "__main__":
    main()

