<template>
  <view class="page">
    <view class="topbar">
      <view class="back-btn" @click="goBack"><text class="back-text">返回</text></view>
      <text class="title">情绪花园</text>
    </view>

    <view class="summary-card">
      <text class="summary-title">今天也在认真照顾自己</text>
      <text class="summary-text">这里不是打分台，而是一张温柔的心情地图。</text>

      <view class="range-row">
        <view class="range-chip" :class="{ active: selectedRange === '7d' }" @click="selectedRange = '7d'">
          <text class="range-chip-text">近7天</text>
        </view>
        <view class="range-chip" :class="{ active: selectedRange === '30d' }" @click="selectedRange = '30d'">
          <text class="range-chip-text">近30天</text>
        </view>
        <view class="range-chip" :class="{ active: selectedRange === 'all' }" @click="selectedRange = 'all'">
          <text class="range-chip-text">全部</text>
        </view>
      </view>

      <view class="kpi-grid">
        <view class="kpi-card">
          <text class="kpi-label">被看见的心情</text>
          <text class="kpi-value">{{ analyzedCount }}</text>
        </view>
        <view class="kpi-card">
          <text class="kpi-label">此刻主色</text>
          <text class="kpi-value">{{ dominantEmotion }}</text>
        </view>
        <view class="kpi-card">
          <text class="kpi-label">平衡感</text>
          <text class="kpi-value">{{ stabilityScore }}</text>
        </view>
        <view class="kpi-card">
          <text class="kpi-label">最近一次心情</text>
          <text class="kpi-value small">{{ latestEmotion }}</text>
        </view>
      </view>

      <view class="healing-note">
        <text class="healing-title">给你的轻声提醒</text>
        <text class="healing-text">{{ comfortMessage }}</text>
      </view>
    </view>

    <view class="panel">
      <text class="panel-title">情绪配色</text>
      <view v-if="!analyzedCount" class="empty-box">
        <text class="empty-text">暂无可用于趋势分析的数据。</text>
      </view>
      <view v-else>
        <view class="bar-row" v-for="item in ratioItems" :key="item.key">
          <text class="bar-label">{{ item.label }}（{{ item.count }}）</text>
          <view class="bar-track">
            <view class="bar-fill" :class="item.className" :style="{ width: item.width }"></view>
          </view>
          <text class="bar-value">{{ item.percent }}</text>
        </view>
      </view>
    </view>

    <view class="panel">
      <text class="panel-title">最近7天心情小森林</text>
      <view v-if="!hasRecent7dData" class="empty-box">
        <text class="empty-text">近7天没有分析记录。</text>
      </view>
      <view v-else>
        <view class="heat-chart">
          <view class="heat-col" v-for="day in recent7d" :key="day.date">
            <view class="heat-stack">
              <view class="heat-seg c1" :style="{ height: day.h1 }"></view>
              <view class="heat-seg c2" :style="{ height: day.h2 }"></view>
              <view class="heat-seg c3" :style="{ height: day.h3 }"></view>
            </view>
            <text class="heat-total">{{ day.total }}</text>
            <text class="heat-day">{{ day.shortDay }}</text>
          </view>
        </view>

        <view class="legend-row">
          <text class="legend-item"><text class="dot c1"></text>低落</text>
          <text class="legend-item"><text class="dot c2"></text>平稳</text>
          <text class="legend-item"><text class="dot c3"></text>高兴</text>
        </view>
      </view>
    </view>

    <BottomNav current="trend" />
  </view>
</template>

<script>
import { BASE_URL } from '@/common/config.js';
import BottomNav from '@/components/BottomNav.vue';
import { parseAnalysisPayload, normalizePredictionFromAnalysis } from '@/common/emotionAnalysis.js';

export default {
  components: { BottomNav },
  data() {
    return {
      notes: [],
      selectedRange: '30d'
    };
  },
  computed: {
    analyzedNotes() {
      return this.notes
        .map((note) => {
          const analysis = parseAnalysisPayload(note.analysis_result);
          const idx = normalizePredictionFromAnalysis(analysis);
          if (!idx) {
            return null;
          }
          return {
            created_at: note.created_at || '',
            emotionIdx: idx
          };
        })
        .filter((x) => !!x);
    },
    filteredAnalyzedNotes() {
      if (this.selectedRange === 'all') {
        return this.analyzedNotes;
      }
      const now = Date.now();
      const days = this.selectedRange === '7d' ? 7 : 30;
      const cutoff = now - days * 24 * 60 * 60 * 1000;
      return this.analyzedNotes.filter((n) => {
        const ts = this.parseDateSafe(n.created_at);
        return !Number.isNaN(ts) && ts >= cutoff;
      });
    },
    analyzedCount() {
      return this.filteredAnalyzedNotes.length;
    },
    emotionCounts() {
      const counts = { 1: 0, 2: 0, 3: 0 };
      this.filteredAnalyzedNotes.forEach((n) => {
        counts[n.emotionIdx] += 1;
      });
      return counts;
    },
    dominantEmotion() {
      if (!this.analyzedCount) {
        return '暂无';
      }
      const entries = [
        { idx: 1, label: '低落预警', count: this.emotionCounts[1] },
        { idx: 2, label: '平稳', count: this.emotionCounts[2] },
        { idx: 3, label: '高兴', count: this.emotionCounts[3] }
      ];
      entries.sort((a, b) => b.count - a.count);
      return entries[0].label;
    },
    latestEmotion() {
      if (!this.filteredAnalyzedNotes.length) {
        return '暂无';
      }
      const latest = [...this.filteredAnalyzedNotes].sort((a, b) => {
        return this.parseDateSafe(b.created_at) - this.parseDateSafe(a.created_at);
      })[0];
      return this.emotionLabelByIdx(latest.emotionIdx);
    },
    stabilityScore() {
      if (!this.analyzedCount) {
        return '--';
      }
      const hi = this.emotionCounts[3];
      const low = this.emotionCounts[1];
      const calm = this.emotionCounts[2];
      const balancePenalty = Math.abs(hi - low) / this.analyzedCount;
      const calmBonus = calm / this.analyzedCount;
      const score = Math.max(0, Math.min(100, Math.round((1 - balancePenalty) * 60 + calmBonus * 40)));
      return `${score}分`;
    },
    comfortMessage() {
      if (!this.analyzedCount) {
        return '先写下一点点心情吧，哪怕只有一句话，也是在靠近自己。';
      }
      if (this.dominantEmotion === '低落预警') {
        return '你已经很努力了。先慢一点，呼吸一下，再做最小的一步就很好。';
      }
      if (this.dominantEmotion === '平稳') {
        return '你的节奏很稳，这很珍贵。继续温柔地照顾自己就好。';
      }
      return '这份高兴很有力量，记得收藏今天让你发光的小瞬间。';
    },
    ratioItems() {
      const total = this.analyzedCount;
      return [
        this.makeRatioItem('1', '低落预警', this.emotionCounts[1], total, 'c1'),
        this.makeRatioItem('2', '平稳', this.emotionCounts[2], total, 'c2'),
        this.makeRatioItem('3', '高兴', this.emotionCounts[3], total, 'c3')
      ];
    },
    recent7d() {
      const dayMap = {};
      const now = Date.now();
      const start = now - 7 * 24 * 60 * 60 * 1000;
      this.analyzedNotes.forEach((n) => {
        const ts = this.parseDateSafe(n.created_at);
        if (Number.isNaN(ts) || ts < start) {
          return;
        }
        const d = this.formatDay(ts);
        if (!dayMap[d]) {
          dayMap[d] = { date: d, c1: 0, c2: 0, c3: 0 };
        }
        dayMap[d][`c${n.emotionIdx}`] += 1;
      });
      const days = [];
      for (let i = 6; i >= 0; i -= 1) {
        const ts = now - i * 24 * 60 * 60 * 1000;
        const date = this.formatDay(ts);
        const shortDay = this.formatShortDay(ts);
        const base = dayMap[date] || { date, c1: 0, c2: 0, c3: 0 };
        const total = base.c1 + base.c2 + base.c3;
        const maxRef = Math.max(1, total);
        days.push({
          ...base,
          shortDay,
          total,
          h1: `${Math.max(4, (base.c1 / maxRef) * 72)}rpx`,
          h2: `${Math.max(4, (base.c2 / maxRef) * 72)}rpx`,
          h3: `${Math.max(4, (base.c3 / maxRef) * 72)}rpx`
        });
      }
      return days;
    },
    hasRecent7dData() {
      return this.recent7d.some((d) => d.total > 0);
    }
  },
  onShow() {
    this.fetchHistory();
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
    fetchHistory() {
      const token = uni.getStorageSync('token');
      uni.request({
        url: `${BASE_URL}/api/notes`,
        header: { Authorization: `Bearer ${token}` },
        success: (res) => {
          if (res.statusCode === 200 && Array.isArray(res.data)) {
            this.notes = res.data;
          }
        }
      });
    },
    parseDateSafe(value) {
      if (!value) return NaN;
      return Date.parse(String(value).replace(' ', 'T'));
    },
    makeRatioItem(key, label, count, total, className) {
      const ratio = total ? count / total : 0;
      return {
        key,
        label,
        count,
        className,
        width: `${Math.max(2, ratio * 100)}%`,
        percent: `${(ratio * 100).toFixed(1)}%`
      };
    },
    emotionLabelByIdx(idx) {
      if (idx === 1) return '低落预警';
      if (idx === 2) return '平稳';
      if (idx === 3) return '高兴';
      return '未分析';
    },
    formatDay(ts) {
      const d = new Date(ts);
      const y = d.getFullYear();
      const m = `${d.getMonth() + 1}`.padStart(2, '0');
      const day = `${d.getDate()}`.padStart(2, '0');
      return `${y}-${m}-${day}`;
    },
    formatShortDay(ts) {
      const d = new Date(ts);
      const m = `${d.getMonth() + 1}`.padStart(2, '0');
      const day = `${d.getDate()}`.padStart(2, '0');
      return `${m}/${day}`;
    }
  }
};
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: linear-gradient(180deg, #fbf8f2 0%, #f4f7f3 48%, #edf5f7 100%);
  padding-top: calc(14rpx + env(safe-area-inset-top));
  padding-bottom: 170rpx;
  box-sizing: border-box;
}

.topbar {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 24rpx 30rpx;
  background: rgba(255, 250, 242, 0.78);
  backdrop-filter: blur(6px);
}

.back-btn {
  padding: 10rpx 20rpx;
  background: #5a6d63;
  border-radius: 12rpx;
}

.back-text {
  font-size: 24rpx;
  color: #ffffff;
}

.title {
  font-size: 40rpx;
  line-height: 1.2;
  color: #32483d;
  font-weight: 700;
}

.summary-card,
.panel {
  margin: 20rpx 32rpx 0;
  border-radius: 22rpx;
  background: rgba(255, 255, 255, 0.88);
  border: 1rpx solid rgba(130, 150, 120, 0.18);
  box-shadow: 0 10rpx 24rpx rgba(74, 93, 82, 0.09);
  padding: 24rpx;
}

.summary-title {
  display: block;
  font-size: 30rpx;
  line-height: 1.4;
  color: #355245;
  font-weight: 600;
}

.summary-text {
  display: block;
  margin-top: 10rpx;
  font-size: 24rpx;
  line-height: 1.6;
  color: #5a7266;
}

.range-row {
  margin-top: 16rpx;
  display: flex;
  gap: 10rpx;
}

.range-chip {
  padding: 8rpx 18rpx;
  border-radius: 999rpx;
  background: #f2f6ef;
  border: 1rpx solid #d5e1d0;
}

.range-chip.active {
  background: #6f8c7e;
  border-color: #6f8c7e;
}

.range-chip-text {
  font-size: 22rpx;
  color: #4f6a5d;
}

.range-chip.active .range-chip-text {
  color: #ffffff;
}

.kpi-grid {
  margin-top: 16rpx;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10rpx;
}

.kpi-card {
  padding: 14rpx;
  border-radius: 12rpx;
  background: #f9fbf8;
  border: 1rpx solid #dbe7d7;
}

.kpi-label {
  display: block;
  font-size: 21rpx;
  color: #657d72;
}

.kpi-value {
  display: block;
  margin-top: 6rpx;
  font-size: 34rpx;
  line-height: 1.2;
  font-weight: 700;
  color: #365346;
}

.kpi-value.small {
  font-size: 30rpx;
}

.panel-title {
  font-size: 28rpx;
  color: #355245;
  font-weight: 600;
  margin-bottom: 14rpx;
}

.healing-note {
  margin-top: 14rpx;
  padding: 14rpx;
  border-radius: 14rpx;
  background: linear-gradient(120deg, #fff7e7 0%, #f2f8ef 100%);
  border: 1rpx solid #e8e2c9;
}

.healing-title {
  display: block;
  font-size: 22rpx;
  color: #6a7d52;
}

.healing-text {
  margin-top: 6rpx;
  display: block;
  font-size: 24rpx;
  line-height: 1.6;
  color: #4d5f4f;
}

.empty-box {
  padding: 20rpx;
  border-radius: 12rpx;
  background: #f4f7fb;
}

.empty-text {
  font-size: 24rpx;
  line-height: 1.6;
  color: #60738a;
}

.bar-row {
  display: flex;
  align-items: center;
  margin-bottom: 10rpx;
}

.bar-label {
  width: 132rpx;
  font-size: 22rpx;
  color: #5f786a;
}

.bar-track {
  flex: 1;
  height: 14rpx;
  background: #e8eee7;
  border-radius: 999rpx;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 999rpx;
}

.bar-fill.c1 {
  background: #7da78f;
}

.bar-fill.c2 {
  background: #d2a869;
}

.bar-fill.c3 {
  background: #e18ca1;
}

.bar-value {
  width: 110rpx;
  text-align: right;
  font-size: 22rpx;
  color: #4f6a5d;
}

.heat-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 8rpx;
  padding: 8rpx 0;
}

.heat-col {
  width: 84rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.heat-stack {
  width: 56rpx;
  height: 72rpx;
  border-radius: 10rpx;
  background: #edf2ec;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
}

.heat-seg {
  width: 33.3333%;
  min-height: 4rpx;
}

.heat-seg.c1 {
  background: #7da78f;
}

.heat-seg.c2 {
  background: #d2a869;
}

.heat-seg.c3 {
  background: #e18ca1;
}

.heat-total {
  margin-top: 6rpx;
  font-size: 20rpx;
  color: #5a7467;
}

.heat-day {
  margin-top: 2rpx;
  font-size: 20rpx;
  color: #6c8478;
}

.legend-row {
  margin-top: 10rpx;
  display: flex;
  gap: 18rpx;
}

.legend-item {
  font-size: 21rpx;
  color: #5b7568;
  display: inline-flex;
  align-items: center;
}

.dot {
  width: 14rpx;
  height: 14rpx;
  border-radius: 50%;
  margin-right: 8rpx;
}

.dot.c1 {
  background: #7da78f;
}

.dot.c2 {
  background: #d2a869;
}

.dot.c3 {
  background: #e18ca1;
}
</style>
