#pragma once

#include <vector>


namespace graph_diff::algorithm {

/**
 * Class for getting graph statistic
 * Its use is not scientificly stated
 * Works in assumption that graph nodes
 *  that should be matched look alike
 */
template <typename T>
class GraphStat {
public:
    GraphStat(graph::Graph<T> const& graph1,
              graph::Graph<T> const& graph2) :
              in1(graph1.size(), 0),
              in2(graph2.size(), 0),
              out1(graph1.size(), 0),
              out2(graph2.size(), 0),
              statistic_factor(graph1.size() * graph2.size(), 1) {
        for (size_t i = 0; i < graph1.size(); ++i) {
            auto first = i;
            for (auto second : graph1.get_adjacent_list(first)) {
                in1[second]++;
            }

            out1[first] = graph1.get_adjacent_list(first).size();
        }

        for (size_t i = 0; i < graph2.size(); ++i) {
            auto first = i;
            for (auto second : graph2.get_adjacent_list(first)) {
                in2[second]++;
            }

            out2[first] = graph2.get_adjacent_list(first).size();
        }

        for (size_t i = 0; i < graph1.size() * graph2.size(); ++i) {
            auto [first, second] = to_2d_address(i, graph2.size());
            if (graph1.get_nodes()[first].first != graph2.get_nodes()[second].first) {
                statistic_factor[i] = 0;
                continue;
            }
            statistic_factor[i] += std::abs((long long)(in1[first] - in2[second])) + abs((long long)(out1[first] - out2[second]));
            statistic_factor[i] = 1 / statistic_factor[i];
        }
    }

    /**
     * @param   coordinates of the nodes
     * @return  value in (0, 1] how alike are given nodes
     */
    inline auto get_statistic(size_t i) const {
        return statistic_factor[i];
    }

private:
    std::vector<size_t> in1;
    std::vector<size_t> in2;
    std::vector<size_t> out1;
    std::vector<size_t> out2;

    std::vector<double> statistic_factor;

    inline auto to_1d_address(size_t i, size_t j, size_t step) const { return i * step + j; }
    inline auto to_2d_address(size_t i, size_t step) const { 
        return std::make_tuple(i / step, i % step); 
    }
};

}