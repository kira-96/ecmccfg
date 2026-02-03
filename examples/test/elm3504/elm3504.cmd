
require ecmccfg sandst_a, "IOC=$(IOC),EC_RATE=1000"

# Array
#${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd, "SLAVE_ID=19, HW_DESC=ELM3504, NELM=${NELM=10}"

# Scalar
${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd, "SLAVE_ID=19, HW_DESC=ELM3504_Scalar"
