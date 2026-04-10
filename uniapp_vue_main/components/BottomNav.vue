<template>
  <view class="bottom-nav-wrap">
    <view class="bottom-nav">
      <view class="nav-item" :class="{ active: current === 'home' }" @click="goHome">
        <image class="nav-icon" src="/static/image/home.png" />
      </view>
      <view class="nav-item" :class="{ active: current === 'setting' }" @click="goSetting">
        <image class="nav-icon" src="/static/image/setting.png" />
      </view>
      <view class="nav-item" :class="{ active: current === 'music' }" @click="goMusic">
        <image class="nav-icon" src="/static/image/music.png" />
      </view>
    </view>
  </view>
</template>

<script>
export default {
  props: {
    current: {
      type: String,
      default: 'home'
    }
  },
  methods: {
    switchTo(key, url) {
      if (this.current === key) {
        return;
      }
      uni.redirectTo({ url });
    },
    goHome() {
      this.switchTo('home', '/pages/Main_Page/Main_Page');
    },
    goSetting() {
      this.switchTo('setting', '/pages/Setting/Setting');
    },
    goMusic() {
      this.switchTo('music', '/pages/Music/Music');
    }
  }
};
</script>

<style scoped>
.bottom-nav-wrap {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 60;
  padding: 10rpx 0 calc(10rpx + env(safe-area-inset-bottom));
  background-image: linear-gradient(180.9deg, #575757bf 4.2%, #bdbdbdbf 96.2%);
  box-shadow: 0 -6rpx 18rpx rgba(0, 0, 0, 0.12);
}

.bottom-nav {
  display: flex;
  justify-content: center;
  gap: 26rpx;
  margin: 0 32rpx;
}

.nav-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 132rpx;
  height: 102rpx;
  border-radius: 14rpx;
  border: 2rpx solid rgba(0, 0, 0, 0.85);
  background: rgba(217, 217, 217, 0.55);
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.88);
  transform: translateY(-2rpx);
}

.nav-icon {
  width: 52rpx;
  height: 52rpx;
}
</style>
