import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
ALL_FILES = [
    "food-main.html",
    "exercise-main.html",
    "lifestyle-main.html",
    "news-main.html",
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
    "food-피해야할과일.html",
    "food-질환별식단.html",
    "food-모르면독이된다.html",
    "exercise-질환별운동가이드.html",
    "exercise-운동팁.html",
    "lifestyle-생활습관.html",
    "lifestyle-생활습관바꾸기팁.html",
]


def fix_media_queries(filepath):
    """미디어 쿼리 구조 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 빈 CSS 블록 제거
        content = re.sub(
            r'\.main-nav\.active\s*\{\s*\}',
            '',
            content,
            flags=re.MULTILINE
        )
        
        # 2. 미디어 쿼리 구조 확인 및 수정
        # 미디어 쿼리 안에 있는 스타일이 밖으로 나온 경우 수정
        if '@media (max-width: 768px)' in content:
            # 미디어 쿼리 시작 위치 찾기
            media_start = content.find('@media (max-width: 768px)')
            
            if media_start != -1:
                # 미디어 쿼리 블록의 끝 찾기
                brace_count = 0
                media_end = media_start
                in_media = False
                
                for i in range(media_start, len(content)):
                    if content[i] == '{':
                        brace_count += 1
                        in_media = True
                    elif content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0 and in_media:
                            media_end = i + 1
                            break
                
                # 미디어 쿼리 내용 확인
                media_content = content[media_start:media_end]
                
                # 미디어 쿼리 안에 .health-cards-grid가 있는지 확인
                # 만약 미디어 쿼리 밖에 .health-cards-grid { grid-template-columns: 1fr; }가 있으면
                # 그것은 미디어 쿼리 안에 있어야 함
                
                # 미디어 쿼리 밖의 잘못된 스타일 찾기
                after_media = content[media_end:]
                
                # 미디어 쿼리 밖에 있는 .health-cards-grid { grid-template-columns: 1fr; } 찾기
                pattern = r'(</style>|</head>)'
                style_end_match = re.search(pattern, after_media)
                
                if style_end_match:
                    before_style_end = after_media[:style_end_match.start()]
                    
                    # .health-cards-grid { grid-template-columns: 1fr; } 패턴 찾기
                    wrong_grid = re.search(
                        r'\.health-cards-grid\s*\{\s*grid-template-columns:\s*1fr;\s*gap:\s*\d+px;\s*\}',
                        before_style_end
                    )
                    
                    if wrong_grid and '.health-cards-grid' not in media_content:
                        # 미디어 쿼리 안에 추가
                        # .main-nav.active .mobile-close-btn 다음에 추가
                        if '.main-nav.active .mobile-close-btn' in media_content:
                            insert_pos = media_content.rfind('.main-nav.active .mobile-close-btn')
                            next_brace = media_content.find('}', insert_pos)
                            if next_brace != -1:
                                new_media_content = (
                                    media_content[:next_brace] +
                                    '\n            \n            .health-cards-grid {\n                grid-template-columns: 1fr;\n                gap: 20px;\n            }' +
                                    media_content[next_brace:]
                                )
                                content = content[:media_start] + new_media_content + content[media_end:]
                                media_end = content.find('}', media_start) + 1
                                
                                # 잘못된 위치의 스타일 제거
                                wrong_start = media_end + wrong_grid.start()
                                wrong_end = media_end + wrong_grid.end()
                                content = content[:wrong_start] + content[wrong_end:]
        
        # 3. 미디어 쿼리 밖에 있는 모바일 전용 스타일 제거
        # .health-cards-grid { grid-template-columns: 1fr; } 같은 것
        # 단, 미디어 쿼리 안에 있는 것은 제외
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 미디어 쿼리 수정 완료")
            return True
        else:
            print(f"  ℹ️ {filepath} - 변경사항 없음")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 모든 파일 미디어 쿼리 구조 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 빈 CSS 블록 제거")
    print("   2. 미디어 쿼리 구조 정리")
    print("   3. 잘못된 위치의 스타일 수정\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_media_queries(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

