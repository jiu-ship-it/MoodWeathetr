<template>
	<view class="page">
		<view class="topbar">
			<text class="topbar-title">{{ simpleMode ? '分析查看' : '分析结果' }}</text>
		</view>

		<view class="content">
			<view class="summary-card">
				<view class="summary-head">
					<text class="note-title">{{ title || '未命名笔记' }}</text>
					<text class="analysis-time" v-if="analyzedAt">分析时间：{{ formattedAnalyzedAt }}</text>
					<text class="analysis-time" v-if="modelStatusText">模型状态：{{ modelStatusText }}</text>
					<text class="note-content" v-if="noteContent">{{ noteContent }}</text>
				</view>
				<view class="summary-main" :class="summaryEmotion.className" v-if="hasAnalysis">
					<text class="label">综合结论</text>
					<text class="prediction-text">{{ predictionLabel }}</text>
					<text class="confidence-text">融合置信度：{{ fusionConfidenceText }}</text>
					<text class="summary-desc">{{ summaryDescription }}</text>
				</view>
				<view class="summary-main" v-else>
					<text class="empty-text">暂无分析结果，可点击“重新分析”生成。</text>
				</view>
			</view>

			<view class="panel simple-panel" v-if="hasAnalysis && simpleMode">
				<text class="panel-title">分析文本摘要</text>
				<text class="simple-text">综合结论：{{ predictionLabel }}</text>
				<text class="simple-text">融合置信度：{{ fusionConfidenceText }}</text>
				<text class="simple-text">{{ summaryDescription }}</text>
			</view>

			<view class="panel" v-if="hasAnalysis && !simpleMode">
				<text class="panel-title">三分支对比</text>
				<view class="branch-row">
					<view v-for="card in branchCards" :key="card.key" class="branch-chip" :class="card.className">
						<text class="chip-key">{{ card.title }}</text>
						<text class="chip-val">{{ card.label }}</text>
					</view>
				</view>
			</view>

			<view class="panel" v-if="hasAnalysis && !simpleMode">
				<text class="panel-title">概率可视化</text>
				<view v-for="block in probabilityBlocks" :key="block.key" class="prob-block">
					<text class="prob-title">{{ block.title }}</text>
					<view v-for="(item, idx) in block.items" :key="idx" class="bar-row">
						<text class="bar-label">{{ item.label }}</text>
						<view class="bar-track">
							<view class="bar-fill" :style="{ width: item.width, background: item.color }"></view>
						</view>
						<text class="bar-value">{{ item.percent }}</text>
					</view>
				</view>
			</view>

			<view class="panel push-panel" v-if="hasAnalysis && !simpleMode">
				<text class="panel-title">情绪推送</text>
				<view class="push-list">
					<view class="push-item" v-for="(item, idx) in emotionPushList" :key="idx">
						<view class="push-head" @click="togglePush(idx)">
							<text class="push-title">{{ item.title }}</text>
							<text class="push-toggle">{{ expandedPushIndex === idx ? '收起' : '展开' }}</text>
						</view>
						<text class="push-desc" v-if="expandedPushIndex === idx">{{ item.desc }}</text>
						<view class="push-actions" v-if="expandedPushIndex === idx">
							<view class="push-action muted" @click="readPushInPage(item)">
								<text class="push-action-text dark">当前查看</text>
							</view>
							<view class="push-action" @click="handlePushAction(item.action)">
								<text class="push-action-text">{{ item.actionText }}</text>
							</view>
						</view>
					</view>
				</view>
			</view>

			<view class="panel resource-panel" v-if="hasAnalysis && !simpleMode">
				<text class="panel-title">资源区</text>
				<text class="resource-subtitle">以下内容已按当前分析结果自动匹配。</text>

				<view class="resource-block">
					<text class="resource-title">图文资源</text>
					<view class="resource-grid">
						<view class="resource-card" v-for="(item, idx) in resourceImageText" :key="`img-${idx}`">
							<text class="resource-badge">图文</text>
							<image v-if="item.cover" class="resource-cover" :src="item.cover" mode="aspectFill" />
							<text class="resource-name">{{ item.title }}</text>
							<text class="resource-desc">{{ item.desc }}</text>
							<view class="resource-action" @click="openResourceDetail(item)">
								<text class="resource-action-text">查看详情</text>
							</view>
						</view>
					</view>
					<text class="resource-empty" v-if="!resourceImageText.length">暂无图文资源</text>
				</view>

				<view class="resource-block">
					<text class="resource-title">视频资源</text>
					<scroll-view class="resource-scroll" scroll-x enable-flex show-scrollbar="false">
						<view class="resource-row">
							<view class="resource-card h-card" v-for="(item, idx) in resourceVideos" :key="`video-${idx}`">
							<text class="resource-badge">视频</text>
							<image v-if="item.cover" class="resource-video-cover" :src="item.cover" mode="aspectFill" />
							<text class="resource-name">{{ item.title }}</text>
							<text class="resource-desc">{{ item.desc }}</text>
							<view class="resource-action primary" @click="openVideoResource(item)">
								<text class="resource-action-text light">直接播放视频</text>
							</view>
						</view>
						</view>
					</scroll-view>
					<text class="resource-empty" v-if="!resourceVideos.length">暂无视频资源</text>
				</view>

				<view class="resource-block">
					<text class="resource-title">音乐资源</text>
					<scroll-view class="resource-scroll" scroll-x enable-flex show-scrollbar="false">
						<view class="resource-row">
							<view class="resource-card h-card" v-for="(item, idx) in resourceMusic" :key="`music-${idx}`">
							<text class="resource-badge">音乐</text>
							<text class="resource-name">{{ item.name }}</text>
							<text class="resource-desc">创作者：{{ item.author }}</text>
							<view class="resource-action" @click="openMusicPage">
								<text class="resource-action-text">去音乐页播放</text>
							</view>
						</view>
						</view>
					</scroll-view>
					<text class="resource-empty" v-if="!resourceMusic.length">暂无音乐资源</text>
				</view>
			</view>

			<view class="panel error-panel" v-if="errorText">
				<text class="error-text">{{ errorText }}</text>
			</view>

			<view class="actions" v-if="!simpleMode">
				<view class="btn" :class="{ 'btn-disabled': isLoading }" @click="analyzeNow">
					<text class="btn-text">{{ isLoading ? '分析中...' : '重新分析' }}</text>
				</view>
			</view>
		</view>

		<view class="support-popup-mask" v-if="showSupportPopup" @click="closeSupportPopup">
			<view class="support-popup-card" @click.stop>
				<text class="support-popup-deco left">✦</text>
				<text class="support-popup-deco right">✿</text>
				<view class="support-header">
					<image class="support-avatar" src="/static/image/smileICON.png" mode="aspectFill" />
					<view class="support-head-text">
						<text class="support-title">心理支持小站</text>
						<text class="support-subtitle">先抱抱你，今天也已经很努力了</text>
					</view>
				</view>
				<view class="support-tags">
					<text class="support-tag">慢一点也没关系</text>
					<text class="support-tag">你值得被好好照顾</text>
				</view>
				<text class="support-desc">检测到你现在有些低落。你可以先休息一下，也可以前往心理咨询入口，获取更及时、温柔的支持。</text>
				<view class="support-popup-actions">
					<view class="support-popup-btn ghost" @click="closeSupportPopup">
						<text class="support-popup-btn-text ghost">稍后再看</text>
					</view>
					<view class="support-popup-btn solid" @click="confirmSupportPopup">
						<text class="support-popup-btn-text">查看咨询入口</text>
					</view>
				</view>
			</view>
		</view>

		<BottomNav current="analysis" />
	</view>
</template>

<script>
	import { BASE_URL } from '@/common/config.js';
	import BottomNav from '@/components/BottomNav.vue';
	import { parseAnalysisPayload, normalizePredictionFromAnalysis, isLowAlertFromAnalysis } from '@/common/emotionAnalysis.js';

	export default {
		components: { BottomNav },
		data() {
			return {
				noteId: null,
				title: '',
				noteContent: '',
				analyzedAt: '',
				analysisObj: null,
				errorText: '',
				isLoading: false,
				simpleMode: false,
				expandedPushIndex: 0,
				resourceImageText: [],
				resourceVideos: [],
				resourceMusic: [],
				modelReachable: null,
				modelStatusText: '',
				pendingSupportPrompt: false,
				hasShownSupportPrompt: false,
				supportPromptTimer: null,
				showSupportPopup: false,
				supportCloseCallback: null
			};
		},
		computed: {
			hasAnalysis() {
				return !!(this.analysisObj && this.analysisObj.probabilities);
			},
			normalizedPrediction() {
				const normalized = normalizePredictionFromAnalysis(this.analysisObj);
				return normalized || '-';
			},
			fusionConfidence() {
				const m = this.analysisObj && this.analysisObj.probabilities && this.analysisObj.probabilities.M;
				if (!Array.isArray(m) || m.length === 0) {
					return 0;
				}
				const idx = Math.max(0, Number(this.normalizedPrediction) - 1);
				return Number(m[idx] || 0);
			},
			fusionConfidenceText() {
				return this.toPercent(this.fusionConfidence);
			},
			formattedAnalyzedAt() {
				if (!this.analyzedAt) {
					return '';
				}
				const d = new Date(String(this.analyzedAt).replace(' ', 'T').replace(/\.\d+Z$/, 'Z'));
				if (Number.isNaN(d.getTime())) {
					return String(this.analyzedAt).replace('T', ' ').replace('Z', '');
				}
				const y = d.getFullYear();
				const m = `${d.getMonth() + 1}`.padStart(2, '0');
				const day = `${d.getDate()}`.padStart(2, '0');
				const hh = `${d.getHours()}`.padStart(2, '0');
				const mm = `${d.getMinutes()}`.padStart(2, '0');
				const ss = `${d.getSeconds()}`.padStart(2, '0');
				return `${y}-${m}-${day} ${hh}:${mm}:${ss}`;
			},
			summaryEmotion() {
				const idx = Number(this.normalizedPrediction) - 1;
				return this.emotionMetaByIndex(idx);
			},
			predictionLabel() {
				if (this.normalizedPrediction === '-') {
					return '-';
				}
				const idx = Number(this.normalizedPrediction) - 1;
				const meta = this.emotionMetaByIndex(idx);
				return `${meta.label}（第 ${this.normalizedPrediction} 类）`;
			},
			summaryDescription() {
				const mIdx = this.branchPredictionIndex('M');
				const tIdx = this.branchPredictionIndex('T');
				const aIdx = this.branchPredictionIndex('A');
				if (mIdx < 0 || tIdx < 0 || aIdx < 0) {
					return '当前结果已生成，可结合三分支概率进行判断。';
				}
				if (mIdx === tIdx && mIdx === aIdx) {
					return `文本、音频与融合分支均倾向「${this.emotionLabelByIndex(mIdx)}」，结果稳定性较高。`;
				}
				if (mIdx === tIdx) {
					return '融合结果更接近文本分支，建议优先参考文字内容。';
				}
				if (mIdx === aIdx) {
					return '融合结果更接近音频分支，建议重点关注语音表达。';
				}
				return '文本与音频分支存在差异，融合分支已给出综合结论。';
			},
			probabilityBlocks() {
				const probs = (this.analysisObj && this.analysisObj.probabilities) || {};
				return [
					{ key: 'M', title: '融合分支 M', items: this.makeProbItems(probs.M) },
					{ key: 'T', title: '文本分支 T', items: this.makeProbItems(probs.T) },
					{ key: 'A', title: '音频分支 A', items: this.makeProbItems(probs.A) }
				];
			},
			branchCards() {
				return [
					{ key: 'M', title: '融合 M', label: this.branchPredictionLabel('M'), className: this.branchClass('M') },
					{ key: 'T', title: '文本 T', label: this.branchPredictionLabel('T'), className: this.branchClass('T') },
					{ key: 'A', title: '音频 A', label: this.branchPredictionLabel('A'), className: this.branchClass('A') }
				];
			},
			emotionPushList() {
				if (!this.hasAnalysis) {
					return [];
				}
				const idx = Number(this.normalizedPrediction) - 1;
				const packs = {
					0: [
						{ title: '低落预警关怀', desc: '模型检测到低落倾向，建议先降低任务难度并给自己短暂缓冲。', actionText: '去音乐页舒缓', action: 'music' },
						{ title: '结构化表达', desc: '把当前困扰拆成“事实-感受-下一步”三段，写下来会更清晰。', actionText: '去写减压笔记', action: 'notebook' },
						{ title: '回看自我支持', desc: '查看历史中你曾经走出低谷的记录，给自己更具体的信心。', actionText: '查看历史记录', action: 'history' }
					],
					1: [
						{ title: '稳定状态建议', desc: '你当前情绪较平稳，建议保持规律作息并记录今天做对的一件事。', actionText: '去写今日笔记', action: 'notebook' },
						{ title: '轻量放松内容', desc: '可尝试 5 分钟深呼吸或短时散步，帮助稳定保持专注。', actionText: '去音乐页放松', action: 'music' },
						{ title: '自我复盘提示', desc: '回看历史记录，找到让你稳定的触发点，后续可重复使用。', actionText: '查看历史记录', action: 'history' }
					],
					2: [
						{ title: '高兴能量延续', desc: '你当前状态明显高兴，适合推进一个关键任务并及时复盘。', actionText: '去写行动计划', action: 'notebook' },
						{ title: '节奏管理建议', desc: '建议用短时番茄钟保持节奏，避免高状态下过度消耗。', actionText: '去音乐页调节', action: 'music' },
						{ title: '成果沉淀提醒', desc: '把今天的积极因素记下来，作为之后低谷时的参考。', actionText: '查看历史记录', action: 'history' }
					]
				};
				return packs[idx] || packs[0];
			},
			isLowAlertCurrent() {
				return this.isLowAlertAnalysis(this.analysisObj);
			}
		},
		onLoad(options) {
			if (options && options.id) {
				this.noteId = options.id;
				this.simpleMode = String(options.simple || '') === '1';
				this.pendingSupportPrompt = String(options.supportPrompt || '') === '1';
				this.fetchModelStatus();
				this.fetchNoteDetail();
			}
		},
		onUnload() {
			if (this.supportPromptTimer) {
				clearTimeout(this.supportPromptTimer);
				this.supportPromptTimer = null;
			}
			this.showSupportPopup = false;
			this.supportCloseCallback = null;
		},
		methods: {
			fetchModelStatus() {
				uni.request({
					url: `${BASE_URL}/api/model-status`,
					method: 'GET',
					success: (res) => {
						if (res.statusCode === 200 && res.data) {
							this.modelReachable = !!res.data.reachable;
							this.modelStatusText = res.data.message || (this.modelReachable ? '可用' : '不可用');
						}
					}
				});
			},
			extractAnalyzeError(res) {
				if (!res || !res.data) {
					return '分析失败';
				}
				const payload = res.data;
				if (payload.detail) {
					if (typeof payload.detail === 'string') {
						return `${payload.error || '分析失败'}：${payload.detail}`;
					}
					try {
						return `${payload.error || '分析失败'}：${JSON.stringify(payload.detail)}`;
					} catch (e) {
						return payload.error || '分析失败';
					}
				}
				return payload.error || payload.message || '分析失败';
			},
			emotionMetaByIndex(idx) {
				const metas = [
					{ label: '低落预警', className: 'emotion-3', color: '#8b2f4f' },
					{ label: '平稳', className: 'emotion-1', color: '#2f7a6a' },
					{ label: '高兴', className: 'emotion-2', color: '#9a5a14' }
				];
				return metas[idx] || { label: `第 ${idx + 1} 类`, className: '', color: '#355067' };
			},
			emotionLabelByIndex(idx) {
				return this.emotionMetaByIndex(idx).label;
			},
			emotionColorByIndex(idx) {
				return this.emotionMetaByIndex(idx).color;
			},
			fetchNoteDetail() {
				const token = uni.getStorageSync('token');
				uni.request({
					url: `${BASE_URL}/api/notes/${this.noteId}`,
					header: { Authorization: `Bearer ${token}` },
					success: (res) => {
						if (res.statusCode === 200 && res.data) {
							this.title = res.data.title || '';
							this.noteContent = res.data.content || '';
							this.analyzedAt = res.data.analyzed_at || '';
							this.applyAnalysis(res.data.analysis_result);
						}
					}
				});
			},
			applyAnalysis(payload) {
				this.analysisObj = this.parseAnalysis(payload);
				this.expandedPushIndex = this.hasAnalysis ? 0 : -1;
				if (this.hasAnalysis) {
					this.fetchEmotionResources(String(this.normalizedPrediction || ''));
					if (this.pendingSupportPrompt && this.isLowAlertCurrent) {
						this.queueSupportPrompt(900);
					}
				} else {
					this.resourceImageText = [];
					this.resourceVideos = [];
					this.resourceMusic = [];
				}
			},
			parseAnalysis(payload) {
				return parseAnalysisPayload(payload);
			},
			branchPredictionIndex(branchKey) {
				const probs = this.analysisObj && this.analysisObj.probabilities && this.analysisObj.probabilities[branchKey];
				if (!Array.isArray(probs) || probs.length === 0) {
					return -1;
				}
				let maxIdx = 0;
				for (let i = 1; i < probs.length; i += 1) {
					if (Number(probs[i]) > Number(probs[maxIdx])) {
						maxIdx = i;
					}
				}
				return maxIdx;
			},
			normalizeProbArray(values) {
				if (!Array.isArray(values)) {
					return [];
				}
				return values.map((v) => {
					const num = Number(v);
					if (Number.isNaN(num)) {
						return 0;
					}
					return Math.max(0, Math.min(1, num));
				});
			},
			makeProbItems(values) {
				const normalized = this.normalizeProbArray(values);
				return normalized.map((p, idx) => ({
					label: this.emotionLabelByIndex(idx),
					color: this.emotionColorByIndex(idx),
					width: `${Math.max(2, p * 100)}%`,
					percent: this.toPercent(p)
				}));
			},
			branchPredictionLabel(branchKey) {
				const idx = this.branchPredictionIndex(branchKey);
				if (idx < 0) {
					return '-';
				}
				return `${this.emotionLabelByIndex(idx)}（第 ${idx + 1} 类）`;
			},
			branchClass(branchKey) {
				const idx = this.branchPredictionIndex(branchKey);
				return this.emotionMetaByIndex(idx).className;
			},
			toPercent(value) {
				const num = Number(value);
				if (Number.isNaN(num)) {
					return '0.00%';
				}
				return `${(num * 100).toFixed(2)}%`;
			},
			isLowAlertAnalysis(analysis) {
				return isLowAlertFromAnalysis(analysis);
			},
			suggestProfessionalSupport(onClose) {
				this.supportCloseCallback = typeof onClose === 'function' ? onClose : null;
				this.showSupportPopup = true;
			},
			closeSupportPopup() {
				this.showSupportPopup = false;
				const cb = this.supportCloseCallback;
				this.supportCloseCallback = null;
				if (typeof cb === 'function') {
					cb();
				}
			},
			confirmSupportPopup() {
				this.openSupportEntry();
				this.closeSupportPopup();
			},
			queueSupportPrompt(delay = 700) {
				if (this.simpleMode || this.hasShownSupportPrompt || !this.isLowAlertCurrent) {
					return;
				}
				if (this.supportPromptTimer) {
					clearTimeout(this.supportPromptTimer);
				}
				this.$nextTick(() => {
					this.supportPromptTimer = setTimeout(() => {
						this.suggestProfessionalSupport(() => {
							this.fetchModelStatus();
						});
						this.hasShownSupportPrompt = true;
						this.pendingSupportPrompt = false;
						this.supportPromptTimer = null;
					}, delay);
				});
			},
			openSupportEntry() {
				uni.showToast({ title: '请前往设置页查看咨询入口', icon: 'none' });
				uni.navigateTo({ url: '/pages/Setting/Setting' });
			},
			analyzeNow() {
				if (!this.noteId || this.isLoading) {
					return;
				}
				if (this.modelReachable === false) {
					const tip = this.modelStatusText || '模型服务不可用，请稍后重试';
					this.errorText = tip;
					uni.showToast({ title: tip, icon: 'none' });
					return;
				}
				this.errorText = '';
				this.isLoading = true;
				const token = uni.getStorageSync('token');
				uni.request({
					url: `${BASE_URL}/api/notes/${this.noteId}/analyze`,
					method: 'POST',
					header: { Authorization: `Bearer ${token}` },
					success: (res) => {
						this.isLoading = false;
						if (res.statusCode === 200 && res.data) {
							this.analyzedAt = res.data.analyzed_at || '';
							const analysis = this.parseAnalysis(res.data.analysis);
							this.applyAnalysis(analysis);
							uni.showToast({ title: '分析完成', icon: 'success' });
							if (this.isLowAlertAnalysis(analysis)) {
								this.queueSupportPrompt(850);
								return;
							}
							this.fetchModelStatus();
							return;
						}
						const msg = this.extractAnalyzeError(res);
						this.errorText = msg;
						uni.showToast({ title: msg, icon: 'none' });
					},
					fail: () => {
						this.isLoading = false;
						this.errorText = '网络错误，请稍后重试';
						uni.showToast({ title: this.errorText, icon: 'none' });
					}
				});
			},
			handlePushAction(action) {
				if (action === 'music') {
					uni.navigateTo({ url: '/pages/Music/Music' });
					return;
				}
				if (action === 'history') {
					uni.navigateTo({ url: '/pages/History_Page/History_Page' });
					return;
				}
				uni.navigateTo({ url: '/pages/MainNoteSet/MainNoteSet' });
			},
			togglePush(idx) {
				this.expandedPushIndex = this.expandedPushIndex === idx ? -1 : idx;
			},
			readPushInPage(item) {
				if (!item) {
					return;
				}
				uni.showModal({
					title: item.title || '情绪推送',
					content: item.desc || '暂无内容',
					showCancel: false,
					confirmText: '知道了'
				});
			},
			fetchEmotionResources(emotionTag) {
				uni.request({
					url: `${BASE_URL}/api/resource-bundles`,
					method: 'GET',
					data: { emotion: emotionTag || '' },
					success: (res) => {
						const body = res && res.data ? res.data : {};
						const payload = body.data && body.code === 0 ? body.data : body;
						const recommended = payload && payload.recommended_group ? payload.recommended_group : null;
						if (!recommended) {
							this.resourceImageText = [];
							this.resourceVideos = [];
							this.resourceMusic = [];
							return;
						}
						const imageText = Array.isArray(recommended.imageText) ? recommended.imageText : [];
						const videos = Array.isArray(recommended.videos) ? recommended.videos.filter((item) => !!(item && item.url)) : [];
						const music = Array.isArray(recommended.music) ? recommended.music : [];
						this.resourceImageText = imageText;
						this.resourceVideos = videos;
						this.resourceMusic = music;
					},
					fail: () => {
						this.resourceImageText = [];
						this.resourceVideos = [];
						this.resourceMusic = [];
					}
				});
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
			openVideoResource(item) {
				const rawUrl = String((item && item.url) || '');
				if (!rawUrl) {
					uni.showToast({ title: '视频地址为空', icon: 'none' });
					return;
				}
				const title = encodeURIComponent(item.title || '视频播放');
				const url = encodeURIComponent(rawUrl);
				uni.navigateTo({ url: `/pages/VideoPlayer/VideoPlayer?title=${title}&url=${url}` });
			},
			openMusicPage() {
				uni.navigateTo({ url: '/pages/Music/Music' });
			}
		}
	};
</script>

<style scoped lang="css">
	.note-content {
		display: block;
		font-size: 24rpx;
		line-height: 34rpx;
		color: #4f687e;
	}

	.simple-panel {
		background: rgba(255, 255, 255, 0.86);
		border: none;
		box-shadow: none;
	}

	.simple-text {
		display: block;
		font-size: 25rpx;
		line-height: 38rpx;
		color: #2a4257;
		margin-top: 8rpx;
	}

	.page {
		min-height: 100vh;
		background: linear-gradient(180deg, #f2f6f9 0%, #ecf1f6 40%, #eef4f8 100%);
		padding-top: calc(14rpx + env(safe-area-inset-top));
		padding-bottom: 170rpx;
		box-sizing: border-box;
	}

	.topbar {
		padding: 42rpx 28rpx;
		background: linear-gradient(120deg, #1f2a37 0%, #2b3d4f 65%, #3a5268 100%);
	}

	.topbar-title {
		font-size: 52rpx;
		line-height: 56rpx;
		font-weight: 700;
		color: #f5f8fb;
	}

	.content {
		padding: 24rpx;
	}

	.summary-card,
	.panel {
		background: #ffffff;
		border-radius: 20rpx;
		padding: 26rpx;
		margin-bottom: 20rpx;
		border: 1rpx solid #dde5ed;
		box-shadow: 0 8rpx 18rpx rgba(31, 42, 55, 0.06);
	}

	.summary-head {
		display: flex;
		flex-direction: column;
		gap: 10rpx;
	}

	.note-title {
		font-size: 34rpx;
		line-height: 42rpx;
		font-weight: 600;
		color: #1f2a37;
	}

	.analysis-time {
		font-size: 24rpx;
		line-height: 30rpx;
		color: #5f7184;
	}

	.summary-main {
		margin-top: 20rpx;
		padding: 20rpx;
		background: linear-gradient(120deg, #f5f9fd 0%, #eef4fb 100%);
		border-radius: 14rpx;
	}

	.summary-main.emotion-1 {
		background: linear-gradient(120deg, #edf8f4 0%, #e1f3ec 100%);
	}

	.summary-main.emotion-2 {
		background: linear-gradient(120deg, #fff7ea 0%, #ffefd9 100%);
	}

	.summary-main.emotion-3 {
		background: linear-gradient(120deg, #fff0f5 0%, #ffe6ef 100%);
	}

	.label {
		font-size: 24rpx;
		color: #5c7083;
	}

	.prediction-text {
		display: block;
		margin-top: 8rpx;
		font-size: 42rpx;
		line-height: 48rpx;
		font-weight: 700;
		color: #1e4f74;
	}

	.confidence-text {
		display: block;
		margin-top: 8rpx;
		font-size: 25rpx;
		color: #315f80;
	}

	.summary-desc {
		display: block;
		margin-top: 10rpx;
		font-size: 23rpx;
		line-height: 34rpx;
		color: #4f687e;
	}

	.empty-text {
		font-size: 26rpx;
		line-height: 36rpx;
		color: #667789;
	}

	.panel-title {
		font-size: 28rpx;
		font-weight: 600;
		color: #223444;
		margin-bottom: 16rpx;
	}

	.branch-row {
		display: flex;
		gap: 12rpx;
	}

	.branch-chip {
		flex: 1;
		padding: 14rpx 12rpx;
		border-radius: 12rpx;
		background: #f4f8fc;
		border: 1rpx solid #dbe5ef;
	}

	.branch-chip.emotion-1 {
		background: #edf8f4;
		border-color: #c9e8dd;
	}

	.branch-chip.emotion-2 {
		background: #fff6e8;
		border-color: #f6dfbc;
	}

	.branch-chip.emotion-3 {
		background: #fff0f4;
		border-color: #f4d3de;
	}

	.chip-key {
		display: block;
		font-size: 22rpx;
		color: #60778f;
	}

	.chip-val {
		display: block;
		margin-top: 6rpx;
		font-size: 27rpx;
		font-weight: 600;
		color: #1f2a37;
	}

	.prob-block {
		margin-bottom: 16rpx;
	}

	.prob-title {
		display: block;
		font-size: 24rpx;
		color: #4b6075;
		margin-bottom: 8rpx;
	}

	.bar-row {
		display: flex;
		align-items: center;
		margin-bottom: 8rpx;
	}

	.bar-label {
		width: 118rpx;
		font-size: 22rpx;
		color: #5d7287;
	}

	.bar-track {
		flex: 1;
		height: 14rpx;
		background: #e6edf4;
		border-radius: 999rpx;
		overflow: hidden;
	}

	.bar-fill {
		height: 100%;
		background: linear-gradient(90deg, #5c9ecf 0%, #3a6f98 100%);
		border-radius: 999rpx;
	}

	.bar-value {
		width: 120rpx;
		text-align: right;
		font-size: 22rpx;
		color: #2f475c;
	}

	.error-panel {
		background: #fff4f3;
		border-color: #f3d3ce;
	}

	.error-text {
		font-size: 24rpx;
		color: #a34135;
	}

	.push-list {
		display: flex;
		flex-direction: column;
		gap: 14rpx;
	}

	.push-item {
		padding: 18rpx;
		border-radius: 14rpx;
		background: linear-gradient(120deg, #f7fbff 0%, #eef6ff 100%);
		border: 1rpx solid #d9e8f8;
	}

	.push-head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 14rpx;
	}

	.push-title {
		font-size: 27rpx;
		line-height: 38rpx;
		font-weight: 600;
		color: #1d3850;
		display: block;
	}

	.push-desc {
		margin-top: 8rpx;
		font-size: 24rpx;
		line-height: 34rpx;
		color: #496782;
		display: block;
	}

	.push-toggle {
		font-size: 22rpx;
		line-height: 30rpx;
		color: #51708a;
		padding: 4rpx 10rpx;
		border-radius: 999rpx;
		background: #eaf2fa;
	}

	.push-actions {
		display: flex;
		gap: 10rpx;
		margin-top: 12rpx;
	}

	.push-action {
		align-self: flex-start;
		display: inline-flex;
		padding: 8rpx 20rpx;
		background: #1f4f7f;
		border-radius: 999rpx;
	}

	.push-action.muted {
		background: #e6edf4;
	}

	.push-action-text {
		font-size: 22rpx;
		line-height: 30rpx;
		color: #ffffff;
	}

	.push-action-text.dark {
		color: #2f4a5f;
	}

	.support-popup-mask {
		position: fixed;
		left: 0;
		right: 0;
		top: 0;
		bottom: 0;
		background: rgba(30, 33, 40, 0.48);
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 28rpx;
		z-index: 1200;
	}

	.support-popup-card {
		position: relative;
		width: 100%;
		max-width: 640rpx;
		border-radius: 28rpx;
		padding: 26rpx;
		background: linear-gradient(140deg, #fff5f7 0%, #fffdf6 65%, #f6fff8 100%);
		border: 2rpx solid #f6dce5;
		box-shadow: 0 24rpx 46rpx rgba(66, 38, 50, 0.26);
	}

	.support-popup-deco {
		position: absolute;
		font-size: 30rpx;
		color: #f08cab;
	}

	.support-popup-deco.left {
		left: 18rpx;
		top: 14rpx;
	}

	.support-popup-deco.right {
		right: 18rpx;
		top: 14rpx;
	}

	.support-header {
		display: flex;
		align-items: center;
		gap: 16rpx;
	}

	.support-avatar {
		width: 78rpx;
		height: 78rpx;
		border-radius: 50%;
		border: 3rpx solid #ffd7e4;
		background: #fff;
	}

	.support-head-text {
		flex: 1;
	}

	.support-title {
		display: block;
		font-size: 29rpx;
		font-weight: 700;
		color: #8d3955;
	}

	.support-subtitle {
		display: block;
		margin-top: 4rpx;
		font-size: 23rpx;
		color: #a95f76;
	}

	.support-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 10rpx;
		margin-top: 12rpx;
	}

	.support-tag {
		padding: 6rpx 14rpx;
		background: #fff0f5;
		border-radius: 999rpx;
		font-size: 21rpx;
		color: #964e65;
		border: 1rpx solid #f8d8e2;
	}

	.support-desc {
		display: block;
		margin-top: 12rpx;
		font-size: 24rpx;
		line-height: 34rpx;
		color: #744654;
	}

	.support-action {
		display: inline-flex;
		margin-top: 14rpx;
		padding: 10rpx 22rpx;
		border-radius: 999rpx;
		background: linear-gradient(120deg, #ff9fbc 0%, #ff7ea3 100%);
	}

	.support-action-text {
		font-size: 23rpx;
		font-weight: 600;
		color: #ffffff;
	}

	.support-popup-actions {
		display: flex;
		gap: 12rpx;
		margin-top: 16rpx;
	}

	.support-popup-btn {
		flex: 1;
		display: inline-flex;
		justify-content: center;
		align-items: center;
		padding: 12rpx 18rpx;
		border-radius: 999rpx;
	}

	.support-popup-btn.solid {
		background: linear-gradient(120deg, #ff9fbc 0%, #ff7ea3 100%);
	}

	.support-popup-btn.ghost {
		background: #fff;
		border: 1rpx solid #f0cdd8;
	}

	.support-popup-btn-text {
		font-size: 23rpx;
		font-weight: 600;
		color: #ffffff;
	}

	.support-popup-btn-text.ghost {
		color: #9a5a70;
	}

	.resource-panel {
		background: linear-gradient(180deg, #f8fbff 0%, #f3f8fd 100%);
	}

	.resource-subtitle {
		display: block;
		font-size: 23rpx;
		color: #597289;
		margin-bottom: 14rpx;
	}

	.resource-block {
		margin-bottom: 20rpx;
	}

	.resource-title {
		display: block;
		font-size: 25rpx;
		font-weight: 600;
		color: #284258;
		margin-bottom: 10rpx;
	}

	.resource-grid {
		display: grid;
		grid-template-columns: repeat(1, minmax(0, 1fr));
		gap: 10rpx;
	}

	.resource-scroll {
		margin-top: 8rpx;
	}

	.resource-row {
		display: flex;
		gap: 10rpx;
	}

	.resource-card {
		position: relative;
		background: #ffffff;
		border: 1rpx solid #d9e6f2;
		border-radius: 12rpx;
		padding: 14rpx;
	}

	.resource-badge {
		position: absolute;
		top: 10rpx;
		right: 10rpx;
		background: #2b4e48;
		color: #ffffff;
		font-size: 18rpx;
		padding: 4rpx 10rpx;
		border-radius: 999rpx;
	}

	.resource-cover {
		width: 100%;
		height: 200rpx;
		border-radius: 10rpx;
		margin-bottom: 10rpx;
		background: #e8f1f9;
	}

	.resource-video-cover {
		width: 100%;
		height: 170rpx;
		border-radius: 10rpx;
		margin-bottom: 10rpx;
		background: #e8f1f9;
	}

	.resource-name {
		display: block;
		font-size: 26rpx;
		font-weight: 600;
		color: #203a4d;
	}

	.resource-desc {
		display: block;
		margin-top: 6rpx;
		font-size: 23rpx;
		line-height: 34rpx;
		color: #4a667f;
	}

	.h-card {
		width: 380rpx;
	}


	.resource-action {
		display: inline-flex;
		margin-top: 10rpx;
		padding: 8rpx 18rpx;
		border-radius: 999rpx;
		background: #e7eff7;
	}

	.resource-action.primary {
		background: #214f7a;
	}

	.resource-action-text {
		font-size: 22rpx;
		color: #2d4f68;
	}

	.resource-action-text.light {
		color: #ffffff;
	}

	.resource-empty {
		display: block;
		font-size: 23rpx;
		color: #6a8093;
	}

	@media (max-width: 420px) {
		.resource-grid {
			grid-template-columns: repeat(1, minmax(0, 1fr));
		}
	}

	.actions {
		display: flex;
		justify-content: flex-end;
		padding: 6rpx 0 30rpx;
	}

	.btn {
		padding: 16rpx 28rpx;
		border-radius: 12rpx;
		background: linear-gradient(120deg, #263747 0%, #355067 100%);
	}

	.btn-disabled {
		opacity: 0.72;
	}

	.btn-text {
		color: #f3f7fb;
		font-size: 26rpx;
		font-weight: 600;
	}
</style>
