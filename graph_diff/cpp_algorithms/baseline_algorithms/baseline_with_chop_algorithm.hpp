#pragma once

#include "../graph.hpp"


namespace graph_diff::algorithm {

/**
 * Baseline algorithm that uses bruteforce search with chops
 */
class BaselineWithChopAlgorithm {
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

        std::vector<long long> result(best_choice.size());

        for (size_t i = 0; i < result.size(); ++i) {
            result[order_of_choice_first[i]] = order_of_choice_second[current_choice[i]];
        }

        return result;
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
        best_choice.resize(graph1.size());

        order_of_choice_first.clear();
        order_of_choice_first.resize(graph1.size());
        for (size_t i = 0; i < order_of_choice_first.size(); ++i) {
        	order_of_choice_first[i] = i;
        }
        auto comparator_first = [&graph1](size_t i, size_t j) {
        	return graph1.get_adjacent_list(i).size() > graph1.get_adjacent_list(j).size();
        };
        std::sort(order_of_choice_first.begin(), order_of_choice_first.end(), comparator_first);

        order_of_choice_second.clear();
        order_of_choice_second.resize(graph2.size());
        for (size_t i = 0; i < order_of_choice_second.size(); ++i) {
        	order_of_choice_second[i] = i;
        }
        auto comparator_second = [&graph2](size_t i, size_t j) {
        	return graph2.get_adjacent_list(i).size() > graph2.get_adjacent_list(j).size();
        };
        std::sort(order_of_choice_second.begin(), order_of_choice_second.end(), comparator_second);

        current_score = 0;
        max_left_score = 0;
        for (size_t i = 0; i < graph1.size(); ++i) {
        	max_left_score += graph1.get_adjacent_list(i).size();
        }
        max_score = 0;
    }

    template <typename T>
    void bruteforce_search(graph_diff::graph::Graph<T> const& graph1, 
                           graph_diff::graph::Graph<T> const& graph2, 
                           size_t current_position,
                           size_t last_position,
                           size_t choice_size) {
        if (current_position == choice_size) {
            if (current_score > max_score) {
                copy(current_choice.cbegin(), current_choice.cbegin() + graph1.size(), best_choice.begin());
                max_score = current_score;
            }
            return;
        }

    	auto first = order_of_choice_first[current_position];
        for (size_t i = current_position; i < last_position; ++i) {
        	auto second = order_of_choice_second[current_choice[i]];
            if (graph1.get_nodes()[first].first != graph2.get_nodes()[second].first) {
                continue;
            }
            auto score_addition = score(graph1, graph2, first, second);

            std::swap(current_choice[i], current_choice[current_position]);
            current_score += score_addition;
            max_left_score -= graph1.get_adjacent_list(first).size();

            if (current_score + max_left_score > max_score) {
	            bruteforce_search(graph1, 
	                              graph2, 
	                              current_position + 1, 
	                              last_position, 
	                              choice_size);
            }

            current_score -= score_addition;
            max_left_score += graph1.get_adjacent_list(first).size();
            std::swap(current_choice[i], current_choice[current_position]);
        }

        std::swap(current_choice[current_position], current_choice[last_position]);
		max_left_score -= graph1.get_adjacent_list(first).size();

        bruteforce_search(graph1, 
                          graph2, 
                          current_position + 1, 
                          last_position + 1, 
                          choice_size);

        max_left_score += graph1.get_adjacent_list(first).size();
        std::swap(current_choice[current_position], current_choice[last_position]);
    }

    template <typename T>
    auto score(graph_diff::graph::Graph<T> const& graph1, 
              graph_diff::graph::Graph<T> const& graph2,
              size_t first,
              size_t second) {
        size_t score = 0;
        for (size_t j = 0; j < graph1.get_adjacent_list(first).size(); ++j) {
            auto mapped = current_choice[graph1.get_adjacent_list(first)[j]];
            graph2.get_adjacent_list(second);
            if (mapped != -1
                && !graph2.get_adjacent_list(second).empty()
                    && graph2.is_adjacent(second, mapped)) {
                score++;
            }
        }
        return score;
    }

    std::vector<long long> current_choice;
    std::vector<long long> best_choice;
    std::vector<size_t> order_of_choice_first;
    std::vector<size_t> order_of_choice_second;
    size_t current_score;
    size_t max_left_score;
    size_t max_score;
};

} // end namespace graph_diff::algorithm