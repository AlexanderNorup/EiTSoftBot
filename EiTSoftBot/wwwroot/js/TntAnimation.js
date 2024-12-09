class TntAnimation {
    x = 0;
    z = 0;
    y = 8;

    v = -0.05;
    a = 0.1;
    explosionA = 25;

    mirHeight = 0.55;

    isDone = false;
    explosionPhase = false;
    explosionMaxSize = 12;
    explosionSize = 0;
    explosionOpacity = 1;

    explosionXRot = Math.floor(Math.random() * 8);
    explosionYRot = Math.floor(Math.random() * 8);
    explosionZRot = Math.floor(Math.random() * 8);
    explosionSound = new Audio('/models/explosion.mp3');

    /**
     * @type {THREE.Mesh<THREE.BoxGeometry,THREE.MeshBasicMaterial,THREE.Object3DEventMap>}
     */
    cube = null;
    explosion = null;
    scene = null;

    constructor(cube, explosion) {
        this.cube = cube;
        this.explosion = explosion;
    }

    update(dt) {
        if (!this.explosionPhase) {
            if (this.y > this.mirHeight) {
                this.v += this.a * dt;
                this.y -= this.v;
                this.cube.position.set(this.x, this.y, this.z);
            } else {
                this.cube.visible = false;
                this.explosionPhase = true;
                this.explosionSound.play();
            }
        } else {
            if (this.explosionSize < this.explosionMaxSize) {
                this.explosion.visible = true;
                this.explosionSize += this.explosionA * dt;
                this.explosion.scale.set(this.explosionSize, this.explosionSize, this.explosionSize);
                this.explosion.rotation.set(this.explosion.rotation.x + this.explosionXRot * dt,
                    this.explosion.rotation.y + this.explosionYRot * dt,
                    this.explosion.rotation.z + this.explosionZRot * dt);
            } else {
                this.isDone = true;
            }
        }
    }
}
