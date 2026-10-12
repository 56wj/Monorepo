import { getTaskJob } from '@/api/task'
import TaskStatusPoller from '@/utils/taskStatusPoller'

export default {
  created() {
    this._taskPoller = new TaskStatusPoller({
      fetchJob: taskId => getTaskJob(taskId).then(response => response.data),
      onUpdate: job => this.applyTaskSnapshot(job),
      onError: error => {
        const status = error.response && error.response.status
        if ([401, 403, 404].includes(status)) {
          this.loading = false
          this.loading2 = false
          this.$message.error('任务不存在或登录已失效，请重新选择任务')
        } else {
          console.warn('Task status refresh failed; retrying', error)
        }
      }
    })
  },
  mounted() {
    const { taskId, jobType } = this.$route.query
    if (/^[1-9]\d*$/.test(String(taskId)) && this.$options.taskJobTypes.includes(jobType)) {
      this.taskId = Number(taskId)
      this._restoreTaskConfig = true
      this.loading = jobType !== 'PALLET_SECOND'
      this.loading2 = jobType === 'PALLET_SECOND'
      this._taskPoller.start(this.taskId, jobType)
    }
  },
  activated() {
    if (this._resumeTaskPolling) {
      this._resumeTaskPolling = false
      this._taskPoller.start(this._taskPoller.taskId, this._taskPoller.jobType)
    }
  },
  deactivated() {
    // Cached pages must not navigate the visible page when a background task finishes.
    this._resumeTaskPolling = this._taskPoller.active
    this._taskPoller.stop()
  },
  beforeDestroy() {
    this._resumeTaskPolling = false
    this._taskPoller.stop()
  },
  methods: {
    trackTask(taskId, jobType) {
      this.taskId = taskId
      this._restoreTaskConfig = false
      // Persist only the identifier and stage in the URL, never results or credentials.
      this.$router.replace({ query: { ...this.$route.query, taskId: String(taskId), jobType }}).catch(() => {})
      this._taskPoller.start(taskId, jobType)
    },
    refreshTaskStatus() {
      return this._taskPoller.refresh()
    },
    applyTaskSnapshot(job) {
      if (this._restoreTaskConfig && job.config && typeof job.config === 'object') {
        this.form = { ...this.form, ...job.config }
        this._restoreTaskConfig = false
      }
      if (job.status === 'SUCCEEDED') {
        if (!job.output || job.output.result == null) throw new Error('Completed task has no result')
        const result = typeof job.output.result === 'string' ? JSON.parse(job.output.result) : job.output.result
        this.handleTaskCompletion(job, result)
        this.loading = false
        this.loading2 = false
      } else if (job.status === 'DEAD_LETTER' || job.status === 'CANCELLED') {
        this.loading = false
        this.loading2 = false
        this.dialogTableVisible = false
        this.$message.error(job.errorMessage || (job.status === 'CANCELLED' ? '任务已取消' : '计算失败'))
      } else {
        this.loading = job.jobType !== 'PALLET_SECOND'
        this.loading2 = job.jobType === 'PALLET_SECOND'
      }
    }
  }
}
