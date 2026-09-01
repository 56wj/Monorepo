<template>
  <div class="dashboard-container">
    <el-form ref="form" :model="form" label-width="100px" style="box-shadow: 6px 6px 6px rgba(0,0,0,0.1)">
      <el-row>
        <el-col :span=24>
          <el-form-item label="纸管管理：" class="title" label-width="230px"></el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-table :data="pageData" style="width: 100%; margin-top: 20px" height=530px border :default-sort="{ prop: 'id' }"
      :key="forceRefresh">
      <el-table-column prop="id" label="id" width="100" sortable>
      </el-table-column>
      <el-table-column prop="tubeName" label="规格" width="300">
        <template slot-scope="scope">
          <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.tubeName" placeholder="请输入内容"></el-input>
          <div v-else class="txt">{{ scope.row.tubeName }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="tubeApproximate" label="近似值">
        <template slot-scope="scope">
          <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.tubeApproximate" placeholder="请输入内容" @input="exitcheck('tubeApproximate', scope.row)"></el-input>
          <div v-else class="txt">{{ scope.row.tubeApproximate }}</div>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="200">
        <template slot="header" slot-scope="scope">
          <el-button type="primary" @click="drawer = true">新增数据</el-button>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" v-if="scope.row.isEdit" @click="handleSave(scope.$index, scope.row)">保存</el-button>
          <el-button size="mini" v-else @click="handleEdit(scope.$index, scope.row)" :disable="oneEdit">编辑</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--分页-->
    <el-row>
      <el-col style="text-align:center">
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentpage"
          :page-sizes="[10, 20, 50]" :page-size="pagesize" layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </el-col>
    </el-row>
    <!-- 新增抽屉 -->
    <el-drawer title="新增配置项" :before-close="handleClose" :with-header="false" :visible.sync="drawer" direction="ltr"
      custom-class="demo-drawer" ref="drawer">
      <div class="demo-drawer__content">
        <el-row><span style="font-size: 30px;font-weight :600;">新增配置项</span></el-row>
        <el-form ref="department" :model="form" :rules="rules" style="margin-top: 20px;">
          <el-form-item label="规格" label-width="120px" prop="tubeName">
            <el-input v-model="form.tubeName" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="近似直径" label-width="120px" prop="tubeApproximate">
            <el-input v-model="form.tubeApproximate" autocomplete="off" @input="exitcheck('tubeApproximate')"></el-input>
          </el-form-item>
        </el-form>
        <div class="demo-drawer__footer">
          <el-button @click="cancelForm">取 消</el-button>
          <el-button type="primary" @click="$refs.drawer.closeDrawer()" :loading="loading">{{ loading ? '提交中 ...' : '确定'
            }}</el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
// import SockJS from  'sockjs-client';  
import { get_tube,tube_delete,update_tube,add_tube } from '@/api/tube'
import { mapGetters } from 'vuex'
import { check } from '@/utils/inputCheck' 


export default {
  data() {
    return {
      form: {
        tubeName: '',
        tubeApproximate: ''
      },
      rules: {
        tubeName: [
          { required: true, message: '请输入规格名', trigger: 'blur' },
        ],
        tubeApproximate: [
          { required: true, message: '请输入近似直径', trigger: 'blur' },
        ]
      },
      tableData: [],
      total: 0,  //总数据条数
      currentpage: 1,  //当前所在页默认是第一页
      pagesize: 10,  //每页显示多少行数据 默认设置为10
      pageData: [],//分页后的当前页数据
      loading: false,
      drawer: false,
      forceRefresh: '',
      oneEdit: false,
      temp: {}
    }
  },
  methods: {
    async get_tableData() {
      try {
        const res = await get_tube();
        this.$data.tableData = res.data;
        this.$data.tableData.forEach((res) => {
          Object.assign(res, { isEdit: false });
        })
        console.log(this.$data.tableData)
        this.$data.total = res.data.length;
        this.getPageInfo();
      } catch(error) {
        // this.$message.error("获取部门数据失败，请刷新页面")
      }
    },
    //分页数据刷新
    getPageInfo() {
      //清空pageTicket中的数据
      this.$data.pageData = [];
      // 获取当前页的数据
      for (let i = (this.$data.currentpage - 1) * this.$data.pagesize; i < this.$data.total; i++) {
        //把遍历的数据添加到pageTicket里面
        this.$data.pageData.push(this.$data.tableData[i]);
        //判断是否达到一页的要求
        if (this.$data.pageData.length === this.$data.pagesize) break;
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
            tubeName: row.tubeName,
            tubeApproximate: row.tubeApproximate
          }
          update_tube(data).then(() => {
            this.$message({
              type: 'success',
              message: '更新成功!'
            });
            row.isEdit = false;
            this.$data.oneEdit = false;
            this.get_tableData();
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
    handleDelete(index, row) {
      this.$confirm('将删除本条数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        tube_delete({id: row.id}).then(() => {
          this.get_tableData();
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
        }).catch(() => {this.$message.error("删除失败")})
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    },
    handleClose(done) {
      if (this.$data.loading) {
        return;
      }
      this.$confirm('确定要提交表单吗？')
        .then(() => {
          this.loading = true;
          add_tube(this.$data.form).then(() => {
            done();
            this.$data.form = 
            {
              tubeName: '',
              tubeApproximate: ''
            }
            this.$data.loading = false;
            this.get_tableData();
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
      this.$refs.department.clearValidate()
    },
    exitcheck(name, row) {
      // row[name] = row[name]
      //              .replace(/[^\-\d.]/g, '')  //只能输入   数字 小数点 -
      //              .replace(/\-{2,}/g, "-") // 只能出现一次- 
      //              .replace(/^0+(\d)/, '$1') //如果第一位是 0 就替换成后面的数字
      //              .replace(/^\./, '0.') //如果第一位是 . 就 替换成  0.
      //              .match(/^[\d\-]*(\.?\d{0,5})/g)[0] || ''  //开头只能允许数字或者 -
      row[name] = check(row[name])
    }
  },
  created() {
    this.get_tableData();
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