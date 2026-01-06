

require ecmccfg "ENG_MODE=1,MASTER_ID=0"

${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd,        "SLAVE_ID=7, HW_DESC=EL7211-9014_CSP_STD"
#- Limit torque to 50% of motor rated torque.  Rated current = 2710mA, set to half I_MAX_MA=1355
${SCRIPTEXEC} ${ecmccfg_DIR}applyComponent.cmd   "COMP=Motor-Beckhoff-AM8111-XFX0, MACROS='I_MAX_MA=1355'"
${SCRIPTEXEC} ${ecmccfg_DIR}applyComponent.cmd   "COMP=Drive-Generic-Ctrl-Params,  MACROS='P_KP=20'"
$(SCRIPTEXEC) $(ecmccfg_DIR)loadYamlAxis.cmd     "FILE=./cfg/axis_csp.yaml,        DRV_ID=$(ECMC_EC_SLAVE_NUM), AX_NAME='Axis1', AX_ID=1"
$(SCRIPTEXEC) $(ecmccfg_DIR)loadYamlEnc.cmd      "FILE=./cfg/enc_sim_linear.yaml,  DRV_ID=$(ECMC_EC_SLAVE_NUM)"

