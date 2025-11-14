#!/bin/bash

# defaults (PSI test setup)
P=${1:-c6025a-08}
AX=${2:-M1}

# pvt-controller params
caput ${P}:PVT-MoveMode 0
caput ${P}:PVT-NumPulses 10
caput ${P}:PVT-NumPoints 10
caput ${P}:PVT-EndPulses 10

# axis related params
caput ${P}:${AX}-PVT-UseAxis 1
caput -a ${P}:${AX}-PVT-Positions '0 1 2 3 5 6 7 8 7 6'

# optional time array
#caput -a ${P}:PVT-Times "0.8 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0"

# build
caput ${P}:PVT-Build 1

