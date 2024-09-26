window.startP5Sketch = () => {
    new p5(sketch, window.document.getElementById('canvasContainer'));
    return true;
};

window.sketch = (p) => {

    let boxes = [new Box(0, 0, 100, 100, 100, 100)];
    let dragging = false;
    let currentBox = null;
    let hoverBox = null;
    let highlightBox = null;
    let snapping = true;
    let snappingFactor = 50;
    
    window.changeSnapping = () => {
        snapping = document.getElementById('snapping').checked;
    };
    
    window.changeSnappingFactor = () => {
        snappingFactor = parseInt(document.getElementById('snappingFactor').value);
    };

    p.setup = () => {
        let canvas = p.createCanvas(450, 760); // MIR size: w: 4.5, h: 7.6: 
        canvas.parent("canvasContainer");
    };

    p.draw = () => {
        p.background(220);
        sortBoxes(boxes);
        drawBoxes(boxes, hoverBox, currentBox, p);
    };

    window.addBox = (x, y, width, length, height, weight) => {
        let newBox = new Box(x, y, width, length, height, weight);
        boxes.push(newBox);
        handleCollisionCurrentOrNew(newBox, boxes, false);
        sortBoxes(boxes);
    };
    
    function drawBoxes() {
        if (!dragging) {
            let newHoverBox = getBoxUnderMouse(p, boxes);
            if (newHoverBox == null && highlightBox != null) {
                highlightBox.mouseOver = false;
                highlightBox = null;
            }
            else if (newHoverBox != null && highlightBox != null) {
                highlightBox.mouseOver = false;
                highlightBox = newHoverBox;
                highlightBox.mouseOver = true;
            } else if (newHoverBox != null && highlightBox == null) {
                highlightBox = newHoverBox;
                highlightBox.mouseOver = true;
            }
        }
        boxes.forEach((box) => {
            if (box === currentBox) {
                handleCollisionCurrentOrNew(box, boxes, snapping);
                box.update(p);
                if (snapping) {
                    box.showSnap(p, snappingFactor);
                }
            }
            box.show(p);
        });
    }
    
    window.highlight2DBox = (id) => {
        if (highlightBox != null) {
            highlightBox.highlight = false;
            highlightBox = null;
        }

        boxes.forEach((box) => {
            if (box.id === id) {
                highlightBox = box;
                highlightBox.highlight = true;
            }
        })
    };

    

    p.mousePressed = (event) => {
        if (event.which === 1) {
            dragging = true;
            currentBox = getBoxUnderMouse(p, boxes);
            if (currentBox != null) {
                highlightBox = removeHighlight(highlightBox);
                dragging = true;
                currentBox.dragging = true;
                currentBox.offsetX = currentBox.x - p.mouseX;
                currentBox.offsetY = currentBox.y - p.mouseY;
            }
        } else if (event.which === 2) {
            let toRemove = getBoxUnderMouse(p, boxes);
            if (toRemove != null) {
                highlightBox = removeHighlight(highlightBox);
                boxes.splice(boxes.indexOf(toRemove), 1);
                window.remove3DBox(toRemove.id);
            }
        }
    };

    p.mouseReleased = () => {
        if (snapping && currentBox != null) {
            currentBox.x = currentBox.snapX;
            currentBox.y = currentBox.snapY;
        }
        
        mouseReleaseCollision(boxes);
        if (currentBox != null) {
            currentBox.dragging = false;
            currentBox = null;
        }
        dragging = false;
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

