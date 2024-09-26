class Box {
  id = crypto.randomUUID();
  dragging = false;
  mouseOver = false;
  highlight = false;
  x = 0;
  y = 0;
  z = 0;
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
  */
  constructor(x, y, width, length, height, weight) {
    this.x = x;
    this.y = y;
    this.width = width;
    this.length = length;
    this.height = height;
    this.weight = weight;
  }

  update(p) {
    if (this.dragging) {
      this.x = p.mouseX + this.offsetX;
      this.y = p.mouseY + this.offsetY;
    }
  }

  show(p) {
    p.stroke(0);
    if (this.dragging) {
      p.fill(50);
    } else if (this.mouseOver) {
      p.fill(100);
    } else if (this.highlight) {
      p.fill('green');
    } else {
      p.fill(150);
    }
    p.rect(this.x, this.y, this.width, this.length);
    p.fill(0);
    p.stroke(0);
    p.text(`Z: ${this.z}\nH: ${this.height}`, this.x + 10, this.y + 20);

    if (window.update3DBox !== undefined) {
      window.update3DBox(this);
    }
  }

}