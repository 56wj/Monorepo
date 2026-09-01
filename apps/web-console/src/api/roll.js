import request from '@/utils/request'
import qs from 'qs'

export function roll_delete(data) {
    return request({
      url: '/specification/roll/delete',
      method: 'delete',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      data: qs.stringify(data)
    })
}

export function get_roll() {
    return request({
      url: '/specification/roll/queryAll',
      method: 'get'
    })
}

export function update_roll(data) {
    return request({
      url: '/specification/roll/update',
      method: 'post',
      data: data
    })
}

export function add_roll(data) {
    return request({
      url: '/specification/roll/add',
      method: 'put',
      data: data
    })
}