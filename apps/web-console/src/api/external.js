import request from '@/utils/request'

export function get_task(data) {
    return request({
      url: '/externalApi/stock/get_push_task',
      method: 'get',
      params: data
    })
}