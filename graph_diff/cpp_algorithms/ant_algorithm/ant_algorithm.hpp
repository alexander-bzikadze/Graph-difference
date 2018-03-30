#pragma once

#include <unordered_set>
#include <unordered_map>
#include <tuple>
#include <random>

#include "ant_parameters.hpp"
#include "pheromon_table.hpp"
#include "pathfinder.hpp"


constexpr static int NUMBER_OF_ITERATIONS = 128;
constexpr static int NUMBER_OF_AGENTS = 16;
constexpr static int MAX_NUMBER_OF_ITERATIONS_WITH_THE_SAME_SCORE = 8;
namespace graph_diff::algorithm {

template <template <typename> typename Pathfinder = Pathfinder,
          int NUMBER_OF_ITERATIONS = ant_parameters::NUMBER_OF_ITERATIONS,
          int NUMBER_OF_AGENTS = ant_parameters::NUMBER_OF_AGENTS,
          int MAX_NUMBER_OF_ITERATIONS_WITH_THE_SAME_SCORE = 
              ant_parameters::MAX_NUMBER_OF_ITERATIONS_WITH_THE_SAME_SCORE>
class AntAlgorithm {
public:
    template <typename T>
    std::vector<int> construct_diff(graph_diff::graph::Graph<T> const& graph1, 
                                    graph_diff::graph::Graph<T> const& graph2) {
        auto const& graph_minimal = graph1.size() <= graph2.size() ?
            graph1 : graph2;
        auto const& graph_maximal = graph1.size() <= graph2.size() ?
            graph2 : graph1;

        PheromonTable<int> pheromon;
        best_choice.resize(graph_minimal.size(), 0);


        Pathfinder<T> pathfinder(graph_minimal,
                                 graph_maximal,
                                 pheromon);

        for (int i = 0; i < 100; ++i) {
            auto choice = pathfinder.find_path();
            auto chosen_score = score(graph_minimal, graph_maximal, choice);
            if (chosen_score > best_score) {
                best_score = chosen_score;
                std::copy(choice.cbegin(), choice.cend(), best_choice.begin());  
            }
            for (int j = 0; j < choice.size(); ++j) {
                for (int k = 0; k < choice.size(); ++k) {
                    pheromon.add_update(j, choice[j], k, choice[k], 1 / (1 + best_score - chosen_score));
                }
            }
        }

        return best_choice;
    }

    template <typename T>
    int score(graph_diff::graph::Graph<T> const& graph1, 
              graph_diff::graph::Graph<T> const& graph2,
              std::vector<int> const& choice) {
        int score = 0;
        for (int i = 0; i < graph1.size(); ++i) {
            auto first = i;
            auto second = choice[i];
            if (second == -1) {
                continue;
            }
            for (int j = 0; j < graph1.get_adjacent_list(first).size(); ++j) {
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

    int best_score = -1;
    std::vector<int> best_choice;

};

} // end graph_diff::algorithm