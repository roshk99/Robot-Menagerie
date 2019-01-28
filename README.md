# Dancing Robot Menagerie

This document will explain step-by-step the process for obtaining data from the OptiTrack system and using the provided python code library to generate a dancing robot menagerie. The type of robot available for plotting is the Broombot

## Step 1: Record Data using the OptiTrack System in RAD Lab

### Setting up the computer
1. The computer you will be using is the one by the wall of the lab
2. Make sure the Netgear box power cord is plugged in
3. Make sure the Ethernet cord from the Netgear box is plugged into the computer
4. Make sure the the USB License Key is plugged into the computer. The USB stick will be in the Motion Capture Box inside a yellow envelope
5. Make sure the USB cord from the Netgear is plugged into the computer
6. Open the Motive Software on the computer

### Calibration
1. Open `File -> New Project` in Motive
2. Set the working directory to a folder named with your name and the date
3. Open `Layout -> Calibrate`
4. Mask visible markers for each camera after you have cleared everything from the space
5. Click `Start Wanding`
6. Take the motion capture wand and wave it around the entire capture space (don't forget to go high and low!) until you have about 2000 points for each camera
7. Click `Calculate`
8. Click `Apply`

### Setting the Ground Plane
1. Make sure the wand is away from the space
2. Set the L-shaped piece in the center of the capture space preferably with the edges lined up with the tiles on the floor. The long side is z and the short side is x
3. Set the vertical offset to 19mm
4. Click `Calibrate`
5. Save the calibration resutls in the working directory

### Creating the Skeleton
1. Open the skeleton pane to view the markerset. Select the Baseline Markerset.
2. Have the person who will be performing the motion put on the motion capture suit.
3. Place the markesr on the person in the same locations as the image in Motive. Make sure you rotate the skeleton to ensure you have all the markers.
4. Have the person stand in the T-position in the center of the space and click `Create`
5. Save the skeleton data

### Recording a Take
1. Click the record button at the bottom of the screen to record.
2. Press the same button when done recording.
3. You can record as many takes as you like. They will appear on the left side labelled with a time-code.

### Exporting the Data
1. `File -> Export`
2. Export the CSV file format with global coordinates and rotation set to XYZ. You do not need the Rigid Bodies and Rigid Body Markers selected, but make sure Markers is selected.
3. Export as a BVH file
4. Make sure you save all files (calibration, skeleton, take, csv, etc.) to your working directory before closing Motive
5. Unplug the Netgear power cord after you are done using the motion capture system and make sure all markers, suits, etc. are properly put away in the motion capture equipment box. Also make sure the USB key is put back in the yellow envelope which goes inside the motion capture equipment box.

## Step 2: Generating the Simulation 

### Requirements
1. Python 3 <https://www.python.org/downloads/>
2. Pip <https://pypi.org/project/pip/>
 - This should work `python -m pip install -U pip`
3. Numpy and Matplotlib <https://scipy.org/install.html>
 - This should work `python -m pip install --user numpy matplotlib`
4. FFMPEG to save the video
 - How to for Windows: <http://adaptivesamples.com/how-to-install-ffmpeg-on-windows/>
 - FFMPEG site: <https://ffmpeg.zeranoe.com/builds/>
5. An environment to run python (Sublime <https://www.sublimetext.com/3> is nice)

### Step 1: Motion Capture Data Computations (Only need to complete once per csv file if you are not adding any more vectors to compute!)
1. `human_data_import.py` is the file you should run. This calls the file `analyze_human_data.py`.
2. Modify the `filename` field to include the csv file from Motive, which you should move to the same folder as the repository.
3. Modify the `data_filename` field to whatever you want the `npz` file containing the computed motion capture data to be called.
4. The `dim_transfer` field adjusts the xyz coordinates to match the convention of the z-direction pointing up.
5. The next section includes a list of vectors with the start and end points as the first and second elements. If you wish to add another vector to compute, add it here and make sure you add it to the end of `vectors`
6. You should be able to run `human_data_import.py` now. It will take a little while and will print out a message when completed. The data will be saved in a `.npz` file in the same directory.

### Step 2: Video Generation
1. `main.py` is the file you want to run.
2. Uncomment the section (Single Video Generation or Multiple Video Generation based on what you want to do)
3. The vectors at the top should match the vectors from `human_data_import.py` and are the options you can use for the movers below.
4. You can add/change the list of positions, which are the options you can use for the movers below.
5. File Options:
	* `start_ind` and `end_ind` are the portions of motion capture you wish to use
	* `filename` should match the `.npz` file you saved from Step 1
	* `paths` controls what points are connected in the skeleton
6. Video Options:
	* `video_filename` is the name of the `.mp4` video you want to create
	* `video_flag` is True if you want to create a video
	* `img_flag` is True if you want to save each frame as an image
	* `video_fps` is the frames per second of the video. 120fps is what Motive uses
	* `ffmpeg_path` should be the path to `ffmpeg.exe` on your computer with an extra `\ffmpeg` added
	* `elevation` and `azimuth` are the perspective of the video in degrees. 15 and -180 are recommended
	* `plane_start`, `plane_end`, and `height_max` control the ground plane and z-axis limits. -5, 5, and 5 are recommended
	* `color_key` must have at least 2 elements and contains the colors scheme for the movers
7. Mover Options:
	* You should include the movers here. The format for each mover type is:
		* `{'type': 'human', 'pos': mid_pos}`
		* `{'type': 'broombot', 'pos': left_pos, 'vector': vectors[ind2], 'radius': 0.25, 'height': 0.5, 'n': 10}`
	* Make sure all movers you want to plot are put into the list `mover_opt`
8. Multiple Video Generation
	* There are three different for-loops here for generating videos with different motion capture segments, left-movers, and right-movers. Feel free to customize as you like.

### Running the Simulation
Simply run the file `main.py` to create the simulation