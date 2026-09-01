export const ORDER_DATA_COLUMNS = [
  { label: '品名', key: 'name', width: 24 },
  { label: '订单厚度', key: 'order_thickness', width: 14 },
  { label: '厚度', key: 'real_thickness', width: 14 },
  { label: '宽度', key: 'width', width: 14 },
  { label: '订单长度', key: 'order_height', width: 14 },
  { label: '长度', key: 'real_height', width: 14 },
  { label: '卷数', key: 'number', width: 10 },
  { label: '密度', key: 'density', width: 12 },
  { label: '重量', key: 'weight', width: 14 },
  { label: '直径', key: 'diameter', width: 14 },
  { label: '优先级', key: 'priority', width: 10 }
]

export function getOrderWeightUnit(sourceJson) {
  return sourceJson && sourceJson.config && sourceJson.config.t_or_kg ? 'kg' : 'T'
}

export function toOrderExportRows(tableData, weightUnit = 'T') {
  if (!Array.isArray(tableData)) return []

  return tableData.map(item => {
    const row = {}
    ORDER_DATA_COLUMNS.forEach(column => {
      let value = item && item[column.key] != null ? item[column.key] : ''
      // 计算前端会把kg转成T再保存历史源数据，导出时还原为用户选择的单位。
      if (column.key === 'weight' && weightUnit === 'kg' && value !== '') {
        const numericValue = Number(value)
        value = Number.isFinite(numericValue) ? numericValue * 1000 : value
      }
      row[column.label] = value
    })
    return row
  })
}

export function sanitizeOrderFileName(orderId) {
  const normalized = String(orderId == null ? '' : orderId)
    .trim()
    .replace(/[\\/:*?"<>|]+/g, '_')
  return normalized || '未命名订单'
}
