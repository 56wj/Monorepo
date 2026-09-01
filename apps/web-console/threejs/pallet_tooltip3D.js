import * as THREE from 'three';
//导入轨道控制器
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
// 导入CSS3
import { CSS3DRenderer, CSS3DObject } from 'three/addons/renderers/CSS3DRenderer.js'
//导入lil-GUI
import { GUI } from 'three/addons/libs/lil-gui.module.min.js'
// mockData
// import { mockData } from './mockData';
const mockData = {
    singleContainerLoadingSolutions: [
      {
        container: {
          containerId: 'container',
          cube: {
            height: 2698,
            length: 12032,
            volume: 76351414272,
            width: 2352,
          },
          price: 3400.0,
          volume: 76351414272,
          weight: 30400.0,
        },
        placedItems: [
          {
            itemId: 'EBD0100000074785',
            orientation: 'FRONT_DOWN',
            position: { x: 0, y: 0, z: 0 },
            rotatedCube: {
              height: 1140,
              length: 1270,
              volume: 1867662000,
              width: 1290,
            },
          },
          {
            itemId: 'EBD0100000089800',
            orientation: 'FRONT_UP',
            position: { x: 1270, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089800',
            orientation: 'FRONT_UP',
            position: { x: 2470, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089800',
            orientation: 'FRONT_UP',
            position: { x: 3670, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089800',
            orientation: 'FRONT_UP',
            position: { x: 4870, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089800',
            orientation: 'FRONT_UP',
            position: { x: 0, y: 0, z: 1140 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089800',
            orientation: 'FRONT_UP',
            position: { x: 6070, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089801',
            orientation: 'FRONT_UP',
            position: { x: 7270, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089801',
            orientation: 'FRONT_UP',
            position: { x: 1200, y: 0, z: 1160 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089801',
            orientation: 'FRONT_UP',
            position: { x: 8470, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089801',
            orientation: 'FRONT_UP',
            position: { x: 2400, y: 0, z: 1160 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089801',
            orientation: 'FRONT_UP',
            position: { x: 9670, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089801',
            orientation: 'BOTTOM_UP',
            position: { x: 10870, y: 0, z: 0 },
            rotatedCube: {
              height: 1200,
              length: 1160,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000083166',
            orientation: 'FRONT_UP',
            position: { x: 0, y: 1290, z: 0 },
            rotatedCube: {
              height: 500,
              length: 3480,
              volume: 1513800000,
              width: 870,
            },
          },
          {
            itemId: 'EBD0100000083166',
            orientation: 'FRONT_UP',
            position: { x: 0, y: 1290, z: 500 },
            rotatedCube: {
              height: 500,
              length: 3480,
              volume: 1513800000,
              width: 870,
            },
          },
          {
            itemId: 'EBD010220600022',
            orientation: 'FRONT_UP',
            position: { x: 3480, y: 1200, z: 0 },
            rotatedCube: {
              height: 550,
              length: 1980,
              volume: 1056330000,
              width: 970,
            },
          },
          {
            itemId: 'EBD0100000072512',
            orientation: 'FRONT_UP',
            position: { x: 0, y: 1290, z: 1000 },
            rotatedCube: {
              height: 750,
              length: 1380,
              volume: 1055700000,
              width: 1020,
            },
          },
          {
            itemId: 'EBD0100000072513',
            orientation: 'FRONT_UP',
            position: { x: 5460, y: 1200, z: 0 },
            rotatedCube: {
              height: 750,
              length: 1380,
              volume: 1055700000,
              width: 1020,
            },
          },
          {
            itemId: 'EBD010220600023',
            orientation: 'FRONT_UP',
            position: { x: 3480, y: 1200, z: 550 },
            rotatedCube: {
              height: 750,
              length: 1380,
              volume: 1055700000,
              width: 1020,
            },
          },
          {
            itemId: 'EBD0100000083503',
            orientation: 'SIDE_UP',
            position: { x: 1380, y: 1200, z: 1000 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1009800000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000083503',
            orientation: 'SIDE_UP',
            position: { x: 6840, y: 1200, z: 0 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1009800000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000072510',
            orientation: 'SIDE_UP',
            position: { x: 2400, y: 1200, z: 1000 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'SIDE_UP',
            position: { x: 7860, y: 1200, z: 0 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'SIDE_UP',
            position: { x: 8880, y: 1200, z: 0 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'SIDE_UP',
            position: { x: 4860, y: 1200, z: 750 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'SIDE_UP',
            position: { x: 0, y: 1200, z: 1750 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'SIDE_UP',
            position: { x: 9900, y: 1200, z: 0 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'FRONT_UP',
            position: { x: 10920, y: 1200, z: 0 },
            rotatedCube: {
              height: 900,
              length: 1090,
              volume: 1000620000,
              width: 1020,
            },
          },
          {
            itemId: 'EBD010220600025',
            orientation: 'SIDE_UP',
            position: { x: 3600, y: 0, z: 1160 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'SIDE_UP',
            position: { x: 3420, y: 1200, z: 1300 },
            rotatedCube: {
              height: 900,
              length: 1010,
              volume: 999900000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'BOTTOM_UP',
            position: { x: 5880, y: 1200, z: 750 },
            rotatedCube: {
              height: 1010,
              length: 900,
              volume: 999900000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'SIDE_UP',
            position: { x: 4620, y: 0, z: 1160 },
            rotatedCube: {
              height: 900,
              length: 1010,
              volume: 999900000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'SIDE_UP',
            position: { x: 6780, y: 1200, z: 900 },
            rotatedCube: {
              height: 900,
              length: 1010,
              volume: 999900000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'SIDE_UP',
            position: { x: 5630, y: 0, z: 1160 },
            rotatedCube: {
              height: 900,
              length: 1010,
              volume: 999900000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'FRONT_UP',
            position: { x: 7790, y: 1200, z: 900 },
            rotatedCube: {
              height: 850,
              length: 1080,
              volume: 991440000,
              width: 1080,
            },
          },
          {
            itemId: 'EBD010220600021',
            orientation: 'FRONT_UP',
            position: { x: 1020, y: 1200, z: 1900 },
            rotatedCube: {
              height: 550,
              length: 1980,
              volume: 838530000,
              width: 770,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'FRONT_UP',
            position: { x: 6640, y: 0, z: 1160 },
            rotatedCube: {
              height: 550,
              length: 1980,
              volume: 838530000,
              width: 770,
            },
          },
          {
            itemId: 'EBD0100000084194',
            orientation: 'FRONT_UP',
            position: { x: 6640, y: 770, z: 1160 },
            rotatedCube: {
              height: 550,
              length: 3430,
              volume: 792330000,
              width: 420,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'SIDE_UP',
            position: { x: 4430, y: 1100, z: 1650 },
            rotatedCube: {
              height: 660,
              length: 800,
              volume: 580800000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'FRONT_UP',
            position: { x: 8870, y: 1200, z: 900 },
            rotatedCube: {
              height: 600,
              length: 1200,
              volume: 576000000,
              width: 800,
            },
          },
          {
            itemId: 'EBD0100000072510',
            orientation: 'BOTTOM_UP',
            position: { x: 5230, y: 1100, z: 1760 },
            rotatedCube: {
              height: 770,
              length: 850,
              volume: 575960000,
              width: 880,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'BOTTOM_UP',
            position: { x: 10070, y: 1200, z: 900 },
            rotatedCube: {
              height: 770,
              length: 850,
              volume: 575960000,
              width: 880,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'FRONT_UP',
            position: { x: 8620, y: 0, z: 1160 },
            rotatedCube: {
              height: 850,
              length: 880,
              volume: 575960000,
              width: 770,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'BOTTOM_UP',
            position: { x: 3600, y: 0, z: 2060 },
            rotatedCube: {
              height: 600,
              length: 660,
              volume: 475200000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_UP',
            position: { x: 9500, y: 0, z: 1200 },
            rotatedCube: {
              height: 500,
              length: 1480,
              volume: 458800000,
              width: 620,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_UP',
            position: { x: 4260, y: 0, z: 2060 },
            rotatedCube: {
              height: 500,
              length: 1480,
              volume: 458800000,
              width: 620,
            },
          },
          {
            itemId: 'EBD0100000093099',
            orientation: 'FRONT_UP',
            position: { x: 10920, y: 1200, z: 900 },
            rotatedCube: {
              height: 530,
              length: 1060,
              volume: 410114000,
              width: 730,
            },
          },
          {
            itemId: 'EBD0100000095770',
            orientation: 'FRONT_DOWN',
            position: { x: 6080, y: 1100, z: 1760 },
            rotatedCube: {
              height: 590,
              length: 590,
              volume: 313290000,
              width: 900,
            },
          },
          {
            itemId: 'EBD0100000095770',
            orientation: 'FRONT_DOWN',
            position: { x: 6640, y: 0, z: 1710 },
            rotatedCube: {
              height: 590,
              length: 590,
              volume: 313290000,
              width: 900,
            },
          },
          {
            itemId: 'EBD0100000095770',
            orientation: 'BOTTOM_UP',
            position: { x: 10980, y: 0, z: 1200 },
            rotatedCube: {
              height: 590,
              length: 900,
              volume: 313290000,
              width: 590,
            },
          },
          {
            itemId: 'EBD0100000095770',
            orientation: 'FRONT_DOWN',
            position: { x: 7230, y: 0, z: 1710 },
            rotatedCube: {
              height: 590,
              length: 590,
              volume: 313290000,
              width: 900,
            },
          },
          {
            itemId: 'EBD0100000093099',
            orientation: 'FRONT_UP',
            position: { x: 6670, y: 900, z: 1800 },
            rotatedCube: {
              height: 550,
              length: 680,
              volume: 269280000,
              width: 720,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_DOWN',
            position: { x: 3000, y: 1200, z: 2200 },
            rotatedCube: {
              height: 420,
              length: 1280,
              volume: 268800000,
              width: 500,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_DOWN',
            position: { x: 3000, y: 1700, z: 2200 },
            rotatedCube: {
              height: 420,
              length: 1280,
              volume: 268800000,
              width: 500,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'FRONT_UP',
            position: { x: 0, y: 0, z: 2300 },
            rotatedCube: {
              height: 310,
              length: 930,
              volume: 268119000,
              width: 930,
            },
          },
          {
            itemId: 'EBD0100000086191',
            orientation: 'FRONT_UP',
            position: { x: 10920, y: 1930, z: 900 },
            rotatedCube: {
              height: 550,
              length: 880,
              volume: 203280000,
              width: 420,
            },
          },
          {
            itemId: 'EBD0100000086191',
            orientation: 'FRONT_UP',
            position: { x: 4260, y: 620, z: 2060 },
            rotatedCube: {
              height: 550,
              length: 880,
              volume: 203280000,
              width: 420,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'FRONT_UP',
            position: { x: 10070, y: 620, z: 1160 },
            rotatedCube: {
              height: 520,
              length: 650,
              volume: 192660000,
              width: 570,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'FRONT_DOWN',
            position: { x: 10980, y: 590, z: 1200 },
            rotatedCube: {
              height: 400,
              length: 790,
              volume: 186440000,
              width: 590,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'SIDE_UP',
            position: { x: 930, y: 0, z: 2320 },
            rotatedCube: {
              height: 320,
              length: 660,
              volume: 185856000,
              width: 880,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'SIDE_UP',
            position: { x: 6670, y: 1620, z: 1800 },
            rotatedCube: {
              height: 530,
              length: 550,
              volume: 174900000,
              width: 600,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'FRONT_DOWN',
            position: { x: 1020, y: 1970, z: 1900 },
            rotatedCube: {
              height: 600,
              length: 800,
              volume: 168000000,
              width: 350,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'BOTTOM_UP',
            position: { x: 4430, y: 1100, z: 1300 },
            rotatedCube: {
              height: 270,
              length: 380,
              volume: 121068000,
              width: 1180,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_DOWN',
            position: { x: 1820, y: 1970, z: 1900 },
            rotatedCube: {
              height: 270,
              length: 1180,
              volume: 121068000,
              width: 380,
            },
          },
          {
            itemId: 'EBD0100000083166',
            orientation: 'BOTTOM_UP',
            position: { x: 3000, y: 1200, z: 1900 },
            rotatedCube: {
              height: 270,
              length: 380,
              volume: 112860000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000091595',
            orientation: 'SIDE_UP',
            position: { x: 1590, y: 0, z: 2320 },
            rotatedCube: {
              height: 210,
              length: 580,
              volume: 87696000,
              width: 720,
            },
          },
          {
            itemId: 'EBD0100000083166',
            orientation: 'FRONT_UP',
            position: { x: 0, y: 930, z: 2300 },
            rotatedCube: {
              height: 380,
              length: 680,
              volume: 69768000,
              width: 270,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_DOWN',
            position: { x: 1820, y: 1970, z: 2170 },
            rotatedCube: {
              height: 270,
              length: 680,
              volume: 69768000,
              width: 380,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_DOWN',
            position: { x: 1590, y: 720, z: 2320 },
            rotatedCube: {
              height: 270,
              length: 680,
              volume: 69768000,
              width: 380,
            },
          },
        ],
        totalVolume: 56630547000,
        totalWeight: 69.0,
      },
    ],
};

let cartonWidth;
let cartonHeight;
let cartonLength;
let detailIndex = 0;
// let angle = 0;
let intersections;
let intersected;
const defaults = {
    result: [],
    detailList: [],
    dataList: [],
    detailNum: 0,
    cartonNum: 0,
    taskNum: 0,
    cartonList: [],
};
let HEIGHT;
let WIDTH;
let boxArr = [];

// 创建场景
const scene = new THREE.Scene();
// 场景颜色
scene.background = new THREE.Color(0x999999);

// 创建相机 参数：（视角， 宽高比，近平面，远平面）
const camera = new THREE.PerspectiveCamera(
    45,
    window.innerWidth / window.innerHeight,
    1,
    99999
);
// 调整相机位置
camera.position.set(12000, 0, 0);
camera.up.x = 0;
camera.up.y = 1;
camera.up.z = 0;
camera.lookAt({
    x: 0,
    y: 0,
    z: 200,
});
scene.add(camera);

// 初始化网格
const grid = new THREE.GridHelper(15000, 20, 0x333333, 0x333333);

// 初始化渲染器并设置场景大小
const renderer = new THREE.WebGLRenderer({
    antialias: true, // 开启锯齿
    alpha: true, // 透明度
});
renderer.setSize( window.innerWidth, window.innerHeight );
//添加到相应元素中
document.body.appendChild( renderer.domElement );

// 初始化CSS3D渲染器
const labelRenderer = new CSS3DRenderer();
labelRenderer.setSize(window.innerWidth, window.innerHeight);
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0px';
document.body.appendChild(labelRenderer.domElement);
labelRenderer.domElement.addEventListener("click", onMouseClick);
//
let css3DObject;

// 初始化轨道控制器
const controls = new OrbitControls(camera, labelRenderer.domElement);
// 控制器阻尼
controls.enableDamping = true;
// 动态阻尼系数
controls.dampingFactor = 0.1;
// 旋转中心点
controls.target.set(0, 0, 0);

// 三维坐标轴
const axesHelper = new THREE.AxesHelper(5000);
scene.add( axesHelper );

// 选中子级盒子
const mouse = new THREE.Vector3();
// 射线
const raycaster = new THREE.Raycaster();
// window.addEventListener("click", (event) => {
// 	// 设置鼠标向量的xy值（归一化，使xy坐标的范围在-1到1之间）
// 	mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
// 	mouse.y = -((event.clientY / window.innerHeight) * 2 - 1);
// 	// 通过摄像机和鼠标位置更新射线
// 	raycaster.setFromCamera(mouse, camera);
// 	// 计算物体和射线的焦点
// 	intersections = raycaster.intersectObjects(boxArr);
// 	// 
// 	if(intersections.length > 0) {
//         intersected = intersections[0].object;
//         console.log(intersected);
//         css3DObject.visible = true;
//         css3DObject.position.x = intersected.position.x - 50 + 18;
//         css3DObject.position.y = intersected.position.y + 50 + 38;
//         css3DObject.position.z = intersected.position.z;
//         modifyDocument("lableItemId", "red", intersected.itemId);
// 	}else{
//         css3DObject.visible = false;
//     }
// });
function onMouseClick(event) {
	// 设置鼠标向量的xy值（归一化，使xy坐标的范围在-1到1之间）
	mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
	mouse.y = -((event.clientY / window.innerHeight) * 2 - 1);
	// 通过摄像机和鼠标位置更新射线
	raycaster.setFromCamera(mouse, camera);
	// 计算物体和射线的焦点
	intersections = raycaster.intersectObjects(boxArr);
	// 
	if(intersections.length > 0) {
        intersected = intersections[0].object;
        console.log(intersected);
        css3DObject.visible = true;
        css3DObject.position.x = intersected.position.x - 50 + 18;
        css3DObject.position.y = intersected.position.y + 50 + 38;
        css3DObject.position.z = intersected.position.z;
        console.log(css3DObject);
        modifyDocument("lableItemId", "red", intersected.itemId);
	}else{
        css3DObject.visible = false;
    }
};

// 悬浮信息框
function addCSS3DLabelToScene() {
    var element = document.getElementById("WebGL-output");

    //把生成的CSSDOM对象处理成three的节点对象
    css3DObject = new CSS3DObject(element);
    //设置CSS3DObject对象
    css3DObject.position.x = 0;
    css3DObject.position.y = 0;
    css3DObject.position.z = 0;
    //在第二个场景中添加这个对象
    scene.add(css3DObject);
    // 默认不显示
    css3DObject.visible = false;
}
addCSS3DLabelToScene();
function modifyDocument(id, color, value) {
    var dom = document.getElementById(id);
    dom.style.color = color;
    dom.textContent = value;
}

// 获取详细数据(获取货物数据)
function getInfoDetail() {
    const res = { status: 200, data: [], success: true };
    console.log(mockData.singleContainerLoadingSolutions);
    res.data = mockData.singleContainerLoadingSolutions;
    defaults.result = res;
    defaults.detailList = [];

    // 初始装货箱信息
    const { width, length, height } = res.data[0].container.cube;
    initBox(width, height, length, res.data[0].container);

    // 单个详情
    const placedItemsArr = res.data[0].placedItems;
    detailIndex = defaults.detailNum = placedItemsArr.length;

    // 渲染单个子级盒子
    boxArr = [];
    for (let i = 0; i < defaults.detailNum; i++) {
        const detail = placedItemsArr[i];
        defaults.detailList.push(
            initObject(
                detail.rotatedCube.width,
                detail.rotatedCube.height,
                detail.rotatedCube.length,
                detail.position.x,
                detail.position.y,
                detail.position.z,
                // i
                detail.itemId
            )
        );
    }
};
// 初始化纸箱(车箱)
function initBox(xLen, yLen, zLen, context) {
    // setContainerContext(context);
    cartonWidth = xLen;
    cartonHeight = yLen;
    cartonLength = zLen;
    // 声明几何体
    const geometry = new THREE.BoxGeometry(xLen, yLen, zLen);
    // 声明材质;
    const edges = new THREE.EdgesGeometry(geometry);
    // 几何体+ 材质 = 物体
    const containerBox = new THREE.LineSegments(edges);
    containerBox.material.color = new THREE.Color(0x000000);
    containerBox.position.set(0, 0, 0);
    // 将物体添加到场景中
    scene.add(containerBox);
    // 添加网格
    grid.position.y = -(cartonHeight / 2) - cartonHeight / 8;
    scene.add(grid);

    css3DObject.visible = true;
    css3DObject.position.x = 0;
    css3DObject.position.y = 0;
    css3DObject.position.z = 0;


    return containerBox;
};
// 设置每个子级盒子（这里创建了车箱中的货物几何体，其中对其顶面通过getTextCanvas单独设置了材质，还再货物外面套了一个相同大小的边缘几何体）
function initObject(width, height, length, x, y, z, index) {
    const mesh = new THREE.Object3D();
    const geometry = new THREE.BoxGeometry(width, height, length);
    // 设置随机颜色
    const color = new THREE.Color(0xff794204);
    // 设置子级盒子材质
    const material = [];
    for (let j = 0; j < geometry.groups.length; j++) {
        const mats = new THREE.MeshBasicMaterial({
            color,
            transparent: true,
            opacity: 0.8,
        });
        material.push(mats);
    }

    // console.log(
    //   '宽:',
    //   width,
    //   '高:',
    //   height,
    //   '长:',
    //   length,
    //   '体积:',
    //   width * height * length,
    // );

    // 上下面
    // material[2].map = new THREE.CanvasTexture(
    //     getTextCanvas(width, height, length, index)
    // );

    // 几何体 + 材质 = 物体
    const cube = new THREE.Mesh(geometry, material);

    // !!! 添加额外物体属性
    cube.itemId = index;

    // 3D模型添加 材质和几何体
    mesh.add(cube);
    // 设置子级盒子边框
    const wideFrame = new THREE.BoxGeometry(width, height, length);
    const materialBorder = new THREE.EdgesGeometry(wideFrame);
    const lineFrame = new THREE.LineSegments(
        materialBorder,
        new THREE.LineBasicMaterial({ color: 0xff131313 })
    );
    mesh.add(lineFrame);
    // 装箱复位
    mesh.position.set(
        y + width / 2 - cartonWidth / 2,
        z + height / 2 - cartonHeight / 2,
        x + length / 2 - cartonLength / 2,
        'XYZ'
    );
    // mesh.object.itemId = index;
    scene.add(mesh);
    boxArr.push(cube);
    return mesh;
};
getInfoDetail()

//渲染函数
function animate() {
	//这里是动画函数，会不断调用，刷新帧(拖动、缩放也需要)
	requestAnimationFrame( animate );

	controls.update();
	//渲染
    labelRenderer.render(scene, camera);
	renderer.render( scene, camera );
}
animate();

// 监听窗口变化
window.addEventListener("resize", () => {
	// 重置渲染器宽高比
	renderer.setSize(window.innerWidth, window.innerHeight);
	// 重置相机宽高比
	camera.aspect = window.innerWidth / window.innerHeight;
	// 更新相机投影矩阵
	camera.updateProjectionMatrix();
})

