<template>
  <view class="flex-col justify-start relative page">
    <view class="shrink-0 section"></view>
    <view class="flex-col justify-start items-start text-wrapper pos"><text class="text">暖言纸条</text></view>
    <view class="flex-col section_2 pos_2">
      <text class="self-start font text_2">Music</text>
      <text class="self-start font_2 text_3">音乐</text>
      <view class="shrink-0 self-stretch divider view"></view>
      <view class="flex-col self-stretch group">
        <view class="flex-col group_2">
          <view class="flex-col group_3">
            <view class="flex-row justify-between self-stretch">
              <text class="font_2">音乐1</text>
              <view class="group_4"></view>
            </view>
            <text class="mt-10 self-start font">创作者：.</text>
          </view>
          <view class="flex-col items-start group_3">
            <text class="font_2">音乐2</text>
            <text class="font mt-11">创作者：.</text>
          </view>
        </view>
        <view class="flex-col justify-start group_5"><view class="divider view_2"></view></view>
      </view>
    </view>
    <view class="flex-col justify-start section_3 pos_3">
      <view class="flex-row justify-between equal-division">
        <view class="flex-col justify-start items-center equal-division-item">
          <image
            class="image"
            src="https://ide.code.fun/api/image?token=6870b54f2b2a8200119ceee7&name=630fdbc11dccdc6d74ad3cecdd9496de.png"
          />
        </view>
        <view class="flex-col justify-start items-center equal-division-item">
          <image
            class="image"
            src="https://ide.code.fun/api/image?token=6870b54f2b2a8200119ceee7&name=85e6c4051832477789a9c724127ba087.png"
          />
        </view>
        <view class="flex-col justify-start items-center equal-division-item">
          <image
            class="image"
            src="https://ide.code.fun/api/image?token=6870b54f2b2a8200119ceee7&name=3de231db41c1ba966cf2300f4c51043e.png"
          />
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
    background-color: #ffffff80;
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
</style>