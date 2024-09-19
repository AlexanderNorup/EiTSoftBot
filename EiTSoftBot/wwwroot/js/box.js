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
      } else {
        p.fill(150);
      }
      p.rect(this.x, this.y, this.width, this.length);
      p.fill(0);
      p.stroke(0);
      p.text(`Z: ${this.z}\nH: ${this.height}`, this.x + 10, this.y + 20)
    }
  
  }