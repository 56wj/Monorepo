import * as THREE from 'three';
//导入轨道控制器
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
//导入lil-GUI
import { GUI } from 'three/addons/libs/lil-gui.module.min.js'
// 导入GLTF加载器
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js"

// 导入解压器
import { DRACOLoader } from "three/addons/loaders/DRACOLoader.js"

console.log(THREE.Scene)
// 创建场景
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x999999);
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


const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath(
  "https://threejs.org/examples/jsm/libs/draco/gltf/"
);

const loader = new GLTFLoader();
loader.setDRACOLoader(dracoLoader);
// 实例化加载器
// 加载模型
loader.load(
	"./model/ferrari.glb",
	(gltf) => {
		// 加载到创建（一个模型可能有多个场景）如果模型全黑可能是没有光源
        console.log(gltf)
		scene.add(gltf.scene);
	}
)

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
// controls.autoRotate = true;


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

