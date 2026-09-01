import request from '@/utils/request'
import qs from 'qs'

export function department_delete(data) {
    return request({
      url: '/department/delete',
      method: 'delete',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      data: qs.stringify(data)
    })
}

export function get_department() {
    return request({
      url: '/department/queryAll',
      method: 'get'
    })
}

export function update_department(data) {
    return request({
      url: '/department/update',
      method: 'post',
      data: data
    })
}

export function add_department(data) {
    return request({
      url: '/department/add',
      method: 'post',
      data: data
    })
}