# Mujoco Simulation

This simulation uses [Mujoco](https://mujoco.org/) to simulate the box-configurations it recieves from the Web-UI and maximises speed and acceleration.

## Getting started

Before building and running the simulation, change the MQTT config in `data_transciever.py` (lines 14-21) to match your MQTT broker.

The simulation can be visualized by setting the `VISUALIZE` environment variable to either `true` or `false` (Defaults to `false`)

### Using Docker (Recommended)

1. Have Docker installed
2. Build the Docker image: `docker build -t mujoco -f Dockerfile .`
    - The `deps` target is prebuilt here: `registry.gitlab.sdu.dk/alnoe20/docker-images/mujoco-deps:v1`. Speed up building using the `--from` flag.
3. Run the image and set the `MQTT_PASSWORD` environment vairable to be your MQTT password: `docker run -e "MQTT_PASSWORD=<password here>" mujoco`.

If you want to develop, there is a devcontainer provided. Use Visual Studio Code with the "Dev Containers" plugin: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

Then open the `/mujocoSimulation` folder in VSCode and run the "Dev Containers: Reopen in container" command. If you change the `deps` Docker taget, reconfigure `.devcontainer/devcontainer.json` to use the `build` block instead of the provided `image`. This will spawn you in a VSCode environment ready for running the simulation.

### Without Docker

1. Ensure the following packages are installed on your system:
  - `gcc g++ gfortran libopenblas-dev liblapack-dev pkg-config 
    build-essential checkinstall zlib1g-dev libssl-dev cmake 
    ffmpeg libsm6 libxext6` (These are all packages in Debian APT. If you're using a non-debian OS you can figure it our yourself.)
2. Use Python <= 3.11
3. Install dependencies from `requirements.txt` using `pip -r requirements.txt`
4. Run the code using `python data_transciever.py`
