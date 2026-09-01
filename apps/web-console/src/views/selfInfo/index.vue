<template>
  <div class="app-container">
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-menu-item index="1">总览</el-menu-item>
      <el-menu-item index="2">密码</el-menu-item>
    </el-menu>
    <div style="margin-top: 30px;width: 500px;">
      <el-form v-show="show_flag1" :model="info_form" :rules="info_rules">
        <el-form-item style="margin-bottom: 0px;">
          <div style="width: 100%; text-align: center;">
            <el-avatar size="large" :src="info_form.avatar" style="margin:0 auto;"></el-avatar>
          </div>
        </el-form-item>
        <el-form-item label="用户名">
          <el-input v-model="info_form.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="部门">
          <el-input v-model="info_form.department" disabled></el-input>
        </el-form-item>
        <el-form-item label="电话号码" prop="phone">
          <el-input v-model="info_form.phone" clearable></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="info_form.email" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <div style="width: 100%; text-align: center;">
            <el-button type="primary" @click="onSubmit1">更新</el-button>
          </div>
        </el-form-item>
      </el-form>
      <el-form v-show="show_flag2" :model="password_form" :rules="password_rules">
        <el-form-item label="用户名">
          <el-input v-model="password_form.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="旧密码" prop="old_password">
          <el-input v-model="password_form.old_password" show-password></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="password">
          <el-input v-model="password_form.password" show-password></el-input>
        </el-form-item>
        <el-form-item label="确认密码"prop="re_password">
          <el-input v-model="password_form.re_password" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <div style="width: 100%; text-align: center;">
            <el-button type="primary" @click="onSubmit2">确认</el-button>
          </div>
          <!-- <el-button>取消</el-button> -->
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { getInfo,update_password,update_userinfo } from '@/api/user'
export default {
  data() {
    var validatePass = ((rule, value, callback) => {
      if(value === ''){
        callback(new Error('请再次输入密码'))
      } else if(value != this.$data.password_form.password){
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    })
    return {
      activeIndex: '1',
      info_form: {
        id: '',
        username: '',
        department: '',
        phone: '',
        email: '',
        avatar: ''
      },
      password_form: {
        username: '',
        old_password: '',
        password: '',
        re_password: '',
      },
      info_rules: {
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { len: 11, message: '请输入正确的手机号码', trigger: 'blur' },
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
        ]
      },
      password_rules: {
        old_password: [
          { required: true, message: '请输入原密码', trigger: 'blur' },
          { min: 6, max: 19, message: '密码长度在 6 到 19 位', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, max: 19, message: '密码长度在 6 到 19 位', trigger: 'blur' }
        ],
        re_password: [
          { required: true, validator: validatePass, trigger: 'blur' },
          { min: 6, max: 19, message: '密码长度在 6 到 19 位', trigger: 'blur' },
        ]
      },
      show_flag1: true,
      show_flag2: false
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath)
      if (key == 1) { this.$data.show_flag1 = true; this.$data.show_flag2 = false; }
      if (key == 2) { this.$data.show_flag1 = false; this.$data.show_flag2 = true; }
    },
    async onSubmit1() {
      var data = {
        id: this.$data.info_form.id,
        username: this.$data.info_form.username,
        email: this.$data.info_form.email,
        phone: this.$data.info_form.phone
      }
      try {
        const res = await update_userinfo(data)
        this.$message.success("更新成功")
      } catch(error) {
        this.$message.error("更新失败")
      }
    },
    async onSubmit2() {
      var data = {oldPassword:this.$data.password_form.old_password,newPassword:this.$data.password_form.password}
      try {
        const res = await update_password(data);
        this.$message.success("更新成功")
        await this.$store.dispatch('user/logout')
        this.$router.push(`/login?redirect=${this.$route.fullPath}`)
      } catch(error) {
        this.$message.error("更新失败")
      }
    },
    async init() {
      try {
        const res = await getInfo();
        this.$data.info_form.id = res.data.userInfo.id;
        this.$data.info_form.username = res.data.userInfo.username;
        this.$data.password_form.username = res.data.userInfo.username;
        this.$data.info_form.department = res.data.userInfo.department;
        this.$data.info_form.email = res.data.userInfo.email;
        this.$data.info_form.avatar = res.data.userInfo.avatar;
        this.$data.info_form.phone = res.data.userInfo.phone;
      } catch(error) {
        // this.$message.error("获取数据失败，请刷新页面")
      }
    }
  },
  created() {
    this.init();
  }
}
</script>

<style scoped></style>
