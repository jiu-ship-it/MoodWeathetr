<template>
  <view class="flex-col justify-start relative page">
    <view class="shrink-0 section"></view>
    <view class="flex-col section_2 pos">
      <view class="flex-col">
        <text class="self-start font">用户名</text>
        <view class="mt-10 flex-col justify-start items-start self-stretch text-wrapper">
          <input class="font_2 text" placeholder="请输入用户名" v-model.trim="MyEmail" @blur="ValidateUser"></input>
        </view>
      </view>
      <view class="flex-col mt-27">
        <text class="self-start font text_2">密码</text>
        <view class="flex-col self-stretch mt-11">
          <view class="flex-col justify-start items-start self-stretch text-wrapper">
            <input class="font_2 text text_3" placeholder="请输入密码" password="true" v-model.trim="MyPass" @blur="ValidatePass" @confirm="Submit"></input>
          </view>
          <text v-if="errMsg" class="self-end err text_4">{{ errMsg }}</text>
          <view @click="Submit" class="flex-col justify-start items-center self-stretch text-wrapper_2" :class="{'btn-disabled': loading}">
            <text class="font text_5">{{ loading ? '登录中...' : '登入' }}</text>
          </view>
        </view>
      </view>
      <view class="flex-col items-start mt-27">
        <text class="font text_6 text_7"></text>
        <text class="mt-18 font text_6 text_8" @click="GoToZhuCe">注册账号</text>
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
      MyEmail: "",
      MyPass: "",
      errMsg: "",
      loading: false
	  };
    },
    methods: {
    ValidateUser() {
      if (!this.MyEmail || this.MyEmail.length < 3) {
        this.errMsg = "用户名至少3个字符";
        return false;
      }
      this.errMsg = "";
      return true;
    },
    ValidatePass() {
      if (!this.MyPass || this.MyPass.length < 6) {
        this.errMsg = "密码至少6位";
        return false;
      }
      this.errMsg = "";
      return true;
    },
    Submit(){
      if (this.loading) {
        return;
      }
      const userOk = this.ValidateUser();
      const passOk = this.ValidatePass();
      if (!userOk || !passOk) {
        return;
      }

      this.loading = true;
      this.errMsg = "";
      apiRequest({
        url: "/api/login",
        method: "POST",
        data: { username: this.MyEmail, password: this.MyPass }
      })
        .then((res) => {
          if (res.statusCode === 200 && res.data && res.data.token) {
            uni.setStorageSync("token", res.data.token);
            uni.setStorageSync("user", res.data.user || {});
            uni.reLaunch({ url: "/pages/Main_Page/Main_Page" });
            return;
          }
          const msg = (res.data && (res.data.error || res.data.message)) || "登录失败，请稍后重试";
          this.errMsg = msg;
          uni.showToast({ title: msg, icon: "none" });
        })
        .catch(() => {
          this.errMsg = "网络异常，请检查网络";
          uni.showToast({ title: this.errMsg, icon: "none" });
        })
        .finally(() => {
          this.loading = false;
        });
    },
		GoToZhuCe(){
			uni.navigateTo({
        url:'/pages/Regist_Interface/Regist_Interface'
			})
		}
		
	},
  };
</script>

<style scoped lang="css">
	.err{
		font-size: 29.13rpx;
		font-family: Inter;
		line-height: 26.91rpx;
		color: #1e1e1e;
	}
  .btn-disabled {
    opacity: 0.7;
  }
  .mt-27 {
    margin-top: 49.15rpx;
  }
  .mt-11 {
    margin-top: 20.02rpx;
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
    padding: 50.97rpx 36.41rpx 40.05rpx 43.69rpx;
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
  .font {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 26.91rpx;
    color: #1e1e1e;
  }
  .text-wrapper {
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
  .font_2 {
    font-size: 29.13rpx;
    font-family: Inter;
    line-height: 26.91rpx;
    color: #b3b3b3;
  }
  .text {
    margin-left: 29.13rpx;
  }
  .text_2 {
    line-height: 26.8rpx;
  }
  .text_3 {
    line-height: 26.89rpx;
  }
  .text_4 {
    margin-right: 3.64rpx;
    color: #ff0000;
    line-height: 27.18rpx;
  }
  .text-wrapper_2 {
    margin-right: 3.64rpx;
    margin-top: 14.56rpx;
    padding: 21.84rpx 0;
    background-color: #2c2c2c;
    border-radius: 14.56rpx;
    overflow: hidden;
    width: 495.15rpx;
    border-left: solid 1.82rpx #2c2c2c;
    border-right: solid 1.82rpx #2c2c2c;
    border-top: solid 1.82rpx #2c2c2c;
    border-bottom: solid 1.82rpx #2c2c2c;
  }
  .text_5 {
    color: #f5f5f5;
    line-height: 26.69rpx;
  }
  .text_6 {
    text-decoration: underline;
  }
  .text_7 {
    line-height: 26.8rpx;
  }
  .text_8 {
    line-height: 27.03rpx;
  }
</style>