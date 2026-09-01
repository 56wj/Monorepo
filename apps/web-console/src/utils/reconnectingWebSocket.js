const DEFAULT_HEARTBEAT_INTERVAL = 30000
const DEFAULT_CONNECT_TIMEOUT = 10000
const DEFAULT_MAX_RETRY_DELAY = 30000

function trimSlashes(value) {
  return value.replace(/^\/+|\/+$/g, '')
}

/**
 * 默认使用当前页面的 host，避免把服务器上的 localhost 或旧 IP 烘焙进浏览器代码。
 * 如确实需要跨域 WebSocket，仍可通过 VUE_APP_WS_URL 显式覆盖。
 */
export function buildWebSocketUrl(path, token) {
  const configuredBase = (process.env.VUE_APP_WS_URL || '').trim()
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const base = configuredBase || `${protocol}//${window.location.host}`
  const separator = base.indexOf('?') === -1 ? '?' : '&'

  return `${base.replace(/\/+$/, '')}/${trimSlashes(path)}${separator}token=${encodeURIComponent(token || '')}`
}

/**
 * 带连接超时、心跳和指数退避重连的轻量 WebSocket 客户端。
 */
export default class ReconnectingWebSocket {
  constructor(options) {
    this.options = options
    this.socket = null
    this.reconnectTimer = null
    this.heartbeatTimer = null
    this.connectTimer = null
    this.retryCount = 0
    this.stopped = true
  }

  connect() {
    this.stopped = false
    this.clearReconnectTimer()

    if (this.socket && (
      this.socket.readyState === WebSocket.OPEN ||
      this.socket.readyState === WebSocket.CONNECTING
    )) {
      return
    }

    let socket
    try {
      socket = new WebSocket(this.options.url())
    } catch (error) {
      this.notifyStatus(false, error)
      this.scheduleReconnect()
      return
    }

    this.socket = socket
    this.connectTimer = setTimeout(() => {
      if (socket.readyState === WebSocket.CONNECTING) {
        socket.close()
      }
    }, this.options.connectTimeout || DEFAULT_CONNECT_TIMEOUT)

    socket.onopen = () => {
      if (socket !== this.socket) return
      this.clearConnectTimer()
      this.retryCount = 0
      this.startHeartbeat()
      this.notifyStatus(true)
      if (this.options.onOpen) this.options.onOpen(socket)
    }

    socket.onmessage = event => {
      if (socket === this.socket && this.options.onMessage) {
        this.options.onMessage(event)
      }
    }

    socket.onerror = error => {
      if (socket !== this.socket) return
      this.notifyStatus(false, error)
      // 浏览器的 error 事件没有可用错误码；主动关闭后统一走 onclose 重连。
      if (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING) {
        socket.close()
      }
    }

    socket.onclose = event => {
      if (socket !== this.socket) return
      this.clearConnectTimer()
      this.stopHeartbeat()
      this.socket = null
      this.notifyStatus(false, event)
      if (this.options.onClose) this.options.onClose(event)
      if (!this.stopped) this.scheduleReconnect()
    }
  }

  close() {
    this.stopped = true
    this.clearReconnectTimer()
    this.clearConnectTimer()
    this.stopHeartbeat()
    const socket = this.socket
    this.socket = null
    if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) {
      socket.close(1000, 'component destroyed')
    }
  }

  scheduleReconnect() {
    if (this.stopped || this.reconnectTimer) return
    this.retryCount += 1
    const delay = Math.min(1000 * Math.pow(2, this.retryCount - 1), this.options.maxRetryDelay || DEFAULT_MAX_RETRY_DELAY)

    if (this.options.onReconnect) this.options.onReconnect(this.retryCount, delay)
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null
      this.connect()
    }, delay)
  }

  startHeartbeat() {
    this.stopHeartbeat()
    const interval = this.options.heartbeatInterval || DEFAULT_HEARTBEAT_INTERVAL
    this.heartbeatTimer = setInterval(() => {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send('linkCheck')
      }
    }, interval)
  }

  stopHeartbeat() {
    if (this.heartbeatTimer) clearInterval(this.heartbeatTimer)
    this.heartbeatTimer = null
  }

  clearReconnectTimer() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer)
    this.reconnectTimer = null
  }

  clearConnectTimer() {
    if (this.connectTimer) clearTimeout(this.connectTimer)
    this.connectTimer = null
  }

  notifyStatus(connected, detail) {
    if (this.options.onStatusChange) {
      this.options.onStatusChange(connected, detail)
    }
  }
}
