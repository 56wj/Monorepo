import request from '@/utils/request'

export function get_history(data) {
    return request({
      url: '/task/list',
      method: 'get',
      params: data
    })
}

export function to_delete(data) {
    return request({
      url: '/task/delete',
      method: 'delete',
      params: data
    })
}

export function batch_delete(data) {
  return request({
    url: '/task/batch_delete',
    method: 'post',
    data: data
  })
}

export function get_result(data) {
    return request({
      url: '/task/detail',
      method: 'get',
      params: data
    })
  
}

export function get_latestTask() {
    return request({
      url: '/palletpacking/getLatestTask',
      method: 'get'
    })
}

export function get_latestTask2() {
  return request({
    url: '/suspend/getLatestTask',
    method: 'get'
  })
}