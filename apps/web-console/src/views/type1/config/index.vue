<template>
  <div class="dashboard-container">
    <el-form ref="form" :model="form" label-width="100px"
      style="box-shadow: 6px 6px 6px rgba(0,0,0,0.1)">
      <el-row>
        <el-col :span = 24>
          <el-form-item label="卷膜规格表：" class="title" label-width="auto"></el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-table :data="pageData" style="width: 100%; margin-top: 20px" height=530px border
      :default-sort="{ prop: 'id' }">
      <el-table-column prop="id" label="编号" width="100" sortable>
      </el-table-column>
      <el-table-column prop="rollName" label="品名" width="300">
      </el-table-column>
      <el-table-column prop="rollThickness" label="厚度(mm)" width="300">
      </el-table-column>
      <el-table-column prop="rollLength" label="长度(m)">
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="200">
        <template slot-scope="scope">
          <el-button size="mini"  @click="openDialog(scope.$index, scope.row)">查看托盘表</el-button>
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
    <el-dialog title="托盘盛放表" :visible.sync="dialogTableVisible">
      <el-table :data="dialogData" :key="forceRefresh2" height=530px border>
        <el-table-column property="palletId" label="托盘Id" width="100"></el-table-column>
        <el-table-column property="palletName" label="托盘" width="300"></el-table-column>
        <el-table-column property="palletType" label="托盘种类" width="300"></el-table-column>
        <el-table-column property="rollNums" label="单托盘可放个数">
          <template slot-scope="scope">
            <el-input v-if="scope.row.isEdit" class="item" v-model.number="scope.row.rollNums" placeholder="请输入盛放个数"></el-input>
            <div v-else class="txt">{{ tray1111(scope.row) }}</div>
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
import { get_roll } from '@/api/roll'
import { get_palletroll } from '@/api/rollPallet'
import { mapGetters } from 'vuex'
import * as xlsx from 'xlsx/xlsx.mjs'


export default {
  data() {
    return {
      form: {},
      tableData: [],
      total: 0,  //总数据条数
      currentpage: 1,  //当前所在页默认是第一页
      pagesize: 10,  //每页显示多少行数据 默认设置为10
      pageData: [],//分页后的当前页数据
      loading: false,
      dialogTableVisible: false,
      dialogData: []
    }
  },
  methods: {
    async get_tableData() {
      try {
        const res = await get_roll();
        this.$data.tableData = res.data;
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
    // dialog控制
    async openDialog(index, row){
      try {
        var data = {
          rollId: row.id
        }
        const res = await get_palletroll(data);
        this.$data.dialogData = res.data;
        this.$data.dialogTableVisible = true; 
      } catch(error) {
        // this.$message.error("获取数据失败，请刷新页面")
      }
    },
    cancelDialog() {
      this.$data.dialogTableVisible = false;
    },
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
</style>

<style lang="scss">
.title .el-form-item__label {
  font-size: 30px;
}

.title .el-form-item {
  border-bottom-width: none;
}
</style>
<style lang="scss">
.title .el-form-item__label {
  font-size: 30px;
}

.title .el-form-item {
  border-bottom-width: none;
}
</style>