class Mission {
    id;
    name;
    /**
     * @type {Waypoint[]}
     */
    waypoints = [];
    constructor(data = null){
        if(data !== null){
            Object.assign(this, data);
            this.waypoints = [];
            for (let waypoint of data.waypoints){
                this.waypoints.push(new Waypoint(waypoint));
            }
        }
    }
}