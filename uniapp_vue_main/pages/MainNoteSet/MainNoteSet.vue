<template>
	<view class="flex-col page">
		<view class="flex-col justify-start items-start text-wrapper"><text class="text">MoodWeather</text></view>
		<view class="flex-col section mt-21">
			<view class="flex-row group">
				<view class="flex-row justify-between flex-1 section_2">
					<textarea class="font text_2" placeholder="请输入标题"></textarea>
					<image class="image"
						src="https://ide.code.fun/api/image?token=68eb23dc9520a30011f3beeb&name=4aab7942bbb248ea1508400d3100f725.png" />
				</view>
				<view class="ml-14 flex-col justify-start items-center shrink-0 text-wrapper_2">
					<text class="font text_3">搜索</text>
				</view>
			</view>
			
			<view v-for="note in notes" :key="note.id" class="flex-row justify-between items-center section_3"
				@click="toEdit(note.id)">
				<view class="flex-col items-start">
					<text class="text_4">{{ note.title }}</text>
					<text class="text_5 mt-11">{{ formatDateTime(note.created_at) }}</text>
				</view>
				<view class="flex-row">
					<view class="view-btn" @click.stop="viewAnalysis(note)"><text class="view-text">查看</text></view>
					<view class="analyze-btn" @click.stop="analyzeNote(note.id)"><text class="analyze-text">分析</text></view>
					<image class="image_2" src="/static/image/smileICON.png" />
					<image class="image_3" src="/static/image/DeleteICon.png" @click.stop="confirmDelete(note.id)" />
				</view>
			</view>
			
			<view class="flex-row group_2">
				<view class="flex-col justify-start items-center text-wrapper_3" @click="toEdit(null)">
					<text class="font text_6">创建新的笔记</text>
				</view>
				<view class="flex-col justify-start items-center text-wrapper_4 ml-45">
					<text class="font text_7">查看我的报告</text>
				</view>
			</view>
		</view>
		<view class="flex-col justify-start section_4 mt-21">
			<view class="flex-row justify-between equal-division">
				<view class="flex-col justify-start items-center equal-division-item">
					<image class="image_4"
						src="/static/image/home.png" />
				</view>
				<view class="flex-col justify-start items-center equal-division-item">
					<image class="image_4"
						src="/static/image/setting.png" />
				</view>
				<view class="flex-col justify-start items-center equal-division-item">
					<image class="image_4"
						src="/static/image/music.png" />
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import { BASE_URL } from '@/common/config.js';

	export default {
		components: {},
		props: {},
		data() {
			return {
				notes: []
			};
		},
		onLoad() {
			this.fetchNotes();
		},
		onShow() {
			this.fetchNotes();
		},
		methods: {
			formatDateTime(value) {
				if (!value) return '--';
				const normalized = String(value).replace(' ', 'T').replace(/\.\d+Z$/, 'Z');
				const d = new Date(normalized);
				if (Number.isNaN(d.getTime())) {
					return String(value).replace('T', ' ');
				}
				const y = d.getFullYear();
				const m = `${d.getMonth() + 1}`.padStart(2, '0');
				const day = `${d.getDate()}`.padStart(2, '0');
				const hh = `${d.getHours()}`.padStart(2, '0');
				const mm = `${d.getMinutes()}`.padStart(2, '0');
				const ss = `${d.getSeconds()}`.padStart(2, '0');
				return `${y}-${m}-${day} ${hh}:${mm}:${ss}`;
			},
			fetchNotes() {
				const token = uni.getStorageSync('token');
				uni.request({
					url: `${BASE_URL}/api/notes`,
					header: { 'Authorization': 'Bearer ' + token },
					success: (res) => {
						if (res.statusCode === 200 && Array.isArray(res.data)) {
							this.notes = res.data;
						}
					}
				});
			},
			confirmDelete(noteId) {
				uni.showModal({
					title: '删除笔记',
					content: '确定要删除这条笔记吗？',
					success: (res) => {
						if (res.confirm) {
							this.deleteNote(noteId);
						}
					}
				});
			},
			deleteNote(noteId) {
				const token = uni.getStorageSync('token');
				uni.request({
					url: `${BASE_URL}/api/notes/${noteId}`,
					method: 'DELETE',
					header: { 'Authorization': 'Bearer ' + token },
					success: (res) => {
						if (res.statusCode === 200) {
							uni.showToast({ title: '删除成功', icon: 'success' });
							this.fetchNotes();
						} else {
							uni.showToast({ title: '删除失败', icon: 'none' });
						}
					},
					fail: () => {
						uni.showToast({ title: '网络错误', icon: 'none' });
					}
				});
			},
			toEdit(noteId) {
				const url = noteId ? `/pages/EditNote/EditNote?id=${noteId}` : '/pages/EditNote/EditNote';
				uni.navigateTo({ url });
			},
			viewAnalysis(note) {
				if (!note || !note.analysis_result) {
					uni.showToast({ title: '该笔记还没有分析结果', icon: 'none' });
					return;
				}
				uni.navigateTo({ url: `/pages/NoteAnalysis/NoteAnalysis?id=${note.id}` });
			},
			analyzeNote(noteId) {
				const token = uni.getStorageSync('token');
				uni.showLoading({ title: '分析中...' });
				uni.request({
					url: `${BASE_URL}/api/notes/${noteId}/analyze`,
					method: 'POST',
					header: { 'Authorization': 'Bearer ' + token },
					success: (res) => {
						uni.hideLoading();
						if (res.statusCode === 200) {
							uni.navigateTo({ url: `/pages/NoteAnalysis/NoteAnalysis?id=${noteId}` });
						} else if (res.statusCode === 501) {
							uni.showToast({ title: '模型服务未配置', icon: 'none' });
						} else {
							uni.showToast({ title: '分析失败', icon: 'none' });
						}
					},
					fail: () => {
						uni.hideLoading();
						uni.showToast({ title: '网络错误', icon: 'none' });
					}
				});
			}
		},
	};
</script>

<style scoped lang="css">
	.mt-11 {
		margin-top: 20.02rpx;
	}

	.ml-45 {
		margin-left: 81.92rpx;
	}

	.mt-21 {
		margin-top: 38.23rpx;
	}

	.page {
		background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/68eb23ae9520a30011f3bed5/17602405794719744028.png);
		background-size: 100% 100%;
		background-repeat: no-repeat;
		width: 100%;
		overflow-y: auto;
		overflow-x: hidden;
		height: 100%;
	}

	.text-wrapper {
		padding: 40.05rpx 0;
		background-color: #d9d9d9b3;
	}

	.text {
		margin-left: 25.49rpx;
		color: #000000;
		font-size: 65.53rpx;
		font-family: Inter;
		line-height: 60.62rpx;
	}

	.section {
		margin-left: 36.41rpx;
		margin-right: 29.13rpx;
		padding: 0 20.02rpx 16.38rpx;
		background-color: #e9e9e9d4;
		border-radius: 9.1rpx;
	}

	.group {
		padding: 21.84rpx 0;
	}

	.section_2 {
		padding: 21.84rpx 29.13rpx;
		background-color: #ffffff;
		border-radius: 18202.06rpx;
		overflow: hidden;
		height: 74.64rpx;
		border-left: solid 1.82rpx #d9d9d9;
		border-right: solid 1.82rpx #d9d9d9;
		border-top: solid 1.82rpx #d9d9d9;
		border-bottom: solid 1.82rpx #d9d9d9;
	}

	.font {
		font-size: 29.13rpx;
		font-family: Inter;
		line-height: 27.12rpx;
		color: #f5f5f5;
	}

	.text_2 {
		color: #1e1e1e;
	}

	.image {
		width: 29.13rpx;
		height: 29.13rpx;
	}

	.text-wrapper_2 {
		padding: 21.84rpx 0;
		background-color: #2c2c2c;
		border-radius: 14.56rpx;
		overflow: hidden;
		width: 100.12rpx;
		height: 72.82rpx;
		border-left: solid 1.82rpx #2c2c2c;
		border-right: solid 1.82rpx #2c2c2c;
		border-top: solid 1.82rpx #2c2c2c;
		border-bottom: solid 1.82rpx #2c2c2c;
	}

	.text_3 {
		line-height: 27rpx;
	}

	.section_3 {
		margin-top: 43.69rpx;
		padding: 14.56rpx 14.56rpx 14.56rpx 21.84rpx;
		background-color: #ffffff;
		border-radius: 5.46rpx;
		border-left: solid 1.82rpx #000000;
		border-right: solid 1.82rpx #000000;
		border-top: solid 1.82rpx #000000;
		border-bottom: solid 1.82rpx #000000;
	}

	.text_4 {
		color: #000000;
		font-size: 43.69rpx;
		font-family: Inter;
		line-height: 40.38rpx;
	}

	.text_5 {
		margin-left: 3.64rpx;
		color: #000000;
		font-size: 25.49rpx;
		font-family: Inter;
		line-height: 19.04rpx;
	}

	.image_2 {
		width: 94.66rpx;
		height: 94.66rpx;
	}

	.image_3 {
		width: 98.3rpx;
		height: 98.3rpx;
	}

	.analyze-btn {
		margin-right: 12rpx;
		padding: 8rpx 16rpx;
		background-color: #2c2c2c;
		border-radius: 10rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		height: 52rpx;
	}

	.analyze-text {
		color: #f5f5f5;
		font-size: 22rpx;
	}

	.view-btn {
		margin-right: 10rpx;
		padding: 8rpx 16rpx;
		background-color: #4a5a6a;
		border-radius: 10rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		height: 52rpx;
	}

	.view-text {
		color: #f5f5f5;
		font-size: 22rpx;
	}

	.group_2 {
		margin-top: 926.58rpx;
		padding: 0 5.46rpx;
	}

	.text-wrapper_3 {
		padding: 21.84rpx 0;
		flex: 1 1 273.06rpx;
		background-color: #5a5a5a;
		border-radius: 14.56rpx;
		overflow: hidden;
		height: 72.82rpx;
		border-left: solid 1.82rpx #2c2c2c;
		border-right: solid 1.82rpx #2c2c2c;
		border-top: solid 1.82rpx #2c2c2c;
		border-bottom: solid 1.82rpx #2c2c2c;
	}

	.text_6 {
		line-height: 27.05rpx;
	}

	.text-wrapper_4 {
		padding: 21.84rpx 0;
		flex: 1 1 273.06rpx;
		background-color: #f5f5f5;
		border-radius: 14.56rpx;
		overflow: hidden;
		height: 72.82rpx;
		border-left: solid 1.82rpx #2c2c2c;
		border-right: solid 1.82rpx #2c2c2c;
		border-top: solid 1.82rpx #2c2c2c;
		border-bottom: solid 1.82rpx #2c2c2c;
	}

	.text_7 {
		color: #424242;
		line-height: 27.18rpx;
	}

	.section_4 {
		padding: 14.56rpx 0;
		background-image: linear-gradient(180.9deg, #575757bf 4.2%, #bdbdbdbf 96.2%);
		overflow: hidden;
	}

	.equal-division {
		margin-left: 36.41rpx;
		margin-right: 29.13rpx;
	}

	.equal-division-item {
		padding: 7.28rpx 0;
		background-color: #d9d9d980;
		border-radius: 14.56rpx;
		width: 109.22rpx;
		height: 109.22rpx;
		border-left: solid 1.82rpx #000000;
		border-right: solid 1.82rpx #000000;
		border-top: solid 1.82rpx #000000;
		border-bottom: solid 1.82rpx #000000;
	}

	.image_4 {
		width: 87.38rpx;
		height: 87.38rpx;
	}
</style>