const MM_PER_CM = 10

export function heightCmToMm(value) {
  if (value === null || typeof value === 'undefined' || String(value).trim() === '') {
    return null
  }
  const height = Number(value)
  return Number.isFinite(height) ? height * MM_PER_CM : null
}

export function validateOverlapHeightValue(value, fieldLabel) {
  if (value === '' || value === null || typeof value === 'undefined') {
    return `请输入${fieldLabel}(cm)`
  }

  const height = Number(value)
  if (!Number.isFinite(height)) {
    return `${fieldLabel}必须为数字`
  }
  if (height <= 0) {
    return `${fieldLabel}必须大于0cm`
  }
  return ''
}

export function validateOverlapConfig(config, maxVehicleHeightCm) {
  if (!config || !config.overlap) {
    return ''
  }

  const singleError = validateOverlapHeightValue(config.single_max_height, '单层膜卷本体高度上限')
  if (singleError) return singleError

  const totalError = validateOverlapHeightValue(config.entire_max_height, '叠后膜卷本体总高度上限')
  if (totalError) return totalError

  const vehicleHeight = Number(maxVehicleHeightCm)
  if (Number.isFinite(vehicleHeight) && vehicleHeight > 0) {
    if (Number(config.single_max_height) > vehicleHeight || Number(config.entire_max_height) > vehicleHeight) {
      return `叠膜高度上限不得超过所选车厢最小净高${vehicleHeight}cm。本页单位为cm：700mm应填70，780mm应填78。`
    }
  }

  return ''
}
