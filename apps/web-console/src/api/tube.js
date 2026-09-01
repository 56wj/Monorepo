import request from '@/utils/request'
import qs from 'qs'

export function tube_delete(data) {
    return request({
      url: '/specification/tube/delete',
      method: 'delete',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      data: qs.stringify(data)
    })
}

export function get_tube() {
    return request({
      url: '/specification/tube/queryAll',
      method: 'get'
    })
}

export function update_tube(data) {
    return request({
      url: '/specification/tube/update',
      method: 'post',
      data: data
    })
}

export function add_tube(data) {
    return request({
      url: '/specification/tube/add',
      method: 'put',
      data: data
    })
}