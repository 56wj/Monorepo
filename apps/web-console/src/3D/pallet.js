import * as THREE from 'three';
// 导入轨道控制器 只能通过这种方法
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
// 导入CSS3
import { CSS2DRenderer, CSS2DObject } from 'three/examples/jsm/renderers/CSS2DRenderer.js'

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

// 创建相机 参数：（视角， 宽高比，近平面，远平面）
const camera = new THREE.PerspectiveCamera(
    45,
    window.innerWidth / window.innerHeight,
    1,
    99999
);
// scene.add(camera);

// 初始化网格
const grid = new THREE.GridHelper(15000, 20, 0x333333, 0x333333);

// 初始化渲染器并设置场景大小
const renderer = new THREE.WebGLRenderer({
    antialias: true, // 开启锯齿
    alpha: true, // 透明度
});

// 初始化CSS2D渲染器
// const labelRenderer = new CSS2DRenderer();
// labelRenderer.setSize(window.innerWidth, window.innerHeight);
// labelRenderer.domElement.style.position = 'absolute';
// labelRenderer.domElement.style.top = '0px';
// document.body.appendChild(labelRenderer.domElement);
// labelRenderer.domElement.addEventListener("click", onMouseClick);
//
let css2DObject;

// 初始化轨道控制器
// const controls = new OrbitControls(camera, labelRenderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);

// 三维坐标轴
const axesHelper = new THREE.AxesHelper(5000);
// scene.add( axesHelper );

// 选中子级盒子
const mouse = new THREE.Vector3();
// 射线
const raycaster = new THREE.Raycaster();

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
        css2DObject.visible = true;
        css2DObject.position.x = intersected.parent.position.x - 50 + 18;
        css2DObject.position.y = intersected.parent.position.y + 50 + 38;
        css2DObject.position.z = intersected.parent.position.z;
        console.log(css2DObject);
        modifyDocument("lableItemId", "red", intersected.itemId);
	}else{
        css2DObject.visible = false;
    }
};

//渲染函数
function animate() {
	//这里是动画函数，会不断调用，刷新帧(拖动、缩放也需要)
	requestAnimationFrame( animate );

	controls.update();
	//渲染
    // labelRenderer.render(scene, camera);
	renderer.render( scene, camera );
}

// 获取详细数据(获取货物数据)
// function getInfoDetail(data) {
//     const res = { status: 200, data: [], success: true };
//     console.log(data);
//     res.data = data;
//     defaults.result = res;
//     defaults.detailList = [];

//     // 初始装货箱信息
//     const { width, length, height } = res.data[0].container.cube;
//     initBox(width, height, length, res.data[0].container);

//     // 单个详情
//     const placedItemsArr = res.data[0].placedItems;
//     detailIndex = defaults.detailNum = placedItemsArr.length;

//     // 渲染单个子级盒子
//     boxArr = [];
//     for (let i = 0; i < defaults.detailNum; i++) {
//         const detail = placedItemsArr[i];
//         defaults.detailList.push(
//             initObject(
//                 detail.rotatedCube.width,
//                 detail.rotatedCube.height,
//                 detail.rotatedCube.length,
//                 detail.position.x,
//                 detail.position.y,
//                 detail.position.z,
//                 // i
//                 detail.itemId
//             )
//         );
//     }
// };
function getInfoDetail(data) {

    // 初始装货箱信息
    const { bin_width, bin_length, bin_height } = data.container;
    initBox(bin_width, bin_height, bin_length, data.container);

    // 单个详情
    const placedItemsArr = data.placed_items;
    detailIndex = defaults.detailNum = placedItemsArr.length;

    // 渲染单个子级盒子
    boxArr = [];
    for (let i = 0; i < defaults.detailNum; i++) {
        const detail = placedItemsArr[i];
        defaults.detailList.push(
            initObject(
                detail.width,
                detail.height,
                detail.length,
                detail.position_x,
                detail.position_y,
                0,
                // i
                detail.id,
                detail.color
            )
        );
    }
};
// 初始化车箱(车箱)
function initBox(xLen, yLen, zLen, context) {
    console.log(xLen, yLen, zLen);
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

    // css2DObject.visible = true;
    // css2DObject.position.x = 0;
    // css2DObject.position.y = 0;
    // css2DObject.position.z = 0;
    getTruck(xLen, yLen, zLen);

    return containerBox;
};
function getTruck(xLen, yLen, zLen) {
    var head_geometry = new THREE.BoxGeometry(200, 240, 180);
    var head_material = new THREE.MeshBasicMaterial( {color: 0x008B8B} );
    //创建材质
    // const material = [];
    // for (let j = 0; j < head_geometry.groups.length; j++) {
    //     const mats = new THREE.MeshBasicMaterial({
    //         color: 0x00ff00,
    //         transparent: true,
    //         opacity: 0.8,
    //     });
    //     material.push(mats);
    // }
    //创建物体（网格）
    var cube = new THREE.Mesh( head_geometry, head_material );
    cube.position.set(0, -yLen/2+100, 90 + zLen/2);
    // material[4].map = new THREE.CanvasTexture(
    //     getTextCanvas2(xLen, yLen, zLen)
    // );
    scene.add(cube);

    var window_geometry = new THREE.BoxGeometry(180, 70, 10);
    var window_material = new THREE.MeshBasicMaterial( {color: 0xffffff} );
    var window = new THREE.Mesh( window_geometry, window_material );
    window.position.set(0, 30, 180 + zLen/2);
    scene.add( window );

    var radius = 50
    var wheel_geometry = new THREE.CylinderGeometry( radius, radius, 40, 32 );
    var wheel_material = new THREE.MeshBasicMaterial( {color: 0x000000} );
    // 几何体绕着x轴旋转45度
    wheel_geometry.rotateZ(Math.PI / 2);
    var front_wheel1 = new THREE.Mesh( wheel_geometry, wheel_material );
    var front_wheel2 = new THREE.Mesh( wheel_geometry, wheel_material );
    var back_wheel1 = new THREE.Mesh( wheel_geometry, wheel_material );
    var back_wheel2 = new THREE.Mesh( wheel_geometry, wheel_material );
    var back_wheel3 = new THREE.Mesh( wheel_geometry, wheel_material );
    var back_wheel4 = new THREE.Mesh( wheel_geometry, wheel_material );
    front_wheel1.position.set(90, -yLen/2-radius, zLen/2+60);
    front_wheel2.position.set(-90, -yLen/2-radius, zLen/2+60);
    back_wheel1.position.set(90, -yLen/2-radius, -zLen/2+zLen/8);
    back_wheel2.position.set(-90, -yLen/2-radius, -zLen/2+zLen/8);
    back_wheel3.position.set(90, -yLen/2-radius, -zLen/2+zLen/8+100);
    back_wheel4.position.set(-90, -yLen/2-radius, -zLen/2+zLen/8+100);
    scene.add( front_wheel1 );
    scene.add( front_wheel2 );
    scene.add( back_wheel1 );
    scene.add( back_wheel2 );
    scene.add( back_wheel3 );
    scene.add( back_wheel4 );

};
function getTextCanvas2(width, height, length){
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 2*height;
    canvas.height = 2*width;

    // 设置箱子面颜色
    ctx.fillStyle = 'rgba(255,255,5,1)';
    ctx.fillRect(0, 0, 2*height, 2*width);
    ctx.save();

    ctx.fillStyle = 'black';
    ctx.font = 'bold 100px "楷体"';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`车头`, Math.round(height), Math.round(width));
    return canvas;
}
// 设置每个子级盒子（这里创建了车箱中的货物几何体，其中对其顶面通过getTextCanvas单独设置了材质，还再货物外面套了一个相同大小的边缘几何体）
// function initObject(width, height, length, x, y, z, index) {
//     const mesh = new THREE.Object3D();
//     const geometry = new THREE.BoxGeometry(width, height, length);
//     // 设置随机颜色
//     const color = new THREE.Color(0xff794204);
//     // 设置子级盒子材质
//     const material = [];
//     for (let j = 0; j < geometry.groups.length; j++) {
//         const mats = new THREE.MeshBasicMaterial({
//             color,
//             transparent: true,
//             opacity: 0.8,
//         });
//         material.push(mats);
//     }

//     // 几何体 + 材质 = 物体
//     const cube = new THREE.Mesh(geometry, material);

//     // !!! 添加额外物体属性
//     cube.itemId = index;

//     // 3D模型添加 材质和几何体
//     mesh.add(cube);
//     // 设置子级盒子边框
//     const wideFrame = new THREE.BoxGeometry(width, height, length);
//     const materialBorder = new THREE.EdgesGeometry(wideFrame);
//     const lineFrame = new THREE.LineSegments(
//         materialBorder,
//         new THREE.LineBasicMaterial({ color: 0xff131313 })
//     );
//     mesh.add(lineFrame);
//     // 装箱复位
//     mesh.position.set(
//         y + width / 2 - cartonWidth / 2,
//         z + height / 2 - cartonHeight / 2,
//         x + length / 2 - cartonLength / 2,
//         'XYZ'
//     );
//     console.log(mesh.position);
//     // mesh.object.itemId = index;
//     scene.add(mesh);
//     boxArr.push(cube);
//     return mesh;
// };

// 悬浮信息框
// function addCSS2DLabelToScene() {
//     var element = document.getElementById("WebGL-output");

//     //把生成的CSSDOM对象处理成three的节点对象
//     css2DObject = new CSS2DObject(element);
//     //设置CSS2DObject对象
//     css2DObject.position.x = 0;
//     css2DObject.position.y = 0;
//     css2DObject.position.z = 0;
//     //在第二个场景中添加这个对象
//     scene.add(css2DObject);
//     // 默认不显示
//     css2DObject.visible = false;
// }
// function modifyDocument(id, color, value) {
//     var dom = document.getElementById(id);
//     dom.style.color = color;
//     dom.textContent = value;
// }
    // 材质（这里用了canvas绘制了纸箱的顶面，有字体、胶带的那个）
function getTextCanvas(width, height, length, i) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        ctx.globalAlpha = 0.65;
        canvas.width = 2*length;
        canvas.height = 2*width;

        // 设置箱子面颜色
        ctx.fillStyle = 'rgba(255,255,5,1)';
        ctx.fillRect(0, 0, 2*length, 2*width);
        ctx.save();

        ctx.fillStyle = 'black';
        ctx.font = 'bold 40px "楷体"';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`货物${i}`, Math.round(length), Math.round(width));
        return canvas;
}
function initObject(width, height, length, x, y, z, index, c) {
    const mesh = new THREE.Object3D();
    const geometry = new THREE.BoxGeometry(length, height, width);
    // 设置随机颜色
    const color = new THREE.Color(0xff794204);
    // 设置子级盒子材质
    const material = [];
    for (let j = 0; j < geometry.groups.length; j++) {
        const mats = new THREE.MeshBasicMaterial({
            color: c,
            transparent: true,
            opacity: 0.8,
        });
        material.push(mats);
    }

    material[2].map = new THREE.CanvasTexture(
        getTextCanvas(width, height, length, index)
    );

    // 几何体 + 材质 = 物体
    const cube = new THREE.Mesh(geometry, material);

    // !!! 添加额外物体属性
    cube.itemId = index;

    // 3D模型添加 材质和几何体
    mesh.add(cube);
    // 设置子级盒子边框
    const wideFrame = new THREE.BoxGeometry(length, height, width);
    const materialBorder = new THREE.EdgesGeometry(wideFrame);
    const lineFrame = new THREE.LineSegments(
        materialBorder,
        new THREE.LineBasicMaterial({ color: 0xff131313 })
    );
    mesh.add(lineFrame);
    // 装箱复位
    mesh.position.set(
        x + length / 2 - cartonWidth / 2,
        z + height / 2 - cartonHeight / 2,
        cartonLength / 2 -y - width / 2,
        'XYZ'
    );
    // console.log(mesh.position);
    // mesh.object.itemId = index;
    scene.add(mesh);
    boxArr.push(cube);
    return mesh;
};

function init(data) {
    WIDTH =  Number(
        window
            .getComputedStyle(
                document.getElementById(
                    'container'
                )
            )
        .width.split('px')[0]);
    console.log(WIDTH);
    HEIGHT = window.innerHeight;

    // 场景颜色
    scene.background = new THREE.Color(0x999999);

    // 调整相机位置
    camera.position.set(1000, 1000, 1000);
    camera.up.x = 0;
    camera.up.y = 1;
    camera.up.z = 0;
    camera.lookAt({
        x: 0,
        y: 0,
        z: 200,
    });

    scene.add(camera);
    // 添加坐标轴
    // scene.add(axesHelper);

    // 控制器阻尼
    controls.enableDamping = true;
    // 动态阻尼系数
    controls.dampingFactor = 0.1;
    // 旋转中心点
    controls.target.set(0, 0, 0);
    
    renderer.setSize( WIDTH, HEIGHT );
    camera.aspect = WIDTH / HEIGHT;
    camera.updateProjectionMatrix();
    //添加到相应元素中
    document.getElementById('3D_chart').appendChild( renderer.domElement );
    animate();

    // 添加盒子
    // addCSS2DLabelToScene();
    // 添加标签
    getInfoDetail(data);

    // 监听窗口变化
    window.addEventListener("resize", () => {
        WIDTH =  Number(
            window
                .getComputedStyle(
                    document.getElementById(
                        'container'
                    )
                )
            .width.split('px')[0]);
    
        HEIGHT = window.innerHeight;
        // 重置渲染器宽高比
        renderer.setSize(WIDTH, HEIGHT);
        // 重置相机宽高比
        camera.aspect = WIDTH / HEIGHT;
        // 更新相机投影矩阵
        camera.updateProjectionMatrix();
    })
};

// 假设你已经有一个 Three.js 场景实例 scene

function clearScene(scene) {
    // 遍历场景中的所有子对象
    while(scene.children.length > 0){ 
        const obj = scene.children[0];
        scene.remove(obj);
        
        // 如果对象有几何体和材质，进行进一步的清理
        if (obj.geometry) obj.geometry.dispose();
        if (obj.material) {
            // 如果材质是数组（如多材质的网格），则需要逐一释放
            if (Array.isArray(obj.material)) {
                obj.material.forEach(material => material.dispose());
            } else {
                obj.material.dispose();
            }
        }
        
        // 如果有纹理，进行释放
        if(obj.texture){
            obj.texture.dispose();
        }
    }
};


export function PackagePreview3DInit(data) {
    // 初始化
    console.log("3D初始化");
    clearScene(scene);
    init(data);
    // 渲染
    // animate();
};

