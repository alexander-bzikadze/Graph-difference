#pragma once

#include <unordered_map>

#include "../ant_parameters.hpp"
#include "../graph_stat.hpp"
#include "pheromon_table.hpp"

namespace graph_diff::algorithm::ordered_pathfinder {

/**
 * Pathfinder class for ant_algorithm
 * Complexity is squar, order of choice is increasing
 */
template <typename T>
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
               score_factors(graph1.size() * graph2.size(), 0),
               second_graph_label(graph2.size(), std::vector<size_t>()),
               inverse1(invert_edges(graph1)),
               inverse2(invert_edges(graph2)),
               generator(std::random_device()()),
               dis(0, 1) {
        for (size_t i = 0; i < graph2.size(); ++i) {
            second_graph_label[graph2.get_nodes()[i].first].push_back(i);
        }
    }


    /**
     * Make a probabilistic choice of match of given graphs
     * Is crutial method of Pathfinder interface
     * @return  choice represented as vector of long long
     *  -1 states for no match for the node
     */
    auto find_path() {
        init();

        std::vector<long long> choice(graph1.size(), -1);
        for (size_t i = 0; i < graph1.size(); ++i) {
            if (choice.at(i) != -1) {
                continue;
            }

            auto chosen = choose(i);
            choice[i] = chosen;
            update_probs(i, chosen);
        }
        return choice;
    }

private:
    void init() {
        for (size_t i = 0; i < score_factors.size(); ++i) {
            auto [first, second] = to_2d_address(i);
            score_factors[i] = graph1.get_nodes()[first].first == graph2.get_nodes()[second].first;
        }
    }

    long long choose(size_t i) {
        auto label = graph1.get_nodes()[i].first;
        auto const& label_set = second_graph_label[label];
        auto probabilities = std::vector<double>(label_set.size(), 0);
        auto acc = 0.;
        for (size_t j = 0; j < label_set.size(); ++j) {
            if (score_factors[to_1d_address(i, label_set[j])] > 0) {
                acc += pow(pheromon.get_element(i, label_set[j]), ant_parameters::ALPHA)
                     * pow(score_factors[to_1d_address(i, label_set[j])], ant_parameters::BETA)
                     * graph_stat.get_statistic(to_1d_address(i, label_set[j]));
            }
            probabilities[j] = acc;
        }
        if (!acc) {
            return -1ll;
        }

        auto value = dis(generator) * acc;
        auto chosen_position = std::upper_bound(probabilities.cbegin(), probabilities.cend(), value) - probabilities.cbegin();
        return label_set[chosen_position];
    }

    void update_probs(size_t chosen_first, long long chosen_second) {
        for (size_t i = 0; i < graph2.size(); ++i) {
            score_factors[to_1d_address(chosen_first, i)] = 0;
        }

        if (chosen_second < 0) {
            return;
        }

        for (size_t i = 0; i < graph1.size(); ++i) {
            score_factors[to_1d_address(i, chosen_second)] = 0;
        }

        #pragma clang loop vectorize(enable)
        for (auto u : graph1.get_adjacent_list(chosen_first)) {
            for (auto v : graph2.get_adjacent_list(chosen_second)) {
                if (score_factors[to_1d_address(u, v)]) {
                    score_factors[to_1d_address(u, v)]++;
                }
            }
        }

        #pragma clang loop vectorize(enable)
        for (auto u : inverse1[chosen_first]) {
            for (auto v : inverse2[chosen_second]) {
                if (score_factors[to_1d_address(u, v)]) {
                    score_factors[to_1d_address(u, v)]++;
                }
            }
        }
    }

    auto invert_edges(graph::Graph<T> const& graph) {
        std::vector<std::vector<size_t>> adjacent_list(graph.size(), std::vector<size_t>());
        for (size_t i = 0; i < graph.size(); ++i) {
            for (auto v : graph.get_adjacent_list(i)) {
                adjacent_list[v].push_back(i);
            }
        }
        for (size_t i = 0; i < graph.size(); ++i) {
            auto& list = adjacent_list[i];
            std::sort(list.begin(), list.end());
        }
        return adjacent_list;
    }

    graph::Graph<T> const& graph1;
    graph::Graph<T> const& graph2;
    UsedPheromonTable const& pheromon;
    GraphStat<T> const& graph_stat;

    std::vector<double> score_factors;
    std::vector<std::vector<size_t>> second_graph_label;
    std::vector<std::vector<size_t>> inverse1;
    std::vector<std::vector<size_t>> inverse2;
    std::mt19937 generator;
    std::uniform_real_distribution<> dis;

    inline auto to_1d_address(size_t i, size_t j) { return i * graph2.size() + j; }
    inline auto to_2d_address(size_t i) {
        return std::make_tuple(i / graph2.size(), i % graph2.size());
    }
};

} // end of graph::algorithm::linear_pathfinder
