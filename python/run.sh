#!/bin/bash

IN_DIR=/home/maja/store_part/store/PID_data
OUT_DIR=/home/maja/CERN_part/CERN/PID_ML_in_O2/python/data/root
train=208
dataset=LHC18g4
run=285064

for number in 001 002 003 ; do
  # Real tracks
  o2-analysis-pp-pid-ml-producer --aod-file ${IN_DIR}/${dataset}/${run}/AO2D_${number}.root -b \
    --aod-writer-keep AOD/PIDTRACKSREAL/0:::${OUT_DIR}/train_${train}_dataset_${dataset}_run_${run}_${number}_pidtracksreal_globaltracks |
    o2-analysis-trackextension -b | o2-analysis-trackselection -b | o2-analysis-pid-tof -b

  # MC tracks
  o2-analysis-pp-pid-ml-producer --aod-file ${IN_DIR}/${dataset}/${run}/AO2D_${number}.root -b --doMC \
    --aod-writer-keep AOD/PIDTRACKSMC/0:::${OUT_DIR}/train_${train}_dataset_${dataset}_run_${run}_${number}_pidtracksmc_globaltracks |
    o2-analysis-trackextension -b | o2-analysis-trackselection -b | o2-analysis-pid-tof -b
done
