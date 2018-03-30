#include "ant_parameters.hpp"

namespace graph_diff::algorithm {

template<typename T>
class Pathfinder {
public:
    using edge = std::tuple<int, int>;
    using match = std::tuple<int, int>;

    Pathfinder(graph::Graph<T> const& graph1, 
               graph::Graph<T> const& graph2,
               PheromonTable<int>& pheromon) :
               graph1(graph1),
               graph2(graph2),
               sizes(graph1.size(), graph2.size()),
               pheromon(pheromon),
               edges(std::vector<char>(graph1.size() * graph1.size(), 0),
                     std::vector<char>(graph2.size() * graph2.size(), 0)),
               score(0),
               best_choice(std::min(graph1.size(), graph2.size()), 0),
               probabilities(graph1.size() * graph2.size(), 0),
               phero_factors(graph1.size() * graph2.size(), 0),
               score_factors(graph1.size() * graph2.size(), 1),
               generator(std::random_device()()) {
        for (int i = 0; i < graph1.size(); ++i) {
            for (int j = 0; j < graph1.get_adjacent_list(i).size(); ++j) {
                std::get<0>(edges)[i * graph1.size() + j] = true;
            }
        }

        for (int i = 0; i < graph2.size(); ++i) {
            for (int j = 0; j < graph2.get_adjacent_list(i).size(); ++j) {
                std::get<1>(edges)[i * graph2.size() + j] = true;
            }
        }
    }

    auto find_path() {
        phero_factors.clear();
        phero_factors.resize(graph1.size() * graph2.size(), 0);
        score_factors.clear();
        score_factors.resize(graph1.size() * graph2.size(), 0);
        for (int i = 0; i < score_factors.size(); ++i) {
            auto [first, second] = to_2d_address(i);
            score_factors[i] = graph1.get_nodes()[first].first == graph2.get_nodes()[second].first ;
        }
        std::vector<int> choice(graph1.size(), -1);

        std::uniform_int_distribution<> dis(0, graph_size<0>() * graph_size<1>() - 1);
        auto first_choice = dis(generator);
        auto [choice_from_first, choice_from_second] = to_2d_address(first_choice);

        choice[choice_from_first] = choice_from_second;

        update_probs(choice_from_first, choice_from_second);

        // prob - array of partial sums;
        for (int i = 1; i < graph_size<0>(); ++i) {
            find_pair(choice);
        }
        return choice;
    }

    void update_probs(int chosen_first, 
                      int chosen_second) {
        for (int i = 0; i < graph_size<1>(); ++i) {
            score_factors[to_1d_address(i, chosen_second)] = 0;
            score_factors[to_1d_address(chosen_first, i)] = 0;
        }

        auto upper_size = probabilities.size();
        double acc = 0;
        for (int i = 0; i < upper_size; ++i) {
            auto [from_first, from_second] = to_2d_address(i);

            if (contains_edge<0>(from_first, chosen_first) 
                && contains_edge<1>(from_second, chosen_second)
                && score_factors[i] > 0) {
                score_factors[i]++;
            }
            if (contains_edge<0>(chosen_first, from_first) 
                && contains_edge<1>(chosen_second, from_second)
                && score_factors[i] > 0) {
                score_factors[i]++;
            }

            auto pher = pheromon.get_element(from_first, 
                                             from_second, 
                                             chosen_first, 
                                             chosen_second);
            phero_factors[i] += pher;
            acc += pow(phero_factors[i], ant_parameters::ALPHA) * pow(score_factors[i], ant_parameters::BETA);
            probabilities[i] = acc;
        }
        acc_sum = probabilities.back();
    }

    void find_pair(std::vector<int>& choice) {
        std::uniform_real_distribution<> dis(0, acc_sum);
        auto value = dis(generator);
        auto chosen = std::upper_bound(probabilities.cbegin(), probabilities.cend(), value);
        int chosen_position = chosen - probabilities.cbegin();

        auto [chosen_first, chosen_second] = to_2d_address(chosen_position);

        choice[chosen_first] = chosen_second;

        update_probs(chosen_first, chosen_second);

    }

private:
    graph::Graph<T> const& graph1;
    graph::Graph<T> const& graph2;

    std::tuple<unsigned long long, unsigned long long> sizes;
    template <int n>
    inline auto graph_size() { return std::get<n>(sizes); }

    PheromonTable<int> pheromon;

    std::tuple<std::vector<char>, std::vector<char>> edges;

    inline auto to_1d_address(int i, int j) { return i * graph_size<1>() + j; }
    inline auto to_2d_address(int i) { 
        return std::make_tuple(i / graph_size<1>(), i % graph_size<1>()); 
    }

    template <int n>
    inline bool contains_edge(int i, int j) {
        return std::get<n>(edges)[i * std::get<n>(sizes) + j];
    }

    int score;
    std::vector<int> best_choice;

    std::vector<double> probabilities;
    std::vector<double> phero_factors;
    std::vector<double> score_factors;

    std::mt19937 generator;
    double acc_sum = 0;
};

}