#pragma once

#include <unordered_set>
#include <unordered_map>
#include <tuple>
#include <random>

#include "ant_parameters.hpp"
#include "graph_stat.hpp"


namespace graph_diff::algorithm {

/**
 * Ant algorithm that uses probabilistic choice
 * Template Pathfinder defines which way will be chosen the matches
 */
template <template <typename T> typename Pathfinder>
class AntAlgorithm {
public:
    template <typename T>
    using UsedPheromonTable = typename Pathfinder<T>::UsedPheromonTable;

    AntAlgorithm() = default;

    /**
     * Constructs difference between two given graphs
     * Is crutial method of the graph_diff::algorithm::*Algorithm interface
     * @param   graph1  first graph
     * @param   graph2  second graph
     * graph1 and graph2 may be swapped incide if graph2
     *  is bigger graph1 by nodes
     * @return  heuristic match of first graph to second
     *  represented as vector of long long. -1 states
     *  that node should be matched with nothing
     */
    template <typename T>
    auto construct_diff(graph_diff::graph::Graph<T> const& graph1,
                        graph_diff::graph::Graph<T> const& graph2) {

        auto const& graph_minimal = graph1.size() <= graph2.size() ?
            graph1 : graph2;
        auto const& graph_maximal = graph1.size() <= graph2.size() ?
            graph2 : graph1;
        UsedPheromonTable<T> pheromon;
        GraphStat<T> graph_stat(graph_minimal, graph_maximal);
        best_choice.resize(graph_minimal.size(), 0);

        std::vector<Pathfinder<T>> pathfinders = std::vector<Pathfinder<T>>();
        pathfinders.reserve(ant_parameters::NUMBER_OF_AGENTS);
        for (size_t i = 0; i < ant_parameters::NUMBER_OF_AGENTS; ++i) {
            pathfinders.emplace_back(graph_minimal, graph_maximal, pheromon, graph_stat);
        }

        for (size_t i = 0, same_score = 0; i < ant_parameters::NUMBER_OF_ITERATIONS; ++i, ++same_score) {
            auto choice = std::vector<long long>();
            long long chosen_score = -1;
            for (size_t j = 0; j < ant_parameters::NUMBER_OF_AGENTS; ++j) {
                auto current_choice = pathfinders[j].find_path();
                auto current_score = score(graph_minimal, graph_maximal, current_choice);
                if (current_score > chosen_score) {
                    choice = current_choice;
                    chosen_score = current_score;
                }
            }

            if (chosen_score > best_score) {
                best_score = chosen_score;
                best_choice = choice;
                same_score = 0;
            }

            double addition = 1. / (1 + best_score - chosen_score);
            pheromon.update(choice, addition);

            if (same_score == ant_parameters::MAX_NUMBER_OF_ITERATIONS_WITH_THE_SAME_SCORE) {
                break;
            }
        }

        return best_choice;
    }

private:
    template <typename T>
    auto score(graph_diff::graph::Graph<T> const& graph1, 
               graph_diff::graph::Graph<T> const& graph2,
               std::vector<long long> const& choice) {
        long long score = 0;
        for (size_t i = 0; i < graph1.size(); ++i) {
            auto first = i;
            auto second = choice[i];
            if (second == -1) {
                continue;
            }
            for (size_t j = 0; j < graph1.get_adjacent_list(first).size(); ++j) {
                auto mapped = choice[graph1.get_adjacent_list(first)[j]];
                graph2.get_adjacent_list(second);
                if (mapped != -1
                    && !graph2.get_adjacent_list(second).empty()
                    && graph2.is_adjacent(second, mapped)) {
                    score++;
                }
            }
        }
        return score;
    }

    long long best_score = -1;
    std::vector<long long> best_choice;
};

} // end graph_diff::algorithm