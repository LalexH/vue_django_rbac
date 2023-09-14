<template>
  <el-container>
    <el-header height="60px" style="line-height: 60px">
      <el-row justify="end">
        <el-col :span="2">
          <!-- <span style="color: #409eff;" @click.prevent="logout">注销</span> -->
          <div class="flex justify-space-between mb-4 flex-wrap gap-4">
            <el-button type="primary" text size="large" @click="personDrawer = true">
              <el-icon size="large"><UserFilled /></el-icon>
              个人中心
            </el-button>
          </div>
        </el-col>
      </el-row>
    </el-header>
  </el-container>
  
  <el-container>
    <!-- 侧边栏 -->
    <el-aside>
      <el-menu router>
        <el-sub-menu v-for="item in this.userInfo.menus" :index="item.menu_title" :key="item.id">
          <template #title>
            <el-icon><component :is="item.menu_icon"/></el-icon>
            <span>{{ item.menu_title }}</span>
          </template>

          <el-menu-item v-for="subitem in item.children" :index="subitem.route_path" :key="subitem.id">
            <el-icon><component :is="subitem.menu_icon"/></el-icon>
            <span>{{ subitem.menu_title }}</span>
          </el-menu-item>
          
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <!-- main -->
    <el-main>
      <router-view></router-view>
      <!-- 个人中心抽屉 -->
      <el-drawer v-model="personDrawer" title="个人中心">
        <div class="grid-content bg-purple" style="margin-top: 10px; margin-left: 10px; margin-bottom: 10px;">
          <el-card class="box-card">
            <div class="text item" align="left" style="line-height:200%;letter-spacing:2px">
                <div><span style="font-weight:bold">用户名：</span>{{ this.userInfo.user.username }}</div>
                <div><span style="font-weight:bold">邮箱：</span>{{ this.userInfo.user.email }}</div>
                <div><span style="font-weight:bold">电话：</span>{{ this.userInfo.user.phone }}</div>
                <div>
                  <span style="font-weight:bold">角色：</span>
                  <el-tag v-for="item in this.userInfo.roles" :key="item.id" class="mx-1" effect="dark" type="success">
                    {{ item.role_name }}
                  </el-tag>
                </div>
            </div>
            <div style="margin-top: 10px;">
              <!-- 更新用户信息form -->
              <el-form v-if="user_visible">
                <el-form-item label="用户名:" label-width="60px">
                  <el-input disabled style="width: 200px;" type="text" clearable v-model="this.userInfo.user.username"/>
                </el-form-item>

                <el-form-item label="email:" label-width="60px">
                  <el-input style="width: 200px;" type="text" clearable v-model="this.userInfo.user.email"/>
                </el-form-item>

                <el-form-item label="电话:" label-width="60px">
                  <el-input style="width: 200px;" type="text" clearable v-model="this.userInfo.user.phone"/>
                </el-form-item>
                <el-button type="success" @click="updateResource()">确认</el-button>
                <el-button type="danger" @click="this.user_visible = false">取消</el-button>
              </el-form>
              
              <!-- 重置密码form -->
              <el-form v-if="password_visible">
                <el-form-item label="新密码:" label-width="80px">
                  <el-input style="width: 200px;" type="password" clearable v-model="this.new_password"/>
                </el-form-item>
                <el-form-item label="确认密码:" label-width="80px">
                  <el-input style="width: 200px;" type="password" clearable v-model="this.confirm_password"/>
                </el-form-item>
                <el-button type="success" @click="resetPassword()">确认</el-button>
                <el-button type="danger" @click="this.password_visible = false">取消</el-button>
              </el-form>
            </div>
            <div style="margin-top: 10px; float:right; margin-bottom: 10px;">
              <el-button type="success" @click="this.user_visible = true">更新用户信息</el-button>
              <el-button type="danger" @click="this.password_visible = true">重置密码</el-button>
              <el-button type="primary" @click="logout()">退出登陆</el-button>
            </div>
          </el-card>
          </div>
      </el-drawer>
    </el-main>
  </el-container>
</template>
  
<script>
  import store from "../store/index"
  import Api from "@/api/index"
  import { ElMessage } from 'element-plus'
  export default {
    data() {
      return {
        personDrawer: false,
        password_visible: false,
        user_visible: false,
        new_password: "",
        confirm_password: ""
      }
    },
    computed: {
      userInfo() {
        return store.state.userInfo
      }
    },
    mounted() {
      if (localStorage.token === undefined){
        this.$router.push({ name: "login" });
      }
      Api.userInfo()
    },
    methods: {
      logout(){
        localStorage.clear();
        this.$router.push({ name: "login" });
        this.$message({
          message: "退出登录",
          type: "success",
        });
      },
      updateResource(){
        var r_date = {
          id: this.userInfo.user.id,
          username: this.userInfo.user.username,
          email: this.userInfo.user.email,
          phone: this.userInfo.user.phone,
        }
        Api.user("PUT", r_date, r_date.id).then((response) => {
          if(response.status === 200) {
              ElMessage({
                  showClose: true,
                  message: '更新成功...',
                  type: 'success',
              })
              this.user_visible = false
          }
        })
        this.updateVisible = false
      },
      resetPassword(){
        if(this.new_password !== this.confirm_password){
          ElMessage({
            showClose: true,
            message: '两次输入的密码不一致...',
            type: 'error',
          })
        }else{
          Api.user("PUT", {password: this.new_password, id: this.userInfo.user.id}, this.userInfo.user.id).then((response) => {
          if(response.status === 200) {
              ElMessage({
                  showClose: true,
                  message: '密码更新成功...',
                  type: 'success',
              })
              this.password_visible = false
          }
          this.logout()
        })
        
        }
      }
    },
  }
  
  </script>
  <style>
    .el-header {
      background-color: #d6e2f5;
    }
  </style>
  