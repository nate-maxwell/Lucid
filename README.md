# Lucid Games Asset Pipeline
A video games asset pipeline I'm building and log the development of.

This is strictly for a YouTube vlog that can be found [here](https://youtube.com/playlist?list=PLdFnThjjgy9YIXYQMJhJgwgGUCxSubICY&si=ObTBWf73c1Oh7gMY),
although the repo may be ahead of the recordings.

## Installation
It is still very early days for this repo so getting the project up and running isn't
the easiest at the moment.


### Step 1 - Python Setup:
Download repo, create a python 3.9 venv, and pip install the following:
- pymel 1.4.0
- PySide2 5.1.52.1
- shiboken2 5.15.2.1


### Step 2 - Manual Shortcut Setup:
Copy the shortcut located at lucid/launcher/Lucid Launcher.lnk to wherever you wish the shortcut to live.
Afterward you will need to point the shortcut target to <repo_location>/lucid/launcher/lucid_launcher.bat


### Step 3 - Pipeline Settings:
Run the shortcut starting the launcher and start the Pipeline Settings menu. At minimum, you will need to
fill in the Maya + Unreal paths with the location of your program .exe files.

Next you will need to choose a location in the Project Path section at the bottom. This will be where all
projects, configs, assets, animations, etc. are stored.

Lastly if you are working with a team, you will need to fill out the Network and Install Directories settings.

If your team is working with a common network drive, choose Common Network, otherwise choose Local Networks.

If your team has imaged machines, or identical program install directories, choose Consistent, otherwise choose
Inconsistent.


### Step 4 - Project Creation
Next you will need to make a project for the pipeline to start checking for. From the launcher click the
Project Manager button, then click New Project at the bottom. Fill out the project code and you should be
all set!

From here you can adjust any additional settings, although not all of them are read within the pipeline yet (as
I said, its still early days).


### Step 5 - Unreal
Lastly, drop the unreal plugin, found within the Lucid project, into the plugins folder of your unreal project and
you should be good to go.
