import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def move_back_button_inside(filepath):
    """뒤로가기 버튼을 health-card-container 안으로 이동"""
    print(f"Fixing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 패턴: </header> 다음에 <a href="..." class="back-button"> 다음에 <div class="health-card-container">
        # 원하는: </header> 다음에 <div class="health-card-container"> 안에 <a href="..." class="back-button">
        
        pattern = r'(</header>)\s*<a href="([^"]+)" class="back-button">뒤로가기</a>\s*(<div class="health-card-container">)'
        replacement = r'\1\n\n    \3\n        <a href="\2" class="back-button">뒤로가기</a>\n'
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ 뒤로가기 버튼을 컨테이너 안으로 이동!")
            return True
        else:
            print(f"  ℹ️ 이미 올바른 위치이거나 뒤로가기 없음")
            return False
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🎨 뒤로가기 버튼을 배경 안으로 이동")
    print("=" * 60)
    
    # category와 food 파일만 (뒤로가기가 있는 페이지)
    all_files = glob.glob("category-*.html") + glob.glob("food-*.html")
    # food-main.html 제외 (메인 페이지는 뒤로가기 없음)
    all_files = [f for f in all_files if f != "food-main.html"]
    
    print(f"\n📁 총 {len(all_files)}개 파일")
    
    success_count = 0
    for file in all_files:
        if move_back_button_inside(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}개 파일 수정")
    print("=" * 60)

if __name__ == "__main__":
    main()

