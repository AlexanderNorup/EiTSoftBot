class Waypoint {
    id;
    name;
    /**
     * @type {Number}
     */
    x;
    /**
     * @type {Number}
     */
    y;
    /**
     * @type {Number}
     */
    rotation;
    /**
     * @type {Number}
     */
    speed;
    constructor(data = null){
        if(data !== null){
            Object.assign(this, data);
        }
    }
}