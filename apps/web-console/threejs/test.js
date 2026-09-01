import * as THREE from 'three';

//导入轨道控制器
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
// 基本场景配置
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 创建盒子
const boxWidth = 2;
const boxHeight = 3;
const boxDepth = 4;

const boxGeometry = new THREE.BoxGeometry(boxWidth, boxHeight, boxDepth);
const boxMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true });
const boxMesh = new THREE.Mesh(boxGeometry, boxMaterial);
scene.add(boxMesh);

// 初始化轨道控制器
const controls = new OrbitControls(camera, renderer.domElement);
// 控制器阻尼
controls.enableDamping = true;
// 动态阻尼系数
controls.dampingFactor = 0.1;
// 旋转中心点
controls.target.set(0, 0, 0);

// 创建尺寸框
function createDimensionLines(boxMesh) {
    const dimensionLines = new THREE.Group();
    const lineMaterial = new THREE.LineBasicMaterial({ color: 0xff0000 });

    // 长度框
    const lengthLine = new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(boxWidth / 2, 0, 0),
        new THREE.Vector3(boxWidth / 2, 0, -boxDepth)
    ]), lineMaterial);
    dimensionLines.add(lengthLine);

    // 宽度框
    const widthLine = new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, boxHeight / 2, -boxDepth),
        new THREE.Vector3(boxWidth, boxHeight / 2, -boxDepth)
    ]), lineMaterial);
    dimensionLines.add(widthLine);

    // 高度框
    const heightLine = new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0, -boxDepth / 2),
        new THREE.Vector3(0, boxHeight, -boxDepth / 2)
    ]), lineMaterial);
    dimensionLines.add(heightLine);

    return dimensionLines;
}

const dimensionLines = createDimensionLines(boxMesh);
scene.add(dimensionLines);

// 相机位置
camera.position.z = 5;

// 渲染循环
function animate() {
    controls.update();
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

animate();
