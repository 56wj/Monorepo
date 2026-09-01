<template>
  <div class="dashboard-container">
    <el-form ref="form" :model="form" label-width="100px"
      style="box-shadow: 6px 6px 6px rgba(0,0,0,0.1)">
      <el-row>
        <el-col :span=8>
          <el-form-item label="装箱类型：">
            <el-select v-model="form.type" placeholder="请选择">
              <el-option v-for="item in options_type" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span=8>
          <el-form-item label="计算进度：">
            <el-select v-model="form.state" placeholder="请选择">
              <el-option v-for="item in options_state" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span=8>
          <el-form-item>
            <el-button type="primary" @click="onSubmit(1)">查询</el-button>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span=8>
          <el-form-item label="订单号：">
            <el-input placeholder="请输入6位订单号" v-model="form.orderId" style="width: 202px" clearable>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span=16>
          <el-form-item label="日期：">
              <el-date-picker
              v-model="form.date"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期">
              </el-date-picker>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-table :data="pageData" style="width: 100%; margin-top: 20px" height=1100px border
      :default-sort="{ prop: 'id', order: 'descending' }" @selection-change="handleSelectionChange" ref='table' @header-dragend="changeColWidth"  >
      <el-table-column
      type="selection"
      width="55">
      </el-table-column>
      <el-table-column prop="id" label="编号" width="100" sortable  min-width="10%">
      </el-table-column>
      <el-table-column prop="orderId" label="订单号" width="100" sortable>
      </el-table-column>
      <el-table-column prop="type" label="装箱类型" width="240">
      </el-table-column>
      <el-table-column prop="state" label="计算进度" width="240">
      </el-table-column>
      <el-table-column prop="userName" label="创建人" width="240">
      </el-table-column>
      <el-table-column prop="createTime" label="创立时间" width="330" sortable>
      </el-table-column>
      <el-table-column show-overflow-tooltip="true" prop="updateTime" label="完成时间" width="auto" sortable>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="250">
        <template slot="header" slot-scope="scope">
          <el-button type="danger" @click="multiDelete">删除</el-button>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" @click="handleRead(scope.$index, scope.row)" :disabled="scope.row.state=='整托计算完成'||scope.row.state=='悬空计算完成'?false:true">3D展示</el-button>
          <el-button size="mini" @click="handleConfig(scope.$index, scope.row)">读取配置</el-button>
          <el-button size="mini" @click="handleExport(scope.$index, scope.row)">导出</el-button>
          <!-- <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button> -->
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

  </div>
</template>

<script>
// import SockJS from  'sockjs-client';  
import { get_history, get_result,to_delete,batch_delete } from '@/api/task'
import store from '@/store'
// import download from 'downloadjs'
import { mapGetters } from 'vuex'
import * as xlsx from 'xlsx/xlsx.mjs'
import { downloadAssetFile, getAssetFileName, getAssetUrl } from '@/utils/asset-url'


export default {
  name: 'history',
  data() {
    return {
      form: {
        type: null,
        state: null,
        orderId: "",
        date: ""
      },
      options_type: [{
        value: null,
        label: '全类型'
      }, {
        value: '托盘装箱',
        label: '托盘装箱'
      }, {
        value: '悬空装箱',
        label: '悬空装箱'
      }, {
        value: '散装装箱',
        label: '散装装箱'
      }],
      options_state: [{
        value: null,
        label: '全状态'
      },{
        value: '悬空计算完成',
        label: '悬空计算完成'
      },{
        value: '整托计算完成',
        label: '整托计算完成'
      }, 
       {
        value: '小托计算完成',
        label: '小托计算完成'
      }, {
        value: '计算失败',
        label: '计算失败'
      }, {
        value: '计算中',
        label: '计算中'
      }
      , {
        value: '网络错误',
        label: '网络错误'
      }],
      total: 0,  //总数据条数
      currentpage: 1,  //当前所在页默认是第一页
      pagesize: 20,  //每页显示多少行数据 默认设置为10
      pageData: [],//分页后的当前页数据
      loading: false,
      type: null,
      state: null,
      orderId: "",
      startTime: "",
      endTime: "",
      multipleSelection: []
    }
  },
  methods: {
    //修改、删除数据，以及保存、编辑的按钮切换
    async handleExport(index, row) {
      var data = { taskId: row.id };
      try {
        const res = await get_result(data);
        // var url = store.getters.url + "/" + res.data.resultJson.excel_address;
        // var url = "http://localhost:9001" + "/" + res.data.resultJson.excel_address;
        var url = getAssetUrl(res.data.resultJson.excel_address);
        var fileName = getAssetFileName(res.data.resultJson.excel_address);
        console.log(url)
        console.log(fileName)
        await downloadAssetFile(url, fileName)
        this.$message.success(`结果文件 ${fileName} 已导出`)
      } catch(error) {
        console.error('结果文件导出失败', error)
        this.$message.error(error.message || '结果文件导出失败，请重试')
      }
    },
    async handleRead(index, row) {
      var data = { taskId: row.id };
      try {
        const res = await get_result(data);
        console.log(res)
        var obj = res.data.resultJson;
        var arr = Object.keys(obj);
        console.log(arr)
        var config = res.data.sourceJson.config;
        var taskId = res.data.task.id;
        // var source = res.data.sourceJson;
        if(row.type=="托盘装箱"){
            this.$router.push({
            path: '/type1/3D_result',
            query: {
              obj: JSON.stringify(obj),
              arr: JSON.stringify(arr),
              config: JSON.stringify(config),
              taskId: JSON.stringify(taskId)
              // source: JSON.stringify(source)
            }           
          }) // 带参跳转
        }
        else if(row.type=="悬空装箱"){
            this.$router.push({
            path: '/type2/3D_result2',
            query: {
              data: JSON.stringify(obj),
              arr: JSON.stringify(arr),
              config: JSON.stringify(config),
              taskId: JSON.stringify(taskId)
              // source: JSON.stringify(source)
            }           
          }) // 带参跳转
        }
        else if(row.type=="散装装箱"){}
      } catch(error) {
        // this.$message.error("读取数据失败，请重试")
      }
    },
    async handleConfig(index, row) {
      var data = { taskId: row.id };
      try {
        const res = await get_result(data);
        console.log(res)
        var source = res.data.sourceJson
        if(row.type=="托盘装箱"){
            this.$router.push({
            path: '/type1/get_data',
            query: {
              source: source
            }           
          }) // 带参跳转
        }
        else if(row.type=="悬空装箱"){
            this.$router.push({
            path: '/type2/get_data2',
            query: {
              source: source
            }           
          }) // 带参跳转
        }
        else if(row.type=="散装装箱"){}
      } catch(error) {
        // this.$message.error("读取数据失败，请重试")
      }
    },
    // handleDelete(index, row) {
    //   this.$confirm('将删除本条数据, 是否继续?', '提示', {
    //     confirmButtonText: '确定',
    //     cancelButtonText: '取消',
    //     type: 'warning'
    //   }).then(() => {
    //     to_delete({taskId: row.id}).then(() => {
    //       this.getPageInfo();
    //       this.$message({
    //         type: 'success',
    //         message: '删除成功!'
    //       });
    //     })
    //   }).catch(() => {
    //     this.$message({
    //       type: 'info',
    //       message: '已取消删除'
    //     });
    //   });
    // },
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
        batch_delete(this.$data.multipleSelection).then(() => {
          this.getPageInfo();
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
        })
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
        type: this.$data.type,
        state: this.$data.state,
        orderId: this.$data.orderId,
        startTime: this.$data.startTime,
        endTime: this.$data.endTime
      };
      //清空pageTicket中的数据
      this.$data.pageData = [];
      // 获取当前页的数据
      try{
        const res = await get_history(data);
        this.$data.total = res.data.total;
        this.$data.pageData = res.data.items;
      } catch(error) {
        // this.$message.error("获取下一页数据失败，请重试")
      }
    },
    // async firstPageInfo() {
    //   var data = {
    //     pageNum: this.$data.currentpage,
    //     pageSize: this.$data.pagesize,
    //     type: this.$data.type,
    //     state: this.$data.state
    //   };
    //   // 获取当前页的数据
    //   const res = await get_history(data);
    //   this.$data.total = res.data.total;
    //   this.$data.pageData = res.data.items;
    // },
    async onSubmit(index) {
      this.$data.currentpage = index;
      this.$data.type = this.$data.form.type;
      this.$data.state = this.$data.form.state;
      this.$data.orderId = this.$data.form.orderId;
      this.$data.startTime = this.$data.form.date[0];
      this.$data.endTime = this.$data.form.date[1];
      var data = {
        pageNum: this.$data.currentpage,
        pageSize: this.$data.pagesize,
        type: this.$data.form.type,
        state: this.$data.form.state,
        orderId: this.$data.form.orderId,
        startTime: this.$data.form.date[0],
        endTime: this.$data.form.date[1],
      };
      // 获取当前页的数据
      try {
        const res = await get_history(data);
        this.$data.total = res.data.total;
        this.$data.pageData = res.data.items;
      } catch(error) {
        // this.$message.error("查询失败，请重试")
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
    changeColWidth(nw, ow, col, evt) {
      const widthTable = parseInt(document.querySelector('.addressBook .el-table').offsetWidth);
      let realWidth = parseInt((col.minWidth * widthTable) / 100);
      console.log(widthTable)
      if(nw > realWidth + 50){
        col.width = realWidth + 50;
      }else if(nw < 70){
        col.width = 70;
      }else{
        col.width = realWidth;
      }
    }
  },
  created() {
    console.log("created")
    this.getPageInfo();
  },
  activated(){
    console.log("activated")
    this.onSubmit(this.$data.currentpage);
    this.$refs.table.doLayout();
  },
  mounted() {

  },
  destroyed() {
    console.log("destroyed")
    console.log(store.getters.cachedViews)
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
// .el-table{
//   width: 100%;
//   .el-table__header-wrapper table,.el-table__body-wrapper table{
//     width: 100% !important;
//   }
//   .el-table__body, .el-table__footer, .el-table__header{
//     table-layout: auto;
//   }
// }

</style>
