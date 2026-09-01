import request from '@/utils/request'
import qs from 'qs'

export function to_delete(data) {
    return request({
      url: '/specification/pallet/delete',
      method: 'delete',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      data: qs.stringify(data)
    })
}

export function get_config() {
    return request({
      url: '/specification/pallet/queryAll',
      method: 'get'
    })
}

export function update_config(data) {
    return request({
      url: '/specification/pallet/update',
      method: 'post',
      data: data
    })
}

export function add_config(data) {
    return request({
      url: '/specification/pallet/add',
      method: 'put',
      data: data
    })
}