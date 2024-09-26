window.startP5Sketch = () => {
    new p5(sketch, window.document.getElementById('canvasContainer'));
    return true;
};

window.sketch = (p) => {

    let boxes = [new Box(0, 0, 100, 100, 100, 100)];
    let dragging = false;
    let currentBox = null;
    let hoverBox = null;
    let bgImg = null;
    p.preload = () => {
        bgImg = p.loadImage('/models/mir_surface.png');
    }

    p.setup = () => {
        let canvas = p.createCanvas(450, 760); // MIR size: w: 4.5, h: 7.6: 
        canvas.parent("canvasContainer");
        // Call the resize function
        bgImg.resize(p.width, p.height);
    };

    p.draw = () => {
        p.image(bgImg, 0, 0);
        sortBoxes(boxes);
        drawBoxes();
    };

    window.addBox = (x, y, width, length, height, weight) => {
        let newBox = new Box(x, y, width, length, height, weight);
        boxes.push(newBox);
        handleCollisionCurrentOrNew(newBox, boxes);
        sortBoxes(boxes);
    };

    function drawBoxes() {
        if (!dragging) {
            let newHoverBox = getBoxUnderMouse(p, boxes);

            if (hoverBox !== null && (newHoverBox === undefined || newHoverBox.id !== hoverBox.id)) {
                // We are not hover�ng over the same box anymore.
                hoverBox.mouseOver = false;
                hoverBox = null;
            }

            if (newHoverBox !== undefined) {
                // We are hovering over a box
                hoverBox = newHoverBox;
                hoverBox.mouseOver = true;
            }
        }
        boxes.forEach((box) => {
            if (box === currentBox) {
                handleCollisionCurrentOrNew(box, boxes);
                box.update(p);
            }
            box.show(p);
        });
    }

    window.highlight2DBox = (id) => {
        if (typeof id === "string") {
            let box = boxes.find((box) => {
                return box.id === id;
            })
            box.highlight = true;
        } else {
            let box = id;
            box.highlight = true;
        }
    };

    window.remove2DBox = (id) => {
        removeHighlight(boxes);
        boxes = boxes.filter((box) => box.id !== id);
        mouseReleaseCollision(boxes);
        window.remove3DBox(id);
    };

    p.mousePressed = (event) => {
        if (event.which === 1) {
            dragging = true;
            currentBox = getBoxUnderMouse(p, boxes);
            if (currentBox != null) {
                removeHighlight(boxes);
                dragging = true;
                currentBox.dragging = true;
                currentBox.offsetX = currentBox.x - p.mouseX;
                currentBox.offsetY = currentBox.y - p.mouseY;
            }
        } else if (event.which === 2) {
            let toRemove = getBoxUnderMouse(p, boxes);
            if (toRemove != null) {
                window.remove2DBox(toRemove.id);
            }
        }
    };

    p.mouseReleased = () => {
        mouseReleaseCollision(boxes);
        if (currentBox != null) {
            currentBox.dragging = false;
            currentBox = null;
        }
        dragging = false;
    };

    p.keyPressed = () => {
        if (p.key === "Delete") {
            let boxesToDelete = boxes.filter(box => box.highlight);
            for (var box of boxesToDelete) {
                window.remove2DBox(box.id);
            }
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

