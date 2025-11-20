import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def update_menu(filepath):
    """모든 페이지의 메뉴에서 건강News 링크 업데이트"""
    print(f"Updating: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 건강News 링크 업데이트
        old_link = 'https://health9988234.mycafe24.com/category/건강-new/'
        new_link = 'news-main.html'
        
        if old_link in content:
            content = content.replace(old_link, new_link)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ 업데이트 완료!")
            return True
        else:
            print(f"  ℹ️ 이미 업데이트됨 또는 해당 없음")
            return False
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return False

def main():
    print("=" * 60)
    print("🔗 모든 페이지의 건강News 메뉴 링크 업데이트")
    print("=" * 60)
    
    # 모든 HTML 파일
    all_files = (glob.glob("index-v2.html") + 
                 glob.glob("category-*.html") + 
                 glob.glob("sub-*.html") + 
                 glob.glob("food-*.html") + 
                 glob.glob("exercise-*.html") +
                 glob.glob("lifestyle-*.html") +
                 glob.glob("news-*.html"))
    
    print(f"\n📁 총 {len(all_files)}개 파일")
    
    success_count = 0
    for file in all_files:
        if update_menu(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}개 파일 업데이트됨")
    print("=" * 60)

if __name__ == "__main__":
    main()

