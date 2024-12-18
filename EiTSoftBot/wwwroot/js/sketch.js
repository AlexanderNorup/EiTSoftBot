window.startP5Sketch = () => {
    new p5(sketch, window.document.getElementById('canvasContainer'));
    return true;
};

window.sketch = (p) => {
    const MirLength = 760;
    const MirWidth = 450;
    const RealWorldScale = 0.757276 / MirLength;
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
    let shiftPressed = false;

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
        handleCollisionCurrentOrNew(newBox, boxes, snapping);
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
        highlightBox = null;
        boxes = boxes.filter((box) => box.id !== id);
        mouseReleaseCollision(boxes, snapping);
        window.remove3DBox(id);
    };

    window.removeAll2DBoxes = () => {
        removeHighlight(boxes);
        highlightBox = null;
        for (let box of boxes) {
            window.remove3DBox(box.id);
        }
        boxes = [];
        currentBox = null;
        hoverBox = null;
        dragging = false;
    }

    window.removeAllBoxes = () => {
        if (shiftPressed) {
            window.do3DRemoveAnimation();
        } else {
            window.removeAll2DBoxes();
        }
    };

    window.getAll2DBoxes = () => {
        return boxes;
    };

    window.exportToString = () => {
        let exported = JSON.stringify(boxes);
        prompt("Copy and save this string", exported);
    }

    window.importFromString = () => {
        try {
            let input = prompt("Paste the string to import");
            if (input === null) {
                return;
            }
            let importBoxes = JSON.parse(input);
            mapBoxesToClasses(importBoxes);
            window.showSuccessToast("Successfully imported boxes");
        } catch (e) {
            window.showErrorToast("Failed to import boxes");
            console.error("Failed to import boxes", e);
            return;
        }
    }

    window.quickSave = () => {
        window.localStorage.setItem("quickSave", JSON.stringify(boxes));
        window.showSuccessToast("Successfully saved to browser's storage");
    }

    window.quickLoad = () => {
        let quickSaved = window.localStorage.getItem("quickSave");
        if (quickSaved === null) {
            return;
        }
        try {
            let importBoxes = JSON.parse(quickSaved);
            mapBoxesToClasses(importBoxes);
            window.showSuccessToast("Successfully loaded boxes from browser's storage");
        } catch (e) {
            window.showErrorToast("Failed to import boxes");
            console.error("Failed to import boxes", e);
            return;
        }
    }

    window.mapBoxesToClasses = (importBoxObjects) => {
        let newBoxes = [];

        for (let box of importBoxObjects) {
            newBoxes.push(new Box(null, null, null, null, null, null, box));
        }

        window.removeAllBoxes();
        boxes = newBoxes;
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
        mouseReleaseCollision(boxes, snapping);
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
        } else if (p.key === "Alt") {
            snapping = false;
        } else if (p.key == "Escape") {
            removeHighlight(boxes);
            highlightBox = null;
        } else if (p.key == "Shift") {
            shiftPressed = true;
        }
    };

    p.keyReleased = () => {
        if (p.key === "Alt") {
            changeSnapping();
        } else if (p.key == "Shift") {
            shiftPressed = false;
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

