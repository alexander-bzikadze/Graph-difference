#pragma once

#include <utility>
#include <iostream>
#include <vector>
#include <algorithm>

namespace graph_diff::graph {

template <typename T>
class Graph {
public:
    using node = std::pair<T, int>;

    Graph() = default;
    Graph(std::vector<node> nodes,
          std::vector<std::vector<int>> adjacent_list) :
        _nodes(std::move(nodes)),
        _adjacent_list(std::move(adjacent_list))
    {}

    Graph(Graph&&) = default;
    Graph& operator=(Graph&&) = default;

    std::vector<node> const& get_nodes() const {
        return _nodes;
    }

    std::vector<std::vector<int>> const& get_adjacent_list() const {
        return _adjacent_list;
    }

private:
    std::vector<node> _nodes;
    std::vector<std::vector<int>> _adjacent_list;
};


template <typename T>
Graph<T> read_graph() {
    int node_number;
    std::cin >> node_number;

    std::vector<std::pair<int, int>> nodes(node_number);
    std::vector<std::vector<int>> adjacent_list(node_number);

    for (int i = 0; i < node_number; ++i) {
        T label;
        int number;
        std::cin >> label >> number;
        nodes[i] = {label, number};
    }

    for (int i = 0; i < node_number; ++i) {
        int number_of_adjacent;
        std::cin >> number_of_adjacent;

        adjacent_list[i].resize(number_of_adjacent);
        for (int j = 0; j < number_of_adjacent; ++j) {
            int adjacent_node;
            std::cin >> adjacent_node;
            adjacent_list[i][j] = adjacent_node;
        }

        if (number_of_adjacent > 0) {
            std::sort(adjacent_list[i].begin(), adjacent_list[i].end());
        }
    }
    auto graph = Graph<int>(std::move(nodes), std::move(adjacent_list));
    return std::move(graph);
}

} // end namespace graph
