class Box {
    constructor (x, y, width, length, height, weight) {
      this.dragging = false;
      this.mouseOver = false;
      this.x = x;
      this.y = y;
      this.z = 0;
      this.width = width;
      this.length = length;
      this.height = height;
      this.weight = weight;
      this.offsetX = 0;
      this.offsetY = 0;
    }
  
    update() {
      if (this.dragging) {
        this.x = mouseX + this.offsetX;
        this.y = mouseY + this.offsetY;
      }
    }
  
    show() {
      stroke(0);
      if (this.dragging) {
        fill(50);
      } else {
        fill(150);
      }
      rect(this.x, this.y, this.width, this.length);
      fill(0);
      stroke(0);
      text(`Z: ${this.z}\nH: ${this.height}`, this.x + 10, this.y + 20)
    }
  
  }