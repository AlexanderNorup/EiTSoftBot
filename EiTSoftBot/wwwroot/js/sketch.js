window.startP5Sketch = () => {
    new p5(sketch, window.document.getElementById('canvasContainer'));
    return true;
};

window.sketch = (p) => {
    const MirLength = 760;
    const MirWidth = 450;
    const RealWorldScale = 0.89 / MirLength;
    const selectedBoxPropertyEditContainer = document.getElementById('selectedBoxEditContainer');
    const selectedBoxWeightInput = document.getElementById('selectedWeightInput');

    selectedBoxWeightInput.addEventListener("change", () => {
        if (highlightBox != null) {
            highlightBox.weight = parseFloat(selectedBoxWeightInput.value);
        }
    })

    window.getRealWorldScale = () => {
        return RealWorldScale;
    };

    let boxes = [];
    let dragging = false;
    let currentBox = null;
    let hoverBox = null;
    let bgImg = null;
    let highlightBox = null;
    let snapping = true;
    let snappingFactor = 50;

    window.changeSnapping = () => {
        snapping = document.getElementById('snapping').checked;
    };

    window.changeSnappingFactor = () => {
        snappingFactor = parseInt(document.getElementById('snappingFactor').value);
    };

    p.preload = () => {
        bgImg = p.loadImage('/models/mir_surface.png');
    }

    p.setup = () => {
        let canvas = p.createCanvas(MirWidth, MirLength); // MIR size: w: 4.5, h: 7.6: 
        canvas.parent("canvasContainer");
        // Call the resize function
        bgImg.resize(p.width, p.height);

        window.addBox(0, 0, 0.1, 0.1, 0.1, 1); // Add default small box
    };

    p.draw = () => {
        p.image(bgImg, 0, 0);
        sortBoxes(boxes);
        drawBoxes();

        if (highlightBox != null) {
            selectedBoxPropertyEditContainer.style.display = "block";
        } else {
            selectedBoxPropertyEditContainer.style.display = "none";
        }
    };

    window.addBox = (x, y, width, length, height, weight) => {
        let newBox = new Box(x / RealWorldScale, y / RealWorldScale, width / RealWorldScale, length / RealWorldScale, height / RealWorldScale, weight);
        boxes.push(newBox);
        handleCollisionCurrentOrNew(newBox, boxes, false);
        sortBoxes(boxes);
    };

    function drawBoxes() {
        if (!dragging) {
            let newHoverBox = getBoxUnderMouse(p, boxes);

            if (hoverBox !== null && (newHoverBox === undefined || newHoverBox.id !== hoverBox.id)) {
                // We are not hoveríng over the same box anymore.
                hoverBox.mouseOver = false;
                hoverBox = null;
            }

            if (newHoverBox !== undefined) {
                // We are hovering over a box
                hoverBox = newHoverBox;
                hoverBox.mouseOver = true;
            }
        }
        window.before3DUpdate();
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
        removeHighlight(boxes);
        if (typeof id === "string") {
            let box = boxes.find((box) => {
                return box.id === id;
            })
            box.highlight = true;
            highlightBox = box;
            selectedBoxWeightInput.value = box.weight;
        } else {
            let box = id;
            box.highlight = true;
            highlightBox = box;
            selectedBoxWeightInput.value = box.weight;
        }
    };

    window.remove2DBox = (id) => {
        removeHighlight(boxes);
        boxes = boxes.filter((box) => box.id !== id);
        mouseReleaseCollision(boxes);
        window.remove3DBox(id);
    };

    window.removeAll2DBoxes = () => {
        removeHighlight(boxes);
        for (let box of boxes) {
            window.remove3DBox(box.id);
        }
        boxes = [];
        currentBox = null;
        hoverBox = null;
        dragging = false;
    }

    window.getAll2DBoxes = () => {
        return boxes;
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
            // Middlemouse
            let toRemove = getBoxUnderMouse(p, boxes);
            if (toRemove != null) {
                window.remove2DBox(toRemove.id);
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
            window.highlight2DBox(currentBox);
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
        if (p.key === "Alt") {
            snapping = false;
        }
        if (p.key == "Escape") {
            removeHighlight(boxes);
            highlightBox = null;
        }
    };

    p.keyReleased = () => {
        if (p.key === "Alt") {
            changeSnapping();
        }
    }
};

window.callAddBox = () => {
    const x = parseFloat(document.getElementById('x').value);
    const y = parseFloat(document.getElementById('y').value);
    const width = parseFloat(document.getElementById('width').value);
    const length = parseFloat(document.getElementById('length').value);
    const height = parseFloat(document.getElementById('height').value);
    const weight = parseFloat(document.getElementById('weight').value);

    window.addBox(x, y, width, length, height, weight);
};

