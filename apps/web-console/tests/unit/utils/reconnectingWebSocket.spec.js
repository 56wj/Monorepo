import ReconnectingWebSocket, { buildWebSocketUrl } from '@/utils/reconnectingWebSocket'

describe('reconnectingWebSocket', () => {
  const originalWebSocket = global.WebSocket
  const originalConfiguredUrl = process.env.VUE_APP_WS_URL

  afterEach(() => {
    global.WebSocket = originalWebSocket
    process.env.VUE_APP_WS_URL = originalConfiguredUrl
    jest.useRealTimers()
  })

  it('uses the current page host and encodes the token by default', () => {
    process.env.VUE_APP_WS_URL = ''
    expect(buildWebSocketUrl('/palletpackingWebsocket', 'a+b/c='))
      .toBe('ws://localhost/palletpackingWebsocket?token=a%2Bb%2Fc%3D')
  })

  it('supports an explicitly configured websocket base URL', () => {
    process.env.VUE_APP_WS_URL = 'wss://example.test/gateway/'
    expect(buildWebSocketUrl('palletpackingWebsocket', 'token'))
      .toBe('wss://example.test/gateway/palletpackingWebsocket?token=token')
  })

  it('sends heartbeats and reconnects after an unexpected close', () => {
    jest.useFakeTimers()

    class FakeWebSocket {
      constructor(url) {
        this.url = url
        this.readyState = FakeWebSocket.CONNECTING
        this.sent = []
        FakeWebSocket.instances.push(this)
      }

      send(message) {
        this.sent.push(message)
      }

      close() {
        this.readyState = FakeWebSocket.CLOSED
      }
    }

    FakeWebSocket.CONNECTING = 0
    FakeWebSocket.OPEN = 1
    FakeWebSocket.CLOSED = 3
    FakeWebSocket.instances = []
    global.WebSocket = FakeWebSocket

    const statuses = []
    const reconnects = []
    const client = new ReconnectingWebSocket({
      url: () => 'ws://localhost/palletpackingWebsocket?token=test',
      heartbeatInterval: 100,
      onStatusChange: connected => statuses.push(connected),
      onReconnect: (count, delay) => reconnects.push([count, delay])
    })

    client.connect()
    const firstSocket = FakeWebSocket.instances[0]
    firstSocket.readyState = FakeWebSocket.OPEN
    firstSocket.onopen()
    jest.advanceTimersByTime(100)

    expect(firstSocket.sent).toEqual(['linkCheck'])
    expect(statuses).toEqual([true])

    firstSocket.readyState = FakeWebSocket.CLOSED
    firstSocket.onclose({ code: 1006 })
    expect(reconnects).toEqual([[1, 1000]])

    jest.advanceTimersByTime(1000)
    expect(FakeWebSocket.instances).toHaveLength(2)
    client.close()
  })
})
