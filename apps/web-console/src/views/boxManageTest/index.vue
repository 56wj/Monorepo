<template>
  <div class="dashboard-container">
    <el-form ref="form" :model="form" label-width="100px" style="box-shadow: 6px 6px 6px rgba(0,0,0,0.1)">
      <el-row>
        <el-col :span=24>
          <el-form-item label="卷膜规格管理：" class="title" label-width="230px"></el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-table :data="pageData" style="width: 100%; margin-top: 20px" height=530px border :default-sort="{ prop: 'id' }"
      :key="forceRefresh">
      <el-table-column prop="id" label="编号" width="100" sortable>
      </el-table-column>
      <el-table-column prop="thickness" label="品名" width="240">
        <template slot-scope="scope">
          <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.thickness" placeholder="请输入内容"></el-input>
          <div v-else class="txt">{{ scope.row.thickness }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="thickness" label="厚度" width="240">
        <template slot-scope="scope">
          <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.thickness" placeholder="请输入内容"></el-input>
          <div v-else class="txt">{{ scope.row.thickness }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="length" label="长度">
        <template slot-scope="scope">
          <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.length" placeholder="请输入内容"></el-input>
          <div v-else class="txt">{{ scope.row.length }}</div>
        </template>
      </el-table-column>
      <!-- <el-table-column prop="tray1111" label="1.1*1.1托盘盛放数" width="300" :formatter="tray1111">
        <template slot-scope="scope">
          <el-input v-if="scope.row.isEdit" class="item" v-model.number="scope.row.tray1111"
            placeholder="请输入内容"></el-input>
          <div v-else class="txt">{{ tray1111(scope.row) }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="tray1311" label="1.3*1.1托盘盛放数" width="300" :formatter="tray1311">
        <template slot-scope="scope">
          <el-input v-if="scope.row.isEdit" class="item" v-model.number="scope.row.tray1311"
            placeholder="请输入内容"></el-input>
          <div v-else class="txt">{{ tray1311(scope.row) }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="tray1411" label="1.4*1.1托盘盛放数" :formatter="tray1411">
        <template slot-scope="scope">
          <el-input v-if="scope.row.isEdit" class="item" v-model.number="scope.row.tray1411"
            placeholder="请输入内容"></el-input>
          <div v-else class="txt">{{ tray1411(scope.row) }}</div>
        </template>
      </el-table-column> -->
      <el-table-column fixed="right" label="操作" width="300">
        <template slot="header" slot-scope="scope">
          <el-button type="primary" @click="drawer = true">新增数据</el-button>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" v-if="scope.row.isEdit" @click="handleSave(scope.$index, scope.row)">保存</el-button>
          <el-button size="mini" v-else @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
          <el-button size="mini" @click="dialogTableVisible=true">查看托盘</el-button>
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
    <!-- 新增表单 -->
    <el-drawer title="新增配置项" :before-close="handleClose" :visible.sync="drawer" direction="ltr"
      custom-class="demo-drawer" ref="drawer">
      <div class="demo-drawer__content">
        <el-form ref="config" :model="form" :rules="rules">
          <el-form-item label="厚度（mm）" label-width="120px" prop="thickness">
            <el-input v-model.number="form.thickness" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="长度（mm）" label-width="120px" prop="length">
            <el-input v-model.number="form.length" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="1.1米托盘盛放数" label-width="120px" prop="tray1111">
            <el-input v-model.number="form.tray1111" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="1.3米托盘盛放数" label-width="120px" prop="tray1311">
            <el-input v-model.number="form.tray1311" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="1.4米托盘盛放数" label-width="120px" prop="tray1411">
            <el-input v-model.number="form.tray1411" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div class="demo-drawer__footer">
          <el-button @click="cancelForm">取 消</el-button>
          <el-button type="primary" @click="$refs.drawer.closeDrawer()" :loading="loading">{{ loading ? '提交中 ...' : '确定'
            }}</el-button>
        </div>
      </div>
    </el-drawer>
    <!-- 查看托盘 -->
    <el-dialog title="规格确认表" :visible.sync="dialogTableVisible">
      <el-table :data="dialog" :key="forceRefresh2">
        <el-table-column property="partno" label="托盘" width="200"></el-table-column>
        <el-table-column property="number" label="单托盘可放个数">
          <template slot-scope="scope">
            <el-input v-if="scope.row.isEdit" class="item" v-model.number="scope.row.number" placeholder="请输入盛放个数"></el-input>
            <div v-else class="txt">{{ scope.row.number }}</div>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="200">
          <template slot-scope="scope">
            <el-button size="mini" v-if="scope.row.isEdit"
            @click="handleSave2(scope.$index, scope.row)">保存</el-button>
            <el-button size="mini" v-else @click="handleEdit2(scope.$index, scope.row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
// import SockJS from  'sockjs-client';  
import { get_config, to_delete, update_config, add_config } from '@/api/config'
import { mapGetters } from 'vuex'
import * as xlsx from 'xlsx/xlsx.mjs'


export default {
  data() {
    return {
      form: {
        length: '',
        thickness: '',
        tray1111: '',
        tray1311: '',
        tray1411: ''
      },
      rules: {
        thickness: [
          { required: true, message: '请输入厚度(cm)', trigger: 'blur' },
          { type: 'number', message: '厚度必须为数字值', trigger: 'blur'}
        ],
        length: [
          { required: true, message: '请输入长度(cm)', trigger: 'blur' },
          { type: 'number', message: '长度必须为数字值', trigger: 'blur'}
        ],
        tray1111: [
          { type: 'number', message: '必须为数字值', trigger: 'blur' }
        ],
        tray1311: [
          { type: 'number', message: '必须为数字值', trigger: 'blur' }
        ],
        tray1411: [
          { type: 'number', message: '必须为数字值', trigger: 'blur' }
        ],
      },
      tableData: [],
      total: 0,  //总数据条数
      currentpage: 1,  //当前所在页默认是第一页
      pagesize: 10,  //每页显示多少行数据 默认设置为10
      pageData: [],//分页后的当前页数据
      dialog:[],
      loading: false,
      drawer: false,
      dialogTableVisible: false,
      forceRefresh: '',
      forceRefresh2: '',
    }
  },
  methods: {
    async get_tableData() {
      try {
        const res = await get_config();
        this.$data.tableData = res.data;
        this.$data.tableData.forEach((res) => {
          Object.assign(res, { isEdit: false });
        })
        console.log(this.$data.tableData)
        this.$data.total = res.data.length;
        this.getPageInfo();
      } catch(error) {
        // this.$message.error("获取数据失败，请刷新页面")
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
    tray1111(row) {
      let showProp = null
      row.tray1111 ? showProp = row.tray1111 : showProp = '---'
      return showProp
    },
    tray1311(row) {
      let showProp = null
      row.tray1311 ? showProp = row.tray1311 : showProp = '---'
      return showProp
    },
    tray1411(row) {
      let showProp = null
      row.tray1411 ? showProp = row.tray1411 : showProp = '---'
      return showProp
    },
    //修改、删除数据，以及保存、编辑的按钮切换
    handleEdit(index, row) {
      row.isEdit = true;
      let time = parseInt(new Date().getTime() / 1000) + '';
      this.$data.forceRefresh = time;
    },
    handleSave(index, row) {
      let time = parseInt(new Date().getTime() / 1000) + '';
      var temp = row;
        this.$confirm('将更新本条数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          update_config(row).then(() => {
            this.$message({
              type: 'success',
              message: '更新成功!'
            });
            row.isEdit = false;
            this.$data.forceRefresh = time;
          }).catch(() => {this.$message.error("更新失败")})
        }).catch(() => {
          row = temp;
          row.isEdit = false;
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
        to_delete({id: row.id}).then(() => {
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
          add_config(this.$data.form).then(() => {
             done();
            this.$data.form = {
              height: '',
              thickness: '',
              tray1111: '',
              tray1311: '',
              tray1411: ''
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
      this.$refs.config.clearValidate()
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