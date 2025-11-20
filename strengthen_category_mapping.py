import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 각 질환별 정확한 키워드 매핑 (매우 구체적으로)
STRICT_KEYWORD_MAP = {
    # 소화기 질환
    '역류성식도염': ['digestive'],
    '역류성 식도염': ['digestive'],
    '위염위궤양': ['digestive'],
    '위궤양': ['digestive'],
    '위염': ['digestive'],
    # 과민성대장증후군은 별도로 처리 (역류성 식도염과 무관)
    '과민성대장증후군': ['digestive'],
    # 지방간은 별도로 처리
    '지방간': ['digestive'],
    
    # 심혈관 질환
    '고혈압': ['cardiovascular'],
    '고지혈증': ['cardiovascular'],
    '콜레스테롤': ['cardiovascular'],
    '심근경색': ['cardiovascular'],
    '협심증': ['cardiovascular'],
    '뇌졸중': ['cardiovascular'],
    '동맥경화': ['cardiovascular'],
    
    # 당뇨병
    '당뇨병': ['diabetes'],
    '당뇨': ['diabetes'],
    '공복혈당장애': ['diabetes'],
    '공복혈당': ['diabetes'],
    '당뇨합병증': ['diabetes'],
    '인슐린': ['diabetes'],
    '혈당': ['diabetes'],
    
    # 관절/근골격계
    '퇴행성관절염': ['musculoskeletal'],
    '오십견': ['musculoskeletal'],
    '유착성관절낭염': ['musculoskeletal'],
    '허리디스크': ['musculoskeletal'],
    '목디스크': ['musculoskeletal'],
    '골다공증': ['musculoskeletal'],
    '관절염': ['musculoskeletal'],
    
    # 호르몬/내분비
    '갱년기증후군': ['endocrine'],
    '갱년기': ['endocrine'],
    '갑상선': ['endocrine'],
    '대사증후군': ['endocrine'],
    
    # 정신 건강/신경계
    '우울증번아웃': ['neuroscience'],
    '우울증': ['neuroscience'],
    '수면장애불면증': ['neuroscience'],
    '수면장애': ['neuroscience'],
    '치매경도인지장애': ['neuroscience'],
    '치매': ['neuroscience'],
    '이명어지럼증': ['neuroscience'],
    '이명현훈': ['neuroscience'],
    '이명': ['neuroscience'],
    '어지럼증': ['neuroscience'],
    
    # 안과/치과/기타
    '백내장녹내장': ['eyes-dental'],
    '백내장': ['eyes-dental'],
    '녹내장': ['eyes-dental'],
    '치주염치아손실': ['eyes-dental'],
    '치주질환': ['eyes-dental'],
    '비만체형변화': ['eyes-dental'],
    '비만': ['eyes-dental'],
}

def get_strict_keywords_for_page(page_title):
    """페이지 제목에 따라 정확한 키워드만 반환"""
    page_lower = page_title.lower().replace(' ', '').replace('-', '')
    
    # 정확한 매칭만 반환
    for keyword, categories in STRICT_KEYWORD_MAP.items():
        keyword_lower = keyword.lower().replace(' ', '').replace('-', '')
        if keyword_lower in page_lower or page_lower in keyword_lower:
            return {keyword: categories}
    
    return {}

def fix_file(filepath):
    """파일의 매핑을 더 엄격하게 수정"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 페이지 제목 추출
        page_title_match = re.search(r'<h1 class="page-title">(.*?)</h1>', content)
        if not page_title_match:
            page_title_match = re.search(r'<title>(.*?)(?:\s*-\s*9988.*?)?</title>', content)
        
        page_title = page_title_match.group(1).strip() if page_title_match else ''
        print(f"  페이지 제목: {page_title}")
        
        # 해당 페이지에 맞는 정확한 키워드만 추출
        strict_keywords = get_strict_keywords_for_page(page_title)
        
        if not strict_keywords:
            print(f"  ⚠️  정확한 키워드를 찾지 못함, 기본 키워드 사용")
            # 기본 키워드 맵 사용
            new_keyword_map = STRICT_KEYWORD_MAP
        else:
            # 해당 페이지와 직접 관련된 키워드만 포함
            print(f"  ✅ 정확한 키워드: {list(strict_keywords.keys())}")
            new_keyword_map = strict_keywords
        
        # 키워드 맵 생성
        keyword_map_js = "const keywordMap = {\n"
        for keyword, categories in new_keyword_map.items():
            keyword_map_js += f"                    '{keyword}': {categories},\n"
        keyword_map_js += "                };"
        
        # 기존 키워드 맵 교체
        old_keyword_map = r"const keywordMap = \{[\s\S]*?\};"
        if re.search(old_keyword_map, content):
            content = re.sub(old_keyword_map, keyword_map_js, content, flags=re.DOTALL)
            print(f"  ✅ 키워드 맵 업데이트")
        
        # 관련성 점수 기준 상향 (20점 → 50점)
        old_min_score = r"score >= 20"
        new_min_score = "score >= 50"
        if re.search(old_min_score, content):
            content = re.sub(old_min_score, new_min_score, content)
            print(f"  ✅ 최소 점수 기준 상향 (20 → 50)")
        
        # 핵심 키워드 매칭 비율 상향 (50% → 70%)
        old_match_ratio = r"matchedWords < pageTitleWords\.length \* 0\.5"
        new_match_ratio = "matchedWords < pageTitleWords.length * 0.7"
        if re.search(old_match_ratio, content):
            content = re.sub(old_match_ratio, new_match_ratio, content)
            print(f"  ✅ 키워드 매칭 비율 상향 (50% → 70%)")
        
        # 카테고리 매칭 점수 상향
        old_cat_score = r"score \+= 10; // 점수 감소"
        new_cat_score = "score += 5; // 점수 감소 (더 엄격)"
        if re.search(old_cat_score, content):
            content = re.sub(old_cat_score, new_cat_score, content)
        
        # 필터링 메시지 업데이트
        old_filter_msg = r"min score: 20"
        new_filter_msg = "min score: 50"
        if re.search(old_filter_msg, content):
            content = re.sub(old_filter_msg, new_filter_msg, content)
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🔒 매핑 강화 - 관련 없는 글 완전 차단")
    print("=" * 60)
    
    # news-main.html과 모든 sub-*.html 파일 처리
    target_files = ['news-main.html'] + glob.glob("sub-*.html")
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if fix_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 각 페이지별 정확한 키워드만 매핑")
    print("  ✅ 최소 점수 기준 상향 (20점 → 50점)")
    print("  ✅ 키워드 매칭 비율 상향 (50% → 70%)")
    print("  ✅ 관련 없는 글 완전 차단")

if __name__ == "__main__":
    main()

