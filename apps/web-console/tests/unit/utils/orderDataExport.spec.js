import {
  getOrderWeightUnit,
  sanitizeOrderFileName,
  toOrderExportRows
} from '@/utils/orderDataExport'

describe('历史订单数据导出', () => {
  test('按导入模板列名和顺序转换订单数据', () => {
    const rows = toOrderExportRows([{
      name: 'A',
      order_thickness: 12,
      real_thickness: 11.8,
      width: 780,
      order_height: 1000,
      real_height: 998,
      number: 2,
      density: 0.905,
      weight: 1.25,
      diameter: 600,
      priority: 1,
      isEdit: false
    }])

    expect(Object.keys(rows[0])).toEqual([
      '品名', '订单厚度', '厚度', '宽度', '订单长度', '长度',
      '卷数', '密度', '重量', '直径', '优先级'
    ])
    expect(rows[0].品名).toBe('A')
    expect(rows[0].重量).toBe(1.25)
    expect(rows[0].isEdit).toBeUndefined()
  })

  test('对kg历史订单还原存储前的重量单位', () => {
    expect(getOrderWeightUnit({ config: { t_or_kg: true }})).toBe('kg')
    expect(toOrderExportRows([{ weight: 1.25 }], 'kg')[0].重量).toBe(1250)
    expect(getOrderWeightUnit({ config: { t_or_kg: false }})).toBe('T')
  })

  test('清理文件名非法字符', () => {
    expect(sanitizeOrderFileName(' PO/2026:08*21 ')).toBe('PO_2026_08_21')
    expect(sanitizeOrderFileName('')).toBe('未命名订单')
  })
})
