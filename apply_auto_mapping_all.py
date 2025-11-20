import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def get_keyword_map_for_page(page_title):
    """페이지 제목에 따라 정확한 키워드 맵 반환"""
    page_lower = page_title.lower().replace(' ', '').replace('-', '').replace('/', '').replace('(', '').replace(')', '')
    
    # 각 페이지별 키워드 맵
    page_keyword_map = {
        # 역류성 식도염
        '역류성식도염': {'역류성식도염': ['digestive'], '역류성 식도염': ['digestive'], '역류': ['digestive'], '식도염': ['digestive']},
        '역류성 식도염': {'역류성식도염': ['digestive'], '역류성 식도염': ['digestive'], '역류': ['digestive'], '식도염': ['digestive']},
        # 위염
        '위염': {'위염': ['digestive'], '위궤양': ['digestive'], '위염위궤양': ['digestive']},
        '위염위궤양': {'위염': ['digestive'], '위궤양': ['digestive'], '위염위궤양': ['digestive']},
        '위궤양': {'위염': ['digestive'], '위궤양': ['digestive'], '위염위궤양': ['digestive']},
        # 과민성대장증후군
        '과민성대장증후군': {'과민성대장증후군': ['digestive'], '대장': ['digestive']},
        # 지방간
        '지방간': {'지방간': ['digestive'], '간기능': ['digestive']},
        '간기능': {'지방간': ['digestive'], '간기능': ['digestive']},
        # 고혈압
        '고혈압': {'고혈압': ['cardiovascular']},
        # 고지혈증
        '고지혈증': {'고지혈증': ['cardiovascular'], '콜레스테롤': ['cardiovascular']},
        '콜레스테롤': {'고지혈증': ['cardiovascular'], '콜레스테롤': ['cardiovascular']},
        # 당뇨
        '당뇨': {'당뇨': ['diabetes'], '당뇨병': ['diabetes'], '공복혈당': ['diabetes'], '공복혈당장애': ['diabetes'], '당뇨합병증': ['diabetes'], '인슐린': ['diabetes'], '혈당': ['diabetes']},
        '당뇨병': {'당뇨': ['diabetes'], '당뇨병': ['diabetes'], '공복혈당': ['diabetes'], '공복혈당장애': ['diabetes'], '당뇨합병증': ['diabetes']},
        '공복혈당': {'공복혈당': ['diabetes'], '공복혈당장애': ['diabetes']},
        '공복혈당장애': {'공복혈당': ['diabetes'], '공복혈당장애': ['diabetes']},
        '당뇨합병증': {'당뇨합병증': ['diabetes']},
        '인슐린': {'인슐린': ['diabetes']},
        '혈당': {'혈당': ['diabetes']},
        # 관절
        '관절염': {'관절염': ['musculoskeletal'], '퇴행성관절염': ['musculoskeletal']},
        '퇴행성관절염': {'관절염': ['musculoskeletal'], '퇴행성관절염': ['musculoskeletal']},
        '오십견': {'오십견': ['musculoskeletal'], '유착성관절낭염': ['musculoskeletal']},
        '허리디스크': {'허리디스크': ['musculoskeletal'], '목디스크': ['musculoskeletal']},
        '목디스크': {'허리디스크': ['musculoskeletal'], '목디스크': ['musculoskeletal']},
        '골다공증': {'골다공증': ['musculoskeletal']},
        # 호르몬
        '갑상선': {'갑상선': ['endocrine']},
        '갱년기': {'갱년기': ['endocrine'], '갱년기증후군': ['endocrine']},
        '갱년기증후군': {'갱년기': ['endocrine'], '갱년기증후군': ['endocrine']},
        '대사증후군': {'대사증후군': ['endocrine']},
        # 정신 건강
        '우울증': {'우울증': ['neuroscience'], '번아웃': ['neuroscience'], '우울증번아웃': ['neuroscience']},
        '우울증번아웃': {'우울증': ['neuroscience'], '번아웃': ['neuroscience'], '우울증번아웃': ['neuroscience']},
        '수면장애': {'수면장애': ['neuroscience'], '불면증': ['neuroscience'], '수면장애불면증': ['neuroscience']},
        '수면장애불면증': {'수면장애': ['neuroscience'], '불면증': ['neuroscience'], '수면장애불면증': ['neuroscience']},
        '치매': {'치매': ['neuroscience'], '경도인지장애': ['neuroscience'], '치매경도인지장애': ['neuroscience']},
        '치매경도인지장애': {'치매': ['neuroscience'], '경도인지장애': ['neuroscience'], '치매경도인지장애': ['neuroscience']},
        '이명': {'이명': ['neuroscience'], '어지럼증': ['neuroscience'], '이명어지럼증': ['neuroscience'], '이명현훈': ['neuroscience'], '현훈': ['neuroscience']},
        '이명어지럼증': {'이명': ['neuroscience'], '어지럼증': ['neuroscience'], '이명어지럼증': ['neuroscience']},
        '이명현훈': {'이명': ['neuroscience'], '현훈': ['neuroscience'], '이명현훈': ['neuroscience']},
        '어지럼증': {'어지럼증': ['neuroscience'], '이명': ['neuroscience']},
        # 안과/치과
        '백내장': {'백내장': ['eyes-dental'], '녹내장': ['eyes-dental'], '백내장녹내장': ['eyes-dental']},
        '녹내장': {'백내장': ['eyes-dental'], '녹내장': ['eyes-dental'], '백내장녹내장': ['eyes-dental']},
        '백내장녹내장': {'백내장': ['eyes-dental'], '녹내장': ['eyes-dental'], '백내장녹내장': ['eyes-dental']},
        '치주염': {'치주염': ['eyes-dental'], '치아손실': ['eyes-dental'], '치주염치아손실': ['eyes-dental'], '치주질환': ['eyes-dental']},
        '치주질환': {'치주염': ['eyes-dental'], '치주질환': ['eyes-dental']},
        '비만': {'비만': ['eyes-dental'], '체형변화': ['eyes-dental'], '비만체형변화': ['eyes-dental']},
        '비만체형변화': {'비만': ['eyes-dental'], '체형변화': ['eyes-dental'], '비만체형변화': ['eyes-dental']},
        # 심혈관
        '심근경색': {'심근경색': ['cardiovascular'], '협심증': ['cardiovascular']},
        '협심증': {'협심증': ['cardiovascular'], '심근경색': ['cardiovascular']},
        '뇌졸중': {'뇌졸중': ['cardiovascular']},
        '동맥경화': {'동맥경화': ['cardiovascular']},
    }
    
    # 정확한 매칭 찾기
    for key, keyword_map in page_keyword_map.items():
        key_lower = key.lower().replace(' ', '').replace('-', '').replace('/', '').replace('(', '').replace(')', '')
        if key_lower in page_lower or page_lower in key_lower:
            return keyword_map
    
    # 부분 매칭
    for key, keyword_map in page_keyword_map.items():
        key_lower = key.lower().replace(' ', '').replace('-', '').replace('/', '').replace('(', '').replace(')', '')
        if any(kw.lower().replace(' ', '') in page_lower for kw in keyword_map.keys()):
            return keyword_map
    
    return {}

def enhance_file(filepath):
    """파일에 자동 매핑 기능 강화"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 페이지 제목 추출
        page_title_match = re.search(r'<h1 class="page-title">(.*?)</h1>', content)
        if not page_title_match:
            page_title_match = re.search(r'<title>(.*?)(?:\s*-\s*9988.*?)?</title>', content)
        
        page_title = page_title_match.group(1).strip() if page_title_match else ''
        
        # 해당 페이지의 키워드 맵 가져오기
        keyword_map = get_keyword_map_for_page(page_title)
        
        if not keyword_map:
            print(f"  ⚠️  키워드 맵을 찾을 수 없음, 기본 맵 사용")
            return False
        
        # 키워드 맵을 JavaScript 코드로 변환
        keyword_map_js = "const keywordMap = {\n"
        for keyword, categories in keyword_map.items():
            keyword_map_js += f"                    '{keyword}': {categories},\n"
        keyword_map_js += "                };"
        
        # 기존 키워드 맵 교체
        old_keyword_map = r"const keywordMap = \{[\s\S]*?\};"
        if re.search(old_keyword_map, content):
            content = re.sub(old_keyword_map, keyword_map_js, content, flags=re.DOTALL)
            print(f"  ✅ 키워드 맵 업데이트")
        
        # findCategoryByPageTitle 함수 강화
        old_find_func = r"// 페이지 제목 기반 카테고리 자동 매핑[\s\S]*?async function findCategoryByPageTitle\(pageTitle\) \{[\s\S]*?\}"
        
        new_find_func = '''// 페이지 제목 기반 카테고리 자동 매핑 (강화된 버전)
            // 🚀 워드프레스에 새 글이 올라오면 자동으로 매핑됨!
            async function findCategoryByPageTitle(pageTitle) {
                if (!pageTitle) return [];

                try {
                    // 모든 카테고리 가져오기 (더 많이, 인기순으로 정렬)
                    const response = await fetch('https://health9988234.mycafe24.com/wp-json/wp/v2/categories?per_page=100&orderby=count&order=desc');
                    const categories = await response.json();

                    const matchedSlugs = [];
                    const pageTitleLower = pageTitle.toLowerCase().replace(/\\s+/g, '').replace(/[()]/g, '');

                    // 1. 정확히 일치하는 카테고리 찾기 (상위 카테고리 'disease-info' 제외)
                    let matched = categories.find(cat => {
                        const catNameLower = cat.name.toLowerCase().replace(/\\s+/g, '').replace(/[()]/g, '');
                        return catNameLower === pageTitleLower && cat.slug !== 'disease-info';
                    });
                    if (matched) {
                        matchedSlugs.push(matched.slug);
                        console.log(`✅ 정확히 일치하는 카테고리: ${matched.name} (${matched.slug})`);
                    }

                    // 2. 부분 일치 찾기 (상위 카테고리 'disease-info' 제외)
                    matched = categories.find(cat => {
                        const catNameLower = cat.name.toLowerCase().replace(/\\s+/g, '').replace(/[()]/g, '');
                        return (catNameLower.includes(pageTitleLower) || pageTitleLower.includes(catNameLower)) &&
                               !matchedSlugs.includes(cat.slug) &&
                               cat.slug !== 'disease-info';
                    });
                    if (matched) {
                        matchedSlugs.push(matched.slug);
                        console.log(`✅ 부분 일치하는 카테고리: ${matched.name} (${matched.slug})`);
                    }

                    // 3. 워드프레스 카테고리 이름으로 자동 매핑 (더 정확하게)
                    // 카테고리 이름에 페이지 제목의 핵심 키워드가 포함되어 있으면 매핑
                    const pageKeywords = pageTitleLower.split(/[/\\-]+/).filter(w => w.length > 2);
                    categories.forEach(cat => {
                        if (cat.slug === 'disease-info' || matchedSlugs.includes(cat.slug)) return;
                        
                        const catNameLower = cat.name.toLowerCase().replace(/\\s+/g, '').replace(/[()]/g, '');
                        const matchedKeywords = pageKeywords.filter(kw => catNameLower.includes(kw) || kw.includes(catNameLower));
                        
                        if (matchedKeywords.length > 0 && matchedKeywords.length >= pageKeywords.length * 0.5) {
                            matchedSlugs.push(cat.slug);
                            console.log(`✅ 키워드 매칭 카테고리: ${cat.name} (${matchedKeywords.join(', ')})`);
                        }
                    });

                    // 4. 키워드 기반 매핑 (더 구체적인 키워드를 우선적으로 매칭)
                    ''' + keyword_map_js + '''

                    const sortedKeywords = Object.keys(keywordMap).sort((a, b) => b.length - a.length);

                    for (const keyword of sortedKeywords) {
                        const keywordLower = keyword.toLowerCase().replace(/\\s+/g, '').replace(/[()]/g, '');
                        if (pageTitleLower.includes(keywordLower) || keywordLower.includes(pageTitleLower)) {
                            const slugs = keywordMap[keyword];
                            slugs.forEach(slug => {
                                if (!matchedSlugs.includes(slug)) {
                                    matchedSlugs.push(slug);
                                    console.log(`✅ 키워드 맵 매칭: ${keyword} → ${slug}`);
                                }
                            });
                            break;
                        }
                    }
                    
                    // 중복 제거
                    return [...new Set(matchedSlugs)];
                } catch (error) {
                    console.error('Category mapping error:', error);
                    return [];
                }
            }'''
        
        # findCategoryByPageTitle 함수 교체
        if re.search(old_find_func, content, flags=re.DOTALL):
            content = re.sub(old_find_func, new_find_func, content, flags=re.DOTALL)
            print(f"  ✅ 자동 매핑 함수 강화")
        else:
            print(f"  ⚠️  findCategoryByPageTitle 함수를 찾을 수 없음")
            return False
        
        # 자동 매핑 안내 메시지 추가
        old_log = r"console\.log\('Category IDs:', categoryIds\);"
        new_log = '''console.log('Category IDs:', categoryIds);
                    console.log('📝 자동 매핑: 워드프레스에 새 글이 올라오면 자동으로 이 페이지에 표시됩니다!');
                    console.log('   - 글의 카테고리와 제목을 분석하여 관련 페이지에 자동 매핑됩니다.');'''
        
        if re.search(old_log, content):
            content = re.sub(old_log, new_log, content)
            print(f"  ✅ 자동 매핑 안내 메시지 추가")
        
        # 파일 저장
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
    print("🚀 자동 매핑 기능 강화 - 워드프레스 새 글 자동 매핑")
    print("=" * 60)
    
    # news-main.html과 모든 sub-*.html 파일 처리
    target_files = ['news-main.html'] + glob.glob("sub-*.html")
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if enhance_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 워드프레스 카테고리 이름 자동 매핑 강화")
    print("  ✅ 글 제목 키워드 분석 개선")
    print("  ✅ 새 글이 올라오면 자동으로 관련 페이지에 표시")
    print("  ✅ 카테고리 정보 우선 활용")

if __name__ == "__main__":
    main()

