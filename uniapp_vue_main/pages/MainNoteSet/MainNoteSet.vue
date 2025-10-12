<template>
	<view class="flex-col page">
		<view class="flex-col justify-start items-start text-wrapper"><text class="text">暖言纸条</text></view>
		<view class="flex-col section mt-21">
			<view class="flex-row group">
				<view class="flex-row justify-between flex-1 section_2">
					<text class="font text_2">搜索笔记</text>
					<image class="image"
						src="https://ide.code.fun/api/image?token=68eb23dc9520a30011f3beeb&name=4aab7942bbb248ea1508400d3100f725.png" />
				</view>
				<view class="ml-14 flex-col justify-start items-center shrink-0 text-wrapper_2">
					<text class="font text_3">搜索</text>
				</view>
			</view>
			
			<view class="flex-row justify-between items-center section_3">
				<view class="flex-col items-start">
					<text class="text_4">笔记标题</text>
					<text class="text_5 mt-11">2025-10-12</text>
				</view>
				<view class="flex-row">
					<image class="image_2"
						src="https://ide.code.fun/api/image?token=68eb23dc9520a30011f3beeb&name=b222b87d510dbb319fb6478585ec803d.png" />
					<image class="image_3"
						src="https://ide.code.fun/api/image?token=68eb23dc9520a30011f3beeb&name=2a9bbd492d5ab45a3db0b0699ea2d726.png" />
				</view>
			</view>
			
			<view class="flex-row group_2">
				<view class="flex-col justify-start items-center text-wrapper_3">
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
						src="https://ide.code.fun/api/image?token=68eb23dc9520a30011f3beeb&name=630fdbc11dccdc6d74ad3cecdd9496de.png" />
				</view>
				<view class="flex-col justify-start items-center equal-division-item">
					<image class="image_4"
						src="https://ide.code.fun/api/image?token=68eb23dc9520a30011f3beeb&name=85e6c4051832477789a9c724127ba087.png" />
				</view>
				<view class="flex-col justify-start items-center equal-division-item">
					<image class="image_4"
						src="https://ide.code.fun/api/image?token=68eb23dc9520a30011f3beeb&name=3de231db41c1ba966cf2300f4c51043e.png" />
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
			return {};
		},

		methods: {},
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