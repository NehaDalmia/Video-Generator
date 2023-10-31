# Video Generator

## Setup 

Here are the setup instructions for deploying Video Generator on a remote server. 

### Install TDW
The instructions to install TDW for servers can be found in [its installation guide](https://github.com/threedworld-mit/tdw/blob/master/Documentation/lessons/setup/server.md#install-tdw). Video Generator requires the TDW build to be present in a separte directory called `tdw_build`. The directory structure will be as follows: 

```
~  
├── tdw_build/
│   └── TDW/
│       └── TDW.x86_64
└── Video Generator
```
`TDW.x86_64` accepts a connection from a program using TDW and performs its various functionalities. 

### Install Video Generator 
Video generator can be cloned from this repository. Once cloned, you need to install all the requirements present by running the following from the `Video Generator` directory. 
```
pip3 install -r requirements.txt
```

### Run Video Generator 

Once all requirements have been installed and the TDW build is in place, Video Generator can be run. From the `Video Generator` directory simply do 
```
python3 app.py
``` 
In the current flask application, it has been configured to run on `localhost:5000` but this can be changed to your desired IP address and port depending on the server. Requests can now be sent to `localhost:5000` to interact with the Video Generator server. 

All the features and the User Interface of Video Generator have been discussed in this video. 

## Debugging Guide
In order to debug any issues arising in the setup or in the working, it is import to understand the flow of execution of Video Generator. Then we will discuss the possible issues that can arise. 
 
### General Workflow 
Once the user requests a video to be made several steps are triggered. 

  1. <b>Starting the TDW instance : </b> This is done to remove the starting of the TDW port from the hands of the user and because certain flags are required to be passed to make it run for the video generation logic. Once the TDW build is running and capable of accepting a connection, we store the PID of this process so that it can be terminated later when needed. 

  2. <b>Parsing the JSON and creating the simulation configurations : </b> Based on the input json which has already been verified in the front end a json which contains data for 125 frames is generated. Each frame contains information regarding the position and velocity of all the involved objects. This is generated using pybullet which uses a physics engine to manage the motion,materials etc of the objects. This code is present in `utils/pybullet_simulation.py`


  3. <b> Generating the frames and the video from the frame configurations : </b> Here , using TDW each frame is generated . These individual frames are processed and combined into a video using `ffmpeg`. This code is present in `util/recreate.py`. 


  4. <b>Uploading the video on a cloud server : </b> The temporary video in the static folder is uploaded on `ImageKit.io` , a free media storage platform and a url for this is generated. This url is the response sent back to the client side.


  5. <b> Clean up : </b> All temporary files or media generated in the `static` folder are deleted.  The TDW build is terminated using the PID generated earlier, if needed. 

### Common Issues

- _Missing requirements_ : install any missing requiremnts separately using `pip`.
- _Unable to connect to TDW build_ : This can happen if the TDW build is not placed correctly as explained in the installation guide or if multiple instanced of the build are present and the wrong one is being contacted for the generation. 
- _Unable to upload the video_ : By default, the code contains dummy `ImageKit.io` credentials, which are the `PUBLIC_KEY`, `PRIVATE_KEY` and the `URL`.   
- _Unable to generate videos after an initial generation_ : This can happen when due to some reason the TDW build was not terminated properly. Removing the TDW running instance using `kill` should resolve this issue.   
