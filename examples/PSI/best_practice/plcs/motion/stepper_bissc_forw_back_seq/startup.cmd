require ecmccfg "ENG_MODE=1"

# EL7041    1Ch Stepper
${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd,       "SLAVE_ID=14,HW_DESC=EL7041-0052"
${SCRIPTEXEC} ${ecmccfg_DIR}applyComponent.cmd  "COMP=Motor-Generic-2Phase-Stepper,  MACROS='I_MAX_MA=1500, I_STDBY_MA=1000, U_NOM_MV=48000, R_COIL_MOHM=1230'"
epicsEnvSet(DRV_SID,${ECMC_EC_SLAVE_NUM})

# EL5042    2Ch BiSS-C Encoder, RLS-LA11
${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd,       "SLAVE_ID=9,HW_DESC=EL5042"
${SCRIPTEXEC} ${ecmccfg_DIR}applyComponent.cmd  "COMP=Encoder-RLS-LA11-26bit-BISS-C,CH_ID=1"
${SCRIPTEXEC} ${ecmccfg_DIR}applyComponent.cmd  "COMP=Encoder-RLS-LA11-26bit-BISS-C,CH_ID=2"
epicsEnvSet(ENC_SID,${ECMC_EC_SLAVE_NUM})

${SCRIPTEXEC} ${ecmccfg_DIR}loadYamlAxis.cmd,   "FILE=./cfg/axis.yaml,          DEV=${IOC}, AX_NAME=M1, AXIS_ID=1, DRV_SID=${DRV_SID}, ENC_SID=${ENC_SID}, ENC_CH=01"
${SCRIPTEXEC} ${ecmccfg_DIR}loadYamlEnc.cmd,    "FILE=./cfg/enc_open_loop.yaml, DEV=${IOC}, ENC_SID=${DRV_SID}"

${SCRIPTEXEC} ${ecmccfg_DIR}loadPLCFile.cmd     "FILE=./cfg/backForwSeq.plc, SAMPLE_RATE_MS=100, PLC_MACROS='AX_ID=1'"
dbLoadRecords("ecmcPlcAnalog.db","P=$(IOC):,PORT=MC_CPU1,ASYN_NAME=plcs.plc${ECMC_PLC_ID}.static.seqStep,REC_NAME=-M${AX_ID=1}-State")
dbLoadRecords("ecmcPlcBinary.db","P=$(IOC):,PORT=MC_CPU1,ASYN_NAME=plcs.plc${ECMC_PLC_ID}.static.doMotion,REC_NAME=-M${AX_ID=1}-DoMtn")

# Trigger motion with caput <IOC>Set-M<AX_ID>-DoMtn-RB 1


