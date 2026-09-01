import {
  heightCmToMm,
  validateOverlapConfig,
  validateOverlapHeightValue
} from '@/utils/overlapValidation'

describe('膜叠膜高度规则校验', () => {
  test('cm和mm换算口径明确', () => {
    expect(heightCmToMm(70)).toBe(700)
    expect(heightCmToMm('78')).toBe(780)
    expect(heightCmToMm('')).toBeNull()
    expect(heightCmToMm('   ')).toBeNull()
  })

  test('开启膜叠膜后两个高度必填', () => {
    expect(validateOverlapConfig({
      overlap: true,
      single_max_height: '',
      entire_max_height: ''
    }, 250)).toContain('请输入')

    expect(validateOverlapConfig({
      overlap: true,
      single_max_height: 70,
      entire_max_height: ''
    }, 250)).toContain('总高度')
  })

  test('关闭膜叠膜时不要求高度', () => {
    expect(validateOverlapConfig({ overlap: false }, 250)).toBe('')
  })

  test('拒绝非正数和超出车厢的cm值', () => {
    expect(validateOverlapHeightValue(0, '单层高度')).toContain('大于0')
    expect(validateOverlapConfig({
      overlap: true,
      single_max_height: 700,
      entire_max_height: 700
    }, 250)).toContain('700mm应填70')
  })
})
