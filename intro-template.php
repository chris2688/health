<?php
/**
 * Template Name: 인트로 메인 페이지
 * Description: 메인 카드 그리드 페이지
 */

get_header(); ?>

<style>
    /* 페이지 타이틀 숨기기 */
    .entry-title, .page-title, .entry-header {
        display: none !important;
    }
    
    /* 메인 콘텐츠 영역 */
    .site-main {
        padding: 0 !important;
    }
    
    .health-card-container {
        padding: 60px 20px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 70vh;
    }
    
    .health-cards-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 30px;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .health-card {
        position: relative;
        padding: 40px 30px;
        border-radius: 24px;
        background: linear-gradient(135deg, var(--card-color-1) 0%, var(--card-color-2) 100%);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        overflow: hidden;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-decoration: none;
    }
    
    .health-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.25);
    }
    
    .health-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 150px;
        height: 150px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        transform: translate(50%, -50%);
    }
    
    .health-card-icon {
        font-size: 48px;
        margin-bottom: 20px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
        position: relative;
        z-index: 1;
    }
    
    .health-card h3 {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 12px 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: relative;
        z-index: 1;
    }
    
    .health-card p {
        font-size: 15px;
        color: rgba(255,255,255,0.9);
        margin: 0;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    .section-title {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .section-title .subtitle {
        font-size: 16px;
        font-weight: 600;
        color: #4A90E2;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }
    
    .section-title h2 {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 50px 0;
    }
    
    @media (max-width: 768px) {
        .health-cards-grid {
            grid-template-columns: 1fr;
            gap: 20px;
        }
        .section-title h2 {
            font-size: 32px;
        }
    }
</style>

<div class="health-card-container">
    <div class="section-title">
        <p class="subtitle">9988 건강 연구소 핵심 가이드</p>
        <h2>중년 건강의 모든 것, 분야별로 찾아보세요</h2>
    </div>
    
    <div class="health-cards-grid">
        <a href="<?php echo home_url('/category/질환별-정보/심혈관-질환/'); ?>" class="health-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;">
            <div class="health-card-icon">❤️</div>
            <h3>심혈관 질환</h3>
            <p>고혈압, 심근경색, 동맥경화</p>
        </a>
        
        <a href="<?php echo home_url('/category/질환별-정보/당뇨병/'); ?>" class="health-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
            <div class="health-card-icon">💉</div>
            <h3>당뇨병</h3>
            <p>혈당관리, 공복혈당, 합병증</p>
        </a>
        
        <a href="<?php echo home_url('/category/질환별-정보/관절-근골격계-질환/'); ?>" class="health-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">
            <div class="health-card-icon">🦴</div>
            <h3>관절/근골격계 질환</h3>
            <p>관절염, 허리디스크, 골다공증</p>
        </a>
        
        <a href="<?php echo home_url('/category/질환별-정보/호르몬-내분비-질환/'); ?>" class="health-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
            <div class="health-card-icon">🌡️</div>
            <h3>호르몬/내분비 질환</h3>
            <p>갱년기, 갑상선, 대사증후군</p>
        </a>
        
        <a href="<?php echo home_url('/category/질환별-정보/정신-건강-신경계/'); ?>" class="health-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
            <div class="health-card-icon">🧠</div>
            <h3>정신 건강/신경계</h3>
            <p>우울증, 치매, 수면장애</p>
        </a>
        
        <a href="<?php echo home_url('/category/질환별-정보/소화기-질환/'); ?>" class="health-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;">
            <div class="health-card-icon">🍽️</div>
            <h3>소화기 질환</h3>
            <p>위염, 지방간, 역류성 식도염</p>
        </a>
        
        <a href="<?php echo home_url('/category/질환별-정보/안과-치과-기타/'); ?>" class="health-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;">
            <div class="health-card-icon">👁️</div>
            <h3>안과/치과/기타</h3>
            <p>백내장, 녹내장, 치주질환</p>
        </a>
    </div>
</div>

<?php get_footer(); ?>

