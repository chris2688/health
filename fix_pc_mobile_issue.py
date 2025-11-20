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


def fix_pc_mobile_issue(filepath):
    """PC에서 모바일 스타일이 적용되는 문제 수정"""
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
        
        # 2. 미디어 쿼리 밖에 있는 모바일 전용 스타일 제거
        # 패턴: 미디어 쿼리 닫힌 후, </style> 전에 있는 .health-cards-grid { grid-template-columns: 1fr; }
        
        # 미디어 쿼리 위치 찾기
        media_match = re.search(r'@media\s*\(max-width:\s*768px\)\s*\{', content)
        if media_match:
            # 미디어 쿼리 블록의 끝 찾기
            brace_count = 0
            media_start = media_match.start()
            media_end = media_start
            
            for i in range(media_start, len(content)):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        media_end = i + 1
                        break
            
            # 미디어 쿼리 밖의 내용 확인
            after_media = content[media_end:]
            
            # </style> 전까지의 내용
            style_end = after_media.find('</style>')
            if style_end != -1:
                before_style_end = after_media[:style_end]
                
                # 미디어 쿼리 밖에 있는 모바일 전용 스타일 제거
                # .health-cards-grid { grid-template-columns: 1fr; } 같은 것
                patterns_to_remove = [
                    r'\.health-cards-grid\s*\{\s*grid-template-columns:\s*1fr;\s*gap:\s*\d+px;\s*\}',
                    r'\.section-title\s+h2\s*\{\s*font-size:\s*32px;\s*\}',
                    r'\.main-icon\s*\{\s*font-size:\s*56px;\s*\}',
                    r'\.back-button\s*\{\s*margin-left:\s*20px;\s*\}',
                ]
                
                for pattern in patterns_to_remove:
                    # 미디어 쿼리 안에 있는지 확인
                    media_content = content[media_start:media_end]
                    if pattern.replace(r'\s*', ' ') not in media_content:
                        # 미디어 쿼리 밖에 있으면 제거
                        before_style_end = re.sub(pattern, '', before_style_end, flags=re.MULTILINE)
                
                # 수정된 내용으로 교체
                content = content[:media_end] + before_style_end + after_media[style_end:]
        
        # 3. 미디어 쿼리 안에 필요한 스타일 추가 (없으면)
        if '@media (max-width: 768px)' in content:
            media_start = content.find('@media (max-width: 768px)')
            brace_count = 0
            media_end = media_start
            
            for i in range(media_start, len(content)):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        media_end = i + 1
                        break
            
            media_content = content[media_start:media_end]
            
            # .mobile-menu-btn { display: block; } 추가 (없으면)
            if '.mobile-menu-btn' not in media_content or 'display: block' not in media_content.split('.mobile-menu-btn')[1].split('}')[0]:
                # .nav-item 다음에 추가
                if '.nav-item' in media_content:
                    insert_pos = media_content.rfind('.nav-item')
                    next_brace = media_content.find('}', insert_pos)
                    if next_brace != -1:
                        new_content = (
                            media_content[:next_brace] +
                            '\n            \n            .mobile-menu-btn {\n                display: block;\n            }\n            \n            .main-nav.active .mobile-close-btn {\n                display: block;\n            }' +
                            media_content[next_brace:]
                        )
                        content = content[:media_start] + new_content + content[media_end:]
                        media_end = content.find('}', media_start) + 1
            
            # .health-cards-grid 추가 (없으면)
            media_content = content[media_start:media_end]
            if '.health-cards-grid' not in media_content:
                # .main-nav.active .mobile-close-btn 다음에 추가
                if '.main-nav.active .mobile-close-btn' in media_content:
                    insert_pos = media_content.rfind('.main-nav.active .mobile-close-btn')
                    next_brace = media_content.find('}', insert_pos)
                    if next_brace != -1:
                        new_content = (
                            media_content[:next_brace] +
                            '\n            \n            .health-cards-grid {\n                grid-template-columns: 1fr;\n                gap: 20px;\n            }' +
                            media_content[next_brace:]
                        )
                        content = content[:media_start] + new_content + content[media_end:]
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - PC/모바일 문제 수정 완료")
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
    print("🔧 PC에서 모바일 스타일 적용 문제 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 미디어 쿼리 밖의 모바일 스타일 제거")
    print("   2. 미디어 쿼리 안에 필요한 스타일 추가\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_pc_mobile_issue(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

