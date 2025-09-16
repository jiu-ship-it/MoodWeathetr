<template>
  <view class="flex-col justify-start relative page">
    <view class="shrink-0 section"></view>
    <view class="flex-col section_2 pos">
      <view class="flex-col">
        <text class="self-start font">邮箱</text>
        <view class="mt-10 flex-col justify-start items-start self-stretch text-wrapper">
          <input class="font_2 text" placeholder="请输入邮箱" v-model="MyEmail"></input>
        </view>
      </view>
      <view class="flex-col mt-27">
        <text class="self-start font text_2">密码</text>
        <view class="flex-col self-stretch mt-11">
          <view class="flex-col justify-start items-start self-stretch text-wrapper">
            <input class="font_2 text text_3" placeholder="请输入密码" v-model="MyPass"></input>
          </view>
          <text class="self-end err text_4" id="err">信息有误！</text>
          <view @click="Submit" class="flex-col justify-start items-center self-stretch text-wrapper_2">
            <text class="font text_5">登入</text>
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
  export default {
    components: {},
    props: {},
    data() {
      return {
		  MyEmail:null,
		  MyPass:null,
	  };
    },
    methods: {
		Submit(){//判断关键字并上传数据
			var reaserch_at = RegExp(/@/)
			var reaserch_com = RegExp(/.com/)
			if(reaserch_at.test(this.MyEmail)==false || reaserch_com.test(this.MyEmail)==false || this.MyPass == null){
				console.log("err")
				document.getElementById('err').style.visibility = 'visible'
			}else{
				console.log("upload")
				document.getElementById('err').style.visibility = 'hidden'
			}//如果什么都没有不传输数据且报错,如果正常则上传用户数据!!!!比对服务器信息，存在才可以进入页面
		},
		GoToZhuCe(){
			uni.navigateTo({
				url:'/pages/Main_Page/Main_Page'
			})
		}
		
	},
  };
</script>

<style scoped lang="css">
	.err{
		visibility: hidden;
		font-size: 29.13rpx;
		font-family: Inter;
		line-height: 26.91rpx;
		color: #1e1e1e;
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