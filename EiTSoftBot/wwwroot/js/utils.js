/**
 * @param {Box[]} bs
 */
function mouseReleaseCollision(bs, snapping) {
    sortBoxes(bs);
    bs.forEach((box) => {
        // If box is already at the bottom don't do anything
        if (box.z === 0) return;

        let collidingBoxes = getBoxTopsBelow(box, bs, snapping);
        // If box has no boxes below it, snap to bottom
        if (collidingBoxes.length === 0) {
            box.z = 0;
            return;
        }
        // If the box has boxes below it, snap to the highest top below
        box.z = Math.max(...collidingBoxes);
    })
}

/**
 * If a box is being dragged around or added, it is placed on top of any colliding boxes
 * @param {Box} targetBox
 * @param {Box[]} bs
 * @param {boolean} snapping
 */
function handleCollisionCurrentOrNew(targetBox, bs, snapping) {
    let topZ = 0;
    bs.forEach((box) => {
        if (targetBox === box) return;
        if (snapping) {
            if (collisionCheckSnap(targetBox, box)) {
                if (topZ < box.z + box.height) topZ = box.z + box.height
            }
        } else {
            if (collisionCheck(targetBox, box)) {
                if (topZ < box.z + box.height) topZ = box.z + box.height
            }
        }
    })
    targetBox.z = topZ;
}

/**
 * @param {Box} boxA
 * @param {Box} boxB
 * @returns {boolean}
 */
function collisionCheck(boxA, boxB) {
    return boxA.x + boxA.width > boxB.x && // A right edge past B left
        boxA.x < boxB.x + boxB.width && // A left edge past B right
        boxA.y + boxA.length > boxB.y && // A bottom edge past B top
        boxA.y < boxB.y + boxB.length;

}

/** Check collision between boxA's snap position, to boxB's position
 * @param {Box} boxA
 * @param {Box} boxB
 * @returns {boolean}
 */
function collisionCheckSnap(boxA, boxB) {
    return boxA.snapX + boxA.width > boxB.x && // A right edge past B left
        boxA.snapX < boxB.x + boxB.width && // A left edge past B right
        boxA.snapY + boxA.length > boxB.y && // A bottom edge past B top
        boxA.snapY < boxB.y + boxB.length;
}

/**
 * @param {Box[]} bs
 */
function sortBoxes(bs) {
    bs.sort((a, b) => a.z > b.z ? 1 : -1)
}

/**
 * @param {*} p
 * @param {Box[]} bs
 * @returns {Box}
 */
function getBoxUnderMouse(p, bs) {
    let boxUnderMouse;
    let topBoxZ = 0;
    bs.forEach((box) => {
        if (p.mouseX > box.x && p.mouseX < box.x + box.width && p.mouseY > box.y && p.mouseY < box.y + box.length) {
            if (box.z + box.height > topBoxZ) {
                boxUnderMouse = box;
            }
        }
    })
    return boxUnderMouse;
}

/**
 * @param {Box[]} boxes
 */
function removeHighlight(boxes) {
    for (let box of boxes) {
        box.highlight = false;
    }
}

/**
 * Gets the Z value of the top plane of each box directly below the target box
 * @param {Box} targetBox
 * @param {Box[]} bs
 * @param {boolean} snapping
 * @returns {number[]}
 */
function getBoxTopsBelow(targetBox, bs, snapping) {
    let tops = [];
    bs.forEach((box) => {
        if (targetBox === box) return;
        if (snapping) {
            if (collisionCheckSnap(targetBox, box) && box.z + box.height <= targetBox.z) {
                tops.push(box.z + box.height);
            }
        } else {
            if (collisionCheck(targetBox, box) && box.z + box.height <= targetBox.z) {
                tops.push(box.z + box.height);
            }
        }
    })
    return tops;
}