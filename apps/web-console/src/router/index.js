import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '凯利装箱', icon: 'dashboard' }
    }]
  },

  // {
  //   path: '/example',
  //   component: Layout,
  //   redirect: '/example/table',
  //   name: 'Example',
  //   meta: { title: 'Example', icon: 'el-icon-s-help' },
  //   children: [
  //     {
  //       path: 'table',
  //       name: 'Table',
  //       component: () => import('@/views/table/index'),
  //       meta: { title: 'Table', icon: 'table' }
  //     },
  //     {
  //       path: 'tree',
  //       name: 'Tree',
  //       component: () => import('@/views/tree/index'),
  //       meta: { title: 'Tree', icon: 'tree' }
  //     }
  //   ]
  // },

  {
    path: '/type1',
    component: Layout,
    redirect: '/type1/get_data',
    name: 'type1',
    meta: { title: '托盘装箱', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'get_data',
        name: 'get_data',
        component: () => import('@/views/type1/get_data/index'),
        meta: { title: '导入货物数据', icon: '工装入库' }
      },
      // {
      //   path: 'history',
      //   name: 'history',
      //   component: () => import('@/views/type1/history/index'),
      //   meta: { title: '查看历史信息', icon: 'history'}
      // },
      {
        path: 'config',
        name: 'config',
        component: () => import('@/views/type1/config/index'),
        meta: { title: '查看卷膜规格', icon: 'config' }
      },
      {
        path: '3D_result',
        name: '3D_result',
        component: () => import('@/views/type1/3D_result/index'),
        meta: { title: '查看3D效果', icon: '3d' }
      }
    ]
  },

  {
    path: '/type2',
    component: Layout,
    redirect: '/type2/get_data2',
    name: 'type2',
    meta: { title: '悬空装箱', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'get_data2',
        name: 'get_data2',
        component: () => import('@/views/type2/get_data2/index'),
        meta: { title: '导入货物数据', icon: '工装入库' }
      },
      {
        path: '3D_result2',
        name: '3D_result2',
        component: () => import('@/views/type2/3D_result2/index'),
        meta: { title: '悬空3D效果', icon: '3d' }
      }
    ]
  },

  {
    path: '/history',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'history',
        component: () => import('@/views/type1/history/index'),
        meta: { title: '查看历史信息', icon: 'history'}
      }
    ]
  },

  {
    path: '/selfInfo',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Form',
        component: () => import('@/views/selfInfo/index'),
        meta: { title: '个人信息维护', icon: 'form' }
      }
    ]
  },

  // {
  //   path: '/form',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'index',
  //       name: 'Form',
  //       component: () => import('@/views/form/index'),
  //       meta: { title: 'Form', icon: 'form' }
  //     }
  //   ]
  // },


  // {
  //   path: 'external-link',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'https://panjiachen.github.io/vue-element-admin-site/#/',
  //       meta: { title: 'External Link', icon: 'link' }
  //     }
  //   ]
  // },

  // 404 page must be placed at the end !!!
  // { path: '*', redirect: '/404', hidden: true }
]

export const asyncRoutes = [
  // 用户端 start
  // 用户端 end
  // 管理员端 start
  // {
  //   path: '/boxManageTest',
  //   redirect: '/boxManageTest',
  //   component: Layout,
  //   meta: { roles: ['admin'] },
  //   children: [
  //     {
  //       path: '/boxManageTest',
  //       name: 'boxManageTest',
  //       component: () => import('@/views/boxManageTest/index'),
  //       meta: { title: '规格管理（测试）', icon: 'boxManage' }
  //     }
  //   ]
  // },
  // {
  //   path: '/trayManage',
  //   redirect: '/trayManage',
  //   component: Layout,
  //   meta: { roles: ['admin'] },
  //   children: [
  //     {
  //       path: '/trayManage',
  //       name: 'trayManage',
  //       component: () => import('@/views/trayManage/index'),
  //       meta: { title: '托盘管理', icon: 'trayManage' }
  //     }
  //   ]
  // },
  {
    path: '/manage',
    component: Layout,
    redirect: '/manage/userManage',
    name: 'manage',
    meta: { title: '数据管理', icon: 'manage', roles: ['admin'] },
    children: [
      {
        path: '/userManage',
        name: 'userManage',
        component: () => import('@/views/manage/userManage/index'),
        meta: { title: '用户管理', icon: 'userManage' }
      },
      {
        path: '/departmentManage',
        name: 'departmentManage',
        component: () => import('@/views/manage/departmentManage/index'),
        meta: { title: '部门管理', icon: 'departmentManage' }
      },
      {
        path: '/boxManage',
        name: 'boxManage',
        component: () => import('@/views/manage/boxManage/index'),
        meta: { title: '车箱管理', icon: 'boxManage' }
      },
      {
        path: '/configManage',
        name: 'configManage',
        component: () => import('@/views/manage/configManage/index'),
        meta: { title: '规格表管理', icon: 'configManage' }
      },
      {
        path: '/palletManage',
        name: 'palletManage',
        component: () => import('@/views/manage/palletManage/index'),
        meta: { title: '托盘管理', icon: 'trayManage' }
      },
      {
        path: '/tubeManage',
        name: 'tubeManage',
        component: () => import('@/views/manage/tubeManage/index'),
        meta: { title: '纸筒管理', icon: 'tubeManage' }
      }
    ]
  },
  // 管理员端 end
  // 404页一定要放在最后！！！
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}




export default router
