# Dancing Robot Menagerie

This document will explain step-by-step the process for obtaining data from the OptiTrack system and using the provided python code library to generate a dancing robot menagerie. The two types of robot simulations currently included are the Rollbot and the Broombot

## Step 1: Record Data using the OptiTrack System

### Setting up the computer
1. The computer you will be using is the one by the wall of the lab
2. Make sure the Netgear box power cord is plugged in
3. Make sure the Ethernet cord from the Netgear box is plugged into the computer
4. Make sure the the USB License Key is plugged into the computer. The USB stick will be either already plugged in, beside the computer, or in the Motion Capture equipment box
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

### Creating the Skeleton (This section needs to be fleshed out)
1. Put the motion capture suit on the person who will be performing the motion and have him/her stand in the center of the space
3. Choose your skeleton and make sure that the number of markers on the skeleton is the same number of markers on the person in the suit
4. Place the markers on the person in the same locations as the image in Motive
5. Have to do something here with the person in the T position
6. Save the skeleton data (skel file?)

### Recording a Take (This section needs to be fleshed out)
1. Something here

### Exporting the Data (This section needs to be fleshed out)
1. `File -> Export`
2. Export the CSV file format with global coordinates and rotation set to XYZ
3. Check the CSV file output to make sure that there are no blank columns or unlabeled markers (which you can just manually delete from the CSV or go into Motive to fix)
4. Make sure you save all files (calibration, skeleton, take, csv, etc.) to your working directory before closing Motive
5. Unplug the Netgear power cord after you are done using the motion capture system and make sure all markers, suits, etc. are properly put away in the motion capture equipment box

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

### Overview of the files included in the library
1. `main.py` is the file you will run to generate the simulation
2. `options.py` should be the only file you need to modify and contains all the file import, appearance of the movers, and the types of motions for the movers (included in `main.py`)
3. `analyze_human_data.py` is the file that processes the Motive csv (called by `main.py`)
4. `animate.py` is the file that actually generates the animation (called by `main.py`)

### Options
1. Mocap File Options
 - Start and ending index of the points used from the specified csv file

2. Animation Options
 - Whether or not to show the animation

3. Video Options
 - Whether to save the video, title on the video, filename of the video, and frames per second (fps) of the video
 - Note that the current code is resampling the data to half the number of desired points and then creating the video with half the frames per second of the original data capture to lower the time to create a video

4. Angle Plot Options
 - Whether to plot the angles and the title of that plot

5. List of Movers
 - `mover_specs` is a list with each element a list containing:
 	- mover type: human, rollbot, or broombot
 	- position: numpy array with x,y,z offset of the mover
 	- motion type: array with motion type (angle or random) as the first element and motion source (i.e. shoulder_hand_right) as a second element

6. FFMPEG Path
 - Make sure you change the value of this to the path to your `ffmpeg.exe` installation file
```python
ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg'
```

### Other Variables in Options
1. `file_info` contains all the info specified above to be used in other files
2. `environ_opt` controls how the plot looks in the simulation (elevation, azimuth, etc.)
3. `color_key` contains colors used for plotting
4. `paths` contains the indices of nodes to be connected in the human motion capture skeleton plot and which color in `color key` they will be plotted in
5. `geometry specs` contains properties controlling the appearance of the robots such as height and radius

### Running the Simulation
Simply run the file `main.py` to create the simulation