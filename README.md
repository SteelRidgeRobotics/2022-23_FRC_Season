# 2023 FRC Season
All robot code for the 2023 FIRST® Robotics Competition CHARGED UP, Presented by HAAS

This includes the following robot code:
- [Larry](Larry), our first swerve drive robot
- [Mr. Steeltastic](Mr_Steeltastic), our official robot for the season
- [Palpatine](Palpatine_2022), our simple testing robot
- and [Guitar Palpatine](theLab/Guitar_Palpatine2023), which is our first use of the guitar controller

## Important Files (for future use)
- [guitar.py](theLab/Guitar_Palpatine2023/guitar.py): The file for the Guitar Controller. See Guitar Palpatine's [drive_by_guitar.py](theLab/Guitar_Palpatine2023/commands/drive_by_guitar) and [robotcontainer.py](theLab/Guitar_Palpatine2023/robotcontainer.py) for an example.

<sub>Pickle_Face5 (Caden Dalley) takes full credit for the guitar idea   -Pickle_Face5</sub>

# Programming Convention
We use (as of 4/20/23) [Trunk Based Development](https://trunkbaseddevelopment.com/). Look at the linked website for more information.

Basically, **don't commit directly to the main branch**. Instead, create a new branch (known as a "feature branch") and commit changes into that branch. Once your project/feature is finished, submit a pull request to push it into the main branch.

To avoid Merge Pain™, *push your branch into main ASAP*. If you branch off main and make a bunch of changes over a month and try to submit a pull request, it will break ***everything***.

Try to finish feature branches in ~1 week maximum to avoid this.

## theLab
### [theLab](theLab)
As of **5/11/2023** we now have a folder for feature testing, and non-robot specific code. This includes:
- [Guitar Palpatine](theLab/Guitar_Palpatine2023): Testing with Palpatine for the GuitarHero Controller
- [Inverse Kinematics][(theLab/Inverse Kinematics)](https://github.com/SteelRidgeRobotics/2022-23_FRC_Season/tree/main/theLab/Inverse%20Kinematics): Various inverse kinematic code that we were testing for the season
- [Name_In_Progress_Magic](theLab/Name_In_Progress_Magic): The competition robot in the Magic Bot framework (not to be finished, use as reference only)
- [PID_Tuning_Code](theLab/PID_Tuning_Code): A modified version of the [PID tuning code made in the 2022 season](https://github.com/SteelRidgeRobotics/2021-2022_FRC_Season/tree/main/PID_Tuning_Code)
- [PathWeaver2023](theLab/PathWeaver2023): Path Weaver code that was started on, but did not make it Mr.Steeltastic
