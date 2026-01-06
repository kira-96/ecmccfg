#!/bin/bash

 

PREFIX=$1
AXIS=$2

# PREFIX, AXES SUFFIX TIMEOUT
function wait_for_PV() {
  PV=$1:$2-$3
  TIMEOUT=$4   # seconds

  start_time=$(date +%s)
   
  while true; do
      value=$(caget -noname -int "$PV" 2>/dev/null)
   
      if [ "$value" = "1" ]; then
          printf "\n"
          echo "PV '$PV' is 1 — continuing."
          break
      fi
   
      # Check timeout
      now=$(date +%s)
      if (( now - start_time >= TIMEOUT )); then
          echo "Timeout after $TIMEOUT seconds waiting for PV '$PV' to become 1."
          exit 1
      fi
   
      sleep 0.5
      printf "."
  done
}

# PREFIX, AXES SEQ ID
function trigg_home() {
  # Homing
  caput $1:$2-MtnCmd 10
  sleep 1
  # Seq
  caput $1:$2-movHomCmd $3
  sleep 1
  caput $1:$2-ExeCmd 1
} 

function test_home_seq_11() {
  trigg_home $1 $2  11
  sleep $((RANDOM %5 + 1))
  # simulated limits
  caput $PREFIX:m0s002-One 2
  sleep 3
  caput $PREFIX:m0s002-One 3
  wait_for_PV $1 $2 Homed 30
}

function test_home_seq_12() {
  trigg_home $1 $2  12
  sleep $((RANDOM %5 + 1))
  # simulated limits
  caput $PREFIX:m0s002-One 1
  sleep 3
  caput $PREFIX:m0s002-One 3
  wait_for_PV $1 $2 Homed 30
}

# main
while true; do
  #homing seq 11 or 12
  seq=$(( RANDOM % 2 + 11 ))
  test_home_seq_$seq $PREFIX $AXIS
  sleep 1
done
