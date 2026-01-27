#- Load info for axes groups, mainly for allowing automatic GUI generation
epicsEnvShow (ECMC_AX_GRP_ID_${ECMC_LOOP_IDX}_LIST)
epicsEnvShow (ECMC_AX_GRP_ID_${ECMC_LOOP_IDX}_NAME)
dbLoadRecords(ecmcAxisGroup_chX.db,"P=${P},NAME=${ECMC_AX_GRP_ID_${ECMC_LOOP_IDX}_NAME},AXES='${ECMC_AX_GRP_ID_${ECMC_LOOP_IDX}_LIST}',ID=${ECMC_LOOP_IDX}")
