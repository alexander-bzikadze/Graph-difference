#include <iostream>

#include "graph.hpp"

namespace graph_diff::algorithm {

class BaselineAlgorithm {
public:
    template <typename T>
    std::vector<int> const& construct_diff(graph_diff::graph::Graph<T> const& graph1, 
                                           graph_diff::graph::Graph<T> const& graph2) {
        current_choice.clear();
        current_choice.resize(graph1.size() + graph2.size());

        best_choice.clear();
        best_choice.resize(graph1.size());

        for (int i = 0; i < graph2.size(); ++i) {
            current_choice[i] = i;
        }
        for (int i = 0, k = graph2.size(); i < graph1.size(); ++i) {
            current_choice[i + k] = -1;
        }

        start_brute_search(graph1, graph2);
        copy(best_choice.cbegin(), best_choice.cend(), current_choice.begin());

        return best_choice;
    }

private:
    template <typename T>
    void start_brute_search(graph_diff::graph::Graph<T> const& graph1, 
                            graph_diff::graph::Graph<T> const& graph2) {
        bruteforce_search(graph1, 
                          graph2, 
                          0,
                          graph2.size(),
                          graph1.size());
    }

    template <typename T>
    void bruteforce_search(graph_diff::graph::Graph<T> const& graph1, 
                           graph_diff::graph::Graph<T> const& graph2, 
                           int current_position,
                           int last_position,
                           int choice_size) {
        if (current_position == choice_size) {
            auto current_score = score(graph1, graph2);
            if (current_score > max_score) {
                copy(current_choice.cbegin(), current_choice.cbegin() + graph1.size(), best_choice.begin());
                max_score = current_score;
            }
            return;
        }

        for (int i = current_position; i < last_position; ++i) {
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
    int score(graph_diff::graph::Graph<T> const& graph1, 
              graph_diff::graph::Graph<T> const& graph2) {
        int score = 0;
        for (int i = 0; i < graph1.size(); ++i) {
            auto first = i;
            auto second = current_choice[i];
            if (second == -1) {
                continue;
            }
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
        }
        return score;
    }

    std::vector<int> current_choice;
    std::vector<int> best_choice;
    int max_score = 0;
    int num = 0;
};

} // end namespace graph_diff::algorithm
