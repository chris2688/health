import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
ALL_FILES = [
    "index-v2.html",
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
    "food-main.html",
    "exercise-main.html",
    "lifestyle-main.html",
    "news-main.html",
    "food-피해야할과일.html",
    "food-질환별식단.html",
    "food-모르면독이된다.html",
    "exercise-질환별운동가이드.html",
    "exercise-운동팁.html",
    "lifestyle-생활습관.html",
    "lifestyle-생활습관바꾸기팁.html",
]


def restore_file(filepath):
    """파일을 깨끗한 상태로 복구"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 깨진 mobile-close-btn 스타일 수정
        content = re.sub(
            r'\.mobile-close-btn\s*\{[^}]*?ppx;[^}]*?\}',
            '''        .mobile-close-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 8px 12px;
            position: absolute;
            top: 15px;
            right: 15px;
            z-index: 1001;
            line-height: 1;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            transition: all 0.3s;
        }''',
            content,
            flags=re.DOTALL
        )
        
        # 2. 모든 중복된 모바일 미디어 쿼리 제거 (첫 번째만 남기기)
        # @media (max-width: 768px) 블록이 여러 개 있는 경우
        media_blocks = list(re.finditer(r'@media\s*\(max-width:\s*768px\)\s*\{', content))
        if len(media_blocks) > 1:
            # 첫 번째는 유지, 나머지는 제거
            # 하지만 다른 반응형 스타일도 있을 수 있으므로 주의
            # header-content가 포함된 첫 번째 미디어 쿼리만 유지
            first_header_media = None
            for i, match in enumerate(media_blocks):
                # 이 미디어 쿼리 블록의 내용 확인
                start = match.start()
                # 다음 미디어 쿼리 또는 </style>까지
                if i < len(media_blocks) - 1:
                    end = media_blocks[i+1].start()
                else:
                    end = content.find('</style>', start)
                    if end == -1:
                        end = len(content)
                
                block_content = content[start:end]
                if '.header-content' in block_content and first_header_media is None:
                    first_header_media = i
                    break
            
            # 첫 번째 header-content 미디어 쿼리 이후의 중복 제거
            if first_header_media is not None:
                # 첫 번째 미디어 쿼리 블록의 끝 찾기
                first_end = media_blocks[first_header_media].end()
                # 중괄호 매칭으로 블록 끝 찾기
                brace_count = 0
                first_block_end = first_end
                for i in range(first_end, len(content)):
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            first_block_end = i + 1
                            break
                
                # 두 번째 header-content 미디어 쿼리 찾아서 제거
                second_header_media = None
                for i in range(first_header_media + 1, len(media_blocks)):
                    start = media_blocks[i].start()
                    if i < len(media_blocks) - 1:
                        end = media_blocks[i+1].start()
                    else:
                        end = content.find('</style>', start)
                        if end == -1:
                            end = len(content)
                    
                    block_content = content[start:end]
                    if '.header-content' in block_content:
                        second_header_media = i
                        break
                
                if second_header_media is not None:
                    # 두 번째 미디어 쿼리 블록 제거
                    second_start = media_blocks[second_header_media].start()
                    brace_count = 0
                    second_block_end = second_start
                    for i in range(second_start, len(content)):
                        if content[i] == '{':
                            brace_count += 1
                        elif content[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                second_block_end = i + 1
                                break
                    
                    content = content[:second_start] + content[second_block_end:]
        
        # 3. 모바일 미디어 쿼리 정리 (애니메이션 제거, 단순하게)
        # 첫 번째 모바일 미디어 쿼리에서 애니메이션 관련 속성 제거
        content = re.sub(
            r'(@media\s*\(max-width:\s*768px\)[^}]*?\.main-nav\s*\{[^}]*?)opacity:\s*0;[^}]*?transform:\s*translateY\([^)]*\);[^}]*?transition:[^}]*?max-height:\s*0;[^}]*?overflow:\s*hidden;',
            r'\1',
            content,
            flags=re.DOTALL
        )
        
        content = re.sub(
            r'(@media\s*\(max-width:\s*768px\)[^}]*?\.main-nav\.active\s*\{[^}]*?)opacity:\s*1;[^}]*?transform:\s*translateY\([^)]*\);[^}]*?max-height:\s*\d+px;',
            r'\1',
            content,
            flags=re.DOTALL
        )
        
        content = re.sub(
            r'(@media\s*\(max-width:\s*768px\)[^}]*?\.nav-item\s*\{[^}]*?)opacity:\s*0;[^}]*?transform:\s*translateY\([^)]*\);[^}]*?transition:[^}]*?',
            r'\1',
            content,
            flags=re.DOTALL
        )
        
        content = re.sub(
            r'(@media\s*\(max-width:\s*768px\)[^}]*?\.main-nav\.active\s*\.nav-item\s*\{[^}]*?)opacity:\s*1;[^}]*?transform:\s*translateY\([^)]*\);',
            r'\1',
            content,
            flags=re.DOTALL
        )
        
        # 4. mobile-close-btn 관련 스타일 정리
        content = re.sub(
            r'(@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn\s*\{[^}]*?)display:\s*block;[^}]*?',
            r'\1display: none;',
            content,
            flags=re.DOTALL
        )
        
        content = re.sub(
            r'(@media\s*\(max-width:\s*768px\)[^}]*?\.main-nav\.active\s*~\s*\.mobile-close-btn[^}]*?)opacity:\s*1;[^}]*?transform:\s*scale\([^)]*\);',
            r'',
            content,
            flags=re.DOTALL
        )
        
        # 모바일 미디어 쿼리에 .main-nav.active .mobile-close-btn 추가
        if '@media (max-width: 768px)' in content and '.main-nav.active .mobile-close-btn' not in content:
            content = re.sub(
                r'(@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-menu-btn\s*\{[^}]*?display:\s*block;[^}]*?\})',
                r'''\1
            
            .main-nav.active .mobile-close-btn {
                display: block;
            }''',
                content,
                flags=re.DOTALL
            )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 복구 완료")
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
    print("🔧 파일을 깨끗한 상태로 복구")
    print("=" * 60)
    print("\n💡 복구 사항:")
    print("   1. 깨진 CSS 수정")
    print("   2. 중복된 미디어 쿼리 제거")
    print("   3. 애니메이션 제거 (단순 메뉴)")
    print("   4. X 버튼 스타일 정리\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if restore_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 복구 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

