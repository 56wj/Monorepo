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
      <el-table-column prop="rollName" label="品名" width="300">
        <template slot-scope="scope">
          <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.rollName" placeholder="请输入内容"></el-input>
          <div v-else class="txt">{{ scope.row.rollName }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="rollThickness" label="厚度(mm)" width="300">
        <template slot-scope="scope">
          <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.rollThickness" placeholder="请输入内容" @input="exitcheck('rollThickness', scope.row)"></el-input>
          <div v-else class="txt">{{ scope.row.rollThickness }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="rollLength" label="长度(m)">
        <template slot-scope="scope">
          <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.rollLength" placeholder="请输入内容" @input="exitcheck('rollLength', scope.row)"></el-input>
          <div v-else class="txt">{{ scope.row.rollLength }}</div>
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
      <el-table-column fixed="right" label="操作" width="250">
        <template slot="header" slot-scope="scope">
          <el-button type="primary" @click="drawer = true">新增数据</el-button>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" v-if="scope.row.isEdit" @click="handleSave(scope.$index, scope.row)">保存</el-button>
          <el-button size="mini" v-else @click="handleEdit(scope.$index, scope.row)" :disabled="oneEdit">编辑</el-button>
          <el-button size="mini"  @click="openDialog(scope.$index, scope.row)">编辑托盘表</el-button>
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
    <el-drawer title="新增配置项" :before-close="handleClose" :with-header="false" :visible.sync="drawer" direction="ltr"
      custom-class="demo-drawer" ref="drawer">
      <div class="demo-drawer__content">
        <el-row><span style="font-size: 30px;font-weight :600;">新增配置项</span></el-row>
        <el-form ref="config" :model="form" :rules="rules" style="margin-top: 20px;">
          <el-form-item label="品名" label-width="120px" prop="rollName">
            <el-input v-model.number="form.rollName" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="厚度" label-width="120px" prop="rollThickness">
            <el-input v-model="form.rollThickness" autocomplete="off" @input="handleInput('rollThickness')"><template slot="append">mm</template></el-input>
          </el-form-item>
          <el-form-item label="长度" label-width="120px" prop="rollLength">
            <el-input v-model="form.rollLength" autocomplete="off" @input="handleInput('rollLength')"><template slot="append">m</template></el-input>
          </el-form-item>
        </el-form>
        <div class="demo-drawer__footer">
          <el-button @click="cancelForm">取 消</el-button>
          <el-button type="primary" @click="$refs.drawer.closeDrawer()" :loading="loading">{{ loading ? '提交中 ...' : '确定'
            }}</el-button>
        </div>
      </div>
    </el-drawer>
    <el-dialog title="托盘盛放表" :visible.sync="dialogTableVisible">
      <el-table :data="dialogData" :key="forceRefresh2" height=530px border>
        <el-table-column property="palletId" label="托盘Id" width="200"></el-table-column>
        <el-table-column property="palletName" label="托盘" width="200"></el-table-column>
        <el-table-column property="palletType" label="托盘种类" width="200"></el-table-column>
        <el-table-column property="rollNums" label="单托盘可放个数">
          <template slot-scope="scope">
            <el-input v-if="scope.row.isEdit" class="item" v-model.number="scope.row.rollNums" placeholder="请输入盛放个数"></el-input>
            <div v-else class="txt">{{ tray1111(scope.row) }}</div>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button size="mini" v-if="scope.row.isEdit"
            @click="handleSave2(scope.$index, scope.row)">保存</el-button>
            <el-button size="mini" v-else @click="handleEdit2(scope.$index, scope.row)" :disabled="oneEdit2">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelDialog">取 消</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
// import SockJS from  'sockjs-client';  
import { get_roll, roll_delete, update_roll, add_roll } from '@/api/roll'
import { get_palletroll, update_palletroll } from '@/api/rollPallet'
import { get_pallet } from '@/api/pallet'
import { check } from '@/utils/inputCheck'
import { mapGetters } from 'vuex'
import * as xlsx from 'xlsx/xlsx.mjs'


export default {
  data() {
    return {
      form: {
        rollName: '',
        rollThickness: '',
        rollLength: '',
      },
      rules: {
        rollName: [
        { required: true, message: '请输入品名', trigger: 'blur' },
        ],
        rollThickness: [
          { required: true, message: '请输入厚度(cm)', trigger: 'blur' },
        ],
        rollLength: [
          { required: true, message: '请输入长度(cm)', trigger: 'blur' },
        ],
      },
      tableData: [],
      dialogData: [],
      total: 0,  //总数据条数
      currentpage: 1,  //当前所在页默认是第一页
      pagesize: 10,  //每页显示多少行数据 默认设置为10
      pageData: [],//分页后的当前页数据
      loading: false,
      drawer: false,
      forceRefresh: '',
      forceRefresh2: '',
      oneEdit: false,
      oneEdit2: false,
      dialogTableVisible: false,
      temp: {}
    }
  },
  methods: {
    async get_tableData() {
      try {
        const res = await get_roll();
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
      row.rollNums ? showProp = row.rollNums : showProp = '---'
      return showProp
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
          update_roll(row).then(() => {
            this.$message({
              type: 'success',
              message: '更新成功!'
            });
            row.isEdit = false;
            this.$data.oneEdit = false;
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
        roll_delete({id: row.id}).then(() => {
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
          add_roll(this.$data.form).then(() => {
             done();
            this.$data.form = {
              rollName: '',
              rollThickness: '',
              rollLength: '',
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
    },
    // dialog控制
    async openDialog(index, row){
      try {
        var data = {
          rollId: row.id
        }
        const res = await get_palletroll(data);
        this.$data.dialogData = res.data;
        this.$data.dialogData.forEach((res) => {
          Object.assign(res, { isEdit: false });
        })
        this.$data.dialogTableVisible = true; 
      } catch(error) {
        // this.$message.error("获取数据失败，请刷新页面")
      }
    },
    cancelDialog() {
      this.$data.dialogTableVisible = false;
    },
    handleEdit2(index, row) {
      this.$data.temp = JSON.parse(JSON.stringify(row));
      row.isEdit = true;
      this.$data.oneEdit2 = true;
      let time = parseInt(new Date().getTime() / 1000) + '';
      this.$data.forceRefresh2 = time;
    },
    handleSave2(index, row) {
      var data = {
          palletId: row.palletId,
          rollId: row.rollId,
          rollNums: row.rollNums
        }
      let time = parseInt(new Date().getTime() / 1000) + '';
        this.$confirm('将更新本条数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          update_palletroll(data).then(() => {
            this.$message({
              type: 'success',
              message: '更新成功!'
            });
            row.isEdit = false;
            this.$data.oneEdit2 = false;
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
    // 数据检查
    handleInput(name){         
      this.$data.form[name] = check(this.$data.form[name])
           
    },
    exitcheck(name, row) {
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
.el-input-group__append {
  width: 65px;
  text-align: center;
}
</style>