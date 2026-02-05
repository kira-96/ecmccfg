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
5. [Diagnostics](#Diagnostics)

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

### Diagnostics

The diagnostics buffer can be read with the `ec_diagnostic_messages.py` tool:

Example: EL7211-9014
```
python3 ec_diagnostic_messages.py -m1 -s3  

DEVICE INFORMATION:
===================

name:		EL7211-9014
master id:	1
slave id:	3
vendor id:	0x2
product id:	0x1c2b3052
host time:	2026-02-05 11:33:41.191176


DIAGNOSTIC MESSAGES:
====================
msg_no  time                        text_id  text  flags  diag_code   dynamic  
1       2000-01-01 00:00:00         0x4411         0x1    0x1c21e000  0x0      
2       2026-02-05 10:30:39.407639  0x8406         0x2    0x1c21e000  0x0      
3       2026-02-05 10:30:39.407639  0x8105         0x2    0x1c21e000  0x0    
```

Sometimes the text_id are converted to a readable message by the tool and sometimes not. In the case above we need to look for the meaning of the text_id-s on Beckhoffs website.

Searching for the slave type and error code normally gives you the information:
* 0x4411 : Warning "Drive. DC-Link undervoltage. (Warning). The DC link voltage of the terminal is lower than the parameterized minimum voltage"
* 0x8406 : Error   "Drive. DC-Link undervoltage. (Error). The DC link voltage of the terminal is lower than the parameterized minimum voltage"
* 0x8105 : Error   "General. PD-Watchdog. Communication between the fieldbus and the output stage is secured by a Watchdog."

Here we can see that the drive is missing DC-link voltage (motor power). The watchdog error probably happens during startup of the IOC and is nothing to worry about.

