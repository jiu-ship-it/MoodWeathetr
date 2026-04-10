<template>
  <view class="page">
    <view class="topbar">
      <view class="back-btn" @click="goBack"><text class="back-text">返回</text></view>
      <text class="title">情绪推送</text>
    </view>

    <view class="summary-card">
      <text class="summary-title">当前推荐依据：{{ currentEmotion }}</text>
      <text class="summary-text">根据你最近一次分析结果，系统为你推送更匹配的图文和视频内容。</text>
    </view>

    <view class="panel">
      <text class="panel-title">图文推荐</text>
      <view class="feed-list">
        <view class="feed-card" v-for="(item, idx) in imageTextFeeds" :key="idx">
          <image v-if="item.cover" class="feed-cover" :src="item.cover" mode="aspectFill" />
          <view class="feed-head">
            <text class="feed-emoji">🖼️</text>
            <text class="feed-title">{{ item.title }}</text>
          </view>
          <text class="feed-desc">{{ item.desc }}</text>
          <text class="feed-detail" v-if="item.expanded">{{ item.detail || item.desc || '暂无详情' }}</text>
          <view class="action-btn" @click="toggleArticle(idx)"><text class="action-text">{{ item.expanded ? '收起内容' : '展开全文' }}</text></view>
        </view>
      </view>
      <text class="empty-tip" v-if="!imageTextFeeds.length">暂无图文推荐</text>
    </view>

    <view class="panel">
      <text class="panel-title">视频推荐</text>
      <view class="feed-list">
        <view class="feed-card" v-for="(item, idx) in videoFeeds" :key="idx">
          <view class="feed-head">
            <text class="feed-emoji">🎬</text>
            <text class="feed-title">{{ item.title }}</text>
          </view>
          <text class="feed-desc">{{ item.desc }}</text>
          <view class="action-btn primary" @click="openVideo(item)"><text class="action-text primary-text">直接打开视频</text></view>
        </view>
      </view>
      <text class="empty-tip" v-if="!videoFeeds.length">暂无视频推荐</text>
    </view>

    <BottomNav current="feed" />
  </view>
</template>

<script>
  import { BASE_URL } from '@/common/config.js';
  import BottomNav from '@/components/BottomNav.vue';

  export default {
    components: { BottomNav },
    data() {
      return {
        currentEmotion: '未分析',
        imageTextFeeds: [],
        videoFeeds: []
      };
    },
    onShow() {
      this.loadRecentEmotion();
    },
    methods: {
      goBack() {
        const pages = getCurrentPages();
        if (pages.length > 1) {
          uni.navigateBack({ delta: 1 });
          return;
        }
        uni.reLaunch({ url: '/pages/Main_Page/Main_Page' });
      },
      parseAnalysis(payload) {
        if (!payload) return null;
        if (typeof payload === 'string') {
          try {
            return JSON.parse(payload);
          } catch (e) {
            return null;
          }
        }
        return payload;
      },
      normalizePrediction(analysis) {
        const probs = analysis && analysis.probabilities && analysis.probabilities.M;
        const classCount = Array.isArray(probs) && probs.length ? probs.length : 3;
        const p = Number(analysis && analysis.prediction);
        if (!Number.isNaN(p)) {
          if (p >= 1 && p <= classCount) return p;
          if (p >= 0 && p < classCount) return p + 1;
        }
        if (Array.isArray(probs) && probs.length) {
          let maxIdx = 0;
          for (let i = 1; i < probs.length; i += 1) {
            if (Number(probs[i]) > Number(probs[maxIdx])) {
              maxIdx = i;
            }
          }
          return maxIdx + 1;
        }
        return 0;
      },
      mapEmotion(indexValue) {
        const normalized = Number(indexValue);
        if (normalized === 1) return '低落预警';
        if (normalized === 2) return '平稳';
        if (normalized === 3) return '高兴';
        return '未分析';
      },
      loadRecentEmotion() {
        const token = uni.getStorageSync('token');
        uni.request({
          url: `${BASE_URL}/api/notes`,
          header: { Authorization: `Bearer ${token}` },
          success: (res) => {
            if (!(res.statusCode === 200 && Array.isArray(res.data))) {
              this.applyFeeds('未分析', '');
              return;
            }
            const sorted = [...res.data].sort((a, b) => {
              const ta = Date.parse(a.analyzed_at || a.created_at || '');
              const tb = Date.parse(b.analyzed_at || b.created_at || '');
              return (Number.isNaN(tb) ? 0 : tb) - (Number.isNaN(ta) ? 0 : ta);
            });
            const recentAnalyzed = sorted.find((n) => !!n.analysis_result);
            if (!recentAnalyzed) {
              this.applyFeeds('未分析', '');
              return;
            }
            const analysis = this.parseAnalysis(recentAnalyzed.analysis_result);
            const prediction = this.normalizePrediction(analysis);
            const emotion = this.mapEmotion(prediction);
            this.applyFeeds(emotion, String(prediction || ''));
          },
          fail: () => {
            this.applyFeeds('未分析', '');
          }
        });
      },
      applyFeeds(emotion, emotionTag) {
        this.currentEmotion = emotion;
        const fallbackMap = {
          '平稳': {
            imageText: [
              { title: '稳定情绪维护法', desc: '通过固定作息和轻量复盘，保持心态稳定。', detail: '建议你每天固定一个 10 分钟复盘时间，记录今天最稳的一刻和触发原因。' },
              { title: '专注与放松平衡', desc: '稳定状态下避免过劳，保持节奏更重要。', detail: '可以采用 25-5 的节奏管理，让专注与休息穿插进行。' }
            ],
            videos: [
              { title: '呼吸放松训练（10分钟）', desc: '适合平稳状态下的深度放松。', url: 'https://www.bilibili.com/video/BV1xJ411k7V7' }
            ]
          },
          '高兴': {
            imageText: [
              { title: '积极状态放大术', desc: '趁状态好，把可执行目标拆小并立刻推进。', detail: '把今天最重要任务拆成三步，先完成第一步，形成动量。' },
              { title: '避免高能透支', desc: '在兴奋时段保留精力，防止后续波动。', detail: '每 60-90 分钟主动休息 5 分钟，保证状态可持续。' }
            ],
            videos: [
              { title: '高效行动管理视频', desc: '适合积极状态下的执行力提升。', url: 'https://www.bilibili.com/video/BV1V4411Z7VA' }
            ]
          },
          '低落预警': {
            imageText: [
              { title: '低落期自我支持清单', desc: '先稳住，再行动，先从最小步开始。', detail: '先做一件 5 分钟内可完成的小事，再决定下一步，不强行高压推进。' },
              { title: '负面想法重构', desc: '把绝对化判断改成可验证的中性描述。', detail: '尝试写下：事实是什么、我在担心什么、我能做哪一步。' }
            ],
            videos: [
              { title: '舒缓引导视频（减压）', desc: '当状态低落时，先用呼吸和声音稳定身心。', url: 'https://www.bilibili.com/video/BV1aK4y1r7P2' }
            ]
          },
          '未分析': {
            imageText: [
              { title: '先完成一次情绪分析', desc: '完成分析后可获得更精确的知识推送。', detail: '建议先到笔记页选择一条记录进行分析，然后回到此页查看定制内容。' }
            ],
            videos: [
              { title: '通用情绪调节视频', desc: '适合所有状态的入门调节内容。', url: 'https://www.bilibili.com/video/BV1fL411L7T6' }
            ]
          }
        };

        const fallback = fallbackMap[emotion] || fallbackMap['未分析'];

        uni.request({
          url: `${BASE_URL}/api/emotion-feeds`,
          method: 'GET',
          data: { emotion: emotionTag || '' },
          success: (res) => {
            const payload = res && res.data ? res.data : {};
            const imageText = Array.isArray(payload.imageText)
              ? payload.imageText.map((item) => ({ ...item, expanded: false }))
              : [];
            const videos = Array.isArray(payload.videos)
              ? payload.videos.filter((item) => !!(item && item.url))
              : [];
            this.imageTextFeeds = imageText.length ? imageText : fallback.imageText;
            this.videoFeeds = videos.length ? videos : fallback.videos;
          },
          fail: () => {
            this.imageTextFeeds = fallback.imageText;
            this.videoFeeds = fallback.videos;
          }
        });
      },
      toggleArticle(index) {
        this.imageTextFeeds = this.imageTextFeeds.map((item, idx) => {
          if (idx === index) {
            return { ...item, expanded: !item.expanded };
          }
          return item;
        });
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
      }
    }
  };
</script>

<style scoped lang="css">
  .page {
    min-height: 100vh;
    background: linear-gradient(180deg, #f2f6f9 0%, #ecf1f6 45%, #eef4f8 100%);
    padding-top: calc(14rpx + env(safe-area-inset-top));
    padding-bottom: 170rpx;
  }

  .topbar {
    display: flex;
    align-items: center;
    gap: 20rpx;
    padding: 24rpx 30rpx;
    background: rgba(217, 217, 217, 0.72);
    backdrop-filter: blur(4px);
  }

  .back-btn {
    padding: 10rpx 20rpx;
    background: #2c2c2c;
    border-radius: 12rpx;
  }

  .back-text {
    font-size: 24rpx;
    color: #ffffff;
  }

  .title {
    font-size: 40rpx;
    line-height: 1.2;
    color: #1b2b3a;
    font-weight: 700;
  }

  .summary-card,
  .panel {
    margin: 20rpx 32rpx 0;
    border-radius: 18rpx;
    background: rgba(255, 255, 255, 0.9);
    border: 1rpx solid rgba(0, 0, 0, 0.06);
    box-shadow: 0 10rpx 22rpx rgba(19, 35, 49, 0.07);
    padding: 24rpx;
  }

  .summary-title {
    display: block;
    font-size: 30rpx;
    line-height: 1.4;
    color: #203545;
    font-weight: 600;
  }

  .summary-text {
    display: block;
    margin-top: 10rpx;
    font-size: 24rpx;
    line-height: 1.6;
    color: #4e667d;
  }

  .panel-title {
    font-size: 28rpx;
    color: #223444;
    font-weight: 600;
    margin-bottom: 14rpx;
  }

  .feed-list {
    display: flex;
    flex-direction: column;
    gap: 12rpx;
  }

  .feed-card {
    padding: 18rpx;
    border-radius: 14rpx;
    background: #f7fbff;
    border: 1rpx solid #dbe9f6;
  }

  .feed-cover {
    width: 100%;
    height: 220rpx;
    border-radius: 12rpx;
    margin-bottom: 10rpx;
    background: #e9f1f8;
  }

  .feed-head {
    display: flex;
    align-items: center;
    gap: 10rpx;
  }

  .feed-emoji {
    font-size: 30rpx;
  }

  .feed-title {
    font-size: 27rpx;
    line-height: 1.4;
    color: #1d3850;
    font-weight: 600;
  }

  .feed-desc {
    margin-top: 8rpx;
    display: block;
    font-size: 23rpx;
    line-height: 1.5;
    color: #4b6883;
  }

  .feed-detail {
    margin-top: 10rpx;
    display: block;
    font-size: 23rpx;
    line-height: 1.6;
    color: #35536c;
    background: #f0f6fc;
    border-radius: 10rpx;
    padding: 12rpx;
  }

  .action-btn {
    margin-top: 12rpx;
    align-self: flex-start;
    display: inline-flex;
    padding: 8rpx 18rpx;
    border-radius: 999rpx;
    background: #edf3f9;
    border: 1rpx solid #d1deeb;
  }

  .action-btn.primary {
    background: #2b4f71;
    border-color: #2b4f71;
  }

  .action-text {
    font-size: 22rpx;
    color: #35556f;
  }

  .action-text.primary-text {
    color: #ffffff;
  }

  .empty-tip {
    display: block;
    margin-top: 8rpx;
    color: #6c8296;
    font-size: 23rpx;
  }
</style>
