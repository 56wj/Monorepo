import TaskStatusPoller from '@/utils/taskStatusPoller'

const flush = async() => { for (let i = 0; i < 8; i++) await Promise.resolve() }
const snapshot = (status = 'RUNNING', extra = {}) => ({ taskId: 42, jobId: 'job-42', jobType: 'PALLET_FIRST', status, ...extra })

describe('TaskStatusPoller', () => {
  let fetchJob, onUpdate, onError, poller
  beforeEach(() => {
    jest.useFakeTimers()
    fetchJob = jest.fn().mockResolvedValue(snapshot())
    onUpdate = jest.fn()
    onError = jest.fn()
    poller = new TaskStatusPoller({ fetchJob, onUpdate, onError })
  })
  afterEach(() => { poller.stop(); jest.clearAllTimers(); jest.useRealTimers() })

  it('recovers completion through polling with no WebSocket', async() => {
    fetchJob.mockResolvedValueOnce(snapshot()).mockResolvedValueOnce(snapshot('SUCCEEDED'))
    await poller.start(42, 'PALLET_FIRST')
    jest.advanceTimersByTime(5000); await flush()
    expect(onUpdate).toHaveBeenCalledTimes(2)
    expect(poller.active).toBe(false)
    jest.advanceTimersByTime(30000); await flush()
    expect(fetchJob).toHaveBeenCalledTimes(2)
  })

  it.each(['DEAD_LETTER', 'CANCELLED'])('stops after %s', async status => {
    fetchJob.mockResolvedValue(snapshot(status))
    await poller.start(42, 'PALLET_FIRST')
    expect(poller.active).toBe(false)
    expect(onUpdate).toHaveBeenCalledTimes(1)
  })

  it('refreshes immediately on reconnect and coalesces concurrent wakeups', async() => {
    let resolve
    fetchJob.mockImplementationOnce(() => new Promise(r => { resolve = r }))
    poller.start(42, 'PALLET_FIRST')
    poller.refresh(); poller.refresh()
    expect(fetchJob).toHaveBeenCalledTimes(1)
    resolve(snapshot()); await flush()
    jest.advanceTimersByTime(0); await flush()
    expect(fetchJob).toHaveBeenCalledTimes(2)
  })

  it('ignores in-flight responses after component teardown', async() => {
    let resolve
    fetchJob.mockImplementation(() => new Promise(r => { resolve = r }))
    poller.start(42, 'PALLET_FIRST'); poller.stop()
    resolve(snapshot('SUCCEEDED')); await flush()
    expect(onUpdate).not.toHaveBeenCalled()
    expect(poller.timer).toBe(null)
  })

  it('ignores old responses after switching task', async() => {
    let resolve
    fetchJob.mockImplementationOnce(() => new Promise(r => { resolve = r }))
      .mockResolvedValueOnce(snapshot('RUNNING', { taskId: 43 }))
    poller.start(42, 'PALLET_FIRST')
    await poller.start(43, 'PALLET_FIRST')
    resolve(snapshot('SUCCEEDED')); await flush()
    expect(onUpdate).toHaveBeenCalledTimes(1)
    expect(onUpdate.mock.calls[0][0].taskId).toBe(43)
  })

  it('does not reopen first-stage results while waiting for the second stage', async() => {
    fetchJob.mockResolvedValueOnce(snapshot('SUCCEEDED')).mockResolvedValueOnce(snapshot('SUCCEEDED', { jobType: 'PALLET_SECOND' }))
    await poller.start(42, 'PALLET_SECOND')
    expect(onUpdate).not.toHaveBeenCalled()
    expect(poller.active).toBe(true)
    jest.advanceTimersByTime(5000); await flush()
    expect(onUpdate).toHaveBeenCalledTimes(1)
    expect(poller.active).toBe(false)
  })

  it('accepts advancement to the latest second stage when reopening a task', async() => {
    fetchJob.mockResolvedValue(snapshot('RUNNING', { jobType: 'PALLET_SECOND' }))
    await poller.start(42, 'PALLET_FIRST')
    expect(onUpdate).toHaveBeenCalledTimes(1)
  })

  it('backs off and recovers from a network outage', async() => {
    fetchJob.mockRejectedValueOnce(new Error('offline')).mockResolvedValueOnce(snapshot('SUCCEEDED'))
    await poller.start(42, 'PALLET_FIRST')
    expect(onError).toHaveBeenCalledTimes(1)
    jest.advanceTimersByTime(9999); await flush()
    expect(fetchJob).toHaveBeenCalledTimes(1)
    jest.advanceTimersByTime(1); await flush()
    expect(poller.active).toBe(false)
  })

  it.each([401, 403, 404])('stops retrying HTTP %s', async status => {
    fetchJob.mockRejectedValue({ response: { status }})
    await poller.start(42, 'PALLET_FIRST')
    jest.advanceTimersByTime(60000); await flush()
    expect(fetchJob).toHaveBeenCalledTimes(1)
    expect(poller.active).toBe(false)
  })

  it('retries result-processing errors instead of losing a completion', async() => {
    fetchJob.mockResolvedValue(snapshot('SUCCEEDED'))
    onUpdate.mockImplementationOnce(() => { throw new Error('invalid output') })
    await poller.start(42, 'PALLET_FIRST')
    expect(poller.active).toBe(true)
    jest.advanceTimersByTime(10000); await flush()
    expect(poller.active).toBe(false)
  })
})
