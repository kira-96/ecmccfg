+++  
title = "tuning"   
weight = 16
chapter = false  
+++

### Tuning

There are normally several control loops in an ecmc motion system:
* Position loop (centralized in ecmc if CSV)
* Velocity loop (in drive)
* Current loop (in drive)

#### Position loop
The position loop control parameters can be accessed and tuned by PVs. Normally, a pure P controller is enough (ki and kp set to 0) but sometimes the I and D part can be needed for instance if the drive is running in CSP mode with ecmc position loop enabled (ecmc mode CSP_PC) or if the system has backlash.

#### Velocity and Current loop
These control loops need to be tuned in the drive.

For EL70x1, see [EL70x1 Tuning](../hardware/el70x1/#tuning)
For other drives, consult the dedicated manual.

#### EL7062
EL7062 have an autotune feature that works well. For more info see knowledge-base/hardware/el7062.

#### Backlash 
Tuning systems with backlash can be difficult. Sometimes a D-part helps to reduce spikes in the centralized ecmc position loop controller output and almost always a small I is needed in order to reach in the end. To conclude, the following is normally good: 
* Low velocity
* Small I part to integrate the backlash
* Some D-part to dampen the output mainly from integrator

If system is not possible to tune then it could be needed to run the system in open loop (with the option of using motor record retries). Note, this is not a good option for axes involved in a kinematic system.

##### Motor record backlash compensation 
The motor record backlash compensation fields can be used if needed. Basically they ensure that the system approaches always from the same direction by issueing two move commands:
1. A first move that is longer `target + BDST` or shorter `target - BDST` (depending on which dir to approach from)
2. An approach command to go to the final taeget position

* BDST: Distance for the second approach move comamnd
* BVEL: Velocity for approach move
* BACC: Acceleration for approach move

If the motion axis in an syncronized system then using the motor record backlash field is not a good approach.

