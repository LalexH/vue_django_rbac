<template>
  <div class="login-div-class">
    <el-form :model="form" ref="form" label-width="60px" class="login-form-class">
      <h2 class="login-title-class">CMDB管理系统</h2>
      
      <el-form-item label="用户名">
        <el-input placeholder="请输入用户名" v-model="form.username"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input placeholder="请输入密码" v-model="form.password" type="password"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="login">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import router from "@/router/index"
import Api from "@/api/index"

export default {
  data(){
    return {
      form: { username: "admin", password: "123456"},
    }
  },
  methods: {
    login(){
      Api.login(this.form).then((response)=>{
        localStorage.setItem("token",response.data.token)
        router.push("/")
      }).catch(()=>{
        this.$message({
            message: '用户名或密码错误',
            type: 'warnning'
          });
        })
    },
  },
}
</script>

<style scoped>
.login-div-class{
  position: absolute;
  width: 100%;
  height: 100%;
  background: #ccc;
}
.login-title-class{
  color: #333;
  text-align: center;
  margin-top: 10px;
  margin-bottom: 30px;
}
.login-form-class{
  width: 350px;
  background-color: #fff;
  padding: 15px;
  height: 250px;
  border-radius: 20px;
  position: absolute;
  margin-top: -125px;
  margin-left: -175px;
  top:50%;
  left:50%;
}
</style>