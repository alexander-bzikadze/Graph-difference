#pragma once

#include "../ant_parameters.hpp"
#include "../graph_stat.hpp"
#include "pheromon_table.hpp"


namespace graph_diff::algorithm::cubed_pathfinder {

/**
 * Pathfinder class for ant_algorithm
 * Complexity is cubic, order of choice is probabilistic
 */
template<typename T>
class Pathfinder {
public:
    using edge = std::tuple<size_t, size_t>;
    using match = std::tuple<size_t, size_t>;
    using UsedPheromonTable = PheromonTable<size_t>;

    Pathfinder(graph::Graph<T> const& graph1,
               graph::Graph<T> const& graph2,
               UsedPheromonTable const& pheromon,
               GraphStat<T> const& graph_stat) :
               graph1(graph1),
               graph2(graph2),
               pheromon(pheromon),
               graph_stat(graph_stat),
               edges(std::vector<char>(graph1.size() * graph1.size(), 0),
                     std::vector<char>(graph2.size() * graph2.size(), 0)),
               score(0),
               best_choice(std::min(graph1.size(), graph2.size()), 0),
               phero_factors(graph1.size() * graph2.size(), 0),
               score_factors(graph1.size() * graph2.size(), 0),
               probabilities(graph1.size() * graph2.size(), 0),
               acc_sum(0),
               generator(std::random_device()()),
               dis(0, 1) {
        for (size_t i = 0; i < graph1.size(); ++i) {
            for (size_t j = 0; j < graph1.get_adjacent_list(i).size(); ++j) {
                std::get<0>(edges)[i * graph1.size() + j] = true;
            }
        }

        for (size_t i = 0; i < graph2.size(); ++i) {
            for (size_t j = 0; j < graph2.get_adjacent_list(i).size(); ++j) {
                std::get<1>(edges)[i * graph2.size() + j] = true;
            }
        }
    }

    /**
     * Make a probabilistic choice of match of given graphs
     * Is crutial method of Pathfinder interface
     * @return  choice represented as vector of long long
     *  -1 states for no match for the node
     */
    auto find_path() {
        phero_factors.clear();
        phero_factors.resize(graph1.size() * graph2.size(), 0);
        score_factors.clear();
        score_factors.resize(graph1.size() * graph2.size(), 0);
        // generator = std::mt19937(std::random_device()());

        for (size_t i = 0; i < score_factors.size(); ++i) {
            auto [first, second] = to_2d_address(i);
            score_factors[i] += graph1.get_nodes()[first].first == graph2.get_nodes()[second].first;
        }
        std::vector<long long> choice(graph1.size(), -1);

        auto upper_size = probabilities.size();
        double acc = 0;
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < upper_size; ++i) {
            auto [from_first, from_second] = to_2d_address(i);
            if (score_factors[i] > 0) {
                acc += 1
                    // * graph_stat.get_statistic(i);
                    ;
            }
            probabilities[i] = acc;
        }
        acc_sum = probabilities.back();

        // prob - array of partial sums;
        for (size_t i = 0; i < graph1.size() && acc_sum > 0; ++i) {
            find_pair(choice);
        }

        return choice;
    }

private:
    void update_probs(size_t chosen_first,
                      size_t chosen_second) {
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < graph1.size(); ++i) {
            score_factors[to_1d_address(i, chosen_second)] = 0;
        }

        for (size_t i = 0; i < graph2.size(); ++i) {
            score_factors[to_1d_address(chosen_first, i)] = 0;
        }

        auto upper_size = probabilities.size();
        double acc = 0;
        // #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < upper_size; ++i) {
            auto [from_first, from_second] = to_2d_address(i);
            if (score_factors[i] > 0) {
                score_factors[i] += !!(contains_edge<0>(from_first, chosen_first)
                    && contains_edge<1>(from_second, chosen_second));
                score_factors[i] += !!(contains_edge<0>(chosen_first, from_first)
                    && contains_edge<1>(chosen_second, from_second));
            }
        }

        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < upper_size; ++i) {
            auto [from_first, from_second] = to_2d_address(i);
            auto pher = pheromon.get_element(from_first,
                                             from_second,
                                             chosen_first,
                                             chosen_second);
            phero_factors[i] += pher;
            if (score_factors[i] > 0) {
                acc += pow(phero_factors[i], ant_parameters::ALPHA)
                     * pow(score_factors[i], ant_parameters::BETA)
                     * graph_stat.get_statistic(i);
            }
            probabilities[i] = acc;
        }
        acc_sum = probabilities.back();
    }

    void find_pair(std::vector<long long>& choice) {
        auto value = dis(generator) * acc_sum;
        auto chosen_position = std::upper_bound(probabilities.cbegin(), probabilities.cend(), value) - probabilities.cbegin();

        auto [chosen_first, chosen_second] = to_2d_address(chosen_position);

        choice[chosen_first] = chosen_second;

        update_probs(chosen_first, chosen_second);

    }


    inline auto to_1d_address(size_t i, size_t j) { return i * graph2.size() + j; }
    inline auto to_2d_address(size_t i) {
        return std::make_tuple(i / graph2.size(), i % graph2.size());
    }


    graph::Graph<T> const& graph1;
    graph::Graph<T> const& graph2;
    PheromonTable<size_t> const& pheromon;
    GraphStat<T> const& graph_stat;

    std::tuple<std::vector<char>, std::vector<char>> edges;
    template <size_t n> inline bool contains_edge(size_t i, size_t j) {
        if constexpr (n == 0){
            return std::get<n>(edges)[i * graph1.size() + j];
        } else {
            return std::get<n>(edges)[i * graph2.size() + j];
        }
    }

    size_t score;
    std::vector<long long> best_choice;

    std::vector<double> phero_factors;
    std::vector<double> score_factors;
    std::vector<double> probabilities;
    double acc_sum;

    std::mt19937 generator;
    std::uniform_real_distribution<> dis;
};

}