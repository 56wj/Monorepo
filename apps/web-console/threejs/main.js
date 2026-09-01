import * as THREE from 'three';
//导入轨道控制器
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
//导入lil-GUI
import { GUI } from 'three/addons/libs/lil-gui.module.min.js'

console.log(THREE.Scene)
// 创建场景
const scene = new THREE.Scene();
// 创建相机 参数：（视角， 宽高比，近平面，远平面）
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
//创建渲染器并设置场景大小
const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
//添加到相应元素中
document.body.appendChild( renderer.domElement );

//创建并添加世界坐标辅助器
const axesHelper = new THREE.AxesHelper( 2, 3, 4 ); //参数为坐标线长度
scene.add( axesHelper );

//创建立方体,，threejs中还有圆、圆柱、圆锥等各种几合体类
const geometry = new THREE.BoxGeometry( 1, 0.2, 1 );
//创建材质
const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
//创建物体（网格）
var cube = new THREE.Mesh( geometry, material );
cube.position.set(0.5, 0.1, 0.5)

// const geometry1 = new THREE.CylinderGeometry( 5, 5, 20, 32 );
// const material1 = new THREE.MeshBasicMaterial( {color: 0xffff00} );
// const cylinder = new THREE.Mesh( geometry1, material1 );
// cylinder.position.set(0, 0.2, 0)
var geometry1 = new THREE.CylinderGeometry( 0.25, 0.25, 0.4, 32 );
var material1 = new THREE.MeshBasicMaterial( {color: 0xffff00} );
var cylinder = new THREE.Mesh( geometry1, material1 );
cylinder.position.set(0.25, 0.3, 0.25)



let group = new THREE.Group();
// group.add(cube, cylinder);
group.add( cube );
group.add( cylinder );
//添加网格到场景，add也可以用于Mesh对象中，给父几何体添加子几何体（很多局部属性会根据其父对象来确定具体值），此时position.set()会以父几何体为原点。
scene.add( group );

//设置相机位置，默认是0
camera.position.z = 8;
//相机看向哪一点，默认为0，0，0
camera.lookAt(0, 0, 0);

//添加轨道控制器（旋转、缩放控制）
const controls = new OrbitControls(camera,renderer.domElement)
//设置带阻尼的惯性
controls.enableDamping = true;
//设值阻尼系数
controls.dampingFactor = 0.05;
//设置自动旋转
controls.autoRotate = true;

//创建射线
const raycaster = new THREE.Raycaster();
//创建鼠标向量
const mouse = new THREE.Vector2();
//监听点击事件
window.addEventListener("click", (event) => {
	// 设置鼠标向量的xy值（归一化，使xy坐标的范围在-1到1之间）
	mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
	mouse.y = -((event.clientY / window.innerHeight) * 2 - 1);
	// 通过摄像机和鼠标位置更新射线
	raycaster.setFromCamera(mouse, camera);
	// 计算物体和射线的焦点
	const intersects = raycaster.intersectObjects(scene.children);
	// 点击变为红色，再点变回原色
	if(intersects.length > 0) {

		if(intersects[0].object._isSelect) {
			intersects[0].object.material.color.set(
				intersects[0].object._originColor
			)
			intersects[0].object._isSelect = false;
			return;
		}

		// 自定义属性记录是否被点击，以及原色
		intersects[0].object._isSelect = true;
		// 这里获取的不能是对象，负责之后改色后，_originColor也会更改
		intersects[0].object._originColor = intersects[0].object.material.color.getHex();
		intersects[0].object.material.color.set(0xff0000);
	}
});

//渲染函数
function animate() {
	//这里是动画函数，会不断调用，刷新帧(拖动、缩放也需要)
	requestAnimationFrame( animate );

	controls.update();
	// 旋转
    // cube.rotation.x += 0.01;
	// cube.rotation.y += 0.01;

	//渲染
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

//lil-gui
let eventObj = {
	Fullscreen: function() {
		document.body.requestFullscreen();
		console.log("全屏");
	},
	ExitFullscreen: function() {
		document.exitFullscreen();
		console.log("退出全屏");
	}
}

//创建GUI
const gui = new GUI();
//添加按钮(对象，对象中的属性函数)
gui.add(eventObj, "Fullscreen").name("全屏");
gui.add(eventObj, "ExitFullscreen").name("退出全屏");
//控制立方体位置
let folder = gui.addFolder("立方体位置")
folder.add(cube.position, "x", -5, 5).name("立方体x轴位置").onChange((val) => {
	console.log(val);
});
folder.add(cube.position, "y", -5, 5).name("立方体y轴位置").onFinishChange((val) => {
	//只在拖动结束后执行一次
	console.log(val);
});;
folder.add(cube.position, "z", -5, 5).name("立方体z轴位置");
// 第二种写法 gui.add(cube.position, "x").min(-10).max(10).step(1).name("立方体x轴位置");
//立方体线框模式
gui.add(cube.material, "wireframe").name("立方体线框模式");
//立方体颜色更改
let colorParams = {
	cubeColor: "#00ff00"
}
gui.addColor(colorParams, "cubeColor").name("立方体颜色").onChange((val) => {
	cube.material.color.set(val);
})