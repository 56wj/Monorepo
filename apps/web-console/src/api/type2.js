import request from '@/utils/request'

export function post_al_first(data) {
    return request({
      url: '/suspend/computer_first',
      method: 'post',
      data: data
    })
}