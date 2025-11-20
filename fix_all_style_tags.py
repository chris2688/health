import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
ALL_FILES = [
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


def fix_style_tag(filepath):
    """</style> 태그 추가"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # </style> 태그가 없고 </head>가 있으면 </style> 추가
        if '</style>' not in content and '</head>' in content:
            # </head> 앞에 </style> 추가
            content = re.sub(
                r'(\s+)(</head>)',
                r'\1    </style>\n\1\2',
                content,
                count=1
            )
        
        # 또는 미디어 쿼리 닫는 } 다음에 </style> 추가
        if '</style>' not in content:
            # 마지막 } 다음에 </style> 추가 (</head> 전에)
            content = re.sub(
                r'(\s+)(\n\s*</head>)',
                r'\1    </style>\2',
                content,
                count=1
            )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - </style> 태그 추가 완료")
            return True
        else:
            # 이미 </style> 태그가 있는지 확인
            if '</style>' in content:
                print(f"  ℹ️ {filepath} - </style> 태그 이미 있음")
            else:
                print(f"  ⚠️ {filepath} - </style> 태그 추가 실패")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 모든 파일 </style> 태그 추가")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   </style> 태그 추가 (없는 경우)\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_style_tag(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

