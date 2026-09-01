import request from '@/utils/request'
import qs from 'qs'

export function box_delete(data) {
    return request({
      url: '/specification/truck/delete',
      method: 'delete',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      data: qs.stringify(data)
    })
}

export function get_box() {
    return request({
      url: '/specification/truck/queryAll',
      method: 'get'
    })
}

export function update_box(data) {
    return request({
      url: '/specification/truck/update',
      method: 'post',
      data: data
    })
}

export function add_box(data) {
    return request({
      url: '/specification/truck/add',
      method: 'put',
      data: data
    })
}