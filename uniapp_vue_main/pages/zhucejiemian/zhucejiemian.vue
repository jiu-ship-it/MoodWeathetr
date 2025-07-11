<template>
  <view class="flex-col justify-start relative page">
    <view class="shrink-0 section"></view>
    <view class="flex-col section_2 pos">
      <view class="flex-col">
        <view class="flex-row justify-between items-center group">
          <text class="font text">昵称</text>
          <text class="font_2">昵称不可用！</text>
        </view>
        <view class="flex-col justify-start items-start text-wrapper">
          <text class="font_3 text_2 text_3">请输入昵称</text>
        </view>
      </view>
      <view class="mt-26 flex-col">
        <view class="flex-row justify-between group_2">
          <text class="font text_4">邮箱</text>
          <text class="font_2 text_5">邮箱不可用！</text>
        </view>
        <view class="flex-col justify-start items-start text-wrapper">
          <text class="font_3 text_2 text_6">请输入邮箱</text>
        </view>
      </view>
      <view class="mt-26 flex-col">
        <text class="self-start font text_7">密码</text>
        <view class="mt-10 flex-col justify-start items-start self-stretch text-wrapper">
          <text class="font_3 text_2">请输入密码</text>
        </view>
      </view>
      <view class="mt-26 flex-row">
        <view class="flex-col justify-start items-center text-wrapper_2"><text class="font text_8">返回</text></view>
        <view class="flex-col justify-start items-center text-wrapper_3 ml-15">
          <text class="font text_9">注册</text>
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
  .ml-15 {
    margin-left: 27.31rpx;
  }
  .page {
    background-color: #ffffff;
    overflow: hidden;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163590829399947.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    width: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    height: 100%;
  }
  .section {
    overflow: hidden;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163590829399947.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    width: 750rpx;
    height: 1669.3rpx;
  }
  .section_2 {
    padding: 50.97rpx 18.2rpx 71rpx 43.69rpx;
    background-color: #ffffff;
    border-radius: 14.56rpx;
    width: 582.52rpx;
    border-left: solid 1.82rpx #d9d9d9;
    border-right: solid 1.82rpx #d9d9d9;
    border-top: solid 1.82rpx #d9d9d9;
    border-bottom: solid 1.82rpx #d9d9d9;
  }
  .pos {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }
  .group {
    padding: 0 3.64rpx 14.56rpx;
  }
  .font {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 26.89rpx;
    color: #1e1e1e;
  }
  .text {
    line-height: 26.69rpx;
  }
  .font_2 {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 26.89rpx;
    color: #ff0000;
  }
  .text-wrapper {
    margin-right: 18.2rpx;
    padding: 21.84rpx 0;
    background-color: #ffffff;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 496.97rpx;
    border-left: solid 1.82rpx #d9d9d9;
    border-right: solid 1.82rpx #d9d9d9;
    border-top: solid 1.82rpx #d9d9d9;
    border-bottom: solid 1.82rpx #d9d9d9;
  }
  .font_3 {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 26.89rpx;
    color: #b3b3b3;
  }
  .text_2 {
    margin-left: 29.13rpx;
  }
  .text_3 {
    line-height: 26.85rpx;
  }
  .group_2 {
    padding: 0 3.64rpx 18.2rpx;
  }
  .text_4 {
    line-height: 26.91rpx;
  }
  .text_5 {
    line-height: 27.05rpx;
  }
  .text_6 {
    line-height: 26.91rpx;
  }
  .text_7 {
    line-height: 26.8rpx;
  }
  .text-wrapper_2 {
    padding: 21.84rpx 0;
    flex: 1 1 233.01rpx;
    background-color: #ffffff;
    border-radius: 14.56rpx;
    overflow: hidden;
    height: 72.82rpx;
    border-left: solid 1.82rpx #000000;
    border-right: solid 1.82rpx #000000;
    border-top: solid 1.82rpx #000000;
    border-bottom: solid 1.82rpx #000000;
  }
  .text_8 {
    color: #303030;
    line-height: 26.07rpx;
  }
  .text-wrapper_3 {
    padding: 21.84rpx 0;
    flex: 1 1 233.01rpx;
    background-color: #2c2c2c;
    border-radius: 14.56rpx;
    overflow: hidden;
    height: 72.82rpx;
    border-left: solid 1.82rpx #2c2c2c;
    border-right: solid 1.82rpx #2c2c2c;
    border-top: solid 1.82rpx #2c2c2c;
    border-bottom: solid 1.82rpx #2c2c2c;
  }
  .text_9 {
    color: #f5f5f5;
    line-height: 27.03rpx;
  }
</style>