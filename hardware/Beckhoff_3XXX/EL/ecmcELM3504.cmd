#-d /**
#-d   \brief hardware script for ELM3504
#-d   \details 4-channel analog input for bridge measurement; 24 bit, 10 ksps
#-d   Supported signal types (choose via SDO settings):
#-d   * strain gauge - internal bridge completion and supply adjustable 0…5 V:
#-d      * quarter bridge           1 kOhm + 350 Ohm + 120 Ohm, +-2/4/8/32 mV/V (2-/3-wire connection)
#-d      * half bridge              +-2/4/8/16 mV/V (3-/5-wire connection)
#-d      * full bridge              +-2/4/8/32 mV/V (4-/6-wire connection)
#-d   * Voltage:    	            +-10 V, +-80 mV (actually +-10.737V / +-85.9mV), (2-wire connection)
#-d   * Potentiometer:	            potentiometer > 1 kOhm, supply integrated and adjustable 0…5 V (3-/5-wire connection)
#-d   * Temperature (RTD):          PT1000 (2-/3-/4-wire connection)
#-d
#-d   Minimum sample time          = 100000 ns (oversampling rate of 10 in 1 kHz ec rate)
#-d   Maximum Oversampling factor  = 100       (if ec rate is 100 Hz then a NELM of 100 can be used)
#-d
#-d   \author Scott A. Stubbs
#-d   \file
#-d */

epicsEnvSet("ECMC_EC_HWTYPE"             "ELM3504")
epicsEnvSet("ECMC_EC_VENDOR_ID"          "0x2")
epicsEnvSet("ECMC_EC_PRODUCT_ID"         "0x50218d09")
epicsEnvSet("ECMC_OVER_SAMP_MAX"         "100")
epicsEnvSet("ECMC_SAMP_TIME_MIN"         "100000")

#- Call generic for ELM3504
< ${ecmccfg_DIR}ecmcELM3504-XXXX.cmd
