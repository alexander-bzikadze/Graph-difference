#pragma once

#include "../graph.hpp"


namespace graph_diff::algorithm {

/**
 * Baseline algorithm that uses bruteforce search
 */
class BaselineAlgorithm {
public:
    /**
     * Constructs difference between two given graphs
     * Is crutial method of the graph_diff::algorithm::*Algorithm interface
     * @param   graph1  first graph
     * @param   graph2  second graph
     * graph1 and graph2 may be swapped incide if graph2 
     *  is bigger graph1 by nodes
     * @return  exact match of first graph to second
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

        initialization(graph_minimal, graph_maximal);

        bruteforce_search(graph_minimal, 
                          graph_maximal, 
                          0,
                          graph_maximal.size(),
                          graph_minimal.size());

        return best_choice;
    }

private:
    template <typename T>
    void initialization(graph_diff::graph::Graph<T> const& graph1, 
                        graph_diff::graph::Graph<T> const& graph2) {
        current_choice.clear();
        current_choice.resize(graph2.size());

        for (size_t i = 0; i < graph2.size(); ++i) {
            current_choice[i] = i;
        }
        current_choice.resize(graph2.size() + graph1.size(), -1);

        best_choice.clear();
        best_choice.resize(graph1.size(), -1);
    }

    template <typename T>
    void bruteforce_search(graph_diff::graph::Graph<T> const& graph1, 
                           graph_diff::graph::Graph<T> const& graph2, 
                           size_t current_position,
                           size_t last_position,
                           size_t choice_size) {
        if (current_position == choice_size) {
            long long current_score = score(graph1, graph2);
            if (current_score > max_score) {
                copy(current_choice.cbegin(), current_choice.cbegin() + graph1.size(), best_choice.begin());
                max_score = current_score;
            }
            return;
        }

        for (size_t i = current_position; i < last_position; ++i) {
            if (graph1.get_nodes()[current_position].first != graph2.get_nodes()[current_choice[i]].first) {
                continue;
            }

            std::swap(current_choice[i], current_choice[current_position]);
            bruteforce_search(graph1,
                              graph2,
                              current_position + 1,
                              last_position,
                              choice_size);
            std::swap(current_choice[i], current_choice[current_position]);
        }

        std::swap(current_choice[current_position], current_choice[last_position]);
        bruteforce_search(graph1,
                          graph2,
                          current_position + 1,
                          last_position + 1,
                          choice_size);
        std::swap(current_choice[current_position], current_choice[last_position]);
    }

    template <typename T>
    auto score(graph_diff::graph::Graph<T> const& graph1,
              graph_diff::graph::Graph<T> const& graph2) {
        size_t score = 0;

        for (size_t i = 0; i < graph1.size(); ++i) {
            auto first = i;
            auto second = current_choice[i];
            if (second == -1) {
                continue;
            }
            for (size_t j = 0; j < graph1.get_adjacent_list(first).size(); ++j) {
            auto mapped = current_choice[graph1.get_adjacent_list(first)[j]];
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

    std::vector<long long> current_choice;
    std::vector<long long> best_choice;
    long long max_score = -1;
};

} // end namespace graph_diff::algorithm
