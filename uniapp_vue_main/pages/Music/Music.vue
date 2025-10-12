<template>
	<view class="flex-col justify-start relative page">
		<view class="shrink-0 section"></view>
		<view class="flex-col justify-start items-start text-wrapper pos"><text class="text">暖言纸条</text></view>
		<view class="flex-col section_2 pos_2">
			<text class="self-start font text_2">Music</text>
			<text class="self-start font_2 text_3">音乐</text>
			<view class="shrink-0 self-stretch divider view"></view>
			<view class="flex-col self-stretch group">
				<view class="flex-col group_2 ">

					<scroll-view class="scrollSize" scroll-y="true">
						<li class="flex-col items-start group_3" v-for="current in MusicData">
							<view class="flex-col items-start group_3" @click="playMusic(current.url)">
								<text class="font_2">{{current.name}}</text>
								<text class="mt-10 self-start font">创作者：{{current.author}}</text>
							</view>
						</li>
					</scroll-view>

					<view class="PauseAndStart">
						<view class="PauseIcon"  @click="PauseButton">{{isPlay}}</view>
					</view>
					
				</view>
				<view class="flex-col justify-start group_5">
					<view class="divider view_2"></view>
				</view>
			</view>
		</view>

		<view class="flex-col justify-start section_3 pos_3">
			<view class="flex-row justify-between equal-division">
				<view class="flex-col justify-start items-center equal-division-item">
					<image class="image" src="/static/image/home.png" />
				</view>
				<view class="flex-col justify-start items-center equal-division-item">
					<image class="image" src="/static/image/setting.png" />
				</view>
				<view class="flex-col justify-start items-center equal-division-item">
					<image class="image" src="/static/image/music.png" />
				</view>
			</view>
		</view>

	</view>
</template>

<script>
	export default {
		components: {},
		props: {},
		data() {
			return {
				MusicData: [{
						name: "鸳鸯债",
						author: "纸嫁衣",
						url: "https://m801.music.126.net/20251007132244/e2a4fb786e7c10da82d45b0efed6e3ba/jdymusic/obj/wo3DlMOGwrbDjj7DisKw/12624068215/cac2/00b9/ab3b/2df6bfb2c29586555b2c0a6b6573ca87.mp3?vuutv=BB+xX5kBKQHb0UFeIa9fHYGT2dQQG6cY+xqHV9xw2ws8V2O17hIgC2Vyi1JKsU9o2UzJiClBAS66rqBX1AFmp2NowV4RKpXYrRCz8tdGnhArmqzqpuqygCGf4LAkxCzmHAAms97LsVyxl3xc4m6YrA==&cdntag=bWFyaz1vc193ZWIscXVhbGl0eV9zdGFuZGFyZA"
					},
					{
						name: "abc",
						author: "123",
						url: "null"
					},
					{
						name: "abc",
						author: "123",
						url: "null"
					},
					{
						name: "abc",
						author: "123",
						url: "null"
					}
				],
				OnPlayData: null,
				isPlay: "▶", //▍▍
				ChangeIsPlay: true,
			};
		},
		onShow() {
			//this.fetchMusicAPI();
			this.OnPlayData = getApp().globalData.backgroundAudioCtx;
			if(this.OnPlayData == null || getApp().globalData.isPause == true){
				this.isPlay = "▶";
			}else if(getApp().globalData.isPause == false && this.OnPlayData != null){
				this.isPlay = "⏸";
			};
		},

		methods: {
			fetchMusicAPI() {
				uni.request({
					url: 'http://192.168.28.1:5000/API/music',
					method: 'GET',
					success: (res) => {
						console.log('从 Flask 获取到的数据:', res.data);
						this.MusicData = res.data;
					},
					fail(err) {
						console.log('失败', err.data);
					},
				})
			},
			playMusic(res) {
				const audioContext = uni.createInnerAudioContext();
				if (this.OnPlayData == null) {
					console.log("null") //初始值判断
				} else {
					uni.removeStorageSync('NowPlay');
					this.OnPlayData.pause();
					this.OnPlayData.offPlay();
					this.OnPlayData.offPause();
					this.OnPlayData.offEnded();
					this.OnPlayData.offError();
					this.OnPlayData.destroy(); //移除实例
					this.OnPlayData = false;
					this.isPlay = "▶";
				}
				audioContext.src = res;
				audioContext.volume = 1;
				audioContext.loop = false; //防止循环播放
				this.OnPlayData = audioContext; //保存实例数据
				getApp().globalData.backgroundAudioCtx = this.OnPlayData
				audioContext.play() //开始播放
				this.isPlay = "⏸";
				this.ChangeIsPlay = true;
			},
			PauseButton() {//暂停按键
				this.ChangeIsPlay = !this.ChangeIsPlay;
				if(this.ChangeIsPlay && this.OnPlayData != null){
					this.isPlay = "⏸";
					this.OnPlayData.play();
					getApp().globalData.isPause = false;
				}else if(this.ChangeIsPlay == false || this.OnPlayData == null){
					this.isPlay = "▶";
					this.OnPlayData.pause();
					getApp().globalData.isPause = true;
				}
			},

		},
	};
</script>

<style scoped lang="css">
	.mt-11 {
		margin-top: 20.02rpx;
	}

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

	.group_4 {
		border-radius: 14.56rpx;
		width: 50.97rpx;
		height: 29.13rpx;
	}

	.group_5 {
		padding: 14.56rpx 0;
		border-radius: 14.56rpx;
	}

	.view_2 {
		margin: 0 29.13rpx;
	}

	.section_3 {
		padding: 14.56rpx 0;
		background-image: linear-gradient(180.9deg, #575757bf 4.2%, #bdbdbdbf 96.2%);
		overflow: hidden;
	}

	.pos_3 {
		position: absolute;
		left: 0;
		right: 0;
		top: 1529.13rpx;
	}

	.equal-division {
		margin: 0 32.77rpx;
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

	.image {
		width: 87.38rpx;
		height: 87.38rpx;
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