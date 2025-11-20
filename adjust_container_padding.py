import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def adjust_padding(filepath):
    """health-card-container의 padding을 조정하여 뒤로가기 버튼이 상단에 자연스럽게 위치"""
    print(f"Adjusting: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 기존: padding: 40px 20px 60px;
        # 새로운: padding: 0;
        # 그리고 뒤로가기 버튼에 margin-top: 20px 추가
        
        # 1. health-card-container padding 수정
        old_padding = r'\.health-card-container \{[^}]*padding:\s*40px 20px 60px;[^}]*\}'
        
        new_container_style = '''.health-card-container {
            padding: 0;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: calc(100vh - 80px);
        }
        
        .container-content {
            padding: 20px 20px 60px;
            max-width: 1200px;
            margin: 0 auto;
        }'''
        
        content = re.sub(old_padding, new_container_style, content, flags=re.DOTALL)
        
        # 2. 뒤로가기 버튼 margin 조정
        old_back_button = r'\.back-button \{[^}]*margin:\s*0 0 30px 0;[^}]*margin-left:[^;]+;[^}]*\}'
        
        new_back_button = '''.back-button {
            display: inline-block;
            margin: 20px 0 30px 0;
            margin-left: 0;
            padding: 12px 24px;
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.3s;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }'''
        
        content = re.sub(old_back_button, new_back_button, content, flags=re.DOTALL)
        
        # 3. HTML 구조 수정: container 안에 content wrapper 추가
        # <div class="health-card-container">
        #     <a href="..." class="back-button">뒤로가기</a>
        #     <div class="section-title">...
        # 를
        # <div class="health-card-container">
        #     <div class="container-content">
        #         <a href="..." class="back-button">뒤로가기</a>
        #         <div class="section-title">...
        
        pattern = r'(<div class="health-card-container">)\s*(<a href="[^"]*" class="back-button">뒤로가기</a>)\s*(<div class="section-title">)'
        replacement = r'\1\n        <div class="container-content">\n            \2\n\n            \3'
        
        content = re.sub(pattern, replacement, content)
        
        # 4. 닫는 태그도 수정: </div></div> 전에 </div> 하나 더 추가
        pattern2 = r'(</div>\s*</div>\s*</div>\s*<script>)'
        replacement2 = r'</div>\n        </div>\n    </div>\n\n    <script>'
        
        content = re.sub(pattern2, replacement2, content)
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 조정 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🎨 컨테이너 padding 조정 - 뒤로가기 버튼 자연스럽게")
    print("=" * 60)
    
    # 뒤로가기가 있는 모든 페이지
    all_files = glob.glob("category-*.html") + glob.glob("food-*.html")
    all_files = [f for f in all_files if f != "food-main.html"]
    
    print(f"\n📁 총 {len(all_files)}개 파일")
    
    success_count = 0
    for file in all_files:
        if adjust_padding(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}개 파일")
    print("=" * 60)

if __name__ == "__main__":
    main()

