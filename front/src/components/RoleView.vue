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
  
            <el-button type="primary" @click="this.addVisible = true" :disabled="this.addDisable">
              <el-icon style="vertical-align: middle">
                <Plus />
              </el-icon>
              <span style="vertical-align: middle"> 添加 </span>
            </el-button>
  
          </div>
          <!-- table -->
          <div style="margin-top: 20px;">
            <el-table :data="tableData" style="width: 100%;" row-key="id" default-expand-all>
              <!-- <el-table-column prop="id" label="ID"/> -->
              <el-table-column prop="role_name" label="角色名称"/>
              <el-table-column prop="permission_list" label="菜单列表">
                <template #default="scope">
                    <el-tag v-for="item in scope.row.menu_list" :key="item.id">{{ item.menu_title }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="menu_list" label="权限列表">
                <template #default="scope">
                    <el-tag v-for="item in scope.row.permission_list" :key="item.id">{{ item.per_name }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="Operations">
                <template #default="scope">
                  <el-button @click="updateOpen(scope.row)" :disabled="this.updateDisable">更新</el-button>
                  <el-button type="danger" @click="deleteOpen(scope.row.id)" :disabled="this.deleteDisable">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <!-- add form -->
          <el-dialog width="50%" title="添加" v-model="addVisible" :close-on-click-modal="false" :close-on-press-escape="false">
              <el-form>
                <el-form-item label="角色名称:">
                    <el-input v-model="addForm.role_name"  style="width: 200px;" type="text" clearable></el-input>
                </el-form-item>
                <el-form-item label="菜单列表:">
                  <el-transfer filterable :titles="menus_trans_title" v-model="addForm.menus" :data="menusData" />
                </el-form-item>
                <el-form-item label="权限列表:">
                  <el-transfer filterable :titles="menus_trans_title" v-model="addForm.pers" :data="persData" />
                </el-form-item>
              </el-form>
              <el-row class="mb-4">
                <el-button type="danger" @click="this.addVisible = false">取消</el-button>
                <el-button type="primary" @click="addResource()">确认</el-button>
              </el-row>
            </el-dialog>
          <!-- update form -->
          <el-dialog width="50%" title="更新" v-model="updateVisible" :close-on-click-modal="false" :close-on-press-escape="false">
            <el-form>
                <el-form-item label="角色名称:">
                    <el-input v-model="updateForm.role_name"  style="width: 200px;" type="text" clearable></el-input>
                </el-form-item>
                <el-form-item label="菜单列表:">
                  <el-transfer filterable :titles="menus_trans_title" v-model="updateForm.menus" :data="menusData" />
                </el-form-item>
                <el-form-item label="权限列表:">
                  <el-transfer filterable :titles="pers_trans_title" v-model="updateForm.pers" :data="persData" />
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
        first_lable: "角色管理",
        second_lable: "角色列表",
        tableData: [],
        addForm: {
            role_name: "",
            menus: [],
            pers: [],
        },
        deleteForm: {id: ""},
        updateForm: {
            id: "",
            role_name: "",
            menus: [],
            pers: [],
        },
        selectForm: {menu_title: ""},
        rootMenus: [{id: 0, menu_title: "根菜单"}],
        addVisible: false,
        updateVisible: false,
        deleteVisible: false,
        menusData: [],
        persData: [],
        menus_trans_title: ["未拥有的菜单", "已拥有的菜单"],
        pers_trans_title: ["未拥有的权限", "已拥有的权限"],
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
        Api.role("POST", this.addForm).then((response) => {
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
        Api.role("DELETE", {id: this.deleteForm.id}, this.deleteForm.id).then((response) => {
            if(response.status === 204) {
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
        this.deleteVisible = false
        router.go(0)
      },
      updateResource(){
        Api.role("PUT", this.updateForm, this.updateForm.id).then((response) => {
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
        Api.role("GET", {}).then((response) => {
          this.tableData = response.data
        }),
        Api.menu("GET", {}).then((response) => {
          response.data.forEach((k) => {
              this.menusData.push({
                key: k.id,
                label: k.menu_title,
              })
          })
        }),
        Api.permission("GET", {}).then((response) => {
          response.data.forEach((k) => {
              this.persData.push({
                key: k.id,
                label: k.per_name,
              })
          })
        })
      },
      deleteOpen(id){
        this.deleteForm.id = id
        this.deleteVisible = true
      },
      updateOpen(row){
        this.updateForm.id = row.id
        this.updateForm.role_name = row.role_name
        row.permission_list.forEach((k) => {
          this.updateForm.pers.push(k.id)
        })
        row.menu_list.forEach((k) => {
          this.updateForm.menus.push(k.id)
        })
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