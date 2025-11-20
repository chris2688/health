import os
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def update_exercise_guide_fonts():
    """운동가이드 페이지의 폰트 굵기 차별화"""
    print("Updating: exercise-질환별운동가이드.html")
    
    try:
        with open('exercise-질환별운동가이드.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. CSS 추가: .light 클래스
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
        
        # 2. HTML 텍스트 수정: "질환명 운동가이드" -> "<strong>질환명</strong> <span class="light">운동가이드</span>"
        
        # 고혈압 운동가이드
        content = content.replace(
            '<h3>고혈압 운동가이드</h3>',
            '<h3><strong>고혈압</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 당뇨병 운동가이드
        content = content.replace(
            '<h3>당뇨병 운동가이드</h3>',
            '<h3><strong>당뇨병</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 콜레스테롤(고지혈증) 운동가이드
        content = content.replace(
            '<h3>콜레스테롤(고지혈증) 운동가이드</h3>',
            '<h3><strong>콜레스테롤(고지혈증)</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 협심증/심근경색 운동가이드
        content = content.replace(
            '<h3>협심증/심근경색 운동가이드</h3>',
            '<h3><strong>협심증/심근경색</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 퇴행성 관절염 운동가이드
        content = content.replace(
            '<h3>퇴행성 관절염 운동가이드</h3>',
            '<h3><strong>퇴행성 관절염</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 오십견 운동가이드
        content = content.replace(
            '<h3>오십견 운동가이드</h3>',
            '<h3><strong>오십견</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 골다공증 운동가이드
        content = content.replace(
            '<h3>골다공증 운동가이드</h3>',
            '<h3><strong>골다공증</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 지방간 운동가이드
        content = content.replace(
            '<h3>지방간 운동가이드</h3>',
            '<h3><strong>지방간</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 갱년기 운동가이드
        content = content.replace(
            '<h3>갱년기 운동가이드</h3>',
            '<h3><strong>갱년기</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 우울증 운동가이드
        content = content.replace(
            '<h3>우울증 운동가이드</h3>',
            '<h3><strong>우울증</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 수면장애 운동가이드
        content = content.replace(
            '<h3>수면장애 운동가이드</h3>',
            '<h3><strong>수면장애</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 허리 디스크 운동가이드
        content = content.replace(
            '<h3>허리 디스크 운동가이드</h3>',
            '<h3><strong>허리 디스크</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 목 디스크 운동가이드
        content = content.replace(
            '<h3>목 디스크 운동가이드</h3>',
            '<h3><strong>목 디스크</strong> <span class="light">운동가이드</span></h3>'
        )
        
        # 파일 저장
        with open('exercise-질환별운동가이드.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 폰트 차별화 완료!")
        print(f"     - 질환명: 굵게 (font-weight: 800)")
        print(f"     - 운동가이드: 얇게 (font-weight: 400)")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🎨 운동가이드 폰트 굵기 차별화")
    print("=" * 60)
    
    update_exercise_guide_fonts()
    
    print("\n" + "=" * 60)
    print("✅ 완료!")
    print("=" * 60)

if __name__ == "__main__":
    main()

