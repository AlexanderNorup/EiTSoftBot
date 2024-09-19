window.startP5Sketch = () => {
    new p5(sketch, window.document.getElementById('canvasContainer'));
    return true;
};

window.sketch = (p) => {

    let boxes = [new Box(0, 0, 100, 100, 100, 100)];
    let dragging = false;
    let currentBox = null;
    let hoverBox = null;

    p.setup = () => {
        let canvas = p.createCanvas(450, 760); // MIR size: w: 4.5, h: 7.6: 
        canvas.parent("canvasContainer");
    };

    p.draw = () => {
        p.background(220);
        sortBoxes();
        drawBoxes();
    };

    window.addBox = (x, y, width, length, height, weight) => {
        let newBox = new Box(x, y, width, length, height, weight);
        boxes.push(newBox);
        handleCollisionCurrentOrNew(newBox);
        sortBoxes();
    };

    function drawBoxes() {
        if (!dragging) {
            let newHoverBox = getBoxUnderMouse();
            if (newHoverBox == null && hoverBox != null) {
                hoverBox.mouseOver = false;
                hoverBox = null;
            }
            else if (newHoverBox != null && hoverBox != null) {
                hoverBox.mouseOver = false;
                hoverBox = newHoverBox;
                hoverBox.mouseOver = true;
            } else if (newHoverBox != null && hoverBox == null) {
                hoverBox = newHoverBox;
                hoverBox.mouseOver = true;
            }
        }
        boxes.forEach((box) => {
            if (box === currentBox) {
                handleCollisionCurrentOrNew(box);
                box.update(p);
            }
            box.show(p);
        });
    }

    function mouseReleaseCollision() {
        sortBoxes();
        boxes.forEach((box) => {
            // If box is already at the bottom don't do anything
            if (box.z === 0) return;

            let collidingBoxes = getBoxTopsBelow(box);
            // If box has no boxes below it, snap to bottom
            if (collidingBoxes.length === 0) {
                box.z = 0;
                return;
            }
            // If the box has boxes below it, snap to the highest top below
            box.z = Math.max(...collidingBoxes);
        })
    }

    // Gets the Z value of the top plane of each box directly below the target box
    function getBoxTopsBelow(targetBox) {
        let tops = [];
        boxes.forEach((box) => {
            if (targetBox === box) return;
            if (collisionCheck(targetBox, box) && box.z + box.height <= targetBox.z) {
                tops.push(box.z + box.height);
            }
        })
        return tops;

    }

    // If a box is being dragged around or added, it is placed on top of any colliding boxes
    function handleCollisionCurrentOrNew(targetBox) {
        let topZ = 0;
        boxes.forEach((box) => {
            if (targetBox === box) return;
            if (collisionCheck(targetBox, box)) {
                if (topZ < box.z + box.height) topZ = box.z + box.height
            }
        })
        targetBox.z = topZ;
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
    
    function getBoxUnderMouse() {
        let boxUnderMouse;
        let topBoxZ = 0;
        boxes.forEach((box) => {
            if (p.mouseX > box.x && p.mouseX < box.x + box.width && p.mouseY > box.y && p.mouseY < box.y + box.length) {
                if (box.z + box.height > topBoxZ) {
                    boxUnderMouse = box;
                }
            }
        })
        return boxUnderMouse;
    }

    p.mousePressed = () => {
        dragging = true;
        currentBox = getBoxUnderMouse();
        if (currentBox != null) {
            dragging = true;
            currentBox.dragging = true;
            currentBox.offsetX = currentBox.x - p.mouseX;
            currentBox.offsetY = currentBox.y - p.mouseY;
        }
    };

    p.mouseReleased = () => {
        mouseReleaseCollision();
        if (currentBox != null) {
            currentBox.dragging = false;
            dragging = false;
            currentBox = null;
        }
    };
};



window.callAddBox = () => {
    const x = parseInt(document.getElementById('x').value);
    const y = parseInt(document.getElementById('y').value);
    const width = parseInt(document.getElementById('width').value);
    const length = parseInt(document.getElementById('length').value);
    const height = parseInt(document.getElementById('height').value);
    const weight = parseInt(document.getElementById('weight').value);

    window.addBox(x, y, width, length, height, weight);
};

