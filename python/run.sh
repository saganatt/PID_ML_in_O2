#!/bin/bash

IN_DIR=/home/maja/store_part/store/PID_data
OUT_DIR=/home/maja/CERN_part/CERN/PID_ML_in_O2/python/data/

# MC tracks
train=208
dataset=LHC18g4
run=285064
for number in {001..010}; do
  o2-analysis-timestamp -b | o2-analysis-trackextension -b | o2-analysis-trackselection -b | o2-analysis-pid-tof -b | o2-analysis-pid-tof-beta -b | o2-analysis-pid-tof-full -b | o2-analysis-pid-tpc-full -b |
    o2-analysis-pid-ml-producer --aod-file ${IN_DIR}/${dataset}/${run}/train_${train}/AO2D_${number}.root -b --doMC \
    --aod-writer-keep AOD/PIDTRACKSMC/0:::${OUT_DIR}/train_${train}_dataset_${dataset}_run_${run}_${number}_pidtracksmc_globaltracks
done

# Real tracks
train=204
dataset=LHC18b
run=285064
for number in {001..010}; do
  o2-analysis-timestamp -b | o2-analysis-trackextension -b | o2-analysis-trackselection -b | o2-analysis-pid-tof -b | o2-analysis-pid-tof-beta -b | o2-analysis-pid-tof-full -b | o2-analysis-pid-tpc-full -b |
    o2-analysis-pid-ml-producer --aod-file ${IN_DIR}/${dataset}/${run}/train_${train}/AO2D_${number}.root -b \
    --aod-writer-keep AOD/PIDTRACKSREAL/0:::${OUT_DIR}/train_${train}_dataset_${dataset}_run_${run}_${number}_pidtracksreal_globaltracks
done
