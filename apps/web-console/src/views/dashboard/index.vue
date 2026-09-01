<template>
  <div class="dashboard-container">
    <!-- <div class="dashboard-text">name: {{ name }}</div> -->
    <el-row><span style="font-size: 30px;font-weight :600;">凯利装箱系统</span></el-row>
    <el-row style="margin-top: 20px;">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>更新公告</span>
        </div>
        <div class="text item">
          <el-collapse v-model="activeName" accordion>
            <el-collapse-item title="2024.11.27更新" name="10">
              <div>悬空结果界面：增加半径列。</div>
              <div>悬空结果界面：修复灰图的情况。</div>
              <div>悬空结果界面：修复时间显示错误的情况。</div>
              <div>更正部分名词显示。</div>
            </el-collapse-item>
            <el-collapse-item title="2024.10.29更新" name="9">
              <div>悬空结果界面：货物颜色优化。</div>
              <div>货物数据输入界面：更新了错误检测。</div>
              <div>更正部分名词显示。</div>
            </el-collapse-item>
            <el-collapse-item title="2024.10.17更新" name="8">
              <div>托盘装箱一阶段界面：增加创建。</div>
              <div>悬空装箱界面：增加纸管尺寸。</div>
              <div>悬空装箱界面：增加到货日期。</div>
              <div>悬空结果界面：增加车头显示。</div>
              <!-- <div>用户管理界面：权限修改。</div> -->
            </el-collapse-item>
            <el-collapse-item title="2024.10.10更新" name="7">
              <div>增加悬空装箱。</div>
            </el-collapse-item>
            <el-collapse-item title="2024.9.4更新" name="6">
              <div>托盘装箱导入数据页面：订单号不再限制只有数字。</div>
              <div>3D展示页面修改：增加了excel导出。</div>
            </el-collapse-item>
            <el-collapse-item title="2024.9.1更新" name="5">
              <div>对于导入的货物数据增加了空数据检查。</div>
              <div>3D展示页面修改：增加了托盘总数。</div>
              <div>修复了托盘管理页面托盘重量描述的问题。</div>
            </el-collapse-item>
            <el-collapse-item title="2024.7.21更新" name="4">
              <div>一阶段结果表增加预设表数据显示。</div>
              <div>3D展示页面修改：增加数据读取。</div>
              <div>装箱算法修复。</div>
            </el-collapse-item>
            <el-collapse-item title="2024.7.12更新" name="3">
              <!-- <div>3D展示页面修改：一阶段计算中手动修改的托盘盛放数会在浮动框中标明。</div> -->
              <div>3D展示页面修改：增加显示“订单卷膜数”。</div>
            </el-collapse-item>
            <el-collapse-item title="2024.7.8更新" name="2">
              <div>增加托盘管理页面。</div>
              <div>卷膜规格管理页面修改：根据托盘种类的变化进行显示。</div>
              <div>3D展示页面修改：“合计卷膜数” -> “车箱卷膜数”。</div>
              <div>3D展示页面修改：增加显示“未装入卷膜数”。</div>
              <div>托盘装箱导入数据页面：可以选择自定义的托盘。</div>
              <div>托盘装箱导入数据页面：导入数据时可以选择单位，输入后统一转化为以吨为单位。</div>
              <div>修复了效果图与文字标注数不符的问题。</div>
              <div>优化了侧边栏的显示。</div>
            </el-collapse-item>
            <el-collapse-item title="2024.6.13更新" name="1">
              <div>托盘装箱导入数据页面：订单号不再限制6位。</div>
              <div>3D展示页面修改：字体的颜色进行了加深。</div>
              <div>3D展示页面修改：添加了“合计卷膜数”显示。</div>
              <div>详细展示页面修改：增加了“高度”显示。</div>
              <div>增加顶部历史页面，可以用于快速返回</div>
              <div>修复了服务器配置导致的 WebSocket 连接失败、无法导出、装箱效果图不显示的问题</div>
            </el-collapse-item>
          </el-collapse>
        </div>
      </el-card>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import * as xlsx from 'xlsx/xlsx.mjs'
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ]),
  },
  data() {
    return {
        fileList: [],
        xlsxData: [],
        tableData: [],
        total:0,  //总数据条数
        currentpage:1,  //当前所在页默认是第一页
        pagesize:10,  //每页显示多少行数据 默认设置为10
        pageData:[],//分页后的当前页数据
      }
  },
  methods: {
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
