import tracking from '@/mixins/taskStatusTracking'
import { getTaskJob } from '@/api/task'

jest.mock('@/api/task', () => ({ getTaskJob: jest.fn() }))
const flush = async() => { for (let i = 0; i < 8; i++) await Promise.resolve() }

describe('taskStatusTracking', () => {
  let vm
  beforeEach(() => {
    jest.useFakeTimers()
    vm = {
      $route: { query: {}},
      $router: { replace: jest.fn().mockResolvedValue() },
      $options: { taskJobTypes: ['PALLET_FIRST', 'PALLET_SECOND'] },
      $message: { error: jest.fn() },
      form: {}, loading: false, loading2: false,
      handleTaskCompletion: jest.fn()
    }
    Object.assign(vm, tracking.methods)
    tracking.created.call(vm)
  })
  afterEach(() => { tracking.beforeDestroy.call(vm); jest.clearAllTimers(); jest.useRealTimers() })

  it('restores an in-progress task after page reload', async() => {
    vm.$route.query = { taskId: '42', jobType: 'PALLET_SECOND' }
    getTaskJob.mockResolvedValue({ data: { taskId: 42, jobType: 'PALLET_SECOND', status: 'RUNNING', config: { orderId: 'order-1' }}})
    tracking.mounted.call(vm); await flush()
    expect(getTaskJob).toHaveBeenCalledWith(42)
    expect(vm.form.orderId).toBe('order-1')
    expect(vm.loading2).toBe(true)
  })

  it('keeps the task stage in the URL and consumes persisted results', async() => {
    getTaskJob.mockResolvedValue({ data: { taskId: 42, jobType: 'PALLET_FIRST', status: 'SUCCEEDED', output: { result: '[]' }}})
    vm.trackTask(42, 'PALLET_FIRST'); await flush()
    expect(vm.$router.replace).toHaveBeenCalledWith({ query: { taskId: '42', jobType: 'PALLET_FIRST' }})
    expect(vm.handleTaskCompletion).toHaveBeenCalledWith(expect.objectContaining({ taskId: 42 }), [])
    expect(vm._taskPoller.active).toBe(false)
  })

  it('clears loading and surfaces terminal failure', () => {
    vm.loading = true; vm.dialogTableVisible = true
    vm.applyTaskSnapshot({ status: 'DEAD_LETTER', errorMessage: 'solver failed' })
    expect(vm.loading).toBe(false)
    expect(vm.dialogTableVisible).toBe(false)
    expect(vm.$message.error).toHaveBeenCalledWith('solver failed')
  })

  it('pauses a cached page and resumes its active task on return', async() => {
    getTaskJob.mockResolvedValue({ data: { taskId: 42, jobType: 'PALLET_FIRST', status: 'RUNNING' }})
    vm.trackTask(42, 'PALLET_FIRST'); await flush()
    tracking.deactivated.call(vm)
    expect(vm._taskPoller.active).toBe(false)
    tracking.activated.call(vm); await flush()
    expect(vm._taskPoller.active).toBe(true)
  })

  it('does not overwrite an edited first-stage result when a cached page returns', () => {
    vm._taskPoller.stop()
    tracking.deactivated.call(vm)
    tracking.activated.call(vm)
    expect(vm._taskPoller.active).toBe(false)
  })

  it('does not apply null or malformed completed results', () => {
    expect(() => vm.applyTaskSnapshot({ status: 'SUCCEEDED', output: null })).toThrow()
    expect(vm.handleTaskCompletion).not.toHaveBeenCalled()
  })
})
