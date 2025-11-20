import sys
import io
import random
import time
from datetime import datetime, timedelta
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.transport import Transport

# ---------------------------------------------------------
# ✅ 설정 변수 (여기를 꼭 수정하세요!)
# ---------------------------------------------------------
WP_URL = "https://health9988234.mycafe24.com/xmlrpc.php"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!" 

# 📅 날짜 설정 (이 기간 사이로 랜덤 배정됩니다)
START_DATE = datetime(2024, 1, 1)  # 시작일 (예: 2024년 1월 1일)
END_DATE = datetime(2025, 11, 18)  # 종료일 (예: 어제 날짜)

# ---------------------------------------------------------
# Cafe24 406 에러 우회용 커스텀 전송 객체
# ---------------------------------------------------------
class CustomTransport(Transport):
    def send_user_agent(self, connection):
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def get_random_date(start, end):
    """
    start와 end 사이의 랜덤한 날짜와 시간을 생성합니다.
    (시간은 08:00 ~ 23:00 사이로 자연스럽게 설정)
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    random_date = start + timedelta(seconds=random_second)
    
    # 시간대를 사람이 활동하는 시간(08시~23시)으로 강제 조정
    hour = random.randint(8, 23)
    minute = random.randint(0, 59)
    random_date = random_date.replace(hour=hour, minute=minute)
    
    return random_date

def update_all_posts_date():
    print("🚀 날짜 자동 분산 작업을 시작합니다...")
    print(f"📅 기간 설정: {START_DATE.strftime('%Y-%m-%d')} ~ {END_DATE.strftime('%Y-%m-%d')}")

    try:
        # 워드프레스 연결 (406 에러 방지 Transport 적용)
        client = Client(WP_URL, WP_USER, WP_PASSWORD, transport=CustomTransport())
        
        # 모든 글 가져오기 (발행된 글만)
        # 한 번에 최대 1000개까지 가져오도록 설정
        print("🔍 게시글 목록을 불러오는 중...")
        all_posts = client.call(posts.GetPosts({'number': 1000, 'post_status': 'publish'}))
        
        if not all_posts:
            print("⚠ 수정할 게시글이 없습니다.")
            return

        print(f"✅ 총 {len(all_posts)}개의 글을 발견했습니다. 수정을 시작합니다.\n")

        count = 0
        for post in all_posts:
            old_date = post.date
            new_date = get_random_date(START_DATE, END_DATE)
            
            # 수정할 내용 설정
            post.date = new_date
            
            # 서버에 전송 (업데이트)
            client.call(posts.EditPost(post.id, post))
            
            count += 1
            print(f"[{count}/{len(all_posts)}] '{post.title}'")
            print(f"   └ 📅 변경: {old_date.strftime('%Y-%m-%d')} -> {new_date.strftime('%Y-%m-%d %H:%M')}")
            
            # 서버 부하 방지를 위해 아주 살짝 대기
            time.sleep(0.2)

        print("\n✨ 모든 작업이 완료되었습니다! 워드프레스에서 확인해보세요.")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("팁: 앱 비밀번호가 맞는지, 플러그인 충돌은 없는지 확인하세요.")

if __name__ == "__main__":
    update_all_posts_date()