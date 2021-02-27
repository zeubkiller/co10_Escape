```text
 ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ ▄▄   ▄▄    ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄   ▄▄ 
█       █  █ █  █       █  █ █  █  █       █       █      █  █▄█  █
█    ▄  █  █ █  █    ▄  █  █ █  █  █▄     ▄█    ▄▄▄█  ▄   █       █
█   █▄█ █  █▄█  █   █▄█ █  █▄█  █    █   █ █   █▄▄▄█ █▄█  █       █
█    ▄▄▄█       █    ▄▄▄█       █    █   █ █    ▄▄▄█      █       █
█   █   █       █   █   █       █    █   █ █   █▄▄▄█  ▄   █ ██▄██ █
█▄▄▄█   █▄▄▄▄▄▄▄█▄▄▄█   █▄▄▄▄▄▄▄█    █▄▄▄█ █▄▄▄▄▄▄▄█▄█ █▄▄█▄█   █▄█
```

The mission (if you are playing as BLUFOR)
In this mission you and your squad was send out to scout the military CSAT and AAF presence on Altis in preparation for 
an NATO invasion. But your squad got captured by AAF and you are now held in an improvised prison awaiting CSAT officers 
to arrife for questioning. But NATO loyal insurgent managed to hide a backpack with weapons in the prison. Your task is 
now to overwhelm the guards, escape the prison, find a map of the island, make contact with NATO forces, reach the 
designated evacuation zone and escape Altis!

The mission is fully dynamic. Every playthrough will be different. Also the mission is quite hard to beat completly. 
You will most likely fail at the first try. But the mission is meant to be played more than once 
(infact our squad plays it serveral times the week).

# Get started
Set-up your local
- Clone the repo with git
- Find the `cpbo.exe` and put it in the root
    - You can find it here https://www.armaholic.com/page.php?id=411
- Go in `Code`
- Clone the Revive project https://github.com/zeubkiller/Revive
- Run my_compile.py
- Find your Arma3 editor `missionmp` folder (Most of the time in `C:\Users\YourName\Documents\Arma 3\mpmissions`)
- Create a harlink to one of the mission folder found in `Build/Mission`
```bash
mklink /J MissionFolderName Path/To/Mission/Folder/In/Build
```
- After every change if you want to test it, run `python my_compile.py` to generate the mission file in `Build`


# About the mission
Escape for Arma3 is developped by NeoArmageddon and Scruffy.
Original mod can be found here: https://github.com/NeoArmageddon/co10_Escape/tree/master

Escape was first devloped by Engima of Östgöta Ops for ArmA2. 
At that time me (NeoArmageddon) and Scruffy ported the mission to different islands and began customizing the mission.
When ArmA3 was released, Vormulac and HyperZ made the effort to port the mission over to ArmA3. From that point on Scruffy and me improved and fixed the mission to the current state.
Most of the scripts are replaced and were updated to A3 standards (but there is still some more room for improvements).


## Credits
Original Mission (Arma2) by Engima of Östgöta Ops.
Mission ported to Arma3 by Vormulac and HyperZ.
Continue devlopment by NeoArmageddon and Scruffy.
Island ports and unit configs by Scruffy.
Additional scripting and fixing by abelian, dystopian1, FrozenLiquidity, Cyprus, DPM
Magrepack by outlawled

Additional ports and configs by 
SurvivorOfZeds (IFA3+LEN)
Nils5940 (IFA3)
CRCError1970 (Malden and Kolgujev)
supercereal4 (Malden 2035)


Testing: Maikeks, Darcy, Memphis Belle, Aurelia, Freshman, Roy and many more.

The official co10 Escape mission for Arma3 is currently developed and maintained by NeoArmageddon and Scruffy.


## License
This mission is released under the APL-SA license.

## Modification
When you release a modified version of this mission, please make sure to change the line #define RELEASE "something" in include/defines.hpp to your user/clan/squadname. This makes collecting feedback and issues for me much easier.

## Feedback
Please post bugs and feedback in our Gitlab
