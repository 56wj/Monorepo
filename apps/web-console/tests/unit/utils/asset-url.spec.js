import {
  downloadAssetFile,
  getAssetFileName,
  getAssetUrl
} from '@/utils/asset-url'

describe('结果资源下载', () => {
  test('把历史服务器的 /images/ 地址改为当前页面同源地址', () => {
    expect(getAssetUrl('http://localhost:5001/images/task-1/order.xlsx'))
      .toBe('http://localhost/images/task-1/order.xlsx')
    expect(getAssetFileName('/images/task-1/order.xlsx')).toBe('order.xlsx')
  })

  test('校验文件响应后通过 Blob 触发下载', async() => {
    const click = jest.fn()
    const appendChild = jest.fn()
    const removeChild = jest.fn()
    const link = { style: {}, click }
    const blob = { size: 128 }
    const fetcher = jest.fn().mockResolvedValue({
      ok: true,
      status: 200,
      headers: { get: () => 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' },
      blob: jest.fn().mockResolvedValue(blob)
    })
    const urlApi = {
      createObjectURL: jest.fn().mockReturnValue('blob:test'),
      revokeObjectURL: jest.fn()
    }
    const documentRef = {
      body: { appendChild, removeChild },
      createElement: jest.fn().mockReturnValue(link)
    }

    const result = await downloadAssetFile('/images/task-1/order.xlsx', 'order.xlsx', {
      fetch: fetcher,
      document: documentRef,
      URL: urlApi
    })

    expect(fetcher).toHaveBeenCalledWith('http://localhost/images/task-1/order.xlsx', {
      credentials: 'same-origin'
    })
    expect(link.href).toBe('blob:test')
    expect(link.download).toBe('order.xlsx')
    expect(click).toHaveBeenCalledTimes(1)
    expect(appendChild).toHaveBeenCalledWith(link)
    expect(removeChild).toHaveBeenCalledWith(link)
    expect(urlApi.revokeObjectURL).toHaveBeenCalledWith('blob:test')
    expect(result.size).toBe(128)
  })

  test('拦截 SPA 回退页，避免把 HTML 伪装成 Excel', async() => {
    const fetcher = jest.fn().mockResolvedValue({
      ok: true,
      status: 200,
      headers: { get: () => 'text/html; charset=utf-8' }
    })

    await expect(downloadAssetFile('/images/task-1/order.xlsx', 'order.xlsx', { fetch: fetcher }))
      .rejects.toThrow('/images/ 代理')
  })
})
