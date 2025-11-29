<template>
	<view class="page flex-col section">
		<view class="halfColor">
			<view class="flex-col justify-start items-start text-wrapper pos"><text class="text">暖言纸条</text></view>
			
			<!-- 这里是底部菜单 -->
			<view class="flex-col justify-start section_3 pos_4">
				<view class="flex-row justify-between equal-viewision">
					<view class="flex-col justify-start items-center equal-viewision-item" @click="home">
						<image class="image" src="/static/image/home.png" />
					</view>
					<view class="flex-col justify-start items-center equal-viewision-item" @click="setting">
						<image class="image" src="/static/image/setting.png" />
					</view>
					<view class="flex-col justify-start items-center equal-viewision-item" @click="music">
						<image class="image" src="/static/image/music.png" />
					</view>
				</view>
			</view>
			
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
				<img src="static/image/noon.png" alt="头像" class="ProImag"/>
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
			
		</view>
	</view>
</template>

<script>
	export default {
		components: {},
		props: {},
		data() {
			return {
				NowPage:"main",//当前页面
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
			setting(){
				uni.navigateTo({
					url:"/pages/Setting/Setting"
				})
			},
			music(){
				uni.navigateTo({
					url:"/pages/Music/Music"
				})
			},
			home(){
				uni.navigateTo({
					url:"/pages/Main_Page/Main_Page"
				})
			}
		},
	};
</script>

<style scoped lang="css">
	@import '../../static/css/BootStrapCss/bootstrap.min.css';
	.jumbotron_pos{
		position: absolute;
		display: flex;
		top: 1%;
		right: 50%;
		transform: translate(50%,45%);
		height: 50%;
		width: 80%;
	}
	.ProImag{
		position: absolute;
		display: flex;
		left: 50%;
		top: 10%;
		transform: translateX(-50%);
		border-radius: 75%;
		width: 320rpx;
		height: 320rpx;
		border: 2rpx solid #000000;
		overflow: hidden;
	}
	.ProfitPos{
		position: absolute;
		display: flex;
		width: 100%;
		top: 30%;
		opacity: 0.85;
	}
	.listColor{
		opacity: 0.85;
		border: 2rpx solid #666;
		border-radius: 8rpx;
	}
	.listPos{
		display: flex;
		position: absolute;
		top: 60%;
		width: 100%;
	}
	.mt-37 {
		margin-top: 67.35rpx;
	}
	.EditData{
		visibility: visible;
	}
	.page {
		background-color: #d3d3d3;
		overflow: hidden;
		background-image: url('/static/image/morning.png');
		background-size: 100% 100%;
		background-repeat: no-repeat;
		width: 100%;
		overflow-y: hidden;
		overflow-x: hidden;
		height: 100%;
	}

	.section {
		background-color: #24242433;
		overflow: hidden;
		background-image: url('/static/image/morning.png');
		background-size: 100% 100%;
		background-repeat: no-repeat;
		width: 750rpx;
		height: 1669.3rpx;
	}

	.halfColor {
		backdrop-filter: blur(5px);
		width: 100%;
		height: 100%;
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

	.text-wrapper_2 {
		padding: 21.84rpx 0;
		background-color: #2c2c2c;
		border-radius: 14.56rpx;
		overflow: hidden;
		border-left: solid 1.82rpx #2c2c2c;
		border-right: solid 1.82rpx #2c2c2c;
		border-top: solid 1.82rpx #2c2c2c;
		border-bottom: solid 1.82rpx #2c2c2c;
	}

	.section_3 {
		padding: 14.56rpx 0;
		background-image: linear-gradient(180.9deg, #575757bf 4.2%, #bdbdbdbf 96.2%);
		overflow: hidden;
	}

	.pos_4 {
		position: absolute;
		left: 0;
		right: 0;
		top: 1529.13rpx;
	}

	.equal-viewision {
		margin: 0 32.77rpx;
	}

	.equal-viewision-item {
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
	.CancelButton{
		left: 10%;
	}
</style>