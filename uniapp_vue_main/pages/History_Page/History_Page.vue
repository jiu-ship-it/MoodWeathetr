<template>
  <view class="page">
    <view class="topbar">
      <view class="back-btn" @click="goBack"><text class="back-text">返回</text></view>
      <text class="title">历史记录</text>
      <view class="trend-link" @click="goTrend"><text class="trend-link-text">看趋势</text></view>
    </view>

    <view class="summary-card">
      <text class="summary-title">历史记录有什么用？</text>
      <text class="summary-text">查看情绪变化趋势、复盘触发原因、找到对你有效的调节方式。</text>
    </view>

    <view class="filters-card">
      <view class="filter-group">
        <text class="filter-title">时间范围</text>
        <view class="chip-row">
          <view class="chip" :class="{ active: rangeFilter === '7d' }" @click="rangeFilter = '7d'"><text class="chip-text">近7天</text></view>
          <view class="chip" :class="{ active: rangeFilter === '30d' }" @click="rangeFilter = '30d'"><text class="chip-text">近30天</text></view>
          <view class="chip" :class="{ active: rangeFilter === 'all' }" @click="rangeFilter = 'all'"><text class="chip-text">全部</text></view>
        </view>
      </view>
      <view class="filter-group mt-12">
        <text class="filter-title">记录筛选</text>
        <view class="chip-row">
          <view class="chip" :class="{ active: statusFilter === 'all' }" @click="statusFilter = 'all'"><text class="chip-text">全部</text></view>
          <view class="chip" :class="{ active: statusFilter === 'analyzed' }" @click="statusFilter = 'analyzed'"><text class="chip-text">已分析</text></view>
          <view class="chip" :class="{ active: statusFilter === 'warning' }" @click="statusFilter = 'warning'"><text class="chip-text">低落预警</text></view>
        </view>
      </view>
      <text class="result-count">当前筛选：{{ filteredNotes.length }} 条记录</text>
    </view>

    <view class="insight-panel">
      <text class="panel-title">记录洞察</text>
      <view class="insight-grid">
        <view class="insight-card">
          <text class="insight-label">已筛选记录</text>
          <text class="insight-value">{{ filteredNotes.length }}</text>
        </view>
        <view class="insight-card">
          <text class="insight-label">已分析</text>
          <text class="insight-value">{{ analyzedCount }}</text>
        </view>
        <view class="insight-card">
          <text class="insight-label">连续记录天数</text>
          <text class="insight-value">{{ consecutiveDays }}</text>
        </view>
        <view class="insight-card">
          <text class="insight-label">主导情绪</text>
          <text class="insight-value">{{ dominantEmotion }}</text>
        </view>
      </view>
      <text class="insight-tip">{{ insightText }}</text>
    </view>

    <view class="distribution-panel" v-if="distributionItems.length">
      <text class="panel-title">情绪分布</text>
      <view class="distribution-row" v-for="item in distributionItems" :key="item.key">
        <text class="distribution-label">{{ item.label }}</text>
        <view class="distribution-track">
          <view class="distribution-fill" :class="item.className" :style="{ width: item.width }"></view>
        </view>
        <text class="distribution-value">{{ item.percent }}</text>
      </view>
    </view>

    <view class="list-panel">
      <view v-if="!filteredNotes.length" class="empty-box">
        <text class="empty-text">暂无历史记录，先去写一条笔记吧。</text>
      </view>

      <view v-for="group in groupedNotes" :key="group.date" class="day-group">
        <view class="day-head">
          <text class="day-title">{{ group.dateLabel }}</text>
          <text class="day-count">{{ group.items.length }} 条</text>
        </view>

        <view v-for="note in group.items" :key="note.id" class="note-card">
          <view class="note-head" @click="openNote(note.id)">
            <text class="note-title">{{ note.displayTitle }}</text>
            <text class="note-time">{{ formatTime(note.created_at) }}</text>
          </view>
          <view class="note-foot">
            <text class="emotion-tag" :class="note.emotionClass">{{ note.emotionLabel }}</text>
            <view class="actions">
              <view class="action-btn" @click="openNote(note.id)"><text class="action-text">查看</text></view>
              <view class="action-btn primary" @click="analyzeNow(note.id)"><text class="action-text primary-text">分析</text></view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <BottomNav current="history" />
  </view>
</template>

<script>
  import { BASE_URL } from '@/common/config.js';
  import BottomNav from '@/components/BottomNav.vue';

  export default {
    components: { BottomNav },
    data() {
      return {
        notes: [],
        rangeFilter: '7d',
        statusFilter: 'all'
      };
    },

    computed: {
      viewNotes() {
        return this.notes.map((note) => {
          const emotionLabel = this.getEmotionLabel(note);
          const createdTs = this.parseDateSafe(note.created_at);
          return {
            ...note,
            createdTs,
            displayTitle: note.title || '未命名笔记',
            emotionLabel,
            emotionClass: this.emotionClass(emotionLabel)
          };
        });
      },
      rangeNotes() {
        let list = [...this.viewNotes];
        const now = Date.now();
        if (this.rangeFilter !== 'all') {
          const days = this.rangeFilter === '7d' ? 7 : 30;
          const cutoff = now - days * 24 * 60 * 60 * 1000;
          list = list.filter((note) => !Number.isNaN(note.createdTs) && note.createdTs >= cutoff);
        }
        return list;
      },
      filteredNotes() {
        let list = [...this.rangeNotes];
        if (this.statusFilter === 'analyzed') {
          list = list.filter((note) => note.emotionLabel !== '未分析');
        } else if (this.statusFilter === 'warning') {
          list = list.filter((note) => note.emotionLabel === '低落预警');
        }
        return list.sort((a, b) => (Number.isNaN(b.createdTs) ? 0 : b.createdTs) - (Number.isNaN(a.createdTs) ? 0 : a.createdTs));
      },
      analyzedCount() {
        return this.filteredNotes.filter((n) => n.emotionLabel !== '未分析').length;
      },
      dominantEmotion() {
        const analyzed = this.filteredNotes.filter((n) => n.emotionLabel !== '未分析');
        if (!analyzed.length) return '暂无';
        const counter = { '低落预警': 0, '平稳': 0, '高兴': 0 };
        analyzed.forEach((n) => {
          if (counter[n.emotionLabel] !== undefined) {
            counter[n.emotionLabel] += 1;
          }
        });
        const entries = Object.entries(counter).sort((a, b) => b[1] - a[1]);
        return entries[0][1] ? entries[0][0] : '暂无';
      },
      consecutiveDays() {
        const daySet = new Set(
          this.filteredNotes
            .map((n) => this.formatDay(n.createdTs))
            .filter((d) => !!d)
        );
        if (!daySet.size) return 0;
        let streak = 0;
        let cursor = new Date();
        while (true) {
          const day = this.formatDay(cursor.getTime());
          if (!daySet.has(day)) break;
          streak += 1;
          cursor = new Date(cursor.getTime() - 24 * 60 * 60 * 1000);
        }
        return streak;
      },
      insightText() {
        if (!this.filteredNotes.length) {
          return '当前筛选下暂无记录，先去写一条笔记开始积累。';
        }
        if (!this.analyzedCount) {
          return '已有记录但尚未分析，点“分析”后可看到更准确的情绪洞察。';
        }
        if (this.dominantEmotion === '低落预警') {
          return '近期低落预警占比较高，建议优先保证睡眠与作息，并减少高压任务并行。';
        }
        if (this.dominantEmotion === '高兴') {
          return '近期情绪整体偏高兴，建议把积极触发因素沉淀为可复用习惯。';
        }
        return '近期情绪较平稳，继续保持记录与复盘，有助于提前发现波动。';
      },
      distributionItems() {
        const analyzed = this.filteredNotes.filter((n) => n.emotionLabel !== '未分析');
        if (!analyzed.length) return [];
        const total = analyzed.length;
        const count = { warning: 0, stable: 0, happy: 0 };
        analyzed.forEach((n) => {
          if (n.emotionLabel === '低落预警') count.warning += 1;
          else if (n.emotionLabel === '平稳') count.stable += 1;
          else if (n.emotionLabel === '高兴') count.happy += 1;
        });
        const makeItem = (key, label, value, className) => {
          const ratio = value / total;
          return {
            key,
            label,
            className,
            width: `${Math.max(4, ratio * 100)}%`,
            percent: `${(ratio * 100).toFixed(1)}%`
          };
        };
        return [
          makeItem('warning', '低落预警', count.warning, 'emotion-3'),
          makeItem('stable', '平稳', count.stable, 'emotion-1'),
          makeItem('happy', '高兴', count.happy, 'emotion-2')
        ];
      },
      groupedNotes() {
        const map = {};
        this.filteredNotes.forEach((note) => {
          const day = this.formatDay(note.createdTs) || '未知日期';
          if (!map[day]) {
            map[day] = {
              date: day,
              dateLabel: day,
              items: []
            };
          }
          map[day].items.push(note);
        });
        return Object.keys(map)
          .sort((a, b) => this.parseDateSafe(b) - this.parseDateSafe(a))
          .map((k) => map[k]);
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
      goTrend() {
        uni.navigateTo({ url: '/pages/EmotionTrend/EmotionTrend' });
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
      parseAnalysis(payload) {
        if (!payload) {
          return null;
        }
        if (typeof payload === 'string') {
          try {
            return JSON.parse(payload);
          } catch (e) {
            return null;
          }
        }
        return payload;
      },
      getEmotionLabel(note) {
        const analysis = this.parseAnalysis(note.analysis_result);
        const normalized = this.normalizePrediction(analysis);
        if (normalized === 1) {
          return '低落预警';
        }
        if (normalized === 2) {
          return '平稳';
        }
        if (normalized === 3) {
          return '高兴';
        }
        return '未分析';
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
      parseDateSafe(value) {
        if (!value) return NaN;
        const normalized = String(value).replace(' ', 'T');
        return Date.parse(normalized);
      },
      formatDay(value) {
        const ts = typeof value === 'number' ? value : this.parseDateSafe(value);
        if (Number.isNaN(ts)) return '';
        const d = new Date(ts);
        const y = d.getFullYear();
        const m = `${d.getMonth() + 1}`.padStart(2, '0');
        const day = `${d.getDate()}`.padStart(2, '0');
        return `${y}-${m}-${day}`;
      },
      emotionClass(label) {
        if (label === '平稳') return 'emotion-1';
        if (label === '高兴') return 'emotion-2';
        if (label === '低落预警') return 'emotion-3';
        return 'emotion-0';
      },
      formatTime(value) {
        if (!value) return '--';
        const d = new Date(String(value).replace(' ', 'T').replace(/\.\d+Z$/, 'Z'));
        if (Number.isNaN(d.getTime())) {
          return String(value).replace('T', ' ').replace('Z', '');
        }
        const y = d.getFullYear();
        const m = `${d.getMonth() + 1}`.padStart(2, '0');
        const day = `${d.getDate()}`.padStart(2, '0');
        const hh = `${d.getHours()}`.padStart(2, '0');
        const mm = `${d.getMinutes()}`.padStart(2, '0');
        const ss = `${d.getSeconds()}`.padStart(2, '0');
        return `${y}-${m}-${day} ${hh}:${mm}:${ss}`;
      },
      openNote(id) {
        uni.navigateTo({ url: `/pages/NoteAnalysis/NoteAnalysis?id=${id}&simple=1` });
      },
      analyzeNow(id) {
        uni.navigateTo({ url: `/pages/NoteAnalysis/NoteAnalysis?id=${id}` });
      }
    },
  };
</script>

<style scoped lang="css">
  .page {
    min-height: 100vh;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163844487671632.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    background-attachment: fixed;
    width: 100%;
    box-sizing: border-box;
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

  .trend-link {
    margin-left: auto;
    padding: 10rpx 20rpx;
    border-radius: 12rpx;
    background: #2b4f71;
  }

  .trend-link-text {
    font-size: 22rpx;
    color: #ffffff;
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
    font-size: 44rpx;
    line-height: 1.2;
    color: #1b2b3a;
    font-weight: 700;
  }

  .summary-card,
  .filters-card,
  .insight-panel,
  .distribution-panel,
  .list-panel {
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
    font-size: 25rpx;
    line-height: 1.6;
    color: #4e667d;
  }

  .filters-card {
    margin-top: 14rpx;
  }

  .filter-group {
    display: flex;
    flex-direction: column;
    gap: 10rpx;
  }

  .filter-title {
    font-size: 24rpx;
    color: #3e566e;
  }

  .chip-row {
    display: flex;
    gap: 10rpx;
    flex-wrap: wrap;
  }

  .chip {
    padding: 8rpx 16rpx;
    border-radius: 999rpx;
    background: #edf3f9;
    border: 1rpx solid #d1deeb;
  }

  .chip.active {
    background: #2b4f71;
    border-color: #2b4f71;
  }

  .chip-text {
    font-size: 22rpx;
    color: #35556f;
  }

  .chip.active .chip-text {
    color: #ffffff;
  }

  .result-count {
    margin-top: 14rpx;
    display: block;
    font-size: 22rpx;
    color: #60758b;
  }

  .insight-grid {
    margin-top: 12rpx;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10rpx;
  }

  .insight-card {
    border-radius: 12rpx;
    background: #f7fbff;
    border: 1rpx solid #dbe9f6;
    padding: 14rpx;
  }

  .insight-label {
    display: block;
    font-size: 22rpx;
    color: #60758b;
  }

  .insight-value {
    display: block;
    margin-top: 6rpx;
    font-size: 30rpx;
    color: #1f3b53;
    font-weight: 700;
  }

  .insight-tip {
    display: block;
    margin-top: 12rpx;
    font-size: 22rpx;
    color: #4c6781;
    line-height: 1.5;
  }

  .distribution-row {
    display: flex;
    align-items: center;
    margin-top: 10rpx;
  }

  .distribution-label {
    width: 120rpx;
    font-size: 22rpx;
    color: #4e667d;
  }

  .distribution-track {
    flex: 1;
    height: 14rpx;
    border-radius: 999rpx;
    overflow: hidden;
    background: #e6edf4;
  }

  .distribution-fill {
    height: 100%;
    border-radius: 999rpx;
  }

  .distribution-value {
    width: 96rpx;
    text-align: right;
    font-size: 22rpx;
    color: #4e667d;
  }

  .mt-12 {
    margin-top: 12rpx;
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

  .day-group {
    margin-bottom: 12rpx;
  }

  .day-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8rpx;
    padding: 0 4rpx;
  }

  .day-title {
    font-size: 24rpx;
    color: #2d4a63;
    font-weight: 600;
  }

  .day-count {
    font-size: 20rpx;
    color: #6a8199;
  }

  .note-card {
    margin-bottom: 14rpx;
    padding: 18rpx;
    border-radius: 14rpx;
    background: #f7fbff;
    border: 1rpx solid #dbe9f6;
  }

  .note-head {
    display: flex;
    flex-direction: column;
    gap: 8rpx;
  }

  .note-title {
    font-size: 30rpx;
    line-height: 1.4;
    color: #1d3346;
    font-weight: 600;
    display: block;
  }

  .note-time {
    font-size: 22rpx;
    line-height: 1.4;
    color: #68809a;
    display: block;
  }

  .note-foot {
    margin-top: 14rpx;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .emotion-tag {
    padding: 8rpx 16rpx;
    border-radius: 999rpx;
    font-size: 22rpx;
    line-height: 1.3;
    color: #32516d;
    background: #eaf1f8;
  }

  .emotion-1 {
    background: #eaf6f1;
    color: #2f6d5d;
  }

  .emotion-2 {
    background: #fff4e6;
    color: #8a5a1c;
  }

  .emotion-3 {
    background: #ffeef2;
    color: #924465;
  }

  .actions {
    display: flex;
    gap: 10rpx;
  }

  .action-btn {
    padding: 8rpx 16rpx;
    border-radius: 10rpx;
    border: 1rpx solid #c8d8e9;
    background: #ffffff;
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
</style>