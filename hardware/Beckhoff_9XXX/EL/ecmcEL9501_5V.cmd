#-d /**
#-d   \brief hardware script for EL9410 0..5V range
#-d   \details Power supply terminal with refresh of E-Bus
#-d   \author Anders Sandstroem
#-d   \file
#-d */

epicsEnvSet("ECMC_EC_HWTYPE"             "EL9501_5V")

ecmcFileExist(${ecmccfg_DIR}ecmcEL9501_XXV.cmd,1)
${SCRIPTEXEC} ${ecmccfg_DIR}ecmcEL9501_XXV.cmd

# Voltage range
# 13 = 0..20V
# 15 = 0..5V (this cfg)
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x800D,0x11,15,2)"

