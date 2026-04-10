<template>
  <view class="page">
    <view class="hero-bg"></view>

    <view class="topbar">
      <text class="brand">MoodWeather</text>
    </view>

    <view class="intro-card">
      <text class="welcome-title">欢迎来到 MoodWeather</text>
      <text class="welcome-subtitle">在这里，每一句话都是温暖的拥抱，每一个字都充满了爱与关怀。</text>
    </view>

    <view class="feature-panel">
      <view class="feature-grid">
        <view class="feature-card" @click="ToNotebook">
          <text class="feature-emoji">📔</text>
          <text class="feature-label">笔记本</text>
        </view>
        <view class="feature-card" @click="ToTrend">
          <text class="feature-emoji">📊</text>
          <text class="feature-label">情绪趋势</text>
        </view>
        <view class="feature-card" @click="toEmotionFeed">
          <text class="feature-emoji">🎬</text>
          <text class="feature-label">情绪推送</text>
        </view>
        <view class="feature-card" @click="ToHistory">
          <text class="feature-emoji">🕘</text>
          <text class="feature-label">历史记录</text>
        </view>
      </view>
    </view>

    <BottomNav current="home" />
  </view>
</template>

<script>
  import BottomNav from '@/components/BottomNav.vue';

  export default {
    components: { BottomNav },
    data() {
      return {};
    },

    methods: {
		ToHistory(){
			uni.navigateTo({
				url:"/pages/History_Page/History_Page"
			})
		},
		ToNotebook(){
			uni.navigateTo({
				url:"/pages/MainNoteSet/MainNoteSet"
			})
		},
    ToTrend(){
      uni.navigateTo({
        url:"/pages/EmotionTrend/EmotionTrend"
      })
    },
    toEmotionFeed(){
      uni.navigateTo({
        url:"/pages/EmotionFeed/EmotionFeed"
      })
    },
	},
  };
</script>

<style scoped lang="css">
  .page {
    position: relative;
    min-height: 100vh;
    background-color: #ffffff;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163590829399947.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    background-attachment: fixed;
    width: 100%;
    padding-top: calc(18rpx + env(safe-area-inset-top));
    padding-bottom: 170rpx;
    box-sizing: border-box;
    overflow-y: auto;
    overflow-x: hidden;
  }

  .hero-bg {
    height: 24rpx;
  }

  .topbar {
    padding: 26rpx 32rpx;
    background-color: rgba(217, 217, 217, 0.7);
    backdrop-filter: blur(4px);
  }

  .brand {
    font-size: 56rpx;
    line-height: 1.2;
    color: #101820;
    font-weight: 700;
    text-align: center;
    display: block;
  }

  .intro-card {
    width: 70%;
    min-width: 460rpx;
    max-width: 620rpx;
    margin: 30rpx auto 20rpx;
    border-radius: 20rpx;
    background: rgba(255, 255, 255, 0.88);
    border: 1rpx solid rgba(0, 0, 0, 0.06);
    box-shadow: 0 10rpx 26rpx rgba(25, 39, 52, 0.08);
    padding: 22rpx 22rpx;
  }

  .welcome-title {
    font-size: 30rpx;
    line-height: 1.3;
    text-align: center;
    color: #1f2b38;
    font-weight: 600;
    display: block;
  }

  .welcome-subtitle {
    margin-top: 16rpx;
    display: block;
    font-size: 20rpx;
    line-height: 1.5;
    color: #4a5a6a;
    text-align: center;
  }

  .feature-panel {
    margin: 18rpx 52rpx 0;
    border-radius: 18rpx;
    background: transparent;
    padding: 0;
  }

  .feature-grid {
    display: grid;
    grid-template-columns: repeat(2, 28%);
    justify-content: space-between;
    row-gap: 12rpx;
  }

  .feature-card {
    height: 128rpx;
    border-radius: 14rpx;
    background: rgba(245, 247, 250, 0.82);
    border: 2rpx solid rgba(0, 0, 0, 0.18);
    box-shadow: 0 8rpx 16rpx rgba(25, 39, 52, 0.09);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .feature-emoji {
    font-size: 34rpx;
    line-height: 1.2;
  }

  .feature-label {
    margin-top: 6rpx;
    font-size: 24rpx;
    line-height: 1.3;
    color: #1c2a36;
    text-align: center;
    font-weight: 600;
  }

</style>