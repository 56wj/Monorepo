import request from '@/utils/request'
import qs from 'qs'

export function login(data) {
  console.log(data)
  return request({
    url: '/user/login',
    method: 'post',
    headers:{'Content-Type':'application/x-www-form-urlencoded'},
    data: qs.stringify(data)
  })

}

export function getInfo(token) {
  return request({
    url: '/user/userInfo',
    method: 'get',
    params: { token }
  })

  // var p = new Promise((resolve, reject) => {
  //   resolve({data: {
  //     roles: ['admin'],
  //     introduction: 'I am a super administrator',
  //     avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
  //     name: 'Super Admin'
  //   }})
  // });

  // return p
}

export function logout() {
  // return request({
  //   url: '/vue-admin-template/user/logout',
  //   method: 'post'
  // })
  var p = new Promise((resolve, reject) => {
    resolve({data: {
      code: 20000,
      data: 'success'
    }})
  });
  return p
}

export function post_file(formData) {
  return request({
    url: '/palletpacking/upload',
    method: 'post',
    data: formData
  })
}

export function post_al(tableData) {
  return request({
    url: '/palletpacking/computer',
    method: 'post',
    data: tableData
  })
}

export function get_history(data) {
  return request({
    url: '/palletpacking/list',
    method: 'get',
    params: data
  })
}

export function get_result(data) {
  return request({
    url: '/palletpacking/detail',
    method: 'get',
    params: data
  })

}

export function to_delete(data) {
    return request({
      url: '/palletpacking/delete',
      method: 'get',
      params: data
    })
}

export function update_password(data) {
  return request({
    url: '/user/updatePassword',
    method: 'put',
    params: data
  })
}

export function update_userinfo(data) {
  return request({
    url: '/user/updateUserInfo',
    method: 'post',
    data: data
  })
}

