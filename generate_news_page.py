import os
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 페이지 템플릿 불러오기
from page_template import STANDARD_PAGE_TEMPLATE, STANDARD_FOOTER

def create_news_page():
    """건강News 페이지 생성"""
    print("Creating: news-main.html")
    
    title = '건강News - 9988 건강정보'
    color1 = '#43e97b'
    color2 = '#38f9d7'
    
    header = STANDARD_PAGE_TEMPLATE.format(
        title=title,
        color1=color1,
        color2=color2
    )
    
    # 메뉴 링크를 news-main.html로 업데이트
    header = header.replace(
        'href="https://health9988234.mycafe24.com/category/건강-new/"',
        'href="news-main.html"'
    )
    
    # 추가 CSS for News 스타일
    additional_css = '''
    <style>
        /* 뉴스 그리드 스타일 */
        .news-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
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
    
    # 샘플 뉴스 데이터 (나중에 워드프레스에서 가져올 부분)
    # 실제로는 워드프레스 REST API를 통해 가져와야 함
    sample_news = [
        {
            'id': 1,
            'title': '50대 이후 반드시 챙겨야 할 건강검진 5가지',
            'thumbnail': 'https://via.placeholder.com/400x400/667eea/ffffff?text=건강검진',
            'date': '2024.11.19',
            'link': '#'
        },
        {
            'id': 2,
            'title': '겨울철 혈압 관리, 이것만은 꼭 지키세요',
            'thumbnail': 'https://via.placeholder.com/400x400/43e97b/ffffff?text=혈압관리',
            'date': '2024.11.18',
            'link': '#'
        },
        {
            'id': 3,
            'title': '당뇨 환자를 위한 연말 모임 음식 선택 가이드',
            'thumbnail': 'https://via.placeholder.com/400x400/FA709A/ffffff?text=당뇨식단',
            'date': '2024.11.17',
            'link': '#'
        },
        {
            'id': 4,
            'title': '관절염 악화 막는 겨울철 생활 습관',
            'thumbnail': 'https://via.placeholder.com/400x400/4facfe/ffffff?text=관절염',
            'date': '2024.11.16',
            'link': '#'
        },
        {
            'id': 5,
            'title': '중년 남성 탈모 예방, 지금부터 시작하세요',
            'thumbnail': 'https://via.placeholder.com/400x400/FF6B6B/ffffff?text=탈모예방',
            'date': '2024.11.15',
            'link': '#'
        },
        {
            'id': 6,
            'title': '갱년기 증상 완화에 도움되는 천연 식품',
            'thumbnail': 'https://via.placeholder.com/400x400/A18CD1/ffffff?text=갱년기',
            'date': '2024.11.14',
            'link': '#'
        },
        {
            'id': 7,
            'title': '수면의 질을 높이는 침실 환경 만들기',
            'thumbnail': 'https://via.placeholder.com/400x400/4ECDC4/ffffff?text=수면관리',
            'date': '2024.11.13',
            'link': '#'
        },
        {
            'id': 8,
            'title': '스트레스 줄이는 5분 호흡법',
            'thumbnail': 'https://via.placeholder.com/400x400/f093fb/ffffff?text=스트레스',
            'date': '2024.11.12',
            'link': '#'
        },
    ]
    
    # 뉴스 아이템 HTML 생성
    news_html = ""
    for news in sample_news:
        news_html += f'''            <a href="{news['link']}" class="news-item">
                <div class="news-thumbnail">
                    <img src="{news['thumbnail']}" alt="{news['title']}">
                </div>
                <h3 class="news-title">{news['title']}</h3>
                <p class="news-date">{news['date']}</p>
            </a>
            
'''
    
    content = f'''{additional_css}

    <div class="health-card-container">
        <div class="container-content">
            <a href="index-v2.html" class="back-button">뒤로가기</a>

            <div class="section-title">
                <div class="main-icon">📰</div>
                <h2>건강News</h2>
                <p class="subtitle">최신 건강 정보를 확인하세요</p>
            </div>
            
            <div class="news-grid">
{news_html}        </div>
        </div>
    </div>
'''
    
    # 파일 저장
    with open('news-main.html', 'w', encoding='utf-8') as f:
        f.write(header + content + STANDARD_FOOTER)
    
    print(f"  ✅ 생성 완료! (샘플 뉴스: {len(sample_news)}개)")
    print(f"\n  📝 참고:")
    print(f"     - 현재는 샘플 이미지 사용")
    print(f"     - 실제 운영 시 워드프레스 REST API로 글 가져오기 필요")
    print(f"     - API 엔드포인트: https://health9988234.mycafe24.com/wp-json/wp/v2/posts?categories=건강-new")

def main():
    print("=" * 60)
    print("📰 건강News 페이지 생성")
    print("=" * 60)
    
    create_news_page()
    
    print("\n" + "=" * 60)
    print("✅ 완료: news-main.html 생성")
    print("=" * 60)

if __name__ == "__main__":
    main()

