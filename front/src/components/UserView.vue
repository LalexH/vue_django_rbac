<template>
  <el-container>
    <el-main style="width: 100%;">
      <el-card>
        <div>
          <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ first_lable }}</el-breadcrumb-item>
            <el-breadcrumb-item>{{ second_lable }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div style="margin-top: 20px;">
          <el-input v-model="this.selectForm.username" placeholder="根据名称查询" style="width: 200px;" />

          <el-button type="primary" style="margin-left: 10px;">
            <el-icon style="vertical-align: middle">
              <Search />
            </el-icon>
            <span style="vertical-align: middle" @click="selectResource()"> 搜索 </span>
          </el-button>

          <el-button type="primary" @click="this.addVisible = true" :disabled="this.addDisable">
            <el-icon style="vertical-align: middle">
              <Plus />
            </el-icon>
            <span style="vertical-align: middle"> 添加 </span>
          </el-button>

        </div>
        <!-- table -->
        <div style="margin-top: 20px;">
          <el-table :data="tableData" row-key="id" default-expand-all>
            <!-- <el-table-column prop="id" label="ID"/> -->
            <el-table-column prop="username" label="用户名" />
            <el-table-column prop="email" label="邮箱" />
            <el-table-column prop="phone" label="电话"/>
            <el-table-column prop="is_active" label="是否激活">
              <template #default="scope">
                <el-tag>{{ scope.row.is_active === 1 ? "激活": "未激活" }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="角色">
              <template #default="scope">
                <el-tag v-for="item in scope.row.role" :key="item.id">{{ item.role_name }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="Operations" width="200%">
              <template #default="scope">
                <el-button @click="updateOpen(scope.row)" :disabled="this.updateDisable">更新</el-button>
                <el-button type="danger" @click="deleteOpen(scope.row.id)" :disabled="this.deleteDisable">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <!-- add form -->
        <el-dialog width="30%" title="添加" v-model="addVisible" :close-on-click-modal="false" :close-on-press-escape="false">
            <el-form>
              <el-form-item label="用户:">
                  <el-input v-model="addForm.username"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="密码:">
                  <el-input v-model="addForm.password"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="邮箱:">
                  <el-input v-model="addForm.email"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="电话:">
                  <el-input v-model="addForm.phone"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="角色:">
                  <el-select multiple v-model="addForm.role_id_list" class="m-2" placeholder="Select">
                      <el-option
                      v-for="item in allRole"
                      :key="item.id"
                      :label="item.role_name"
                      :value="item.id"
                      />
                  </el-select>
              </el-form-item>
            </el-form>
            <el-row class="mb-4">
              <el-button type="danger" @click="this.addVisible = false">取消</el-button>
              <el-button type="primary" @click="addResource()">确认</el-button>
          </el-row>
          </el-dialog>
        <!-- update form -->
        <el-dialog width="30%" title="更新" v-model="updateVisible" :close-on-click-modal="false" :close-on-press-escape="false">
          <el-form>
              <el-form-item label="ID:">
                  <el-input disabled v-model="updateForm.id"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="用户:">
                  <el-input v-model="updateForm.username"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="邮箱:">
                  <el-input v-model="updateForm.email"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="电话:">
                  <el-input v-model="updateForm.phone"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="角色:">
                  <el-select multiple v-model="updateForm.role_id_list" class="m-2" placeholder="Select">
                      <el-option v-for="item in allRole" :key="item.id" :label="item.role_name" :value="item.id"/>
                  </el-select>
              </el-form-item>
            </el-form>
            <el-row class="mb-4">
              <el-button type="danger" @click="this.updateVisible = false">取消</el-button>
              <el-button type="primary" @click="updateResource()">更新</el-button>
          </el-row>
          </el-dialog>
        <!-- delete form -->
        <el-dialog v-model="deleteVisible" title="删除" width="30%">
          <span>确认删除吗？</span>
              <template #footer>
              <span class="dialog-footer">
                  <el-button @click="deleteVisible = false">取消</el-button>
                  <el-button type="primary" @click="deleteResource()">确认</el-button>
              </span>
              </template>
        </el-dialog>
      </el-card>
    </el-main>
  </el-container>
</template>
<script>
import Api from '@/api/index';
import { ElMessage } from 'element-plus'
import router from '@/router/index'
import store from '../store';

export default {
  data() {
    return {
      first_lable: "用户管理",
      second_lable: "用户列表",
      tableData: [],
      addForm: {
          username: "",
          password: "",
          email: "",
          phone: "",
          role_id_list: [],
      },
      deleteForm: {id: ""},
      updateForm: {
          id: "",
          email: "",
          phone: "",
          role_id_list: [],
      },
      selectForm: {username: ""},
      allRole: [],
      addVisible: false,
      updateVisible: false,
      deleteVisible: false,
      // 这几个变量用来控制按钮权限
      use_url: "/api/menu",
      addDisable: true,
      updateDisable: true,
      deleteDisable: true,
    } 
  },
  computed: {
    userInfo() {
        return store.state.userInfo
      }
  },
  methods: {
    addResource(){
      Api.user("POST", this.addForm).then((response) => {
          if(response.status === 201) {
              ElMessage({
                  showClose: true,
                  message: '添加成功...',
                  type: 'success',
              })
          }
      })
      this.addVisible = false
      router.go(0)
    },
    deleteResource(){
      Api.user("DELETE", {id: this.deleteForm.id}, this.deleteForm.id).then((response) => {
          if(response.status === 204) {
              ElMessage({
                  showClose: true,
                  message: '删除成功...',
                  type: 'warning',
              })
          }
      })
      this.deleteVisible = false
      router.go(0)
    },
    updateResource(){
      Api.user("PUT", this.updateForm, this.updateForm.id).then((response) => {
          if(response.status === 200) {
              ElMessage({
                  showClose: true,
                  message: '更新成功...',
                  type: 'success',
              })
          }
      })
      this.updateVisible = false
      router.go(0)
    },
    selectResource(){
      Api.user("GET", {"username": this.selectForm.username}).then((response) => {
        console.log(response.data)
        this.tableData = response.data
      })
    },
    getData(){
      Api.user("GET", {}).then((response) => {
        console.log(response)
        this.tableData = response.data
      }),
      Api.role("GET", {}).then((response) => {
        this.allRole = response.data
      })
    },
    deleteOpen(id){
      this.deleteForm.id = id
      this.deleteVisible = true
    },
    updateOpen(row){
      console.log(row)
      this.updateForm.id = row.id
      this.updateForm.username = row.username
      this.updateForm.email = row.email
      this.updateForm.phone = row.phone
      
      row.role.forEach(k => {
        this.updateForm.role_id_list.push(k.role_id)        
      });

      this.updateVisible = true
    },
    setDisable(){
        this.use_url
        this.userInfo["permissions"].forEach(k => {
          console.log(k)
          if(k.per_url === this.use_url){
            if(k.per_method === "POST"){
              this.addDisable = false
            }
            if(k.per_method === "PUT"){
              this.updateDisable = false
            }
            if(k.per_method === "DELETE"){
              this.deleteDisable = false
            }
          } 
        })
      }
  },
  mounted() {
    this.getData()
    Api.userInfo()
    this.setDisable()
  },
}
</script>
<style scoped>
.el-form .el-form-item {
  width: 100%;
}
</style>