<template>
  <view class="flex-col justify-start relative page">
    <view class="shrink-0 section"></view>
    <view class="flex-col section_2 pos">
      <view class="flex-col">
        <view class="flex-row justify-between items-center group">
          <text class="font text">昵称</text>
          <text v-if="errors.name" class="font_2 NameRed">{{ errors.name }}</text>
        </view>
        <view class="flex-col justify-start items-start text-wrapper">
          <input class="font_3 text_2 text_3" placeholder='请输入昵称' v-model.trim="Name" @blur="ValidateName"></input>
        </view>
      </view>
      <view class="mt-26 flex-col">
        <view class="flex-row justify-between group_2">
          <text class="font text_4">邮箱</text>
          <text v-if="errors.email" class="font_2 text_5 EmailRed">{{ errors.email }}</text>
        </view>
        <view class="flex-col justify-start items-start text-wrapper">
          <input class="font_3 text_2 text_6" placeholder="请输入邮箱" v-model.trim="Email" @blur="ValidateEmail"></input>
        </view>
      </view>
      <view class="mt-26 flex-col">
		<view class="flex-row justify-between group_2">
			<text class="self-start font text_7">密码</text>
			<text v-if="errors.password" class="font_2 text_pass PassRed">{{ errors.password }}</text>
		</view>
        <view class="mt-10 flex-col justify-start items-start self-stretch text-wrapper">
          <input class="font_3 text_2" password="true" placeholder="请输入密码" v-model.trim="Password" @blur="ValidatePassword" @confirm="Sign"></input>
        </view>
      </view>
      <view class="mt-26 flex-row">
        <view class="flex-col justify-start items-center text-wrapper_2" @click="Back"><text class="font text_8">返回</text></view>
        <view class="flex-col justify-start items-center text-wrapper_3 ml-15" @click="Sign" :class="{'btn-disabled': loading}">
          <text class="font text_9">{{ loading ? '注册中...' : '注册' }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
  import { apiRequest } from "../../common/request";

  export default {
    components: {},
    props: {},
    data() {
      return {
      Name: "",
      Email: "",
      Password: "",
      errors: {
      name: "",
      email: "",
      password: ""
      },
      loading: false
	  };
    },

    methods: {
		Back(){
			uni.navigateBack()
		},
    ValidateName() {
      if (!this.Name || this.Name.length < 3) {
        this.errors.name = "昵称至少3个字符";
        return false;
      }
      this.errors.name = "";
      return true;
    },
    ValidateEmail() {
      const emailRegex = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;
      if (!this.Email || !emailRegex.test(this.Email)) {
        this.errors.email = "邮箱格式不正确";
        return false;
      }
      this.errors.email = "";
      return true;
    },
    ValidatePassword() {
      if (!this.Password || this.Password.length < 6) {
        this.errors.password = "密码至少6位";
        return false;
      }
      this.errors.password = "";
      return true;
    },
    Sign(){
      if (this.loading) {
        return;
      }
      const nameOk = this.ValidateName();
      const emailOk = this.ValidateEmail();
      const passOk = this.ValidatePassword();
      if (!nameOk || !emailOk || !passOk) {
        return;
      }

      this.loading = true;
      apiRequest({
        url: "/api/register",
        method: "POST",
        data: { username: this.Name, email: this.Email, password: this.Password }
      })
        .then((res) => {
          if (res.statusCode === 201 && res.data && res.data.token) {
            uni.setStorageSync("token", res.data.token);
            uni.setStorageSync("user", res.data.user || {});
            uni.reLaunch({ url: "/pages/Main_Page/Main_Page" });
            return;
          }
          const msg = (res.data && (res.data.error || res.data.message)) || "注册失败，请稍后重试";
          uni.showToast({ title: msg, icon: "none" });
        })
        .catch(() => {
          uni.showToast({ title: "网络异常，请检查网络", icon: "none" });
        })
        .finally(() => {
          this.loading = false;
        });
    },
		}
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
  .NameRed{
	  visibility: hidden;
  }
  .EmailRed{
	  visibility: hidden;
  }
  .PassRed{
	  visibility: hidden;
  }
  .text_pass{
	  line-height: 27.05rpx;
	  float: right;
  }
  .btn-disabled {
    opacity: 0.7;
  }
</style>