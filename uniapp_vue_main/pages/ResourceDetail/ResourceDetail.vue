<template>
  <view class="page">
    <view class="topbar">
      <view class="back-btn" @click="goBack">
        <text class="back-text">返回</text>
      </view>
      <text class="top-title">资源详情</text>
    </view>

    <view class="article-card">
      <text class="badge" v-if="payload.badge">{{ payload.badge }}</text>
      <text class="title">{{ payload.title || '未命名资源' }}</text>
      <text class="desc" v-if="payload.desc">{{ payload.desc }}</text>

      <image v-if="payload.cover" class="cover" :src="payload.cover" mode="widthFix" />

      <text class="content">{{ payload.detail || payload.desc || '暂无详情内容' }}</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      payload: {
        title: '',
        desc: '',
        detail: '',
        cover: '',
        badge: ''
      }
    };
  },
  onShow() {
    const data = uni.getStorageSync('resource_detail_payload');
    if (data && typeof data === 'object') {
      this.payload = {
        title: data.title || '',
        desc: data.desc || '',
        detail: data.detail || '',
        cover: data.cover || '',
        badge: data.badge || ''
      };
      return;
    }
    this.payload = {
      title: '资源详情',
      desc: '',
      detail: '未获取到资源内容，请返回重试。',
      cover: '',
      badge: ''
    };
  },
  methods: {
    goBack() {
      uni.navigateBack({ delta: 1 });
    }
  }
};
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f6f9fc 0%, #eef3f8 100%);
  padding-bottom: 40rpx;
}

.topbar {
  padding: calc(16rpx + env(safe-area-inset-top)) 24rpx 16rpx;
  display: flex;
  align-items: center;
  gap: 18rpx;
  background: #ffffff;
  border-bottom: 1rpx solid #e4ebf2;
}

.back-btn {
  padding: 10rpx 16rpx;
  background: #1f3f5b;
  border-radius: 10rpx;
}

.back-text {
  color: #ffffff;
  font-size: 24rpx;
}

.top-title {
  font-size: 34rpx;
  font-weight: 700;
  color: #1f2a37;
}

.article-card {
  margin: 18rpx 20rpx 0;
  padding: 20rpx;
  background: #ffffff;
  border-radius: 18rpx;
  border: 1rpx solid #dde7f1;
  box-shadow: 0 8rpx 20rpx rgba(31, 42, 55, 0.07);
}

.badge {
  display: inline-flex;
  padding: 4rpx 12rpx;
  border-radius: 999rpx;
  background: #1f4d77;
  color: #ffffff;
  font-size: 20rpx;
}

.title {
  display: block;
  margin-top: 10rpx;
  font-size: 36rpx;
  line-height: 1.3;
  color: #1d2e3f;
  font-weight: 700;
}

.desc {
  display: block;
  margin-top: 8rpx;
  font-size: 24rpx;
  line-height: 1.6;
  color: #4f6478;
}

.cover {
  width: 100%;
  margin-top: 14rpx;
  border-radius: 14rpx;
  background: #edf2f7;
}

.content {
  display: block;
  margin-top: 14rpx;
  font-size: 27rpx;
  line-height: 1.8;
  color: #2a3f54;
}
</style>
