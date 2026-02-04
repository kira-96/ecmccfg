+++  
title = "EL72xx"   
weight = 23
chapter = false  
+++

## Topics
1. [error/warning](#error/warning)
2. [Tuning](#Tuning)
3. [Electrical installation Issues](#Electrical-installation-Issues)
4. [OCT cable failure](#OCT-cable-failure)

### error/warning
If the drive is in error/warning state and not possible to enable:
* Missing power supply
* STO tripped
* Defect cable
* Wrong/messy cabling between connector and actual terminal.
* Phases connected in wrong order resulting in commutation failure

### Tuning

{{% notice warning %}}
** Always be prepared to "KILL" or estop the axes while performing tuning**
{{% /notice %}}

* Make sure scaling factors are correct. Test by setting ecmc position controller parameters to 0 and perform a move. This move will basically be an open loop positioning. Normally the actual and setpoint still track very well during the move; if not, then scaling of drive or encoder is most likely wrong. Check gear ratios.
* For most applications the default values for the current loop and velocity loop is good.
* For slow motion, running slow, accurate and smooth, it could be beneficial to reduce velocity Kp and Ti in the drive.

### Electrical installation Issues
Strange issues have occurred if the OCT cable shielding is not kept intact until close to the terminal. Issues were identified when the individual wires were mixed randomly in cable management trays inside a control cabinet (with OCT connector on outside, then going to terminals, then single wires to EL72xx). This is not a good concept. Keep shielding of encoder and motor cables also inside the crate. 
The diagnostic buffer of EL72xx showed encoder related error messages.


### OCT cable failure
Once identified defect OCT cable. Symptoms were frequent disabling of the drive, going to fault state.
