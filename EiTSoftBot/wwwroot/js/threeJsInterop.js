// inspired by https://github.com/mrdoob/three.js/blob/master/examples/webgl_animation_keyframes.html
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

let scene;
let camera;
let renderer;

window.initScene = (divId) => {
    let containerDiv = document.getElementById(divId);
    if (containerDiv == null) {
        console.error("Failed to initialize scene. Could not find div with id: " + divId);
        return;
    }

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(containerDiv.clientWidth, containerDiv.clientHeight);

    const pmremGenerator = new THREE.PMREMGenerator(renderer);

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xbfe3dd);
    scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture;
    camera = new THREE.PerspectiveCamera(75, containerDiv.clientWidth / containerDiv.clientHeight, 0.1, 1000);
    camera.position.z = 10;

    containerDiv.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(0, 0.5, 0);
    controls.update();
    controls.enablePan = false;
    controls.enableDamping = true;


    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath('jsm/libs/draco/gltf/');

    const loader = new GLTFLoader();
    loader.setDRACOLoader(dracoLoader);
    loader.load('/models/mir200a.glb', function (gltf) {
        const model = gltf.scene;
        model.position.set(0, -3, 0);
        model.scale.set(0.01, 0.01, 0.01);
        scene.add(model);
    }, undefined, function (e) {
        console.error("Failed to load MiR Model: ", e);
    });


    renderer.setAnimationLoop(animate);
    function animate() {
        controls.update();
        renderer.render(scene, camera);
    }

    window.onresize = function () {
        camera.aspect = containerDiv.clientWidth / containerDiv.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(containerDiv.clientWidth, containerDiv.clientHeight);
    };
}

window.addBox = () => {
    if (!isInitialized()) {
        return;
    }
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
}

window.isInitialized = () => {
    return scene != null && camera != null && renderer != null;
}
