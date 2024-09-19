let boxes = [new Box(0, 0, 100, 100, 100, 100)];
let dragging = false;
let currentBox = null;

function setup() {
  let canvas = createCanvas(450, 760); // MIR size: w: 4.5, h: 7.6: 
  canvas.parent("canvasContainer");
}

function draw() {
  background(220);
  drawBoxes();
}

function addBox(x, y, width, length, height, weight) {
  boxes.push(new Box(x, y, width, length, height, weight));
  sortBoxes();
}

function drawBoxes() {
  boxes.forEach((box) => {
    if (box == currentBox) {
      handleCollision();
      box.update();
      sortBoxes();
    }
    box.show();
  });
}

// TODO: On mouse release, check all affect (colliding) boxes, and if one is floating (has nothing below), snap to bottom
// Get all colliding boxes, if they collide with nothing but currentbox, set z = 0. If they collide with something else, ...

function handleCollision() {
  let topZ = 0;
  boxes.forEach((box) => {
    if (currentBox == box) return;
    if (collisionCheck(currentBox, box)) {
      if (topZ < box.z + box.height) topZ = box.z + box.height
    }
  })
  currentBox.z = topZ;
}

function collisionCheck(boxA, boxB) {
  if (
    boxA.x + boxA.width >= boxB.x && // A right edge past B left
    boxA.x <= boxB.x + boxB.width && // A left edge past B right
    boxA.y + boxA.length >= boxB.y && // A bottom edge past B top
    boxA.y <= boxB.y + boxB.length // A top edge past B bottom
  ) return true;

  return false;
}

function sortBoxes() {
  boxes.sort((a, b) => a.z > b.z ? 1 : -1)
}

function mousePressed() {
  dragging = true;
  let topBoxZ = 0;
  boxes.forEach((box) => {
    if (mouseX > box.x && mouseX < box.x + box.width && mouseY > box.y && mouseY < box.y + box.length) {
      if (box.z + box.height > topBoxZ) {
        currentBox = box;
      }
    }
  })
  if (currentBox != null) {
    dragging = true;
    currentBox.dragging = true;
    currentBox.offsetX = currentBox.x - mouseX;
    currentBox.offsetY = currentBox.y - mouseY;
  }
  
}

function mouseReleased() {
  if (currentBox != null) {
    currentBox.dragging = false;
    dragging = false;
    currentBox = null;
  }
}