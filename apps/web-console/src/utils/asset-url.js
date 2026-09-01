const ABSOLUTE_URL_RE = /^[a-z][a-z\d+\-.]*:\/\//i

function getCurrentOrigin() {
  if (typeof window !== 'undefined' && window.location && window.location.origin) {
    return window.location.origin
  }
  return (process.env.VUE_APP_HTTP_URL || '').replace(/\/$/, '')
}

function buildCurrentOriginUrl(pathname, search = '', hash = '') {
  return `${getCurrentOrigin()}${pathname}${search}${hash}`
}

export function getAssetUrl(address) {
  if (!address) {
    return ''
  }

  const rawAddress = String(address).trim()
  if (!rawAddress) {
    return ''
  }

  if (ABSOLUTE_URL_RE.test(rawAddress)) {
    try {
      const url = new URL(rawAddress)
      if (url.pathname.startsWith('/images/')) {
        return buildCurrentOriginUrl(url.pathname, url.search, url.hash)
      }
      return rawAddress
    } catch (error) {
      return rawAddress
    }
  }

  const normalizedPath = rawAddress.replace(/^\/+/, '')
  return buildCurrentOriginUrl(`/${normalizedPath}`)
}

export function getAssetFileName(address) {
  const url = getAssetUrl(address)
  const pathname = ABSOLUTE_URL_RE.test(url) ? new URL(url).pathname : url
  return decodeURIComponent(pathname.split('/').pop() || '')
}

function getResponseContentType(response) {
  return response && response.headers && typeof response.headers.get === 'function'
    ? String(response.headers.get('content-type') || '').toLowerCase()
    : ''
}

function triggerBlobDownload(blob, fileName, documentRef, urlApi) {
  const objectUrl = urlApi.createObjectURL(blob)
  const link = documentRef.createElement('a')
  link.href = objectUrl
  link.download = fileName
  link.style.display = 'none'
  documentRef.body.appendChild(link)
  link.click()
  documentRef.body.removeChild(link)
  urlApi.revokeObjectURL(objectUrl)
}

/**
 * 先请求同源资源并校验响应，避免裸 <a> 下载在 404 或 SPA 回退时仍显示成功。
 * runtime 仅用于单元测试注入 fetch/document/URL。
 */
export async function downloadAssetFile(address, suggestedFileName, runtime = {}) {
  const assetUrl = getAssetUrl(address)
  if (!assetUrl) {
    throw new Error('结果文件地址为空')
  }

  const fetcher = runtime.fetch || (typeof window !== 'undefined' && window.fetch
    ? window.fetch.bind(window)
    : null)
  if (!fetcher) {
    throw new Error('当前浏览器缺少文件下载能力')
  }

  const response = await fetcher(assetUrl, { credentials: 'same-origin' })
  if (!response || !response.ok) {
    const status = response && response.status ? `HTTP ${response.status}` : '无响应'
    throw new Error(`结果文件请求失败（${status}）`)
  }

  const contentType = getResponseContentType(response)
  if (contentType.includes('text/html') || contentType.includes('application/json')) {
    throw new Error('下载地址返回的不是 Excel 文件，请检查 /images/ 代理')
  }

  const blob = await response.blob()
  if (!blob || blob.size === 0) {
    throw new Error('结果文件内容为空')
  }

  const documentRef = runtime.document || (typeof document !== 'undefined' ? document : null)
  const urlApi = runtime.URL || (typeof URL !== 'undefined' ? URL : null)
  if (!documentRef || !documentRef.body || !urlApi || typeof urlApi.createObjectURL !== 'function') {
    throw new Error('当前浏览器不支持 Blob 文件下载')
  }

  const fileName = suggestedFileName || getAssetFileName(address) || '装箱结果.xlsx'
  triggerBlobDownload(blob, fileName, documentRef, urlApi)
  return { url: assetUrl, fileName, size: blob.size }
}
