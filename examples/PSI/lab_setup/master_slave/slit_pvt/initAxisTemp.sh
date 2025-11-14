# Controller params 
#  relative
caput c6025a-08:PVT-MoveMode 0
caput c6025a-08:PVT-NumPulses 10
caput c6025a-08:PVT-NumPoints 10
caput c6025a-08:PVT-EndPulses 10
caput c6025a-08:$1-PVT-UseAxis 1
# pos array
caput -a c6025a-08:$1-PVT-Positions '0 1 2 3 5 6 7 8 7 6'

# Use axis

# build
#caput c6025a-08:PVT-Build 1
# prepare a relative move
#caput c6025a-08:$1-TgtPosCmd 1000
#caput c6025a-08:$1-MtnCmd 2
#caput c6025a-08:$1.CNEN 1
#caput -a c6025a-08:PVT-Times "0.8 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0"



#caput ${P}:PVT-MoveMode 0
#caput ${P}:PVT-NumPulses 10
#caput ${P}:PVT-NumPoints 10
#caput ${P}:PVT-NumEndPulses 10

#caput -a ${P}:TRX1-PVT-Positions '0 1 2 3 5 6 7 8 7 6'
#caput ${P}:TRX1-PVT-UseAxis 1
#caput ${P}:PVT-Build 1
# 
# caput ${P}:TRX1-TgtPosCmd 10
# caput ${P}:TRX1-MtnCmd 2
#caput -a ${P}:PVT-Times "0.8 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0"
