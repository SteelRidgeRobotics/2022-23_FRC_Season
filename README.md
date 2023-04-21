# 2023 FRC Season
All robot code for the 2023 FIRST® Robotics Competition CHARGED UP, Presented by HAAS

This includes the following robot code:
- [Larry](Larry), our first swerve drive robot
- [Mr. Steeltastic](Mr_Steeltastic), our official robot for the season
- [Palpatine](Palpatine_2022), our simple testing robot
- and [Guitar Palpatine](Guitar_Palpatine2023), which is our first use of the guitar controller

## Important Files (for future use)
- [guitar.py](Guitar_Palpatine2023/guitar.py): The file for the Guitar Controller. See Guitar Palpatine's [drive_by_guitar.py](Guitar_Palpatine2023/commands/drive_by_guitar) and [robotcontainer.py](Guitar_Palpatine2023/robotcontainer.py) for an example.

<sub>Pickle_Face5 (Caden Dalley) takes full credit for the guitar idea   -Pickle_Face5</sub>

# Programming Convention
We use (as of 4/20/23) [Trunk Based Development](https://trunkbaseddevelopment.com/). Look at the linked website for more information.

Basically, **don't commit directly to the main branch**. Instead, create a new branch (known as a "feature branch") and commit changes into that branch. Once your project/feature is finished, submit a pull request to push it into the main branch.

To avoid Merge Pain™, *push your branch into main ASAP*. If you branch off main and make a bunch of changes over a month and try to submit a pull request, it will break ***everything***.

Try to finish feature branches in ~1 week maximum to avoid this.
