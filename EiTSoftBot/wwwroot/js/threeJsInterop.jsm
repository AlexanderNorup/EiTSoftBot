// inspired by https://github.com/mrdoob/three.js/blob/master/examples/webgl_animation_keyframes.html
import * as THREE from 'three';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { FontLoader } from 'three/addons/loaders/FontLoader.js';

// Post processing
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { OutlinePass } from 'three/addons/postprocessing/OutlinePass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';


// 2d to 3d Scale
const scale = 0.01;

/**
 * @type {THREE.Scene}
 */
let scene;
/**
 * @type {THREE.PerspectiveCamera}
 */
let camera;
/**
 * @type {THREE.WebGLRenderer}
 */
let renderer;
/**
 * @type {THREE.Mesh<THREE.BoxGeometry,THREE.MeshBasicMaterial,THREE.Object3DEventMap>[]}
 */
let boxMapping = [];

/**
 * @type {THREE.OutlinePass}
 */
let outlinePass;

/**
 * @type {TntAnimation[]}
 */
let currentTntAnims = [];

/**
 * @type {THREE.Font}
 */
let globalFont = null;

let explosionModel = null;
/**
 * @type {Mission}
 */
let currentMission = null;

/**
 * @type {THREE.Mesh<THREE.Mesh,THREE.Material,THREE.Object3DEventMap>[]}
 */
let currentMissionTextLabels = [];
let currentMissionMappings = [];

window.init3DScene = (divId) => {
    let containerDiv = document.getElementById(divId);
    if (containerDiv == null) {
        console.error("Failed to initialize scene. Could not find div with id: " + divId);
        return;
    }

    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(containerDiv.clientWidth, containerDiv.clientHeight);
    renderer.setClearColor(0x222222, .0);
    renderer.shadowMap.enabled = true;

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const pmremGenerator = new THREE.PMREMGenerator(renderer);

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xbfe3dd);
    scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture;
    camera = new THREE.PerspectiveCamera(75, containerDiv.clientWidth / containerDiv.clientHeight, 0.1, 1000);
    camera.position.z = 5;
    camera.position.y = 7;
    camera.position.x = -4;

    containerDiv.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(0, 1.2, 0);
    controls.update();
    controls.enablePan = false;
    controls.enableDamping = true;
    controls.maxPolarAngle = Math.PI / 1.82; 
    controls.maxDistance = 20;
    controls.minDistance = 2;

    const fontLoader = new FontLoader();
    fontLoader.load( '/models/helvetiker_regular.typeface.json', function ( font ) {
        globalFont = font;
    });

    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath('jsm/libs/draco/gltf/');

    const glbLoader = new GLTFLoader();
    glbLoader.setDRACOLoader(dracoLoader);
    glbLoader.load('/models/mir200a.glb', function (gltf) {
        const model = gltf.scene;
        model.position.set(0, -3, 0);
        model.scale.set(0.01, 0.01, 0.01);
        model.receiveShadow = true;
        model.castShadow = false;
        camera.lookAt(model.position);
        scene.add(model);
    }, undefined, function (e) {
        console.error("Failed to load MiR Model: ", e);
    });

    glbLoader.load('/models/warehouse.glb', function (gltf) {
        const model = gltf.scene;
        // model.position.set(-62.5, -3, 150);
        // model.scale.set(8, 8, 8);
        
        model.position.set(-62.5, -3, -30);
        model.quaternion.setFromAxisAngle( new THREE.Vector3( 0, 1, 0 ), Math.PI * 1.5 );
        model.scale.set(8, 8, 8);
        model.receiveShadow = true;
        model.castShadow = false;
        scene.add(model);
    }, undefined, function (e) {
        console.error("Failed to load WareHouse Model: ", e);
    });

    glbLoader.load('/models/explosion.glb', function (gltf) {
        const model = gltf.scene;
        model.position.set(0, 1, 0);
        model.scale.set(2, 2, 2);
        model.receiveShadow = true;
        model.castShadow = false;
        model.castShadow = false;
        explosionModel = model;
    }, undefined, function (e) {
        console.error("Failed to load Explosion Model: ", e);
    });

    // postprocessing

    let composer = new EffectComposer(renderer);

    const renderPass = new RenderPass(scene, camera);
    composer.addPass(renderPass);

    outlinePass = new OutlinePass(new THREE.Vector2(containerDiv.clientWidth, containerDiv.clientHeight), scene, camera);
    outlinePass.renderToScreen = true;
    outlinePass.edgeStrength = 3;
    outlinePass.edgeGlow = 0;
    outlinePass.edgeThickness = 1;
    outlinePass.visibleEdgeColor.set('#ffffff');
    outlinePass.hiddenEdgeColor.set('#eeeeee');

    composer.addPass(outlinePass);

    const outputPass = new OutputPass();
    composer.addPass(outputPass);

    const clock = new THREE.Clock();
    renderer.setAnimationLoop(animate);
    function animate() {
        const dt = clock.getDelta();
        if (currentTntAnims.length > 0) {
            for (let currentTntAnim of currentTntAnims) {
                currentTntAnim.update(dt);
                if (currentTntAnim.isDone) {
                    scene.remove(currentTntAnim.cube);
                    scene.remove(currentTntAnim.explosion);
                    window.removeAll2DBoxes(); // To actually remove the boxes
                }
            }
            currentTntAnims = currentTntAnims.filter(x => !x.isDone);
        }

        if(currentMissionTextLabels.length > 0){
            for(let label of currentMissionTextLabels){
                label.lookAt(camera.position);
            }
        }

        controls.update();
        composer.render();
    }

    window.onresize = function () {
        camera.aspect = containerDiv.clientWidth / containerDiv.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(containerDiv.clientWidth, containerDiv.clientHeight);
        composer.setSize(containerDiv.clientWidth, containerDiv.clientHeight);
    };

    renderer.domElement.style.touchAction = 'none';
    renderer.domElement.addEventListener('pointerdown', onPointerDown);

    function onPointerDown(event) {
        if (event.isPrimary === false || event.buttons !== 1) return;
        const rect = renderer.domElement.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        mouse.x = (x / containerDiv.clientWidth) * 2 - 1;
        mouse.y = (y / containerDiv.clientHeight) * - 2 + 1

        checkIntersection();
    }

    function checkIntersection() {
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObject(scene, true);
        if (intersects.length > 0) {
            const selectedObject = intersects[0].object;
            const boxId = selectedObject.userData.boxId;
            if (boxId !== undefined) {
                window.highlight2DBox(boxId)
            }
        }
    }
}

/**
 * @param {Box} box
 * @returns {void}
 */
window.update3DBox = (box) => {
    let cube = boxMapping[box.id];
    if (cube === undefined) {
        add3DBox(box);
        return;
    }
    let { x, y, z } = getPosFrom2DWorld(box.x, box.y, box.z);;
    cube.position.set(x, y, z);
    if (box.mouseOver || box.highlight) {
        outlinePass.selectedObjects.push(cube);
    }
    if (box.dragging) {
        cube.material.wireframe = true;
    } else {
        cube.material.wireframe = false;
    }
};

window.before3DUpdate = () => {
    if (outlinePass === undefined) {
        return;
    }
    outlinePass.selectedObjects = [];
}

window.do3DRemoveAnimation = () => {
    var textureLoader = new THREE.TextureLoader();
    let sideTexture = textureLoader.load('/models/tnt_side.png');
    let topTexture = textureLoader.load('/models/tnt_top.png');
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const cubeMaterials = [
        new THREE.MeshBasicMaterial({ map: sideTexture }), //right side
        new THREE.MeshBasicMaterial({ map: sideTexture }), //left side
        new THREE.MeshBasicMaterial({ map: topTexture }), //top side
        new THREE.MeshBasicMaterial({ map: topTexture }), //bottom side
        new THREE.MeshBasicMaterial({ map: sideTexture }), //front side
        new THREE.MeshBasicMaterial({ map: sideTexture }), //back side
    ];
    const cube = new THREE.Mesh(geometry, cubeMaterials);
    cube.receiveShadow = true;
    cube.castShadow = true;

    const explosion = explosionModel.clone(true);
    explosion.children[0].transparent = true;
    explosion.visible = false;

    scene.add(cube);
    scene.add(explosion);
    let newAnim = new TntAnimation(cube, explosion);
    currentTntAnims.push(newAnim);
};

function add3DBox(box) {
    if (!is3DInitialized()) {
        return;
    }
    let { x, y, z, width, length, height } = box;
    var textureLoader = new THREE.TextureLoader();
    let texture;
    if (box.weight >= 3) {
        texture = textureLoader.load('/models/heavy_box.png');
    } else {
        texture = textureLoader.load('/models/box.png');
    }

    const geometry = new THREE.BoxGeometry(width * scale, height * scale, length * scale);
    geometry.translate(width * scale / 2, height * scale / 2, length * scale / 2);
    const material = new THREE.MeshBasicMaterial({ map: texture });
    const cube = new THREE.Mesh(geometry, material);
    cube.receiveShadow = true;
    cube.castShadow = true;
    let newPos = getPosFrom2DWorld(x, y, z);
    cube.position.set(newPos.x, newPos.y, newPos.z);
    cube.userData.boxId = box.id;
    boxMapping[box.id] = cube;
    scene.add(cube);
}

window.remove3DBox = (id) => {
    let cube = boxMapping[id];
    if (cube === undefined) {
        return;
    }
    boxMapping[id] = undefined;
    scene.remove(cube);
}

window.is3DInitialized = () => {
    return scene != null && camera != null && renderer != null;
}

window.loadMission = (mission) => {
    const waypointScale = 10;
    const HomePos =  {x: 6, y: 2.5};
    window.clearMission();
    currentMission = new Mission(mission);

    for (let waypoint of currentMission.waypoints) {
        const geometry = new THREE.SphereGeometry( .5, 200, 200 ); 
        const material = new THREE.MeshBasicMaterial( { color: 0xeeeeee } ); 
        const sphere = new THREE.Mesh( geometry, material ); 
        sphere.position.set((waypoint.y - HomePos.y) * waypointScale, 1.5, (waypoint.x - HomePos.x) * waypointScale);
        const text = new TextGeometry( waypoint.name, {
            font: globalFont,
            size: .8,
            depth: .3,
            curveSegments: 12,
        } );
        text.computeBoundingBox();

        let textMesh = new THREE.Mesh( text, material );
        textMesh.lookAt(camera.position);

        textMesh.position.set(sphere.position.x, sphere.position.y + 1, sphere.position.z);
        currentMissionTextLabels.push(textMesh);
        currentMissionMappings.push(sphere);
        scene.add( textMesh );
        scene.add( sphere );
    }

    console.debug("Loaded mission: ", currentMission);
}

window.clearMission = () => {
    currentMission = null;
    for(let elem of currentMissionMappings){
        scene.remove(elem);
    }
    for(let elem of currentMissionTextLabels){
        scene.remove(elem);
    }
};

const mirOffset = { x: -2.25, y: 0.55, z: -3.8 };
/**
 * @param {number} x
 * @param {number} y
 * @param {number} z
 * @returns {THREE.Vector3}
 */
function getMirOffsetVector(x, y, z) {
    return new THREE.Vector3(x + mirOffset.x, y + mirOffset.y, z + mirOffset.z);
}

/**
 * @param {number} x
 * @param {number} y
 * @param {number} z
 * @returns {THREE.Vector3}
 */
function getPosFrom2DWorld(x, y, z) {
    // In the 2D view the Y-axis is our Z-axis
    // The X-axis is our X-axis
    // The Z-axis is our Y-axis

    return new getMirOffsetVector(x * scale, z * scale, y * scale);
}
