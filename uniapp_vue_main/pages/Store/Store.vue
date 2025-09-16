<template>
  <view class="flex-col justify-start relative page">
    <view class="shrink-0 section"></view>
    <view class="flex-row justify-between items-center section_2 pos">
      <view class="flex-col justify-start items-center text-wrapper"><text class="font text">返回</text></view>
      <view class="flex-row items-center section_3">
        <image
          class="image"
          src="https://ide.code.fun/api/image?token=6870b54f2b2a8200119ceee7&name=a777bbd3d0b8f69768e5089e2e926200.png"
        />
        <view class="flex-col justify-start items-start text-wrapper_2 ml-3">
          <text class="font text_2">10000000</text>
        </view>
      </view>
    </view>
    <view class="flex-col justify-start section_4 pos_2">
      <view class="flex-row equal-division">
        <view class="flex-col group equal-division-item">
          <view class="flex-col justify-start group_2"><view class="shrink-0 section_5 view"></view></view>
          <view class="mt-6 flex-col justify-start items-center self-center text-wrapper_3">
            <text class="font">购买</text>
          </view>
        </view>
        <view class="flex-col group equal-division-item">
          <view class="flex-col justify-start group_2"><view class="shrink-0 section_5 view_2"></view></view>
          <view class="mt-6 flex-col justify-start items-center self-center text-wrapper_3">
            <text class="font">购买</text>
          </view>
        </view>
      </view>
    </view>
    <view class="flex-col section_6 pos_3">
      <view class="flex-col">
        <text class="self-start text_3">你想要购买“”吗？</text>
        <view class="mt-14 flex-col items-start self-stretch">
          <text class="font_2">性格：</text>
          <text class="font_2 text_4">价格：</text>
        </view>
      </view>
      <view class="flex-row justify-end group_3">
        <view class="flex-col justify-start items-center text-wrapper_4"><text class="font text_5">返回</text></view>
        <view class="flex-col justify-start items-center text-wrapper_5 ml-15"><text class="font">购买</text></view>
      </view>
      <image
        class="image_2 pos_4"
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
  .ml-3 {
    margin-left: 5.46rpx;
  }
  .ml-15 {
    margin-left: 27.31rpx;
  }
  .page {
    background-color: #ffffff;
    overflow: hidden;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163844543360538.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    width: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    height: 100%;
  }
  .section {
    overflow: hidden;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163844543360538.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    width: 750rpx;
    height: 1669.3rpx;
  }
  .section_2 {
    padding: 7.28rpx 0 25.49rpx 29.13rpx;
    background-color: #d9d9d9b3;
  }
  .pos {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
  }
  .text-wrapper {
    padding: 21.84rpx 0 18.2rpx;
    background-color: #2c2c2c;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 101.94rpx;
    height: 72.82rpx;
    border-left: solid 1.82rpx #2c2c2c;
    border-right: solid 1.82rpx #2c2c2c;
    border-top: solid 1.82rpx #2c2c2c;
    border-bottom: solid 1.82rpx #2c2c2c;
  }
  .font {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 26.85rpx;
    color: #f5f5f5;
  }
  .text {
    line-height: 26.07rpx;
  }
  .section_3 {
    padding: 7.28rpx;
    background-color: #d9d9d9;
    height: 105.58rpx;
    border-left: solid 1.82rpx #000000;
    border-right: solid 1.82rpx #000000;
    border-top: solid 1.82rpx #000000;
    border-bottom: solid 1.82rpx #000000;
  }
  .image {
    width: 143.81rpx;
    height: 91.02rpx;
  }
  .text-wrapper_2 {
    margin-right: 3.64rpx;
    padding: 25.49rpx 0 18.2rpx;
    overflow: hidden;
    width: 245.75rpx;
    height: 69.17rpx;
    border-left: solid 1.82rpx #000000;
    border-right: solid 1.82rpx #000000;
    border-top: solid 1.82rpx #000000;
    border-bottom: solid 1.82rpx #000000;
  }
  .text_2 {
    margin-left: 18.2rpx;
    color: #000000;
    line-height: 21.77rpx;
  }
  .section_4 {
    padding: 61.89rpx 0 684.47rpx;
    background-color: #f8f8f8;
    border-radius: 14.56rpx;
    width: 649.88rpx;
  }
  .pos_2 {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }
  .equal-division {
    padding: 0 14.56rpx;
  }
  .group {
    flex: 1 1 309.47rpx;
  }
  .equal-division-item {
    padding: 10.92rpx 43.69rpx;
  }
  .group_2 {
    margin-right: 7.28rpx;
    padding: 29.13rpx 0;
    overflow: hidden;
    border-left: solid 1.82rpx #000000;
    border-right: solid 1.82rpx #000000;
    border-top: solid 1.82rpx #000000;
    border-bottom: solid 1.82rpx #000000;
  }
  .section_5 {
    margin-left: 7.28rpx;
  }
  .view {
    overflow: hidden;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163844578616786.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    height: 216.63rpx;
  }
  .text-wrapper_3 {
    padding: 21.84rpx 0;
    background-color: #2c2c2c;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 101.94rpx;
    border-left: solid 1.82rpx #2c2c2c;
    border-right: solid 1.82rpx #2c2c2c;
    border-top: solid 1.82rpx #2c2c2c;
    border-bottom: solid 1.82rpx #2c2c2c;
  }
  .view_2 {
    overflow: hidden;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163844581298985.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    height: 216.63rpx;
  }
  .section_6 {
    padding: 61.89rpx 50.97rpx 23.67rpx 58.25rpx;
    background-color: #ffffff;
    border-radius: 14.56rpx;
    box-shadow: 0rpx 7.28rpx 7.28rpx -7.28rpx #0c0c0d0d, 0rpx 29.13rpx 58.25rpx -7.28rpx #0c0c0d1a;
    border-left: solid 1.82rpx #d9d9d9;
    border-right: solid 1.82rpx #d9d9d9;
    border-top: solid 1.82rpx #d9d9d9;
    border-bottom: solid 1.82rpx #d9d9d9;
  }
  .pos_3 {
    position: absolute;
    left: 12rpx;
    right: 13.49rpx;
    top: 704.49rpx;
  }
  .text_3 {
    color: #1e1e1e;
    font-size: 43.69rpx;
    font-family: Inter;
    font-weight: 600;
    line-height: 41.25rpx;
    letter-spacing: -0.87rpx;
  }
  .font_2 {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 49.15rpx;
    color: #1e1e1e;
  }
  .text_4 {
    margin-top: -9.1rpx;
  }
  .group_3 {
    margin-top: 36.41rpx;
    padding: 0 3.64rpx;
  }
  .text-wrapper_4 {
    padding: 21.84rpx 0;
    background-color: #e3e3e3;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 101.94rpx;
    height: 72.82rpx;
    border-left: solid 1.82rpx #767676;
    border-right: solid 1.82rpx #767676;
    border-top: solid 1.82rpx #767676;
    border-bottom: solid 1.82rpx #767676;
  }
  .text_5 {
    color: #1e1e1e;
    line-height: 26.07rpx;
  }
  .text-wrapper_5 {
    padding: 21.84rpx 0;
    background-color: #2c2c2c;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 101.94rpx;
    height: 72.82rpx;
    border-left: solid 1.82rpx #2c2c2c;
    border-right: solid 1.82rpx #2c2c2c;
    border-top: solid 1.82rpx #2c2c2c;
    border-bottom: solid 1.82rpx #2c2c2c;
  }
  .image_2 {
    border-radius: 58.25rpx;
    width: 65.53rpx;
    height: 65.53rpx;
  }
  .pos_4 {
    position: absolute;
    right: 10.92rpx;
    top: 14.56rpx;
  }
</style>