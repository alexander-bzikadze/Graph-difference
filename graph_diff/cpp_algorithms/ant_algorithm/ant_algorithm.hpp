#pragma once

#include <unordered_set>
#include <unordered_map>
#include <tuple>
#include <random>

#include "ant_parameters.hpp"
#include "pheromon_table.hpp"
#include "pathfinder.hpp"
#include "graph_stat.hpp"


namespace graph_diff::algorithm {

class AntAlgorithm {
public:
    AntAlgorithm() = default;

    template <typename T>
    auto construct_diff(graph_diff::graph::Graph<T> const& graph1, 
                        graph_diff::graph::Graph<T> const& graph2) {
        auto const& graph_minimal = graph1.size() <= graph2.size() ?
            graph1 : graph2;
        auto const& graph_maximal = graph1.size() <= graph2.size() ?
            graph2 : graph1;

        PheromonTable<size_t> pheromon;
        GraphStat<T> graph_stat(graph1, graph2);
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
            for (size_t j = 0; j < choice.size(); ++j) {
                for (size_t k = 0; k < choice.size(); ++k) {
                    pheromon.add_update(j, choice.at(j), k, choice.at(k), 1 / (1 + best_score - chosen_score));
                }
            }
            if (chosen_score > best_score) {
                best_score = chosen_score;
                best_choice = choice;
                same_score = 0;
            }
            pheromon.next_interation();

            if (same_score == ant_parameters::MAX_NUMBER_OF_ITERATIONS_WITH_THE_SAME_SCORE) {
                break;
            }
        }

        return best_choice;
    }

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
                auto mapped = choice[graph1.adjacent_to(first, j)];
                graph2.get_adjacent_list(second);
                if (mapped != -1
                    && !graph2.get_adjacent_list(second).empty()
                    && std::binary_search(graph2.get_adjacent_list(second).cbegin(), 
                                          graph2.get_adjacent_list(second).cend(), 
                                          mapped)) {
                    score++;
                }
            }
        }
        return score;
    }

private:
    long long best_score = -1;
    std::vector<long long> best_choice;
};

} // end graph_diff::algorithm