/**
 * @file FastSimulations.hpp
 * @author SwirtaB
 * @brief
 * @version 0.1.1
 * @date 2021-12-20
 *
 * @copyright Copyright (c) 2021
 *
 */

#ifndef ONNX_API_FAST_SIMULATIONS_HPP
#define ONNX_API_FAST_SIMULATIONS_HPP

#include "onnxruntime_cxx_api.h"

#include <array>
#include <string>

namespace fs
{

const std::string ZDCModelPath = "../models/generator.onnx";
const std::string SAEModelPath = "../models/sae_model.onnx";

class NeuralFastSimulation
{
  public:
    NeuralFastSimulation(const std::string  &modelPath,
                         Ort::SessionOptions sessionOptions,
                         OrtAllocatorType    allocatorType,
                         OrtMemType          memoryType);
    ~NeuralFastSimulation() = default;

    virtual void run() = 0;

  protected:
    void set_input_output_data();

    ///ONNX specific attributes
    Ort::Env                         m_env;
    Ort::Session                     m_session;
    Ort::AllocatorWithDefaultOptions m_allocator;
    Ort::MemoryInfo                  m_memoryInfo;

    ///Input/Output names and input shape
    std::vector<char *> m_inputNames;
    std::vector<char *> m_outputNames;
    std::vector<std::vector<int64_t >> m_inputShapes;
};

class VAEModelSimulation : public NeuralFastSimulation
{
  public:
    VAEModelSimulation(std::array<float, 9> conditionalMeans,
                       std::array<float, 9> conditionalScales,
                       float                noiseStdDev);
    ~VAEModelSimulation() = default;

    void               run() override;
    void               set_data(std::array<float, 9> &particle);
    std::array<int, 5> get_prediction();

  private:
    std::array<float, 9> scale_conditional_input(const std::array<float, 9> &rawConditionalInput);
    std::array<int, 5>   calculate_channels();

    std::array<float, 9> m_conditionalMeans;
    std::array<float, 9> m_conditionalScales;
    float                m_noiseStdDev;

    std::vector<float> m_noiseInput;

    std::array<float, 9>    m_particle{};
    std::vector<Ort::Value> m_modelOutput;
};

class SAEModelSimulation : public NeuralFastSimulation
{
  public:
    SAEModelSimulation(std::array<float, 9> conditionalMeans, std::array<float, 9> conditionalScales, float noiseStdev);
    ~SAEModelSimulation() = default;
};

// Czy zawsze return to suma kontrolna pięciu kanałów?
class SimReaderBase
{
  public:
    virtual std::array<int, 5> visit(VAEModelSimulation &model) = 0;
};

class SimReader : public SimReaderBase
{
  public:
    std::array<int, 5> visit(VAEModelSimulation &model) override;
};

} // namespace fs
#endif // ONNX_API_FAST_SIMULATIONS_HPP