import request from '@/utils/request'

export function post_file(formData) {
    return request({
      url: '/palletpacking/upload',
      method: 'post',
      data: formData
    })
  }
  
  export function post_al_first(tableData) {
    return request({
      url: '/palletpacking/computer_first',
      method: 'post',
      data: tableData
    })
  }

  export function post_al_second(data) {
    return request({
      url: '/palletpacking/computer_second',
      method: 'post',
      data: data
    })
  }
  
  export function get_history(data) {
    return request({
      url: '/palletpacking/list',
      method: 'get',
      params: data
    })
  }
  
  export function get_result(data) {
    return request({
      url: '/palletpacking/detail',
      method: 'get',
      params: data
    })
  
  }
  
  export function to_delete(data) {
      return request({
        url: '/palletpacking/delete',
        method: 'delete',
        params: data
      })
  }

  export function batch_delete(data) {
    return request({
      url: '/palletpacking/batch_delete',
      method: 'post',
      data: data
    })
}

  export function get_config() {
    return request({
      url: '/specification/queryAll',
      method: 'get'
    })
}

export function get_latestTask() {
    return request({
      url: '/palletpacking/getLatestTask',
      method: 'get'
    })
}