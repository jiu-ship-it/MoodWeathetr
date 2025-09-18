<template>
	<div class="page flex-col section">
		<div class="halfColor">
			<view class="flex-col justify-start items-start text-wrapper pos"><text class="text">暖言纸条</text></view>
			<!-- 这里是顶部菜单 -->
			<view class="flex-col justify-start section_3 pos_4">
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
			<!-- 这里是底部菜单 -->
			<div class="jumbotron jumbotron-fluid jumbotron_pos">
			  <div class="container">
			    <form>
			      <div class="form-group">
			        <label for="exampleInputEmail1">新昵称(每月修改一次)</label>
			        <input class="form-control">
			      </div>
			      <div class="form-group">
			        <label for="exampleInputPassword1">个人简介(50字)</label>
			        <input class="form-control">
			      </div>
			      <button type="submit" class="btn btn-primary">提交</button>
			    </form>
			  </div>
			</div>
		</div>
	</div>
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
	@import '../../static/css/BootStrapCss/bootstrap.min.css';
	.jumbotron_pos{
		position: absolute;
		display: flex;
		top: 10%;
		right: 50%;
		transform: translate(50%,45%);
		height: 35%;
		width: 80%;
	}
	.mt-37 {
		margin-top: 67.35rpx;
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
		backdrop-filter: blur(10px);
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
</style>