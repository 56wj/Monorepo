const TERMINAL = new Set(['SUCCEEDED', 'DEAD_LETTER', 'CANCELLED'])

/** HTTP is authoritative; WebSocket merely wakes this poller early. */
export default class TaskStatusPoller {
  constructor({ fetchJob, onUpdate, onError = () => {}, interval = 5000 }) {
    this.fetchJob = fetchJob
    this.onUpdate = onUpdate
    this.onError = onError
    this.interval = interval
    this.generation = 0
    this.active = false
    this.timer = null
  }

  start(taskId, jobType) {
    this.stop()
    this.taskId = taskId
    this.jobType = jobType
    this.active = true
    this.inFlight = false
    this.refreshRequested = false
    this.failures = 0
    return this.refresh()
  }

  stop() {
    this.active = false
    this.generation++
    clearTimeout(this.timer)
    this.timer = null
  }

  async refresh() {
    if (!this.active) return
    if (this.inFlight) {
      this.refreshRequested = true
      return
    }
    clearTimeout(this.timer)
    this.inFlight = true
    const generation = this.generation
    try {
      const job = await this.fetchJob(this.taskId)
      if (!this.active || generation !== this.generation) return
      if (!job || String(job.taskId) !== String(this.taskId)) throw new Error('Task snapshot mismatch')
      // A second-stage submission may race an older first-stage response.
      const advanced = this.jobType === 'PALLET_FIRST' && job.jobType === 'PALLET_SECOND'
      if (job.jobType !== this.jobType && !advanced) return
      await this.onUpdate(job)
      if (!this.active || generation !== this.generation) return
      this.failures = 0
      if (TERMINAL.has(job.status)) this.stop()
    } catch (error) {
      if (!this.active || generation !== this.generation) return
      this.failures++
      const status = error.response && error.response.status
      if ([401, 403, 404].includes(status)) this.stop()
      this.onError(error)
    } finally {
      if (this.active && generation === this.generation) {
        this.inFlight = false
        const delay = this.refreshRequested ? 0 : Math.min(this.interval * Math.pow(2, Math.min(this.failures, 3)), 30000)
        this.refreshRequested = false
        this.timer = setTimeout(() => this.refresh(), delay)
      }
    }
  }
}
