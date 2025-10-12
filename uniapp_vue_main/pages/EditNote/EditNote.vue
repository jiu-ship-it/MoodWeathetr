<template>
  <view class="flex-col page">
    <view class="flex-col justify-start items-start text-wrapper"><text class="text">暖言纸条</text></view>
    <view class="flex-col section mt-25">
      <view class="flex-col">
        <text class="self-start font text_2">标题</text>
        <view class="flex-col justify-start items-start self-stretch text-wrapper_2">
          <text class="font_2 text_3">请输入标题</text>
        </view>
        <text class="self-start font text_4">内容</text>
        <view class="flex-col justify-start items-start self-stretch text-wrapper_3">
          <text class="font_2 text_5">请输入内容</text>
        </view>
        <text class="self-start font text_6">选择当前情绪</text>
        <image
          class="self-start image"
          src="https://ide.code.fun/api/image?token=68eb23dc9520a30011f3beeb&name=d229073dc8d8594e10c7eff0923271c4.png"
        />
      </view>
      <view class="flex-col mt-27">
        <view class="flex-col group">
          <text class="self-start font text_7">您可以上传录音（长按录音）</text>
          <view class="flex-row justify-between items-center self-stretch group_2 mt-9">
            <image
              class="image_2"
              src="https://ide.code.fun/api/image?token=68eb23dc9520a30011f3beeb&name=5ef5033cc2663f511dac5fb615fdd5f9.png"
            />
            <image
              class="image_3"
              src="https://ide.code.fun/api/image?token=68eb23dc9520a30011f3beeb&name=c753088c683ea228ac2ad02c11749613.png"
            />
          </view>
        </view>
        <view class="flex-row group_3">
          <view class="flex-col justify-start items-center text-wrapper_4">
            <text class="font text_8">保存并退出</text>
          </view>
          <view class="flex-col justify-start items-center text-wrapper_5 ml-15">
            <text class="font text_9">保存</text>
          </view>
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
  .mt-25 {
    margin-top: 45.51rpx;
  }
  .mt-27 {
    margin-top: 49.15rpx;
  }
  .mt-9 {
    margin-top: 16.38rpx;
  }
  .ml-15 {
    margin-left: 27.31rpx;
  }
  .page {
    padding-bottom: 45.51rpx;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/686f12dad54496f19f53aec9/68eb23ae9520a30011f3bed5/17602405794719744028.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    width: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    height: 100%;
  }
  .text-wrapper {
    padding: 40.05rpx 0;
    background-color: #d9d9d9b3;
  }
  .text {
    margin-left: 25.49rpx;
    color: #000000;
    font-size: 65.53rpx;
    font-family: Inter;
    line-height: 60.62rpx;
  }
  .section {
    margin: 0 29.13rpx;
    padding: 50.97rpx 36.41rpx 322.21rpx 43.69rpx;
    opacity: 0.95;
    background-color: #ffffff;
    border-radius: 14.56rpx;
    border-left: solid 1.82rpx #d9d9d9;
    border-right: solid 1.82rpx #d9d9d9;
    border-top: solid 1.82rpx #d9d9d9;
    border-bottom: solid 1.82rpx #d9d9d9;
  }
  .font {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 26.85rpx;
    color: #1e1e1e;
  }
  .text_2 {
    line-height: 26.76rpx;
  }
  .text-wrapper_2 {
    margin-top: 18.2rpx;
    padding: 21.84rpx 0;
    background-color: #ffffff;
    border-radius: 14.56rpx;
    overflow: hidden;
    border-left: solid 1.82rpx #d9d9d9;
    border-right: solid 1.82rpx #d9d9d9;
    border-top: solid 1.82rpx #d9d9d9;
    border-bottom: solid 1.82rpx #d9d9d9;
  }
  .font_2 {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 26.85rpx;
    color: #b3b3b3;
  }
  .text_3 {
    margin-left: 29.13rpx;
  }
  .text_4 {
    margin-left: 3.64rpx;
    margin-top: 40.05rpx;
  }
  .text-wrapper_3 {
    margin-top: 18.2rpx;
    padding: 29.13rpx 0 294.9rpx;
    background-color: #ffffff;
    border-radius: 14.56rpx;
    overflow: hidden;
    border-left: solid 1.82rpx #d9d9d9;
    border-right: solid 1.82rpx #d9d9d9;
    border-top: solid 1.82rpx #d9d9d9;
    border-bottom: solid 1.82rpx #d9d9d9;
  }
  .text_5 {
    margin-left: 29.13rpx;
    line-height: 26.94rpx;
  }
  .text_6 {
    margin-top: 32.77rpx;
    line-height: 27rpx;
  }
  .image {
    margin-left: 7.28rpx;
    margin-top: 21.84rpx;
    width: 94.66rpx;
    height: 94.66rpx;
  }
  .group {
    margin-right: 3.64rpx;
    padding-bottom: 16.38rpx;
    overflow: hidden;
  }
  .text_7 {
    line-height: 27.72rpx;
  }
  .group_2 {
    padding: 0 10.92rpx;
  }
  .image_2 {
    width: 69.17rpx;
    height: 103.76rpx;
  }
  .image_3 {
    margin-right: 14.56rpx;
    width: 87.38rpx;
    height: 87.38rpx;
  }
  .group_3 {
    padding-top: 32.77rpx;
  }
  .text-wrapper_4 {
    padding: 21.84rpx 0;
    flex: 1 1 286.71rpx;
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
    line-height: 27.09rpx;
  }
  .text-wrapper_5 {
    margin-right: 3.64rpx;
    padding: 21.84rpx 0;
    flex: 1 1 286.71rpx;
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
    line-height: 26.8rpx;
  }
</style>