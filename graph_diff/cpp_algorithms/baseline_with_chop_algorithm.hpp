#include <iostream>

#include "graph.hpp"

namespace graph_diff::algorithm {

class BaselineWithChopAlgorithm {
public:
    template <typename T>
    std::vector<int> construct_diff(graph_diff::graph::Graph<T> const& graph1, 
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

        copy(best_choice.cbegin(), best_choice.cend(), current_choice.begin());

        std::cout << max_score << std::endl;

        return best_choice;
    }

private:
    template <typename T>
    void initialization(graph_diff::graph::Graph<T> const& graph1, 
                        graph_diff::graph::Graph<T> const& graph2) {
        current_choice.clear();
        current_choice.resize(graph1.size() + graph2.size());

        for (int i = 0; i < graph2.size(); ++i) {
            current_choice[i] = i;
        }
        for (int i = 0, k = graph2.size(); i < graph1.size(); ++i) {
            current_choice[i + k] = -1;
        }

        best_choice.clear();
        best_choice.resize(graph1.size());

        order_of_choice.clear();
        order_of_choice.resize(graph1.size());
        for (int i = 0; i < order_of_choice.size(); ++i) {
        	order_of_choice[i] = i;
        }
        auto comparator = [&graph1](int i, int j) {
        	return graph1.get_adjacent_list(i).size() > graph1.get_adjacent_list(j).size();
        };
        std::sort(order_of_choice.begin(), order_of_choice.end(), comparator);

        current_score = 0;
        max_left_score = 0;
        for (int i = 0; i < graph1.size(); ++i) {
        	max_left_score += graph1.get_adjacent_list(i).size();
        }
        max_score = 0;
    }

    template <typename T>
    void bruteforce_search(graph_diff::graph::Graph<T> const& graph1, 
                           graph_diff::graph::Graph<T> const& graph2, 
                           int current_position,
                           int last_position,
                           int choice_size) {
        if (current_position == choice_size) {
            if (current_score > max_score) {
                copy(current_choice.cbegin(), current_choice.cbegin() + graph1.size(), best_choice.begin());
                max_score = current_score;
            }
            return;
        }

    	auto first = order_of_choice[current_position];
        for (int i = current_position; i < last_position; ++i) {
        	auto second = current_choice[i];
            if (graph1.get_nodes()[first].first != graph2.get_nodes()[second].first) {
                continue;
            }
            int score_addition = score(graph1, graph2, first, second);

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
    int score(graph_diff::graph::Graph<T> const& graph1, 
              graph_diff::graph::Graph<T> const& graph2,
              int first,
              int second) {
        int score = 0;
        for (int j = 0; j < graph1.get_adjacent_list(first).size(); ++j) {
            auto mapped = current_choice[graph1.adjacent_to(first, j)];
            graph2.get_adjacent_list(second);
            if (mapped != -1
                && !graph2.get_adjacent_list(second).empty()
                && std::binary_search(graph2.get_adjacent_list(second).cbegin(), 
                                      graph2.get_adjacent_list(second).cend(), 
                                      mapped)) {
                score++;
            }
        }
        return score;
    }

    std::vector<int> current_choice;
    std::vector<int> best_choice;
    std::vector<int> order_of_choice;
    int current_score;
    int max_left_score;
    int max_score;
};

} // end namespace graph_diff::algorithm