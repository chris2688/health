import os
import glob
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_file(filepath):
    """파일의 정렬 로직 수정 - 카테고리 이름 정확 일치 우선"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 수정된 코드가 있으면 스킵
        if 'hasExactCategoryMatch' in content:
            print(f"  ⏭️  이미 수정된 코드가 있음, 스킵")
            return False
        
        # 1. 카테고리 이름 정확 일치 체크 추가
        old_category_score = '''                    // 1. 카테고리 이름과 제목 유사도 (최우선) - 가장 높은 점수
                    let maxCategorySimilarity = 0;
                    categoryNames.forEach(catName => {
                        const similarity = calculateSimilarity(catName, postTitle);
                        if (similarity > maxCategorySimilarity) {
                            maxCategorySimilarity = similarity;
                        }
                    });
                    // 카테고리 이름과 제목이 유사할수록 높은 점수 (최대 200점)
                    score += maxCategorySimilarity * 200;'''
        
        new_category_score = '''                    // 1. 카테고리 이름과 제목 유사도 (최우선) - 가장 높은 점수
                    let maxCategorySimilarity = 0;
                    let hasExactCategoryMatch = false;
                    categoryNames.forEach(catName => {
                        const catNameLower = catName.toLowerCase();
                        const catNameNoSpace = catNameLower.replace(/\\s+/g, '');
                        const postTitleNoSpace = postTitleLower.replace(/\\s+/g, '');
                        
                        // 카테고리 이름이 제목에 정확히 포함되어 있는지 확인 (공백 무시)
                        if (postTitleNoSpace.includes(catNameNoSpace) || catNameNoSpace.includes(postTitleNoSpace)) {
                            hasExactCategoryMatch = true;
                            maxCategorySimilarity = 1.0; // 정확히 일치하면 최고 점수
                        } else {
                            const similarity = calculateSimilarity(catName, postTitle);
                            if (similarity > maxCategorySimilarity) {
                                maxCategorySimilarity = similarity;
                            }
                        }
                    });
                    // 카테고리 이름이 정확히 포함되면 최고 점수, 아니면 유사도 점수
                    if (hasExactCategoryMatch) {
                        score += 300; // 정확히 일치하면 최고 점수 (300점)
                    } else {
                        score += maxCategorySimilarity * 200; // 유사도 점수 (최대 200점)
                    }'''
        
        if old_category_score in content:
            content = content.replace(old_category_score, new_category_score)
            print(f"  ✅ 카테고리 정확 일치 체크 추가")
        else:
            print(f"  ⚠️  카테고리 점수 계산 부분을 찾을 수 없음")
            return False
        
        # 2. return 문에 hasExactCategoryMatch 추가
        old_return = "return { post, score, categorySimilarity: maxCategorySimilarity, titleSimilarity };"
        new_return = "return { post, score, categorySimilarity: hasExactCategoryMatch ? 1.0 : maxCategorySimilarity, titleSimilarity, hasExactCategoryMatch };"
        
        if old_return in content:
            content = content.replace(old_return, new_return)
            print(f"  ✅ return 문 업데이트")
        
        # 3. 정렬 로직 수정
        old_sort = '''                // 정렬: 카테고리 유사도 > 제목 유사도 > 점수 순
                filteredPosts.sort((a, b) => {
                    // 1순위: 카테고리 이름과 제목 유사도
                    if (Math.abs(a.categorySimilarity - b.categorySimilarity) > 0.1) {
                        return b.categorySimilarity - a.categorySimilarity;
                    }
                    // 2순위: 페이지 제목과 제목 유사도
                    if (Math.abs(a.titleSimilarity - b.titleSimilarity) > 0.1) {
                        return b.titleSimilarity - a.titleSimilarity;
                    }
                    // 3순위: 총 점수
                    return b.score - a.score;
                });'''
        
        new_sort = '''                // 정렬: 카테고리 정확 일치 > 카테고리 유사도 > 제목 유사도 > 점수 순
                filteredPosts.sort((a, b) => {
                    // 1순위: 카테고리 이름이 정확히 포함된 글 우선
                    if (a.hasExactCategoryMatch !== b.hasExactCategoryMatch) {
                        return b.hasExactCategoryMatch ? 1 : -1;
                    }
                    // 2순위: 카테고리 이름과 제목 유사도
                    if (Math.abs(a.categorySimilarity - b.categorySimilarity) > 0.1) {
                        return b.categorySimilarity - a.categorySimilarity;
                    }
                    // 3순위: 페이지 제목과 제목 유사도
                    if (Math.abs(a.titleSimilarity - b.titleSimilarity) > 0.1) {
                        return b.titleSimilarity - a.titleSimilarity;
                    }
                    // 4순위: 총 점수
                    return b.score - a.score;
                });'''
        
        if old_sort in content:
            content = content.replace(old_sort, new_sort)
            print(f"  ✅ 정렬 로직 업데이트")
        else:
            print(f"  ⚠️  정렬 로직을 찾을 수 없음")
            return False
        
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
    print("🔧 카테고리 이름 정확 일치 우선 정렬 수정")
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
    print("  ✅ 카테고리 이름이 제목에 정확히 포함된 글 최우선 정렬")
    print("  ✅ 정확 일치 시 300점 부여 (기존 200점보다 높음)")
    print("  ✅ 정렬 기준: 정확 일치 > 유사도 > 제목 유사도 > 점수")

if __name__ == "__main__":
    main()

