<template>
  <el-dialog
    title="历史订单数据导出"
    :visible.sync="dialogVisible"
    width="900px"
    append-to-body
    @open="handleOpen"
  >
    <div class="history-filter">
      <el-input
        v-model.trim="orderId"
        placeholder="输入订单号"
        clearable
        class="order-input"
        @keyup.enter.native="search"
      />
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
      />
      <el-button type="primary" icon="el-icon-search" @click="search">查询</el-button>
      <el-button @click="resetSearch">重置</el-button>
    </div>

    <el-alert
      title="导出文件的“订单数据”工作表可直接重新上传；重量会按历史订单的 kg/T 设置还原。"
      type="info"
      :closable="false"
      show-icon
      class="export-tip"
    />

    <el-table v-loading="loading" :data="orders" height="420" border>
      <el-table-column prop="orderId" label="订单号" min-width="140" show-overflow-tooltip />
      <el-table-column prop="state" label="计算进度" width="140" />
      <el-table-column prop="userName" label="创建人" width="120" />
      <el-table-column prop="createTime" label="创建时间" width="180" />
      <el-table-column label="操作" width="120" fixed="right">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="mini"
            :loading="exportingTaskId === scope.row.id"
            :disabled="isCalculating(scope.row)"
            @click="exportOrder(scope.row)"
          >导出数据</el-button>
        </template>
      </el-table-column>
      <template slot="empty">
        <span>{{ loading ? '加载中' : '暂无可导出的历史订单' }}</span>
      </template>
    </el-table>

    <div class="history-pagination">
      <el-pagination
        :current-page="pageNum"
        :page-size="pageSize"
        :page-sizes="[10, 20, 50]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </el-dialog>
</template>

<script>
import * as xlsx from 'xlsx/xlsx.mjs'
import { get_history, get_result } from '@/api/task'
import {
  ORDER_DATA_COLUMNS,
  getOrderWeightUnit,
  sanitizeOrderFileName,
  toOrderExportRows
} from '@/utils/orderDataExport'

export default {
  name: 'HistoricalOrderExportDialog',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    taskType: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      orderId: '',
      dateRange: [],
      orders: [],
      total: 0,
      pageNum: 1,
      pageSize: 10,
      loading: false,
      exportingTaskId: null
    }
  },
  computed: {
    dialogVisible: {
      get() {
        return this.visible
      },
      set(value) {
        this.$emit('update:visible', value)
      }
    }
  },
  methods: {
    handleOpen() {
      this.pageNum = 1
      this.loadOrders()
    },
    async loadOrders() {
      this.loading = true
      const dateRange = Array.isArray(this.dateRange) ? this.dateRange : []
      try {
        const res = await get_history({
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          type: this.taskType,
          orderId: this.orderId || null,
          startTime: dateRange[0] || null,
          endTime: dateRange[1] || null
        })
        this.orders = res.data.items || []
        this.total = res.data.total || 0
      } catch (error) {
        this.orders = []
        this.total = 0
        this.$message.error('历史订单加载失败，请重试')
      } finally {
        this.loading = false
      }
    },
    search() {
      this.pageNum = 1
      this.loadOrders()
    },
    resetSearch() {
      this.orderId = ''
      this.dateRange = []
      this.pageNum = 1
      this.loadOrders()
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.pageNum = 1
      this.loadOrders()
    },
    handleCurrentChange(page) {
      this.pageNum = page
      this.loadOrders()
    },
    isCalculating(row) {
      return String(row && row.state ? row.state : '').includes('计算中')
    },
    async exportOrder(row) {
      this.exportingTaskId = row.id
      try {
        const res = await get_result({ taskId: row.id })
        const sourceJson = res.data && res.data.sourceJson
        const tableData = sourceJson && sourceJson.tableData
        const weightUnit = getOrderWeightUnit(sourceJson)
        const exportRows = toOrderExportRows(tableData, weightUnit)

        if (!exportRows.length) {
          this.$message.warning('该订单没有可导出的货物数据')
          return
        }

        const workbook = xlsx.utils.book_new()
        const orderSheet = xlsx.utils.json_to_sheet(exportRows, {
          header: ORDER_DATA_COLUMNS.map(column => column.label)
        })
        orderSheet['!cols'] = ORDER_DATA_COLUMNS.map(column => ({ wch: column.width }))
        xlsx.utils.book_append_sheet(workbook, orderSheet, '订单数据')

        const infoRows = [
          { '字段': '订单号', '内容': row.orderId || '' },
          { '字段': '装箱类型', '内容': row.type || this.taskType },
          { '字段': '计算进度', '内容': row.state || '' },
          { '字段': '创建人', '内容': row.userName || '' },
          { '字段': '创建时间', '内容': row.createTime || '' },
          { '字段': '重量单位', '内容': weightUnit }
        ]
        const infoSheet = xlsx.utils.json_to_sheet(infoRows, { header: ['字段', '内容'] })
        infoSheet['!cols'] = [{ wch: 16 }, { wch: 32 }]
        xlsx.utils.book_append_sheet(workbook, infoSheet, '订单信息')

        const fileName = `${sanitizeOrderFileName(row.orderId)}_历史订单数据.xlsx`
        xlsx.writeFile(workbook, fileName)
        this.$message.success(`订单 ${row.orderId || row.id} 数据已导出`)
      } catch (error) {
        this.$message.error('订单数据导出失败，请重试')
      } finally {
        this.exportingTaskId = null
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.history-filter {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.order-input {
  width: 190px;
}

.export-tip {
  margin-bottom: 14px;
}

.history-pagination {
  margin-top: 18px;
  text-align: right;
}
</style>
