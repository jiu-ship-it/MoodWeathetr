<template>
	<view class="flex-col justify-start relative page">
		<view class="shrink-0 section"></view>
		<view class="flex-col justify-start items-start text-wrapper pos"><text class="text">MoodWeather</text></view>
		<view class="flex-col section_2 pos_2">
			<text class="self-start font text_2">Music</text>
			<text class="self-start font_2 text_3">音乐</text>
			<view class="shrink-0 self-stretch divider view"></view>
			<view class="flex-col self-stretch group">
				<view class="flex-col group_2 ">

					<scroll-view class="scrollSize" scroll-y="true">
						<view class="flex-col items-start group_3" v-for="(current, idx) in MusicData" :key="`${current.name}-${idx}`" @tap="playMusic(current)">
							<text class="font_2">{{current.name}}</text>
							<text class="mt-10 self-start font">创作者：{{current.author}}</text>
						</view>
					</scroll-view>

					<view class="PauseAndStart">
						<view class="PauseIcon" @tap="PauseButton">{{isPlay}}</view>
					</view>
					
				</view>
				<view class="flex-col justify-start group_5">
					<view class="divider view_2"></view>
				</view>
			</view>
		</view>

		<BottomNav current="music" />

	</view>
</template>

<script>
	import BottomNav from '@/components/BottomNav.vue';
	import { BASE_URL } from '@/common/config.js';

	export default {
		components: { BottomNav },
		data() {
			return {
				MusicData: [{
						name: "Calm Demo",
						author: "WarmLabel",
						url: `${BASE_URL}/api/local-resources/audio/calm_demo.mp3`
					},
				],
				OnPlayData: null,
				BackgroundAudio: null,
				downloadedAudioCache: {},
				CurrentTrackName: '',
				isPlay: "▶", //▍▍
				ChangeIsPlay: true,
			};
		},
		onShow() {
			this.loadMusicList();
			this.OnPlayData = getApp().globalData.backgroundAudioCtx;
			if(this.OnPlayData == null || getApp().globalData.isPause == true){
				this.isPlay = "▶";
			}else if(getApp().globalData.isPause == false && this.OnPlayData != null){
				this.isPlay = "⏸";
			};
		},

		methods: {
			loadMusicList() {
				uni.request({
					url: `${BASE_URL}/api/music-recommendations`,
					method: 'GET',
					success: (res) => {
						const payload = res && res.data ? res.data : {};
						const items = Array.isArray(payload.items) ? payload.items : [];
						if (items.length) {
							this.MusicData = items;
						}
					},
					fail: () => {
						uni.showToast({ title: '音乐加载失败', icon: 'none' });
					}
				});
			},
			async playMusic(track) {
				const src = track && track.url;
				if (!src) {
					uni.showToast({ title: '音频地址为空', icon: 'none' });
					return;
				}
				this.CurrentTrackName = (track && track.name) || '情绪音乐';
				// #ifdef MP-WEIXIN
				try {
					const localSrc = await this.resolvePlayableSource(src);
					this.playMusicInMiniProgram(localSrc, this.CurrentTrackName);
				} catch (e) {
					uni.showToast({ title: '小程序音频加载失败', icon: 'none' });
				}
				return;
				// #endif
				this.playMusicInCommonPlatform(src);
			},
			resolvePlayableSource(src) {
				return new Promise((resolve, reject) => {
					if (!src) {
						reject(new Error('empty src'));
						return;
					}
					if (this.downloadedAudioCache[src]) {
						resolve(this.downloadedAudioCache[src]);
						return;
					}
					if (!/^https?:\/\//i.test(src)) {
						resolve(src);
						return;
					}
					uni.downloadFile({
						url: src,
						success: (res) => {
							if (res.statusCode === 200 && res.tempFilePath) {
								this.downloadedAudioCache[src] = res.tempFilePath;
								resolve(res.tempFilePath);
								return;
							}
							reject(new Error('download failed'));
						},
						fail: () => reject(new Error('download failed'))
					});
				});
			},
			playMusicInCommonPlatform(src) {
				const audioContext = uni.createInnerAudioContext();
				if (this.OnPlayData != null) {
					this.OnPlayData.pause();
					this.OnPlayData.offPlay();
					this.OnPlayData.offPause();
					this.OnPlayData.offEnded();
					this.OnPlayData.offError();
					this.OnPlayData.destroy(); //移除实例
					this.OnPlayData = false;
					this.isPlay = "▶";
				}
				audioContext.src = src;
				audioContext.volume = 1;
				audioContext.loop = false; //防止循环播放
				audioContext.onError(() => {
					uni.showToast({ title: '音频播放失败', icon: 'none' });
				});
				this.OnPlayData = audioContext; //保存实例数据
				getApp().globalData.backgroundAudioCtx = this.OnPlayData
				audioContext.play() //开始播放
				this.isPlay = "⏸";
				this.ChangeIsPlay = true;
			},
			playMusicInMiniProgram(src, title) {
				if (!this.BackgroundAudio) {
					this.BackgroundAudio = uni.getBackgroundAudioManager();
					this.BackgroundAudio.onError((err) => {
						const msg = err && err.errCode ? `播放失败(${err.errCode})` : '小程序音频播放失败';
						uni.showToast({ title: msg, icon: 'none' });
						this.isPlay = "▶";
						this.ChangeIsPlay = false;
					});
					this.BackgroundAudio.onEnded(() => {
						this.isPlay = "▶";
						this.ChangeIsPlay = false;
					});
				}
				this.BackgroundAudio.title = title || '情绪音乐';
				this.BackgroundAudio.singer = 'MoodWeather';
				this.BackgroundAudio.src = src;
				this.isPlay = "⏸";
				this.ChangeIsPlay = true;
			},
			PauseButton() {//暂停按键
				this.ChangeIsPlay = !this.ChangeIsPlay;
				// #ifdef MP-WEIXIN
				if (this.BackgroundAudio) {
					if (this.ChangeIsPlay) {
						this.isPlay = "⏸";
						this.BackgroundAudio.play();
						getApp().globalData.isPause = false;
					} else {
						this.isPlay = "▶";
						this.BackgroundAudio.pause();
						getApp().globalData.isPause = true;
					}
					return;
				}
				// #endif
				if(this.ChangeIsPlay && this.OnPlayData != null){
					this.isPlay = "⏸";
					this.OnPlayData.play();
					getApp().globalData.isPause = false;
				}else if(this.ChangeIsPlay == false || this.OnPlayData == null){
					this.isPlay = "▶";
					if (this.OnPlayData) {
						this.OnPlayData.pause();
					}
					getApp().globalData.isPause = true;
				}
			},
		},
	};
</script>

<style scoped lang="css">
	.scrollSize {
		position: fixed;
		height: 600rpx;
		width: 95%;
	}

	.page {
		background-color: #d3d3d3;
		overflow: hidden;
		background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163844605899734.png);
		background-size: 100% 100%;
		background-repeat: no-repeat;
		width: 100%;
		overflow-y: auto;
		overflow-x: hidden;
		height: 100%;
	}

	.section {
		background-color: #24242433;
		overflow: hidden;
		background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163844605899734.png);
		background-size: 100% 100%;
		background-repeat: no-repeat;
		width: 750rpx;
		height: 1669.3rpx;
	}

	.text-wrapper {
		padding: 40.05rpx 0;
		background-color: #d9d9d9b3;
	}

	.pos {
		position: absolute;
		left: 0;
		right: 0;
		top: 0;
	}

	.text {
		margin-left: 21.84rpx;
		color: #000000;
		font-size: 65.53rpx;
		font-family: Inter;
		line-height: 60.62rpx;
	}

	.section_2 {
		padding: 36.41rpx 7.28rpx 0 14.56rpx;
		background-color: #e5e5e5fa;
		border-radius: 14.56rpx;
		filter: drop-shadow(0rpx 7.28rpx 3.64rpx #0c0c0d0d, 0rpx 7.28rpx 3.64rpx #0c0c0d1a);
		overflow: hidden;
		border-left: solid 1.82rpx #d9d9d9;
		border-right: solid 1.82rpx #d9d9d9;
		border-top: solid 1.82rpx #d9d9d9;
		border-bottom: solid 1.82rpx #d9d9d9;
	}

	.pos_2 {
		position: absolute;
		left: 45.51rpx;
		right: 43.67rpx;
		top: 50%;
		transform: translateY(-50%);
	}

	.font {
		font-size: 25.49rpx;
		font-family: Inter;
		line-height: 23.45rpx;
		color: #757575;
	}

	.text_2 {
		margin-left: 32.77rpx;
		line-height: 19.41rpx;
	}

	.font_2 {
		font-size: 29.13rpx;
		font-family: Inter;
		line-height: 26.83rpx;
		color: #1e1e1e;
	}

	.text_3 {
		margin-left: 29.13rpx;
		margin-top: 14.56rpx;
		font-weight: 600;
		line-height: 27.34rpx;
	}

	.divider {
		background-color: #d9d9d9;
		height: 1.82rpx;
	}

	.view {
		margin: 29.13rpx 29.13rpx 0;
	}

	.group {
		padding-top: 14.56rpx;
	}

	.group_2 {
		padding-bottom: 784.59rpx;
		border-radius: 14.56rpx;
		overflow: hidden;
	}

	.group_3 {
		padding: 29.13rpx;
		border-radius: 14.56rpx;
		overflow: hidden;
	}

	.group_5 {
		padding: 14.56rpx 0;
		border-radius: 14.56rpx;
	}

	.view_2 {
		margin: 0 29.13rpx;
	}



	.PauseAndStart {
		position: fixed;
		left: 0;
		bottom: 10%;
		width: 100%;
		/* 宽度占满整个屏幕 */
		height: 80rpx;
		/* 自定义高度 */

		/* 2. 使用 Flexbox 进行布局 */
		display: flex;
		justify-content: center;
		/* 水平居中 */
		align-items: center;
		/* 垂直居中 (针对容器内的子元素) */
	}
	.PauseIcon{
		font-size: 300%;
	}
</style>