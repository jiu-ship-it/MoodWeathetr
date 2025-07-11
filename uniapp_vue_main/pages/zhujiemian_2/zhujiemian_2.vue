<template>
  <view class="flex-col relative page">
    <view class="shrink-0 self-stretch section"></view>
    <view class="flex-row justify-between items-center section_2 pos">
      <text class="font">暖言纸条</text>
      <view class="flex-row items-center">
        <image
          class="image"
          src="https://ide.code.fun/api/image?token=6870b54f2b2a8200119ceee7&name=61bdb76f9c7c27375790c89c641b1ba1.png"
        />
        <view class="flex-col justify-start items-start text-wrapper"><text class="font_2 text">10000000</text></view>
      </view>
    </view>
    <view class="flex-col items-center section_3 pos_2">
      <text class="font">欢迎来到暖言纸条</text>
      <text class="font_2 text_2 mt-18">在这里，每一句话都是温暖的拥抱每一个字都充满了爱与关怀</text>
    </view>
    <view class="flex-col justify-start items-center text-wrapper_2 pos_3">
      <text class="text_3">📝 接收暖言</text>
    </view>
    <view class="flex-col justify-start items-center text-wrapper_3 pos_4">
      <text class="font_3 text_4">
        🛍️
        <br />
        商店
      </text>
    </view>
    <view class="flex-col justify-start items-center text-wrapper_4 pos_5">
      <text class="font_3 text_5">
        ✍️
        <br />
        写暖言
      </text>
    </view>
    <view class="flex-col justify-start items-center text-wrapper_5 pos_6">
      <text class="font_3 text_6">
        📝
        <br />
        历史暖言
      </text>
    </view>
    <view class="flex-col justify-start section_4 pos_7">
      <view class="flex-row justify-between equal-division">
        <view class="flex-col justify-start items-center equal-division-item">
          <image
            class="image_2"
            src="https://ide.code.fun/api/image?token=6870b54f2b2a8200119ceee7&name=630fdbc11dccdc6d74ad3cecdd9496de.png"
          />
        </view>
        <view class="flex-col justify-start items-center equal-division-item">
          <image
            class="image_2"
            src="https://ide.code.fun/api/image?token=6870b54f2b2a8200119ceee7&name=85e6c4051832477789a9c724127ba087.png"
          />
        </view>
        <view class="flex-col justify-start items-center equal-division-item">
          <image
            class="image_2"
            src="https://ide.code.fun/api/image?token=6870b54f2b2a8200119ceee7&name=3de231db41c1ba966cf2300f4c51043e.png"
          />
        </view>
      </view>
    </view>
    <view class="flex-col section_5 pos_22">
      <view class="flex-col">
        <text class="self-start font_1 text_7">写暖言：</text>
        <view class="flex-col justify-start items-end self-stretch image-wrapper mt-10">
          <image
            class="shrink-0 image_3"
            src="https://ide.code.fun/api/image?token=6870b54f2b2a8200119ceee7&name=273917bf9d9aa8dd26e1eb38f476c395.png"
          />
        </view>
      </view>
      <view class="flex-row justify-center group mt-213">
        <view class="flex-col justify-start items-center text-wrapper_6"><text class="font_1 text_8">取消</text></view>
        <view class="flex-col justify-start items-center text-wrapper_7 ml-15">
          <text class="font_4 text_9">发送</text>
        </view>
      </view>
    </view>
    <view class="flex-col self-start relative section_6 pos_33">
      <view class="flex-col items-start">
        <text class="text_10">收到暖言：</text>
        <text class="font_1 mt-19">你好</text>
      </view>
      <view class="flex-row justify-end group_2">
        <view class="flex-col justify-start items-center text-wrapper_8"><text class="font_1 text_11">确定</text></view>
        <view class="flex-col justify-start items-center text-wrapper_9 ml-10">
          <text class="font_4 text_12">回礼</text>
        </view>
      </view>
      <image
        class="image_4 pos_9"
        src="https://ide.code.fun/api/image?token=6870b54f2b2a8200119ceee7&name=7e070fc97df1a6e7316e5573026a6d68.png"
      />
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
  .mt-213 {
    margin-top: 387.74rpx;
  }
  .ml-15 {
    margin-left: 27.31rpx;
  }
  .mt-19 {
    margin-top: 34.59rpx;
  }
  .page {
    background-color: #ffffff;
    overflow: hidden;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163590829399947.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    height: 100%;
    width: 100%;
    overflow-y: auto;
    overflow-x: hidden;
  }
  .section {
    overflow: hidden;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163590829399947.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    height: 1669.3rpx;
  }
  .section_2 {
    padding: 27.31rpx 5.46rpx 27.31rpx 23.12rpx;
    background-color: #d9d9d9b3;
  }
  .pos {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
  }
  .font {
    font-size: 65.53rpx;
    font-family: Inter;
    line-height: 60.62rpx;
    color: #000000;
  }
  .image {
    width: 143.81rpx;
    height: 87.38rpx;
  }
  .text-wrapper {
    padding: 24.03rpx 0 16.11rpx;
    overflow: hidden;
    width: 229.37rpx;
    height: 65.53rpx;
    border: solid 1.82rpx #000000;
  }
  .font_2 {
    font-size: 29.13rpx;
    font-family: Inter;
    color: #000000;
  }
  .text {
    margin-left: 18.17rpx;
    line-height: 21.77rpx;
  }
  .section_3 {
    padding: 48.59rpx 0 80.17rpx;
    background-color: #ffffff;
    border-radius: 14.56rpx;
    width: 598.91rpx;
  }
  .pos_2 {
    position: absolute;
    left: 50%;
    top: 387.74rpx;
    transform: translateX(-50%);
  }
  .text_2 {
    line-height: 34.59rpx;
    text-align: center;
    width: 435.07rpx;
  }
  .text-wrapper_2 {
    padding: 44.42rpx 0 46.13rpx;
    background-color: #2c2c2c;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 349.51rpx;
    border: solid 1.82rpx #2c2c2c;
  }
  .pos_3 {
    position: absolute;
    left: 50%;
    top: 686.29rpx;
    transform: translateX(-50%);
  }
  .text_3 {
    color: #f5f5f5;
    font-size: 36.41rpx;
    font-family: Inter;
    line-height: 36.88rpx;
  }
  .text-wrapper_3 {
    padding: 61.31rpx 0 58.54rpx;
    background-color: #ffffffcc;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 203.88rpx;
    height: 223.91rpx;
    border: solid 1.82rpx #000000;
  }
  .pos_4 {
    position: absolute;
    left: 156.55rpx;
    top: 835.56rpx;
  }
  .font_3 {
    font-size: 43.69rpx;
    font-family: Inter;
    line-height: 52.79rpx;
    color: #2c2c2c;
  }
  .text_4 {
    text-align: center;
  }
  .text-wrapper_4 {
    padding: 61.31rpx 0 58.23rpx;
    background-color: #ffffffcc;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 203.88rpx;
    height: 223.91rpx;
    border: solid 1.82rpx #000000;
  }
  .pos_5 {
    position: absolute;
    right: 147.45rpx;
    top: 835.56rpx;
  }
  .text_5 {
    text-align: center;
  }
  .text-wrapper_5 {
    padding: 61.31rpx 0 58.36rpx;
    background-color: #ffffffcc;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 203.88rpx;
    height: 223.91rpx;
    border: solid 1.82rpx #000000;
  }
  .pos_6 {
    position: absolute;
    left: 50%;
    top: 1077.67rpx;
    transform: translateX(-50%);
  }
  .text_6 {
    text-align: center;
  }
  .section_4 {
    padding: 16.38rpx 0 14.4rpx;
    background-image: linear-gradient(180.9deg, #575757bf 4.2%, #bdbdbdbf 96.2%);
    overflow: hidden;
  }
  .pos_7 {
    position: absolute;
    left: 0;
    right: 0;
    top: 1529.13rpx;
  }
  .equal-division {
    margin-left: 32.77rpx;
    margin-right: 32.77rpx;
  }
  .equal-division-item {
    padding: 8.92rpx 0 9.28rpx;
    background-color: #d9d9d980;
    border-radius: 14.56rpx;
    width: 109.22rpx;
    height: 109.22rpx;
    border: solid 1.82rpx #000000;
  }
  .image_2 {
    width: 87.38rpx;
    height: 87.38rpx;
  }
  .section_5 {
    padding: 59.29rpx 38.96rpx 25.67rpx 42.6rpx;
    background-color: #ffffff;
    border-radius: 14.56rpx;
    width: 635.32rpx;
    border: solid 1.82rpx #000000;
  }
  .pos_22 {
    position: absolute;
    left: 50%;
    top: 379.55rpx;
    transform: translateX(-50%);
  }
  .font_1 {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 26.85rpx;
    color: #1e1e1e;
  }
  .text_7 {
    margin-left: 2.51rpx;
    line-height: 26.69rpx;
  }
  .image-wrapper {
    margin-right: 5.83rpx;
    padding: 121.97rpx 0 9.1rpx;
    background-color: #ffffff;
    border-radius: 14.56rpx;
    overflow: hidden;
    border: solid 1.82rpx #d9d9d9;
  }
  .image_3 {
    margin-right: 7.28rpx;
    width: 12.74rpx;
    height: 12.74rpx;
  }
  .group {
    padding: 0 53.7rpx;
  }
  .text-wrapper_6 {
    padding: 22.83rpx 0 19.51rpx;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 203.88rpx;
    height: 72.82rpx;
    border: solid 1.82rpx #000000;
  }
  .text_8 {
    color: #303030;
    line-height: 26.83rpx;
  }
  .text-wrapper_7 {
    padding: 22.75rpx 0 19.42rpx;
    background-color: #2c2c2c;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 203.88rpx;
    height: 72.82rpx;
    border: solid 1.82rpx #2c2c2c;
  }
  .font_4 {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 26.85rpx;
    color: #f5f5f5;
  }
  .text_9 {
    line-height: 27rpx;
  }
  .section_6 {
    padding: 61.89rpx 50.97rpx 49.15rpx 58.25rpx;
    background-color: #ffffff;
    border-radius: 14.56rpx;
    filter: drop-shadow(0rpx 7.28rpx 3.64rpx #0c0c0d0d, 0rpx 29.13rpx 29.13rpx #0c0c0d1a);
    width: 597.09rpx;
    border-left: solid 1.82rpx #757575;
    border-right: solid 1.82rpx #757575;
    border-top: solid 1.82rpx #757575;
    border-bottom: solid 1.82rpx #757575;
  }
  .pos_33 {
    position: absolute;
    left: 50%;
    top: 557.04rpx;
    transform: translateX(-50%);
  }
  .text_10 {
    color: #1e1e1e;
    font-size: 43.69rpx;
    font-family: Inter;
    font-weight: 600;
    line-height: 41.2rpx;
    letter-spacing: -0.87rpx;
  }
  .group_2 {
    margin-top: 161.45rpx;
    padding: 0 3.64rpx;
  }
  .text-wrapper_8 {
    padding: 22.83rpx 0 19.37rpx;
    background-color: #e3e3e3;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 101.94rpx;
    height: 72.82rpx;
    border: solid 1.82rpx #767676;
  }
  .text_11 {
    line-height: 26.98rpx;
  }
  .text-wrapper_9 {
    padding: 22.86rpx 0 19.51rpx;
    background-color: #2c2c2c;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 101.94rpx;
    height: 72.82rpx;
    border: solid 1.82rpx #2c2c2c;
  }
  .text_12 {
    line-height: 26.8rpx;
  }
  .image_4 {
    border-radius: 58.25rpx;
    width: 65.53rpx;
    height: 65.53rpx;
  }
  .pos_9 {
    position: absolute;
    right: 10.92rpx;
    top: 14.56rpx;
  }
</style>