<template>
  <view class="flex-col justify-start relative page">
    <view class="shrink-0 section"></view>
    <view class="flex-col justify-start items-center text-wrapper pos"><text class="font text">返回</text></view>
    <view class="flex-col section_2 pos_2">
      <view class="flex-col items-start group">
        <text class="font_2">History</text>
        <text class="font text_2 mt-5">历史信息</text>
      </view>
      <view class="shrink-0 divider"></view>
      <view class="flex-col group_2">
        <view class="flex-col group_3">
          <view class="flex-col items-start group_4">
            <text class="font text_3">Name</text>
            <text class="font_2 text_4 mt-13">description.</text>
          </view>
          <view class="flex-col items-start group_4">
            <text class="font">Name2</text>
            <text class="font_2 mt-13">description.</text>
          </view>
        </view>
        <view class="flex-col justify-start group_5"><view class="divider_2"></view></view>
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
  .mt-5 {
    margin-top: 9.1rpx;
  }
  .mt-13 {
    margin-top: 23.67rpx;
  }
  .page {
    background-color: #ffffff;
    overflow: hidden;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163844487671632.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    width: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    height: 100%;
  }
  .section {
    overflow: hidden;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/6870b31e2b2a8200119cee14/17522163844487671632.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    width: 750rpx;
    height: 1669.3rpx;
  }
  .text-wrapper {
    padding: 21.84rpx 0 18.2rpx;
    background-color: #2c2c2c;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 101.94rpx;
    border-left: solid 1.82rpx #2c2c2c;
    border-right: solid 1.82rpx #2c2c2c;
    border-top: solid 1.82rpx #2c2c2c;
    border-bottom: solid 1.82rpx #2c2c2c;
  }
  .pos {
    position: absolute;
    left: 42rpx;
    top: 21.84rpx;
  }
  .font {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 21.84rpx;
    color: #1e1e1e;
  }
  .text {
    color: #f5f5f5;
    line-height: 26.07rpx;
  }
  .section_2 {
    padding: 0 7.28rpx 846.48rpx 14.56rpx;
    background-color: #ffffff8c;
    border-radius: 14.56rpx;
    box-shadow: 0rpx 7.28rpx 7.28rpx -1.82rpx #0c0c0d0d, 0rpx 7.28rpx 7.28rpx -1.82rpx #0c0c0d1a;
    overflow: hidden;
    width: 624.39rpx;
    border-left: solid 1.82rpx #d9d9d9;
    border-right: solid 1.82rpx #d9d9d9;
    border-top: solid 1.82rpx #d9d9d9;
    border-bottom: solid 1.82rpx #d9d9d9;
  }
  .pos_2 {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }
  .group {
    padding: 36.41rpx 29.13rpx 29.13rpx;
  }
  .font_2 {
    font-size: 25.49rpx;
    font-family: Inter;
    line-height: 24.32rpx;
    color: #757575;
  }
  .text_2 {
    font-weight: 600;
    line-height: 27.76rpx;
  }
  .divider {
    margin: 0 29.13rpx;
    background-color: #d9d9d9;
    height: 1.82rpx;
  }
  .group_2 {
    padding-top: 14.56rpx;
  }
  .group_3 {
    border-radius: 14.56rpx;
    overflow: hidden;
  }
  .group_4 {
    padding: 32.77rpx 29.13rpx 25.49rpx;
    border-radius: 14.56rpx;
    overflow: hidden;
  }
  .text_3 {
    line-height: 21.55rpx;
  }
  .text_4 {
    margin-left: 7.28rpx;
  }
  .group_5 {
    padding: 14.56rpx 0;
    border-radius: 14.56rpx;
  }
  .divider_2 {
    margin: 0 29.13rpx;
    background-color: #d9d9d9;
    width: 537.01rpx;
    height: 1.82rpx;
  }
</style>