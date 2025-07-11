<template>
  <view class="flex-col justify-start relative page">
    <view class="shrink-0 section"></view>
    <view class="flex-col justify-start items-start text-wrapper pos"><text class="text">暖言纸条</text></view>
    <view class="flex-col section_2 pos_2">
      <view class="flex-row relative group">
        <view class="group_2"></view>
        <view class="flex-col items-start self-start group_3">
          <text class="text_2">Name：</text>
          <text class="mt-10 font text_3">加入时间：</text>
        </view>
        <image
          class="group_2 pos_3"
          src="https://ide.code.fun/api/image?token=6870b54f2b2a8200119ceee7&name=706df767f8e28913573394798731cb23.png"
        />
      </view>
      <view class="flex-col mt-37">
        <view class="flex-col justify-start items-center text-wrapper_2">
          <text class="font text_4">隐私条款</text>
        </view>
        <view class="mt-18 flex-col justify-start items-center text-wrapper_2"><text class="font">关于我们</text></view>
        <view class="mt-18 flex-col items-center text-wrapper_2">
          <text class="font_2">切换语言</text>
          <text class="font_2">当前语言：中文</text>
        </view>
      </view>
    </view>
    <view class="flex-col justify-start section_3 pos_4">
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
  .mt-37 {
    margin-top: 67.35rpx;
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
    padding: 50.97rpx 0 591.63rpx;
    background-color: #ffffff8c;
    border-radius: 14.56rpx;
  }
  .pos_2 {
    position: absolute;
    left: 49.15rpx;
    right: 50.99rpx;
    top: 50%;
    transform: translateY(-50%);
  }
  .group {
    padding: 0 43.69rpx;
  }
  .group_2 {
    border-radius: 18202.06rpx;
    overflow: hidden;
    width: 174.76rpx;
    height: 174.76rpx;
  }
  .group_3 {
    margin-left: 21.84rpx;
    margin-top: 10.92rpx;
  }
  .text_2 {
    color: #1e1e1e;
    font-size: 29.13rpx;
    font-family: Inter;
    font-weight: 600;
    line-height: 21.5rpx;
  }
  .font {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 26.85rpx;
    color: #f5f5f5;
  }
  .text_3 {
    color: #1e1e1e;
    line-height: 26.69rpx;
  }
  .pos_3 {
    position: absolute;
    left: 43.69rpx;
    bottom: 0;
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
  .text_4 {
    line-height: 26.89rpx;
  }
  .font_2 {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 34.59rpx;
    color: #f5f5f5;
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