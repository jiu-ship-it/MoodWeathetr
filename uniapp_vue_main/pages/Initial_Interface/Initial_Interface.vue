<template>
  <view class="flex-col justify-start relative page">
    <view class="shrink-0 section"></view>
    <text class="text pos LargeTitle flex-row justify-start">暖言纸条</text>
    <view @click="New" class="flex-col justify-start items-center text-wrapper pos_2" ><text class="text_2" >进入</text></view>
  </view>
</template>

<script>
	export default {
	  methods: {
		  New(){
			  uni.navigateTo({
			  	url:'/pages/Login_Interface/Login_Interface'
			  })//跳转页面
		  }
	  }
	}
</script>

<style scoped lang="css">
	.LargeTitle{
		-webkit-text-stroke: 1px #ffffff;
	}
  .page {
    background-color: #ffffff;
    overflow: hidden;
    background-image: url(https://bing.img.run/m.php);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    width: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    height: 100%;
  }
  .section {
    overflow: hidden;
    background-image: url(https://bing.img.run/m.php);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    width: 750rpx;
    height: 1669.3rpx;
  }
  .text {
    color: #000000;
    font-size: 116rpx;
    font-family: Inter;
    font-weight: 700;
    line-height: 111.03rpx;
	white-space: nowrap;
  }
  .pos {
    /* position: absolute;
    right: 131.8rpx;
    top: 408.04rpx; */
	position: absolute;
	left: 50%;
	top: 408.04rpx;
	transform: translateX(-50%);
  }
  .text-wrapper {
    padding: 32.77rpx 0 29.13rpx;
    background-color: #4c95de;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 207.52rpx;
    border-left: solid 1.82rpx #4696ff;
    border-right: solid 1.82rpx #4696ff;
    border-top: solid 1.82rpx #4696ff;
    border-bottom: solid 1.82rpx #4696ff;
  }
  .pos_2 {
    position: absolute;
    left: 50%;
    top: 1226.94rpx;
    transform: translateX(-50%);
  }
  .text_2 {
    color: #f5f5f5;
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 26.12rpx;
  }
</style>