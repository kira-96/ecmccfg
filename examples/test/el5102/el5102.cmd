require ecmccfg v11.0.3_RC1 "ENG_MODE=1,ECMC_VER=sandst_a"

${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd,       "SLAVE_ID=3, HW_DESC=EL5102"
epicsEnvSet(ENC_SID,${ECMC_EC_SLAVE_NUM})

# EL7047    1Ch Stepper
${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd,       "SLAVE_ID=2,HW_DESC=EL7047"
${SCRIPTEXEC} ${ecmccfg_DIR}applyComponent.cmd  "COMP=Motor-Generic-2Phase-Stepper, MACROS='I_MAX_MA=1000, I_STDBY_MA=200, U_NOM_MV=48000, R_COIL_MOHM=1230,L_COIL_UH=2000'"
epicsEnvSet(DRV_SID,${ECMC_EC_SLAVE_NUM})

${SCRIPTEXEC} ${ecmccfg_DIR}loadYamlAxis.cmd,   "FILE=./cfg/axis.yaml,              DEV=${IOC}, AX_NAME=M1, AXIS_ID=1, DRV_SID=${DRV_SID}, ENC_SID=${ENC_SID}, ENC_CH=01"
${SCRIPTEXEC} ${ecmccfg_DIR}loadYamlEnc.cmd,    "FILE=./cfg/enc_open_loop.yaml,     DEV=${IOC}, DRV_SID=${DRV_SID}"

#$(SCRIPTEXEC) $(ecmccfg_DIR)loadPLCFile.cmd,    "FILE=./cfg/armEL5102.plc,          PLC_MACROS='ENC_SID=${ENC_SID}, ENC_CH=01'"

