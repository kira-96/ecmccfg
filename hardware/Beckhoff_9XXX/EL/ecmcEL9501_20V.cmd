#-d /**
#-d   \brief hardware script for EL9410 0..20V range
#-d   \details Power supply terminal with refresh of E-Bus
#-d   \author Anders Sandstroem
#-d   \file
#-d */

epicsEnvSet("ECMC_EC_HWTYPE"             "EL9501_20V")

ecmcFileExist(${ecmccfg_DIR}ecmcEL9501_XXV.cmd,1)
${SCRIPTEXEC} ${ecmccfg_DIR}ecmcEL9501_XXV.cmd

# Voltage range
# 13 = 0..20V (this cfg)
# 15 = 0..5V
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x800D,0x11,13,2)"

