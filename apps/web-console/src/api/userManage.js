import request from '@/utils/request'
import qs from 'qs'

export function get_user(data) {
  return request({
    url: '/user/userList',
    method: 'get',
    params: data
  })
}

export function update_password(data) {
    return request({
      url: '/user/adminUpdatePassword',
      method: 'put',
      params: data
    })
  }

export function delete_user(data) {
    return request({
      url: '/user/deleteUsers',
      method: 'delete',
      data: data
    })
  }

export function add_user(data) {
    return request({
      url: '/user/addUser',
      method: 'post',
      data: data
    })
  }

export function update_user(data) {
    return request({
      url: '/user/adminUpdateUserInfo', 
      method: 'put',
      data: data
    })
  }