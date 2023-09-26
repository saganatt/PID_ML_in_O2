#include "FastSimulations.hpp"
#include "Utils.hpp"

#include <cmath>

using namespace fs;

NeuralFastSimulation::NeuralFastSimulation(const std::string  &modelPath,
                                           Ort::SessionOptions sessionOptions,
                                           OrtAllocatorType    allocatorType,
                                           OrtMemType          memoryType) :
    m_session(m_env, modelPath.c_str(), sessionOptions),
    m_memoryInfo(Ort::MemoryInfo::CreateCpu(allocatorType, memoryType)) {}

void NeuralFastSimulation::set_input_output_data() {
    for (size_t i = 0; i < m_session.GetInputCount(); ++i) {
        m_inputNames.push_back(m_session.GetInputName(i, m_allocator));
    }
    for (size_t i = 0; i < m_session.GetInputCount(); ++i) {
        m_inputShapes.emplace_back(m_session.GetInputTypeInfo(i).GetTensorTypeAndShapeInfo().GetShape());
    }
    for (size_t i = 0; i < m_session.GetOutputCount(); ++i) {
        m_outputNames.push_back(m_session.GetOutputName(i, m_allocator));
    }

    // Prevent negative values from being passed as tensor shape
    for (auto &shape : m_inputShapes) {
        for (auto &elem : shape) {
            elem = std::abs(elem);
        }
    }
}

VAEModelSimulation::VAEModelSimulation(std::array<float, 9> conditionalMeans,
                                       std::array<float, 9> conditionalScales,
                                       float                noiseStdDev) :
    NeuralFastSimulation(ZDCModelPath, Ort::SessionOptions{nullptr}, OrtDeviceAllocator, OrtMemTypeCPU),
    m_conditionalMeans(conditionalMeans), m_conditionalScales(conditionalScales), m_noiseStdDev(noiseStdDev),
    m_noiseInput(normal_distribution(0, m_noiseStdDev, 10)) {}

void VAEModelSimulation::set_data(std::array<float, 9> &particle) {
    m_particle = particle;
    set_input_output_data();
}

std::array<int, 5> VAEModelSimulation::get_prediction() {
    return calculate_channels();
}

// TODO what about splitting this function
void VAEModelSimulation::run() {
    //    std::vector<char *> inputNames;
    //    for (size_t i = 0; i < m_session.GetInputCount(); ++i) {
    //        inputNames.push_back(m_session.GetInputName(i, m_allocator));
    //    }
    //    std::vector<std::vector<int64_t>> inputShapes;
    //    for (size_t i = 0; i < m_session.GetInputCount(); ++i) {
    //        inputShapes.emplace_back(m_session.GetInputTypeInfo(i).GetTensorTypeAndShapeInfo().GetShape());
    //    }
    //    std::vector<char *> outputNames;
    //    for (size_t i = 0; i < m_session.GetOutputCount(); ++i) {
    //        outputNames.push_back(m_session.GetOutputName(i, m_allocator));
    //    }
    //
    //    // Prevent negative values from being passed as tensor shape
    //    for (auto &shape : inputShapes) {
    //        for (auto &elem : shape) {
    //            elem = std::abs(elem);
    //        }
    //    }
    //
    //    // Container for all input tensors
    //    std::vector<Ort::Value> inputTensors;
    //
    //    // Create tensor from noise
    //    inputTensors.emplace_back(Ort::Value::CreateTensor<float>(
    //        m_memoryInfo, m_noiseInput.data(), m_noiseInput.size(), inputShapes[0].data(), inputShapes[0].size()));
    //    // Scale raw input and creates tensor from it
    //    auto conditionalInput = scale_conditional_input(m_particle);
    //    inputTensors.emplace_back(Ort::Value::CreateTensor<float>(
    //        m_memoryInfo, conditionalInput.data(), conditionalInput.size(), inputShapes[1].data(),
    //        inputShapes[1].size()));
    //
    //    m_modelOutput = m_session.Run(Ort::RunOptions{nullptr},
    //                                  inputNames.data(),
    //                                  inputTensors.data(),
    //                                  inputTensors.size(),
    //                                  outputNames.data(),
    //                                  outputNames.size());

    // Container for all input tensors
    std::vector<Ort::Value> inputTensors;

    // Create tensor from noise
    inputTensors.emplace_back(Ort::Value::CreateTensor<float>(
        m_memoryInfo, m_noiseInput.data(), m_noiseInput.size(), m_inputShapes[0].data(), m_inputShapes[0].size()));
    // Scale raw input and creates tensor from it
    auto conditionalInput = scale_conditional_input(m_particle);
    inputTensors.emplace_back(Ort::Value::CreateTensor<float>(m_memoryInfo,
                                                              conditionalInput.data(),
                                                              conditionalInput.size(),
                                                              m_inputShapes[1].data(),
                                                              m_inputShapes[1].size()));

    m_modelOutput = m_session.Run(Ort::RunOptions{nullptr},
                                  m_inputNames.data(),
                                  inputTensors.data(),
                                  inputTensors.size(),
                                  m_outputNames.data(),
                                  m_outputNames.size());
}

std::array<float, 9> VAEModelSimulation::scale_conditional_input(const std::array<float, 9> &rawConditionalInput) {
    std::array<float, 9> scaledConditionalInput = {0, 0, 0, 0, 0, 0, 0, 0, 0};
    for (int i = 0; i < 9; ++i) {
        scaledConditionalInput[i] = (rawConditionalInput[i] - m_conditionalMeans[i]) / m_conditionalScales[i];
    }
    return scaledConditionalInput;
}
std::array<int, 5> VAEModelSimulation::calculate_channels() {
    std::array<float, 5> channels = {0}; // 4 photon channels

    auto flattedImageVector = m_modelOutput[0].GetTensorMutableData<float>();
    for (int i = 0; i < 44; i++) {
        for (int j = 0; j < 44; j++) {
            if (i % 2 == j % 2) {
                if (i < 22 && j < 22) {
                    channels[0] = channels[0] + flattedImageVector[i + j * 44];
                } else if (i >= 22 && j < 22) {
                    channels[1] = channels[1] + flattedImageVector[i + j * 44];
                } else if (i < 22 && j >= 22) {
                    channels[2] = channels[2] + flattedImageVector[i + j * 44];
                } else if (i >= 22 && j >= 22) {
                    channels[3] = channels[3] + flattedImageVector[i + j * 44];
                }
            } else
                channels[4] = channels[4] + flattedImageVector[i + j * 44];
        }
    }
    std::array<int, 5> channels_integers = {0};
    for (int ch = 0; ch < 5; ch++) {
        channels_integers[ch] = std::round(channels[ch]);
    }
    return channels_integers;
}
