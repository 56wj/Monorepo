<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import { getToken } from '@/utils/auth'
export default {
  name: 'App',
  // data() {
  //   return {ws: ""}
  // },
  // methods: {
  //   web_socket() {
  //     var that = this
  //     // 如果文件上传成功了 （后续此处补上文件是否上传成功、是否上传的判断）
  //     if (typeof (WebSocket) == "undefined") {
  //       console.log("您的浏览器不支持WebSocket");
  //   } else {
  //       console.log("您的浏览器支持WebSocket");}
  //     // var ws = new WebSocket('ws://localhost:8101/palletpacking/1');
  //     var wsUrl = 'ws://localhost:8101/palletpackingWebsocket?token=' + getToken();
  //     var ws = new WebSocket(wsUrl);
  //     this.$data.ws = ws
  //     ws.onopen = function () {
  //       console.log('ws onopen');
  //       ws.send('from client: hello');
  //     };
  //     ws.onmessage = function (e) {
  //       console.log('ws onmessage');
  //       console.log(JSON.parse(e.data))
  //       var res = JSON.parse(e.data)
  //       // 这里要做一个code的判断 info whole_tray_number
  //       if(res.code = 20000) {
  //         // var obj = JSON.parse(res.data);
  //         var obj = res.data;
  //         var arr = Object.keys(obj);
  //         // var config = that.$data.form;
  //         console.log(obj)
  //         that.$router.push({
  //                 path: '/type1/3D_result',
  //                 query: {
  //                   obj: obj,
  //                   arr: arr,
  //                   // config: config
  //                 }           
  //             }) // 带参跳转
  //       }else {
  //         Message({
  //           message: res.message,
  //           type: 'error',
  //           duration: 5 * 1000
  //         })
  //       }
  //     };
  //     ws.onclose = function () {
  //     };
  //     ws.onerror = function (error) {
  //           alert("发生了错误");
  //           console.log(error)
  //     }
  //   }
  // },
  // created() {
  //   // this.web_socket()
  // }
}
</script>
