class Box {
    id = crypto.randomUUID();
    dragging = false;
    mouseOver = false;
    highlight = false;
    x = 0;
    y = 0;
    z = 0;
    snapX = 0;
    snapY = 0;
    width = 0;
    length = 0;
    height = 0;
    weight = 0;
    offsetX = 0;
    offsetY = 0;

    /**
    * @param {number} x
    * @param {number} y
    * @param {number} width
    * @param {number} length
    * @param {number} height
    * @param {number} weight
    * @param {object} data
    */
    constructor(x, y, width, length, height, weight, data=null) {
        if (data !== null) {
            Object.assign(this, data);
            return;
        }
        this.x = x;
        this.y = y;
        this.width = width;
        this.length = length;
        this.height = height;
        this.weight = weight;
    }

    update(p) {
        if (this.dragging) {
            const xOverhang = this.width / 2;
            const yOverhang = this.length / 2;
            this.x = clamp(p.mouseX + this.offsetX, 0 - xOverhang, p.width - xOverhang);
            this.y = clamp(p.mouseY + this.offsetY, 0 - yOverhang, p.height - yOverhang);
        }
    }

    show(p) {
        p.stroke(0);
        if (this.dragging) {
            p.fill(50);
        } else if (this.highlight) {
            p.fill('green');
        } else if (this.mouseOver) {
            p.fill(100);
        } else {
            p.fill(150);
        }
        p.rect(this.x, this.y, this.width, this.length);
        p.fill(0);
        p.stroke(0);
        let realWorldH = this.height * window.getRealWorldScale();
        let realWorldZ = this.z * window.getRealWorldScale();
        p.text(`Z: ${realWorldZ.toFixed(2)}\nH: ${realWorldH.toFixed(2)}`, this.x + 10, this.y + 20);

        if (window.update3DBox !== undefined) {
            window.update3DBox(this);
        }
    }

    showSnap(p, gridFactor) {
        p.stroke(255);
        p.fill(255);
        this.snapX = Math.round(this.x / gridFactor) * gridFactor + Math.round(this.x / gridFactor);
        this.snapY = Math.round(this.y / gridFactor) * gridFactor + Math.round(this.y / gridFactor);
        p.rect(this.snapX, this.snapY, this.width, this.length);
    }
}



/**
 * Clamps a number between a minimum and maximum value
 * @param {Number} value
 * @param {Number} min
 * @param {Number} max
 * @returns {Number}
 */
function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
}