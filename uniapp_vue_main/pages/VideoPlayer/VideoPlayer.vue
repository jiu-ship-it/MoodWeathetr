<template>
  <view class="page">
    <view class="header">
      <text class="title">{{ title || '视频播放' }}</text>
    </view>
    <view class="player-wrap">
      <video
        id="resourceVideo"
        class="video-player"
        :src="videoUrl"
        controls
        autoplay
        show-fullscreen-btn
        object-fit="contain"
        @error="onVideoError"
      ></video>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      title: '',
      videoUrl: ''
    };
  },
  onLoad(options) {
    this.title = decodeURIComponent((options && options.title) || '视频播放');
    this.videoUrl = decodeURIComponent((options && options.url) || '');
  },
  methods: {
    onVideoError() {
      uni.showToast({ title: '视频播放失败', icon: 'none' });
    }
  }
};
</script>

<style scoped lang="css">
.page {
  min-height: 100vh;
  background: #0f1722;
  padding: 24rpx;
  box-sizing: border-box;
}

.header {
  padding: 12rpx 4rpx 20rpx;
}

.title {
  color: #f5f8fb;
  font-size: 34rpx;
  font-weight: 600;
}

.player-wrap {
  border-radius: 16rpx;
  overflow: hidden;
  background: #000000;
}

.video-player {
  width: 100%;
  height: 420rpx;
}
</style>
