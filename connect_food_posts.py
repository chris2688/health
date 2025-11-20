import os
import sys
import io
import re
import json

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 각 파일의 항목 정의
FOOD_ITEMS = {
    'food-질환별식단.html': [
        {'title': '고혈압', 'keywords': ['고혈압', '식단']},
        {'title': '당뇨', 'keywords': ['당뇨', '식단']},
        {'title': '지방간', 'keywords': ['지방간', '식단']},
        {'title': '갱년기', 'keywords': ['갱년기', '식단']},
        {'title': '우울증', 'keywords': ['우울증', '식단']},
        {'title': '협심증/심근경색', 'keywords': ['협심증', '심근경색', '식단']},
        {'title': '퇴행성 관절염/오십견', 'keywords': ['퇴행성', '관절염', '오십견', '식단']},
        {'title': '골다공증', 'keywords': ['골다공증', '식단']},
        {'title': '역류성 식도염', 'keywords': ['역류성', '식도염', '식단']},
        {'title': '고지혈증(콜레스테롤)', 'keywords': ['고지혈증', '콜레스테롤', '식단']},
    ],
    'food-피해야할과일.html': [
        {'title': '고혈압', 'keywords': ['고혈압', '피해야', '과일'], 'subtitle': '피해야 할 과일 3가지 (의외의 1등은?)'},
        {'title': '당뇨', 'keywords': ['당뇨', '피해야', '과일'], 'subtitle': '이 과일은 꼭 피하세요. 혈당이 확 오릅니다.'},
        {'title': '고지혈증(콜레스테롤)', 'keywords': ['고지혈증', '콜레스테롤', '피해야', '과일'], 'subtitle': '콜레스테롤 높은 분들, 이 과일은 피하셔야 합니다.'},
        {'title': '지방간', 'keywords': ['지방간', '피해야', '과일'], 'subtitle': '간에 독이 되는 과일? 달콤하지만 위험한 선택'},
        {'title': '위염/역류성 식도염', 'keywords': ['위염', '역류성', '식도염', '피해야', '과일'], 'subtitle': '위염 있으세요? 속 쓰리게 만드는 과일 3가지'},
        {'title': '골다공증', 'keywords': ['골다공증', '피해야', '과일'], 'subtitle': '뼈 건강에 안 좋은 과일이 있다고요? 꼭 피하세요!'},
        {'title': '갱년기', 'keywords': ['갱년기', '피해야', '과일'], 'subtitle': '갱년기 증상 더 악화시키는 과일, 의외로 자주 먹는 이것!'},
        {'title': '우울증', 'keywords': ['우울증', '피해야', '과일'], 'subtitle': '기분 더 가라앉게 만드는 과일? 우울증에 안 좋은 과일 리스트'},
        {'title': '수면장애', 'keywords': ['수면장애', '피해야', '과일'], 'subtitle': '잠 안 올 때 피해야 할 과일, 숙면을 방해합니다'},
        {'title': '협심증/심근경색', 'keywords': ['협심증', '심근경색', '피해야', '과일'], 'subtitle': '심장 건강에 해로운 과일? 협심증 환자 주의!'},
    ],
    'food-모르면독이된다.html': [
        {'title': '비타민 먹을 때 절대 같이 먹으면 안되는 음식', 'keywords': ['비타민', '같이', '먹으면', '안되는']},
        {'title': '아침 공복에 먹으면 해로운 음식', 'keywords': ['아침', '공복', '해로운', '음식']},
        {'title': '자기 전에 먹으면 살찌는 음식 TOP3', 'keywords': ['자기', '전', '살찌는', '음식']},
        {'title': '아침에 먹기 좋은 vs 나쁜 음식', 'keywords': ['아침', '좋은', '나쁜', '음식']},
        {'title': '당 줄였는데 더 해로운 \'무설탕\' 음식들', 'keywords': ['무설탕', '해로운', '음식']},
        {'title': '건강식인 줄 알았는데? 숨은 나트륨 폭탄', 'keywords': ['건강식', '나트륨', '폭탄']},
        {'title': '다이어트할 때 절대 같이 먹으면 안되는 조합', 'keywords': ['다이어트', '같이', '먹으면', '안되는', '조합']},
        {'title': '과일주스는 건강할까? 진짜 진실', 'keywords': ['과일주스', '건강', '진실']},
        {'title': '단백질은 많이 먹을수록 좋다?', 'keywords': ['단백질', '많이', '먹을수록']},
        {'title': '밥을 줄였는데도 살 안 빠지는 이유', 'keywords': ['밥', '줄였는데', '살', '안', '빠지는']},
        {'title': '샐러드만 먹는데 혈당 오르는 이유', 'keywords': ['샐러드', '혈당', '오르는']},
        {'title': '오메가3와 절대 같이 먹지 말아야 할 음식', 'keywords': ['오메가3', '같이', '먹지', '말아야']},
        {'title': '칼슘제 복용 시 피해야 할 음료', 'keywords': ['칼슘제', '복용', '피해야', '음료']},
        {'title': '설탕보다 무서운 당분 \'○○ 시럽\'이 문제입니다', 'keywords': ['설탕', '당분', '시럽', '문제']},
        {'title': '건강 간식에 숨은 나트륨', 'keywords': ['건강', '간식', '나트륨']},
    ]
}

def add_post_matching_script(filepath, items):
    """각 카드를 워드프레스 글과 매칭하는 스크립트 추가"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 스크립트가 있으면 제거
        if 'matchFoodPosts' in content:
            print(f"  ⏭️  이미 스크립트가 있음, 업데이트")
            # 기존 스크립트 제거
            content = re.sub(r'<script>\s*//.*?matchFoodPosts.*?</script>', '', content, flags=re.DOTALL)
        
        # items를 JSON 형식으로 변환
        items_json = []
        for item in items:
            items_json.append({
                'title': item['title'],
                'keywords': item.get('keywords', []),
                'subtitle': item.get('subtitle', '')
            })
        
        # items를 JSON 문자열로 변환
        items_json_str = json.dumps(items_json, ensure_ascii=False, indent=2)
        
        # 매칭 스크립트 생성
        matching_script = f'''
    <script>
        // 워드프레스 글과 카드 매칭
        async function matchFoodPosts() {{
            const items = {items_json_str};
            const cards = document.querySelectorAll('.health-card');
            
            try {{
                // 식단/음식 카테고리 글 가져오기 (여러 카테고리 시도)
                const categorySlugs = ['식단-음식', '식단음식', '식단/음식'];
                let categoryId = null;
                
                for (const slug of categorySlugs) {{
                    try {{
                        const catResponse = await fetch(`https://health9988234.mycafe24.com/wp-json/wp/v2/categories?slug=${{encodeURIComponent(slug)}}`);
                        const categories = await catResponse.json();
                        if (categories.length > 0) {{
                            categoryId = categories[0].id;
                            console.log(`카테고리 찾음: ${{slug}} (ID: ${{categoryId}})`);
                            break;
                        }}
                    }} catch (e) {{
                        console.warn(`카테고리 찾기 실패: ${{slug}}`);
                    }}
                }}
                
                let apiUrl = 'https://health9988234.mycafe24.com/wp-json/wp/v2/posts?per_page=100&_embed';
                if (categoryId) {{
                    apiUrl += `&categories=${{categoryId}}`;
                }}
                
                console.log('Fetching posts from:', apiUrl);
                const response = await fetch(apiUrl);
                const posts = await response.json();
                
                console.log('Fetched posts:', posts.length);
                console.log('Post titles:', posts.map(p => p.title.rendered));
                
                // 문자열 유사도 계산 함수
                function calculateSimilarity(str1, str2) {{
                    const s1 = str1.toLowerCase().replace(/[\\s\\/\\-\\(\\)]/g, '');
                    const s2 = str2.toLowerCase().replace(/[\\s\\/\\-\\(\\)]/g, '');
                    if (s1 === s2) return 1.0;
                    if (s1.includes(s2) || s2.includes(s1)) return 0.8;
                    
                    // 공통 문자 비율 계산
                    const longer = s1.length > s2.length ? s1 : s2;
                    const shorter = s1.length > s2.length ? s2 : s1;
                    let matches = 0;
                    for (let i = 0; i < shorter.length; i++) {{
                        if (longer.includes(shorter[i])) matches++;
                    }}
                    return matches / longer.length;
                }}
                
                // 각 카드에 매칭
                cards.forEach((card, index) => {{
                    if (index >= items.length) return;
                    
                    const item = items[index];
                    const cardTitle = item.title;
                    const keywords = item.keywords || [];
                    const cardTitleLower = cardTitle.toLowerCase();
                    
                    // 가장 유사한 글 찾기
                    let bestMatch = null;
                    let bestScore = 0;
                    const usedPostIds = new Set(); // 이미 매칭된 글 제외
                    
                    posts.forEach(post => {{
                        if (usedPostIds.has(post.id)) return; // 이미 매칭된 글은 제외
                        
                        const postTitle = post.title.rendered;
                        const postTitleLower = postTitle.toLowerCase();
                        let score = 0;
                        
                        // 1. 제목 정확 일치 (최고 점수)
                        if (postTitleLower.includes(cardTitleLower) || cardTitleLower.includes(postTitleLower)) {{
                            score += 100;
                        }}
                        
                        // 2. 제목 유사도
                        const similarity = calculateSimilarity(cardTitle, postTitle);
                        score += similarity * 50;
                        
                        // 3. 키워드 매칭 점수
                        keywords.forEach(keyword => {{
                            const keywordLower = keyword.toLowerCase();
                            if (postTitleLower.includes(keywordLower)) {{
                                score += 15;
                            }}
                        }});
                        
                        // 4. 카드 제목의 주요 단어가 글 제목에 포함되는지
                        const cardWords = cardTitleLower.split(/[\\s\\/\\-]/).filter(w => w.length > 1);
                        cardWords.forEach(word => {{
                            if (postTitleLower.includes(word)) {{
                                score += 10;
                            }}
                        }});
                        
                        if (score > bestScore) {{
                            bestScore = score;
                            bestMatch = post;
                        }}
                    }});
                    
                    // 매칭된 글의 링크 설정 (점수가 충분히 높을 때만)
                    if (bestMatch && bestScore >= 20) {{
                        usedPostIds.add(bestMatch.id); // 사용된 글 표시
                        const backUrl = encodeURIComponent(window.location.pathname.split('/').pop());
                        card.href = `post-detail.html?id=${{bestMatch.id}}&back=${{backUrl}}`;
                        console.log(`✅ 매칭: "${{cardTitle}}" -> "${{bestMatch.title.rendered}}" (점수: ${{bestScore}})`);
                    }} else {{
                        console.warn(`⚠️ 매칭 실패: "${{cardTitle}}" (최고 점수: ${{bestScore}})`);
                    }}
                }});
                
            }} catch (error) {{
                console.error('Error matching posts:', error);
            }}
        }}
        
        // 페이지 로드 시 실행
        document.addEventListener('DOMContentLoaded', function() {{
            matchFoodPosts();
        }});
    </script>'''
        
        # </body> 태그 앞에 스크립트 추가
        if '</body>' in content:
            content = content.replace('</body>', matching_script + '\n</body>')
        elif '</html>' in content:
            content = content.replace('</html>', matching_script + '\n</html>')
        else:
            content += matching_script
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🔗 식단/음식 카테고리 글 매칭")
    print("=" * 60)
    
    for filepath, items in FOOD_ITEMS.items():
        if os.path.exists(filepath):
            add_post_matching_script(filepath, items)
        else:
            print(f"⚠️ 파일을 찾을 수 없음: {filepath}")
    
    print("\n" + "=" * 60)
    print("✅ 완료!")
    print("=" * 60)

if __name__ == "__main__":
    main()

