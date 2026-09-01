<template>
  <div class="dashboard-container">
    <el-form ref="form" :model="form" label-width="100px"
      style="box-shadow: 6px 6px 6px rgba(0,0,0,0.1)">
      <el-row>
        <el-col :span=8>
          <el-form-item label="部门：">
            <el-select v-model="form.type" placeholder="请选择">
              <el-option v-for="item in options_department" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span=8>
          <el-form-item label="权限：">
            <el-select v-model="form.state" placeholder="请选择">
              <el-option v-for="item in options_roles" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span=8>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">查询</el-button>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span=8>
          <el-form-item label="用户名：">
            <el-input placeholder="请输入" v-model="form.username" style="width: 202px" clearable>
            </el-input>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-table :data="pageData" style="width: 100%; margin-top: 20px" height=1100px border
      :default-sort="{ prop: 'id', order: 'descending' }" @selection-change="handleSelectionChange" :key="forceRefresh">
      <el-table-column
      type="selection"
      width="55">
      </el-table-column>
      <el-table-column prop="id" label="编号" width="100" sortable>
      </el-table-column>
      <el-table-column prop="username" label="用户名" width="200" sortable>
        <template slot-scope="scope">
          <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.username" placeholder="请输入内容"></el-input>
          <div v-else class="txt">{{ scope.row.username }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="department" label="所属部门" width="240">
        <template slot-scope="scope">
          <el-select v-if="scope.row.isEdit" v-model="scope.row.department">
                    <el-option v-for="item in options_department_update" :key="item.value" :label="item.label"
                      :value="item.value">
                    </el-option>
          </el-select>
          <div v-else class="txt">{{ scope.row.department }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="roles" label="权限类型" width="240">
        <template slot-scope="scope">
          <!-- <el-select v-if="scope.row.isEdit" v-model="scope.row.roles">
                    <el-option v-for="item in options_roles_update" :key="item.value" :label="item.label"
                      :value="item.value">
                    </el-option>
          </el-select>
          <div v-else class="txt">{{ scope.row.roles=="admin" ? "管理员" : "用户" }}</div> -->
          <div class="txt">{{ scope.row.roles=="admin" ? "管理员" : "用户" }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="phone" label="电话" width="240">
      </el-table-column>
      <el-table-column prop="email" label="邮箱">
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="250">
        <template slot="header" slot-scope="scope">
          <el-button type="primary" @click="drawer = true">新增用户</el-button>
          <el-button type="danger" @click="multiDelete">删除</el-button>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" v-if="scope.row.isEdit"
          @click="handleSave(scope.$index, scope.row)">保存</el-button>
          <el-button size="mini" v-else @click="handleEdit(scope.$index, scope.row)" :disabled="oneEdit">编辑</el-button>
          <el-button size="mini" @click="drawerPassword(scope.$index, scope.row)">修改密码</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--分页-->
    <el-row>
      <el-col style="text-align:center">
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentpage"
          :page-sizes="[20, 50, 100]" :page-size="pagesize" layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </el-col>
    </el-row>
    <!-- 新增抽屉 -->
    <el-drawer title="新增用户" :before-close="handleClose" :with-header="false" :visible.sync="drawer" direction="ltr"
      custom-class="demo-drawer" ref="drawer">
      <div class="demo-drawer__content">
        <el-row><span style="font-size: 30px;font-weight :600;">新增用户</span></el-row>
        <el-form ref="user" :model="userForm" :rules="rules" style="margin-top: 20px;">
          <el-form-item label="用户名" label-width="120px" prop="username">
            <el-input v-model="userForm.username" autocomplete="off" style="width: 202px;"></el-input>
          </el-form-item>
          <el-form-item label="所属部门" label-width="120px">
            <el-select v-model="userForm.department">
                    <el-option v-for="item in options_department_update" :key="item.value" :label="item.label"
                      :value="item.value">
                    </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="权限" label-width="120px">
            <el-select v-model="userForm.roles">
                    <el-option v-for="item in options_roles_update" :key="item.value" :label="item.label"
                      :value="item.value">
                    </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div class="demo-drawer__footer">
          <el-button @click="cancelForm">取 消</el-button>
          <el-button type="primary" @click="$refs.drawer.closeDrawer()" :loading="loading">{{ loading ? '提交中 ...' : '确定'
            }}</el-button>
        </div>
      </div>
    </el-drawer>
    <!-- 弹窗 -->
    <el-dialog
      title="修改密码"
      :visible.sync="dialogVisible"
      width="30%">
      <el-form ref="password" :model="passwordForm" :rules="rules">
          <el-form-item label="新密码" label-width="120px" prop="newPassword">
            <el-input v-model="passwordForm.newPassword" autocomplete="off" style="width: 300px;"></el-input>
          </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelDialog">取 消</el-button>
        <el-button type="primary" @click="submitDialog">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
// import SockJS from  'sockjs-client';  
// import { get_history, get_result,to_delete,batch_delete } from '@/api/type1'
import { get_user,update_password,delete_user,add_user,update_user } from '@/api/userManage'
import { get_department } from '@/api/department'
import { mapGetters } from 'vuex'
import * as xlsx from 'xlsx/xlsx.mjs'


export default {
  data() {
    return {
      form: {
        department: null,
        roles: null,
        username: "",
      },
      userForm: {
        department: "",
        roles: "editor",
        username: "",
        password: "change-me",
        phone: "",
        email: ""
      },
      passwordForm: {
        uid: null,
        newPassword: ""
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
        ],
        newPassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, max: 19, message: '密码长度在 6 到 19 位', trigger: 'blur' }
        ],
      },
      options_department: [{
        value: null,
        label: '全部门'
      }],
      options_roles: [{
        value: null,
        label: '全类型'
      },{
        value: 'admin',
        label: '管理员'
      }, {
        value: 'editor',
        label: '用户'
      }],
      options_department_update: [],
      options_roles_update: [{
        value: 'admin',
        label: '管理员'
      }, {
        value: 'editor',
        label: '用户'
      }],
      total: 0,  //总数据条数
      currentpage: 1,  //当前所在页默认是第一页
      pagesize: 20,  //每页显示多少行数据 默认设置为10
      pageData: [],//分页后的当前页数据
      loading: false,
      department: null,
      roles: null,
      username: "",
      forceRefresh: '',
      drawer: false,
      dialogVisible: false,
      id: null,
      multipleSelection: [],
      oneEdit: false,
      temp: {}
    }
  },
  methods: {
    async init() {
      try {
        const res = await get_department()
        this.$data.userForm.department = res.data[0].departmentName;
        res.data.forEach(element => {
          this.$data.options_department.push({
            value: element.departmentName,
            label: element.departmentName
          })
          this.$data.options_department_update.push({
            value: element.departmentName,
            label: element.departmentName
          })
        });
        this.getPageInfo();
      } catch(error) {
        // this.$message.error("获取部门数据失败，请刷新页面")
      }
    },
    //修改、删除数据，以及保存、编辑的按钮切换
    multiDelete() {
      if(this.$data.multipleSelection.length == 0){
        this.$message({
          type: 'info',
          message: '请先选择要删除的数据'
        });
        return;
      }
      this.$confirm('将删除选中数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        if(this.$data.pageData.length == this.$data.multipleSelection.length && this.$data.currentpage != 1){
          this.$data.currentpage -= 1;
        }
        delete_user(this.$data.multipleSelection).then(() => {
          this.getPageInfo();
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
        })
        // console.log(this.$data.multipleSelection)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    },
    //分页数据刷新
    async getPageInfo() {
      var data = {
        pageNum: this.$data.currentpage,
        pageSize: this.$data.pagesize,
        department: this.$data.department,
        roles: this.$data.roles,
        username: this.$data.username
      };
      //清空pageTicket中的数据
      this.$data.pageData = [];
      try {
        // 获取当前页的数据
        const res = await get_user(data);
        this.$data.total = res.data.total;
        this.$data.pageData = res.data.items;
        this.$data.pageData.forEach((res) => {
          Object.assign(res, { isEdit: false });
        })
      } catch(error) {
        // this.$message.error("获取用户数据失败，请重试或刷新页面")
      }
    },
    async onSubmit() {
      this.$data.currentpage = 1;
      this.$data.department = this.$data.form.department;
      this.$data.roles = this.$data.form.roles;
      this.$data.username = this.$data.form.username;
      var data = {
        pageNum: this.$data.currentpage,
        pageSize: this.$data.pagesize,
        department: this.$data.department,
        roles: this.$data.roles,
        username: this.$data.username
      };
      try {
        // 获取当前页的数据
        const res = await get_user(data);
        this.$data.total = res.data.total;
        this.$data.pageData = res.data.items;
      } catch(error) {
        // this.$message.error("查询数据失败，请刷新页面")
      }
    },
    //分页时修改每页的行数,这里会自动传入一个size
    handleSizeChange(size) {
      //修改当前每页的数据行数
      this.$data.pagesize = size;
      //数据重新分页
      this.getPageInfo();
    },
    //调整当前的页码
    handleCurrentChange(pageNumber) {
      //修改当前的页码
      this.$data.currentpage = pageNumber;
      //数据重新分页
      this.getPageInfo()
    },
    // 多选框设置
    handleSelectionChange(val) {
      var id_list = [];
      val.forEach(element => {
        id_list.push(element.id);
      });
      // console.log(id_list);
      this.$data.multipleSelection = id_list;
    },
    //修改、删除数据，以及保存、编辑的按钮切换
    handleEdit(index, row) {
      this.$data.temp = JSON.parse(JSON.stringify(row));
      row.isEdit = true;
      this.$data.oneEdit = true;
      let time = parseInt(new Date().getTime() / 1000) + '';
      this.$data.forceRefresh = time;
    },
    handleSave(index, row) {
      let time = parseInt(new Date().getTime() / 1000) + '';
        this.$confirm('将更新本条数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          var data = {
            id: row.id,
            username: row.username,
            department: row.department,
          }
          update_user(data).then(() => {
            this.$message({
              type: 'success',
              message: '更新成功!'
            });
            row.isEdit = false;
            this.$data.oneEdit = false;
            this.getPageInfo();
            this.$data.forceRefresh = time;
          }).catch(() => {this.$message.error("更新失败")})
        }).catch(() => {
          for (let key in this.$data.temp) {
            if (this.$data.temp.hasOwnProperty(key) && row.hasOwnProperty(key)) {
              row[key] = this.$data.temp[key];
            }
          }
          this.$data.oneEdit = false;
          this.$data.forceRefresh = time;
          this.$message({
            type: 'info',
            message: '已取消更新'
          });
        });
    },
    drawerPassword(index, row) {
      this.$data.passwordForm.uid = row.id;
      this.$data.dialogVisible = true;
    },
    // 抽屉管理
    handleClose(done) {
      if (this.$data.loading) {
        return;
      }
      this.$confirm('确定要提交表单吗？')
        .then(() => {
          this.loading = true;
          var data = 
            {
              department: this.$data.userForm.department,
              roles: this.$data.userForm.roles,
              username: this.$data.userForm.username,
              password: "change-me",
              email: "",
              phone: ""
            }
          add_user(data).then(() => {
            done();
            this.$data.form = 
            {
              department: null,
              roles: null,
              username: ""
            }
            this.$data.loading = false;
            this.getPageInfo();
            this.$message({
              type: 'success',
              message: '新增成功!'
            });
          }).catch(() => {this.$message.error("新增失败")})
        }).catch(() => {
            this.$message({
            type: 'info',
            message: '已取消新增'
          });
        });
    },
    cancelForm() {
      this.$data.loading = false;
      this.$data.drawer = false;
      this.$refs.user.clearValidate()
    },
    // 弹窗管理
    submitDialog() {
      this.$confirm('确定要更新密码吗？')
        .then(() => {
          update_password(this.$data.passwordForm).then(() => {
            this.$data.passwordForm = 
            {
              uid: null,
              newPassword: ""
            }
            this.$message({
              type: 'success',
              message: '修改成功!'
            });
            this.$data.dialogVisible = false;
          });
        }).catch(() => {
            this.$data.passwordForm = 
            {
              uid: null,
              newPassword: ""
            }
            this.$message({
            type: 'info',
            message: '已取消修改'
          });
        });
    },
    cancelDialog() {
      this.$data.passwordForm = 
      {
        uid: null,
        newPassword: ""
      }
      this.$data.dialogVisible = false;
      this.$refs.password.clearValidate()
    }
  },
  created() {
    // this.getPageInfo();
    this.init();
  },
  mounted() {

  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }

  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
.demo-drawer__content {
    display: flex;
    flex-direction: column;
    height: 100%;
}
.demo-drawer__content form {
    flex: 1;
}
.demo-drawer__footer {
    display: flex;
}
.demo-drawer__footer button {
    flex: 1;
}
</style>

<style lang="scss">
.title .el-form-item__label {
  font-size: 30px;
}

.title .el-form-item {
  border-bottom-width: none;
}
.el-drawer__body {
    padding: 20px;
}
</style>