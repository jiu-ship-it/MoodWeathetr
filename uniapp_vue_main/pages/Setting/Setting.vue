<template>
	<view class="page flex-col section">
		<view class="halfColor">
			<view class="flex-col justify-start items-start text-wrapper pos"><text class="text">MoodWeather</text></view>
			
			<view><!-- 设置列表 -->
				<view class="list-group listPos">
				  <navigator :class="{disabled:isListVisible}" class="list-group-item list-group-item-action listColor" aria-current="true" @click="ProSet">个性化设置</navigator>
				  <navigator :class="{disabled:isListVisible}" class="list-group-item list-group-item-action listColor">语言设置：中文</navigator>
				  <navigator :class="{disabled:isListVisible}" class="list-group-item list-group-item-action listColor">您的奖章</navigator>
				  <navigator :class="{disabled:isListVisible}" class="list-group-item list-group-item-action listColor">隐私条款</navigator>
				  <navigator :class="{disabled:isListVisible}" class="list-group-item list-group-item-action listColor">关于我们</navigator>
				</view>
			</view>

			<view class="ProfitThings ProfitPos"><!-- 个人简介 -->
				<view class="jumbotron jumbotron-fluid ProfitPos">
				  <view class="container">
				    <h1 class="display-4">名称：{{MyName}}</h1>
				    <p class="lead">简介：{{Introduction}}</p>
				  </view>
				</view>
			</view>
			<view>
				<img src="static/image/smileICON.png" alt="头像" class="ProImag"/>
			</view>
			
			<view class="jumbotron jumbotron-fluid jumbotron_pos" :style="{visibility:isEditData}">
			  <view class="container">
			    <form>
			      <view class="form-group">
			        <label for="exampleInputEmail1">新昵称(每月修改一次)</label>
			        <input class="form-control"><!-- 名称修改 -->
			      </view>
			      <view class="form-group">
			        <label for="exampleInputPassword1">个人简介(50字)</label>
			        <input class="form-control">
			      </view>
			      <button type="submit" class="btn btn-primary">提交</button>
				  <button type="submit" class="CancelButton btn btn-primary" @click="ProEditCancel">取消</button>
			    </form>
			  </view>
			</view>

			<BottomNav current="setting" />
		</view>
	</view>
</template>

<script>
	import BottomNav from '@/components/BottomNav.vue';

	export default {
		components: { BottomNav },
		data() {
			return {
				MyName:"ME",//名称
				Introduction:"helloWorld",//简介
				isListVisible:false,//是否可使用列表
				isEditData:"hidden",//编辑隐藏
			};
		},

		methods: {
			ProSet(){
				this.isListVisible = true;
				this.isEditData = "visible";
			},
			ProEditCancel(){
				this.isListVisible = false;
				this.isEditData = "hidden";
			},

		},
	};
</script>

<style scoped lang="css">
	.container {
		padding: 24rpx;
	}

	.jumbotron {
		background: rgba(255, 255, 255, 0.9);
		border-radius: 16rpx;
		padding: 20rpx;
	}

	.display-4 {
		font-size: 34rpx;
		line-height: 1.4;
		margin: 0;
	}

	.lead {
		font-size: 26rpx;
		line-height: 1.5;
		margin-top: 12rpx;
	}

	.list-group {
		display: flex;
		flex-direction: column;
		gap: 10rpx;
	}

	.list-group-item {
		display: block;
		padding: 20rpx 24rpx;
		background: rgba(255, 255, 255, 0.92);
		color: #263238;
	}

	.form-group {
		margin-bottom: 20rpx;
	}

	.form-control {
		display: block;
		width: 100%;
		height: 72rpx;
		padding: 0 20rpx;
		box-sizing: border-box;
		border: 1rpx solid #c7d7f7;
		border-radius: 10rpx;
		background: #ffffff;
	}

	.btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-width: 132rpx;
		height: 68rpx;
		padding: 0 24rpx;
		border-radius: 10rpx;
		border: none;
	}

	.btn-primary {
		background: #3a78ff;
		color: #ffffff;
	}

	.disabled {
		pointer-events: none;
		opacity: 0.55;
	}

	.jumbotron_pos{
		position: fixed;
		display: flex;
		left: 32rpx;
		right: 32rpx;
		top: 20vh;
		z-index: 30;
		width: auto;
		height: auto;
		max-height: 65vh;
		overflow-y: auto;
		background: rgba(255, 255, 255, 0.96);
		box-shadow: 0 14rpx 32rpx rgba(0, 0, 0, 0.15);
	}
	.ProImag{
		display: block;
		margin: 24rpx auto 16rpx;
		border-radius: 75%;
		width: 190rpx;
		height: 190rpx;
		border: 2rpx solid #000000;
		overflow: hidden;
	}
	.ProfitPos{
		position: relative;
		display: flex;
		width: 100%;
		top: auto;
		opacity: 1;
	}
	.ProfitThings {
		padding: 0 24rpx;
		margin-top: 8rpx;
	}
	.listColor{
		opacity: 0.92;
		border: 2rpx solid #8fa5d1;
		border-radius: 12rpx;
		text-align: center;
	}
	.listPos{
		display: flex;
		position: relative;
		top: auto;
		padding: 0 24rpx;
		margin-top: 10rpx;
		width: 100%;
		box-sizing: border-box;
	}

	.page {
		background-color: #d3d3d3;
		overflow: visible;
		background-image: linear-gradient(165deg, #eff4ff 0%, #d8e5ff 48%, #bed3ff 100%);
		background-size: 100% 100%;
		background-repeat: no-repeat;
		width: 100%;
		min-height: 100vh;
		height: auto;
		overflow-y: auto;
		overflow-x: hidden;
	}

	.section {
		background-color: #24242433;
		overflow: visible;
		background-image: linear-gradient(180deg, #eef3ff 0%, #dde9ff 100%);
		background-size: 100% 100%;
		background-repeat: no-repeat;
		width: 100%;
		min-height: 100vh;
		height: auto;
	}

	.halfColor {
		backdrop-filter: blur(5px);
		width: 100%;
		min-height: 100vh;
		height: auto;
		padding-bottom: 150rpx;
		box-sizing: border-box;
	}

	.text-wrapper {
		padding: 24rpx 0;
		background-color: rgba(217, 217, 217, 0.7);
		box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.05);
	}

	.pos {
		position: relative;
		left: 0;
		right: 0;
		top: 0;
	}

	.text {
		margin-left: 0;
		color: #000000;
		font-size: 52rpx;
		text-align: center;
		display: block;
		width: 100%;
		font-family: Inter;
		line-height: 1.2;
	}


	.CancelButton{
		margin-left: 20rpx;
	}

	label {
		display: block;
		font-size: 26rpx;
		line-height: 1.4;
		margin-bottom: 8rpx;
		color: #2c3e50;
	}

	form {
		width: 100%;
	}

	button {
		font-size: 26rpx;
	}

	.navigator-hover {
		opacity: 0.85;
	}
</style>