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

export function get_palletroll(data) {
    return request({
      url: '/specification/palletroll/queryByRollId',
      method: 'get',
      params: data
    })
}

export function update_palletroll(data) {
    return request({
      url: '/specification/palletroll/update',
      method: 'post',
      data: data
    })
}

export function create_palletroll(data) {
  return request({
    url: '/specification/palletroll/create',
    method: 'put',
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