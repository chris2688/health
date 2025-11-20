import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 뉴스 스타일 CSS
NEWS_STYLE_CSS = '''
    <style>
        /* 뉴스 그리드 스타일 (건강News와 동일) */
        .news-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 30px;
            max-width: 1200px;
            margin: 40px auto 0;
            padding: 0 20px;
        }
        
        .news-item {
            text-decoration: none;
            display: flex;
            flex-direction: column;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }
        
        .news-item:hover {
            transform: translateY(-8px);
        }
        
        .news-thumbnail {
            width: 100%;
            aspect-ratio: 1 / 1;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            transition: all 0.3s;
            position: relative;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .news-item:hover .news-thumbnail {
            box-shadow: 0 20px 40px rgba(0,0,0,0.25);
        }
        
        .news-thumbnail img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s;
        }
        
        .news-item:hover .news-thumbnail img {
            transform: scale(1.05);
        }
        
        .news-thumbnail::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(to bottom, transparent 50%, rgba(0,0,0,0.3));
        }
        
        .news-thumbnail-placeholder {
            font-size: 60px;
            color: white;
            opacity: 0.8;
        }
        
        .news-title {
            margin-top: 15px;
            font-size: 18px;
            font-weight: 600;
            color: #333;
            line-height: 1.5;
            text-align: center;
            padding: 0 10px;
        }
        
        .news-date {
            margin-top: 8px;
            font-size: 14px;
            color: #999;
            text-align: center;
        }
        
        .no-posts-message {
            text-align: center;
            padding: 60px 20px;
            color: #999;
            font-size: 18px;
        }
        
        @media (max-width: 768px) {
            .news-grid {
                grid-template-columns: 1fr;
                gap: 30px;
            }
            
            .news-title {
                font-size: 16px;
            }
        }
    </style>
'''

def update_sub_page(filepath):
    """서브 페이지의 임시 글 제거 및 뉴스 스타일로 변경"""
    print(f"Updating: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 페이지 제목 추출
        page_title_match = re.search(r'<h1 class="page-title">(.*?)</h1>', content)
        page_title = page_title_match.group(1) if page_title_match else "건강 정보"
        
        # 뒤로가기 링크 추출
        back_link_match = re.search(r'<a href="(category-[^"]+\.html)" class="back-button">', content)
        back_link = back_link_match.group(1) if back_link_match else "index-v2.html"
        
        # CSS 링크 제거 (강력한-카테고리-스타일.css)
        content = re.sub(r'<link rel="stylesheet" href="강력한-카테고리-스타일\.css">\s*', '', content)
        
        # 기존 .site-main 스타일 제거
        content = re.sub(r'<style>[^<]*\.site-main\s*\{[^}]+\}[^<]*</style>\s*', '', content, flags=re.DOTALL)
        
        # </head> 전에 뉴스 스타일 CSS 추가
        if NEWS_STYLE_CSS not in content:
            content = content.replace('</head>', NEWS_STYLE_CSS + '\n</head>')
        
        # 기존 content 영역을 뉴스 그리드로 교체
        # <div class="content">...</div> 부분을 찾아서 교체
        pattern = r'<div class="content">.*?</div>\s*</div>'
        
        new_content = f'''<div class="news-grid">
            <!-- 워드프레스에서 글을 가져와 여기에 표시됩니다 -->
            <div class="no-posts-message">
                <p>📝 곧 업데이트될 예정입니다</p>
                <p style="font-size: 14px; margin-top: 10px; color: #ccc;">워드프레스 글이 연동되면 여기에 표시됩니다</p>
            </div>
        </div>
    </div>'''
        
        content = re.sub(pattern, new_content, content, flags=re.DOTALL)
        
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
    print("🧹 서브 페이지 정리 - 임시 글 제거 및 뉴스 스타일 적용")
    print("=" * 60)
    
    sub_files = glob.glob("sub-*.html")
    print(f"\n📁 총 {len(sub_files)}개 파일")
    
    success_count = 0
    for file in sub_files:
        if update_sub_page(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(sub_files)}개 파일")
    print("=" * 60)
    print("\n📝 변경사항:")
    print("  - 임시 article 제거")
    print("  - 건강News와 동일한 2열 그리드 레이아웃")
    print("  - 1:1 비율 썸네일 준비")
    print("  - 워드프레스 글 연동 준비 완료")

if __name__ == "__main__":
    main()

