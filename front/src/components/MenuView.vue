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
          <el-input v-model="this.selectForm.menu_title" placeholder="根据名称查询" style="width: 200px;" />

          <el-button type="primary" style="margin-left: 10px;">
            <el-icon style="vertical-align: middle">
              <Search />
            </el-icon>
            <span style="vertical-align: middle" @click="selectResource()"> 搜索 </span>
          </el-button>

          <el-button type="primary" :disabled="this.addDisable" @click="this.addVisible = true">
            <el-icon style="vertical-align: middle">
              <Plus />
            </el-icon>
            <span style="vertical-align: middle"> 添加 </span>
          </el-button>

        </div>
        <!-- table -->
        <div style="margin-top: 20px;">
          <el-table :data="tableData" style="width: 100%;" row-key="id" default-expand-all height="520">
            <el-table-column prop="menu_title" label="菜单名称" />
            <el-table-column prop="menu_icon" label="菜单icon" />
            <el-table-column prop="route_path" label="路由path" />
            <el-table-column prop="parent_id" label="父ID" />
            <el-table-column prop="index" label="优先级" />
            <el-table-column label="Operations">
              <template #default="scope">
                <el-button :disabled="this.updateDisable" @click="updateOpen(scope.row)">更新</el-button>
                <el-button :disabled="this.deleteDisable" type="danger" @click="deleteOpen(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <!-- add form -->
        <el-dialog width="30%" title="添加" v-model="addVisible" :close-on-click-modal="false" :close-on-press-escape="false">
            <el-form>
              <el-form-item label="菜单名称:">
                  <el-input v-model="addForm.menu_title"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="菜单icon:">
                  <el-input v-model="addForm.menu_icon"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="路由path:">
                  <el-input v-model="addForm.route_path"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="父级菜单:">
                  <el-select v-model="addForm.parent_id" class="m-2" placeholder="Select">
                      <el-option
                      v-for="item in rootMenus"
                      :key="item.id"
                      :label="item.menu_title"
                      :value="item.id"
                      />
                  </el-select>
              </el-form-item>
              <el-form-item label="优先级:">
                  <el-input v-model="addForm.index"  style="width: 200px;" type="text" clearable></el-input>
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
              <el-form-item label="菜单ID:">
                  <el-input v-model="updateForm.id" disabled style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="菜单名称:">
                  <el-input v-model="updateForm.menu_title"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="菜单icon:">
                  <el-input v-model="updateForm.menu_icon"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="路由path:">
                  <el-input v-model="updateForm.route_path"  style="width: 200px;" type="text" clearable></el-input>
              </el-form-item>
              <el-form-item label="父级菜单:">
                  <el-select v-model="updateForm.parent_id" class="m-2" placeholder="Select">
                      <el-option
                      v-for="item in rootMenus"
                      :key="item.id"
                      :label="item.menu_title"
                      :value="item.id"
                      />
                  </el-select>
              </el-form-item>
              <el-form-item label="优先级:">
                  <el-input v-model="updateForm.index"  style="width: 200px;" type="text" clearable></el-input>
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
      first_lable: "菜单管理",
      second_lable: "菜单列表",
      tableData: [],
      addForm: {
          menu_title: "",
          menu_icon: "",
          route_path: "",
          parent_id: "",
          index: "",
      },
      deleteForm: {id: ""},
      updateForm: {
          id: "",
          menu_title: "",
          menu_icon: "",
          route_path: "",
          parent_id: "",
          index: "",
      },
      selectForm: {menu_title: ""},
      rootMenus: [{id: 0, menu_title: "根菜单"}],
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
      Api.menu("POST", this.addForm).then((response) => {
          if(response.status === 201) {
            this.addVisible = false
            router.go(0)
            ElMessage({
              showClose: true,
              message: '添加成功...',
              type: 'success',
            })
          }
      })
    },
    deleteResource(){
      Api.menu("DELETE", {id: this.deleteForm.id}, this.deleteForm.id).then((response) => {
          if(response.status === 204) {
            this.deleteVisible = false
            router.go(0)
            ElMessage({
                showClose: true,
                message: '删除成功...',
                type: 'warning',
            })
          }
          if(response.status === 301) {
            ElMessage({
              showClose: true,
              message: '请先删除关联资源...',
              type: 'warning',
            })
          } 
      })
      
    },
    updateResource(){
      Api.menu("PUT", this.updateForm, this.updateForm.id).then((response) => {
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
      Api.menu("GET", {"menu_title": this.selectForm.menu_title}).then((response) => {
        this.tableData = response.data
      })
    },
    getData(){
      Api.menu("GET", {}).then((response) => {
        response.data.forEach((k) => {
            if(k.parent_id === 0){
              console.log(k)
              this.tableData.push(k)
              this.rootMenus.push({id: k.id, menu_title: k.menu_title})
            }
        })
      })
    },
    deleteOpen(id){
      this.deleteForm.id = id
      this.deleteVisible = true
    },
    updateOpen(row){
      this.updateForm.id = row.id
      this.updateForm.menu_title = row.menu_title
      this.updateForm.menu_icon = row.menu_icon
      this.updateForm.route_path = row.route_path
      this.updateForm.parent_id = row.parent_id
      this.updateForm.index = row.index
      this.updateVisible = true
    },
    setDisable(){
      this.use_url
      this.userInfo["permissions"].forEach(k => {
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