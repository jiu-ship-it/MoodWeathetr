<script>
  export default {
    onLaunch: function () {
      console.log('App Launch');
    },
    onShow: function () {
      console.log('App Show');
    },
    onHide: function () {
      console.log('App Hide');
    },
  };
</script>

<style>
    /************************************************************
  ** 请将全局样式拷贝到项目的全局 CSS 文件或者当前页面的顶部 **
  ** 否则页面将无法正常显示                                  **
  ************************************************************/

  html {
    font-size: 16px;
  }

  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans',
      'Droid Sans', 'Helvetica Neue', 'Microsoft Yahei', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  view,
  image,
  text {
    box-sizing: border-box;
    flex-shrink: 0;
  }

  #app {
    width: 100vw;
    height: 100vh;
  }
  

  .flex-row {
    display: flex;
    flex-direction: row;
  }

  .flex-col {
    display: flex;
    flex-direction: column;
  }

  .justify-start {
    justify-content: flex-start;
  }

  .justify-end {
    justify-content: flex-end;
  }

  .justify-center {
    justify-content: center;
  }

  .justify-between {
    justify-content: space-between;
  }

  .justify-around {
    justify-content: space-around;
  }

  .justify-evenly {
    justify-content: space-evenly;
  }

  .items-start {
    align-items: flex-start;
  }

  .items-end {
    align-items: flex-end;
  }

  .items-center {
    align-items: center;
  }

  .items-baseline {
    align-items: baseline;
  }

  .items-stretch {
    align-items: stretch;
  }

  .self-start {
    align-self: flex-start;
  }

  .self-end {
    align-self: flex-end;
  }

  .self-center {
    align-self: center;
  }

  .self-baseline {
    align-self: baseline;
  }

  .self-stretch {
    align-self: stretch;
  }

  .flex-1 {
    flex: 1 1 0%;
  }

  .flex-auto {
    flex: 1 1 auto;
  }

  .grow {
    flex-grow: 1;
  }

  .grow-0 {
    flex-grow: 0;
  }

  .shrink {
    flex-shrink: 1;
  }

  .shrink-0 {
    flex-shrink: 0;
  }

  .relative {
    position: relative;
  }

  .ml-2 {
    margin-left: 3.64rpx;
  }

  .mt-2 {
    margin-top: 3.64rpx;
  }

  .ml-4 {
    margin-left: 7.28rpx;
  }

  .mt-4 {
    margin-top: 7.28rpx;
  }

  .ml-6 {
    margin-left: 10.92rpx;
  }

  .mt-6 {
    margin-top: 10.92rpx;
  }

  .ml-8 {
    margin-left: 14.56rpx;
  }

  .mt-8 {
    margin-top: 14.56rpx;
  }

  .ml-10 {
    margin-left: 18.2rpx;
  }

  .mt-10 {
    margin-top: 18.2rpx;
  }

  .ml-12 {
    margin-left: 21.84rpx;
  }

  .mt-12 {
    margin-top: 21.84rpx;
  }

  .ml-14 {
    margin-left: 25.49rpx;
  }

  .mt-14 {
    margin-top: 25.49rpx;
  }

  .ml-16 {
    margin-left: 29.13rpx;
  }

  .mt-16 {
    margin-top: 29.13rpx;
  }

  .ml-18 {
    margin-left: 32.77rpx;
  }

  .mt-18 {
    margin-top: 32.77rpx;
  }

  .ml-20 {
    margin-left: 36.41rpx;
  }

  .mt-20 {
    margin-top: 36.41rpx;
  }

  .ml-22 {
    margin-left: 40.05rpx;
  }

  .mt-22 {
    margin-top: 40.05rpx;
  }

  .ml-24 {
    margin-left: 43.69rpx;
  }

  .mt-24 {
    margin-top: 43.69rpx;
  }

  .ml-26 {
    margin-left: 47.33rpx;
  }

  .mt-26 {
    margin-top: 47.33rpx;
  }

  .ml-28 {
    margin-left: 50.97rpx;
  }

  .mt-28 {
    margin-top: 50.97rpx;
  }

  .ml-30 {
    margin-left: 54.61rpx;
  }

  .mt-30 {
    margin-top: 54.61rpx;
  }

  .ml-32 {
    margin-left: 58.25rpx;
  }

  .mt-32 {
    margin-top: 58.25rpx;
  }

  .ml-34 {
    margin-left: 61.89rpx;
  }

  .mt-34 {
    margin-top: 61.89rpx;
  }

  .ml-36 {
    margin-left: 65.53rpx;
  }

  .mt-36 {
    margin-top: 65.53rpx;
  }

  .ml-38 {
    margin-left: 69.17rpx;
  }

  .mt-38 {
    margin-top: 69.17rpx;
  }

  .ml-40 {
    margin-left: 72.82rpx;
  }

  .mt-40 {
    margin-top: 72.82rpx;
  }

  .ml-42 {
    margin-left: 76.46rpx;
  }

  .mt-42 {
    margin-top: 76.46rpx;
  }

  .ml-44 {
    margin-left: 80.1rpx;
  }

  .mt-44 {
    margin-top: 80.1rpx;
  }

  .ml-46 {
    margin-left: 83.74rpx;
  }

  .mt-46 {
    margin-top: 83.74rpx;
  }

  .ml-48 {
    margin-left: 87.38rpx;
  }

  .mt-48 {
    margin-top: 87.38rpx;
  }

  .ml-50 {
    margin-left: 91.02rpx;
  }

  .mt-50 {
    margin-top: 91.02rpx;
  }

  .ml-52 {
    margin-left: 94.66rpx;
  }

  .mt-52 {
    margin-top: 94.66rpx;
  }

  .ml-54 {
    margin-left: 98.3rpx;
  }

  .mt-54 {
    margin-top: 98.3rpx;
  }

  .ml-56 {
    margin-left: 101.94rpx;
  }

  .mt-56 {
    margin-top: 101.94rpx;
  }

  .ml-58 {
    margin-left: 105.58rpx;
  }

  .mt-58 {
    margin-top: 105.58rpx;
  }

  .ml-60 {
    margin-left: 109.22rpx;
  }

  .mt-60 {
    margin-top: 109.22rpx;
  }

  .ml-62 {
    margin-left: 112.86rpx;
  }

  .mt-62 {
    margin-top: 112.86rpx;
  }

  .ml-64 {
    margin-left: 116.5rpx;
  }

  .mt-64 {
    margin-top: 116.5rpx;
  }

  .ml-66 {
    margin-left: 120.15rpx;
  }

  .mt-66 {
    margin-top: 120.15rpx;
  }

  .ml-68 {
    margin-left: 123.79rpx;
  }

  .mt-68 {
    margin-top: 123.79rpx;
  }

  .ml-70 {
    margin-left: 127.43rpx;
  }

  .mt-70 {
    margin-top: 127.43rpx;
  }

  .ml-72 {
    margin-left: 131.07rpx;
  }

  .mt-72 {
    margin-top: 131.07rpx;
  }

  .ml-74 {
    margin-left: 134.71rpx;
  }

  .mt-74 {
    margin-top: 134.71rpx;
  }

  .ml-76 {
    margin-left: 138.35rpx;
  }

  .mt-76 {
    margin-top: 138.35rpx;
  }

  .ml-78 {
    margin-left: 141.99rpx;
  }

  .mt-78 {
    margin-top: 141.99rpx;
  }

  .ml-80 {
    margin-left: 145.63rpx;
  }

  .mt-80 {
    margin-top: 145.63rpx;
  }

  .ml-82 {
    margin-left: 149.27rpx;
  }

  .mt-82 {
    margin-top: 149.27rpx;
  }

  .ml-84 {
    margin-left: 152.91rpx;
  }

  .mt-84 {
    margin-top: 152.91rpx;
  }

  .ml-86 {
    margin-left: 156.55rpx;
  }

  .mt-86 {
    margin-top: 156.55rpx;
  }

  .ml-88 {
    margin-left: 160.19rpx;
  }

  .mt-88 {
    margin-top: 160.19rpx;
  }

  .ml-90 {
    margin-left: 163.83rpx;
  }

  .mt-90 {
    margin-top: 163.83rpx;
  }

  .ml-92 {
    margin-left: 167.48rpx;
  }

  .mt-92 {
    margin-top: 167.48rpx;
  }

  .ml-94 {
    margin-left: 171.12rpx;
  }

  .mt-94 {
    margin-top: 171.12rpx;
  }

  .ml-96 {
    margin-left: 174.76rpx;
  }

  .mt-96 {
    margin-top: 174.76rpx;
  }

  .ml-98 {
    margin-left: 178.4rpx;
  }

  .mt-98 {
    margin-top: 178.4rpx;
  }

  .ml-100 {
    margin-left: 182.04rpx;
  }

  .mt-100 {
    margin-top: 182.04rpx;
  }
</style>