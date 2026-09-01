import request from '@/utils/request'
import qs from 'qs'

export function delete_pallet(data) {
    return request({
      url: '/specification/pallet/delete',
      method: 'delete',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      data: qs.stringify(data)
    })
}

export function get_pallet() {
    return request({
      url: '/specification/pallet/queryAll',
      method: 'get'
    })
}

export function update_pallet(data) {
    return request({
      url: '/specification/pallet/update',
      method: 'post',
      data: data
    })
}

export function add_pallet(data) {
    return request({
      url: '/specification/pallet/add',
      method: 'put',
      data: data
    })
}