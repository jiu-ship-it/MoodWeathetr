<template>
  <view class="page">
    <view class="hero">
      <text class="hero-title">情绪资源中心</text>
      <text class="hero-subtitle">系统会按分析结果自动匹配资源分组</text>
      <view class="hero-tag" v-if="recommendedGroup.name">
        <text class="hero-tag-text">当前推荐：{{ recommendedGroup.name }} · {{ recommendedGroup.audience }}</text>
      </view>
    </view>

    <scroll-view class="group-strip" scroll-x enable-flex show-scrollbar="false">
      <view
        class="group-chip"
        :class="{ active: activeTag === item.emotion_tag }"
        v-for="item in groupCards"
        :key="item.emotion_tag"
        @click="selectGroup(item.emotion_tag)"
      >
        <text class="chip-title">{{ item.group_name }}</text>
        <text class="chip-meta">{{ item.audience || '情绪人群推荐' }}</text>
      </view>
    </scroll-view>

    <view class="panel" v-if="activeGroup">
      <view class="panel-head">
        <text class="panel-title">{{ activeGroup.group_name }}</text>
        <text class="panel-desc">{{ activeGroup.description }}</text>
      </view>

      <view class="section">
        <text class="section-title">图文资源</text>
        <view class="card-grid">
          <view class="resource-card" v-for="(item, idx) in activeGroup.imageText" :key="`img-${idx}`">
            <text class="corner-badge">图文</text>
            <image v-if="item.cover" class="cover" :src="item.cover" mode="aspectFill" />
            <text class="card-title">{{ item.title }}</text>
            <text class="card-desc">{{ item.desc }}</text>
            <view class="ghost-btn" @click="openResourceDetail(item)"><text class="ghost-btn-text">查看详情</text></view>
          </view>
        </view>
        <text class="empty" v-if="!activeGroup.imageText.length">暂无图文资源</text>
      </view>

      <view class="section">
        <text class="section-title">视频资源</text>
        <scroll-view class="resource-scroll" scroll-x enable-flex show-scrollbar="false">
          <view class="resource-row">
            <view class="h-card" v-for="(item, idx) in activeGroup.videos" :key="`video-${idx}`">
              <text class="corner-badge">视频</text>
              <image v-if="item.cover" class="video-cover" :src="item.cover" mode="aspectFill" />
              <view>
                <text class="card-title">{{ item.title }}</text>
                <text class="card-desc">{{ item.desc }}</text>
              </view>
              <view class="solid-btn" @click="openVideo(item)"><text class="solid-btn-text">播放</text></view>
            </view>
          </view>
        </scroll-view>
        <text class="empty" v-if="!activeGroup.videos.length">暂无视频资源</text>
      </view>

      <view class="section">
        <text class="section-title">音乐资源</text>
        <scroll-view class="resource-scroll" scroll-x enable-flex show-scrollbar="false">
          <view class="resource-row">
            <view class="h-card" v-for="(item, idx) in activeGroup.music" :key="`music-${idx}`">
              <text class="corner-badge">音乐</text>
              <view>
                <text class="card-title">{{ item.name }}</text>
                <text class="card-desc">{{ item.author }}</text>
              </view>
              <view class="solid-btn light" @click="openMusic(item)"><text class="solid-btn-text dark">播放</text></view>
            </view>
          </view>
        </scroll-view>
        <text class="empty" v-if="!activeGroup.music.length">暂无音乐资源</text>
      </view>
    </view>

    <view class="error" v-if="errorText">{{ errorText }}</view>

    <BottomNav current="feed" />
  </view>
</template>

<script>
import BottomNav from '@/components/BottomNav.vue';
import { apiRequestUnified } from '@/common/request.js';
import { parseAnalysisPayload, normalizePredictionFromAnalysis } from '@/common/emotionAnalysis.js';

export default {
  components: { BottomNav },
  data() {
    return {
      activeTag: '',
      groups: {},
      recommendedTag: '',
      errorText: ''
    };
  },
  computed: {
    groupCards() {
      return ['1', '2', '3']
        .map((k) => this.groups[k])
        .filter(Boolean);
    },
    activeGroup() {
      return this.groups[this.activeTag] || null;
    },
    recommendedGroup() {
      return this.groups[this.recommendedTag] || {};
    }
  },
  onShow() {
    this.loadBundle();
  },
  methods: {
    async loadBundle() {
      this.errorText = '';
      const emotionTag = await this.resolveRecentEmotionTag();
      try {
        const res = await apiRequestUnified({
          url: '/api/resource-bundles',
          method: 'GET',
          data: { emotion: emotionTag || '' }
        });
        if (!res.ok || !res.data) {
          this.errorText = res.message || '资源加载失败';
          return;
        }
        const payload = res.data;
        this.groups = payload.groups || {};
        this.recommendedTag = payload.recommended_emotion_tag || emotionTag || '2';
        this.activeTag = this.recommendedTag;
      } catch (e) {
        this.errorText = '网络异常，资源加载失败';
      }
    },
    async resolveRecentEmotionTag() {
      const token = uni.getStorageSync('token');
      if (!token) return '';
      try {
        const res = await apiRequestUnified({
          url: '/api/notes',
          method: 'GET',
          header: { Authorization: `Bearer ${token}` }
        });
        const list = Array.isArray(res.data) ? res.data : [];
        const sorted = [...list].sort((a, b) => {
          const ta = Date.parse(a.analyzed_at || a.created_at || '');
          const tb = Date.parse(b.analyzed_at || b.created_at || '');
          return (Number.isNaN(tb) ? 0 : tb) - (Number.isNaN(ta) ? 0 : ta);
        });
        const recent = sorted.find((n) => !!n.analysis_result);
        if (!recent) return '';
        const parsed = parseAnalysisPayload(recent.analysis_result);
        return String(normalizePredictionFromAnalysis(parsed) || '');
      } catch (e) {
        return '';
      }
    },
    selectGroup(tag) {
      this.activeTag = String(tag || '');
    },
    openResourceDetail(item) {
      if (!item) {
        return;
      }
      uni.setStorageSync('resource_detail_payload', {
        title: item.title || '资源详情',
        desc: item.desc || '',
        detail: item.detail || item.desc || '',
        cover: item.cover || '',
        badge: '图文'
      });
      uni.navigateTo({ url: '/pages/ResourceDetail/ResourceDetail' });
    },
    openVideo(item) {
      const rawUrl = String((item && item.url) || '');
      if (!rawUrl) {
        uni.showToast({ title: '视频地址为空', icon: 'none' });
        return;
      }
      const title = encodeURIComponent(item.title || '视频播放');
      const url = encodeURIComponent(rawUrl);
      uni.navigateTo({ url: `/pages/VideoPlayer/VideoPlayer?title=${title}&url=${url}` });
    },
    openMusic(item) {
      if (!item || !item.url) {
        uni.showToast({ title: '音乐地址为空', icon: 'none' });
        return;
      }
      uni.navigateTo({ url: '/pages/Music/Music' });
    }
  }
};
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: linear-gradient(180deg, #fdf7f2 0%, #f5efe8 48%, #f0e9e0 100%);
  padding: 24rpx 28rpx 170rpx;
}

.hero {
  background: linear-gradient(140deg, #1f3a36 0%, #2b4e48 65%, #355f56 100%);
  border-radius: 24rpx;
  padding: 28rpx;
  box-shadow: 0 14rpx 36rpx rgba(20, 34, 30, 0.24);
}

.hero-title {
  color: #f8f4ec;
  font-size: 40rpx;
  font-weight: 700;
}

.hero-subtitle {
  margin-top: 8rpx;
  color: rgba(248, 244, 236, 0.82);
  font-size: 24rpx;
}

.hero-tag {
  margin-top: 18rpx;
  display: inline-flex;
  background: rgba(248, 244, 236, 0.18);
  border: 1rpx solid rgba(248, 244, 236, 0.28);
  border-radius: 999rpx;
  padding: 10rpx 18rpx;
}

.hero-tag-text {
  color: #f8f4ec;
  font-size: 22rpx;
}

.group-strip {
  margin-top: 20rpx;
  white-space: nowrap;
}

.group-chip {
  display: inline-block;
  vertical-align: top;
  width: 320rpx;
  margin-right: 12rpx;
  background: #fffdf8;
  border-radius: 18rpx;
  border: 2rpx solid #e8ddd0;
  padding: 16rpx 18rpx;
}

.group-chip.active {
  border-color: #2b4e48;
  box-shadow: 0 8rpx 22rpx rgba(43, 78, 72, 0.18);
}

.chip-title {
  color: #203430;
  font-size: 28rpx;
  font-weight: 700;
}

.chip-meta {
  margin-top: 6rpx;
  color: #5f706a;
  font-size: 22rpx;
}

.panel {
  margin-top: 18rpx;
  border-radius: 20rpx;
  background: #fffdf8;
  border: 1rpx solid #efe4d7;
  padding: 20rpx;
}

.panel-title {
  font-size: 30rpx;
  color: #1e2f2c;
  font-weight: 700;
}

.panel-desc {
  margin-top: 8rpx;
  font-size: 23rpx;
  color: #62716d;
}

.section {
  margin-top: 18rpx;
}

.section-title {
  font-size: 26rpx;
  font-weight: 600;
  color: #2d3f3b;
}

.card-grid {
  margin-top: 12rpx;
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 12rpx;
}

.resource-card,
.row-card,
.h-card {
  position: relative;
  border-radius: 16rpx;
  background: #ffffff;
  border: 1rpx solid #ebe2d6;
  padding: 16rpx;
}

.row-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
}

.resource-scroll {
  margin-top: 12rpx;
}

.resource-row {
  display: flex;
  gap: 12rpx;
}

.h-card {
  width: 390rpx;
}

.corner-badge {
  position: absolute;
  right: 14rpx;
  top: 12rpx;
  padding: 4rpx 12rpx;
  border-radius: 999rpx;
  background: #2b4e48;
  color: #f5f8f7;
  font-size: 18rpx;
}

.cover {
  width: 100%;
  height: 220rpx;
  border-radius: 12rpx;
  margin-bottom: 10rpx;
  background: #f4eee6;
}

.video-cover {
  width: 100%;
  height: 190rpx;
  border-radius: 10rpx;
  margin-bottom: 10rpx;
  background: #ebe4d9;
}

.card-title {
  display: block;
  color: #243834;
  font-size: 26rpx;
  font-weight: 600;
}

.card-desc {
  display: block;
  margin-top: 6rpx;
  color: #667671;
  font-size: 22rpx;
  line-height: 1.5;
}

.ghost-btn,
.solid-btn {
  margin-top: 10rpx;
  border-radius: 999rpx;
  padding: 10rpx 18rpx;
  align-self: flex-start;
}

.ghost-btn {
  border: 1rpx solid #2b4e48;
  background: #f7faf9;
}

.ghost-btn-text {
  color: #2b4e48;
  font-size: 22rpx;
}


.solid-btn {
  background: #2b4e48;
}

.solid-btn.light {
  background: #e8f0ed;
}

.solid-btn-text {
  color: #ffffff;
  font-size: 22rpx;
}

.solid-btn-text.dark {
  color: #284640;
}

.list-col {
  margin-top: 12rpx;
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

@media (max-width: 420px) {
  .card-grid {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}

.empty {
  margin-top: 10rpx;
  color: #7d8b87;
  font-size: 22rpx;
}

.error {
  margin-top: 16rpx;
  color: #b42318;
  font-size: 24rpx;
  text-align: center;
}
</style>
