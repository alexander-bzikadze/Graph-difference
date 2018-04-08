#pragma once

#include <utility>
#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>

namespace graph_diff::graph {

template <typename T>
class Graph {
public:
    using node = std::pair<T, size_t>;

    Graph() = default;
    Graph(std::vector<node> nodes,
          std::vector<std::vector<size_t>> adjacent_list) :
        _nodes(nodes),
        _adjacent_list(adjacent_list)
    {}

    Graph(Graph&&) = default;
    Graph& operator=(Graph&&) = default;

    auto const& get_nodes() const {
        return _nodes;
    }

    auto const& get_adjacent_list(size_t i) const {
        return _adjacent_list[i];
    }

    auto adjacent_to(size_t i, size_t j) const {
        return _adjacent_list[i][j];
    }

    size_t size() const {
        return _nodes.size();
    }

private:
    std::vector<node> _nodes;
    std::vector<std::vector<size_t>> _adjacent_list;
};


template <typename T>
auto read_graph() {
    // std::ifstream file;
    // file.open ("main.in");

    size_t node_number;
    std::cin >> node_number;

    std::vector<std::pair<size_t, size_t>> nodes(node_number, std::pair<size_t, size_t>());
    std::vector<std::vector<size_t>> adjacent_list(node_number, std::vector<size_t>());

    for (size_t i = 0; i < node_number; ++i) {
        T label;
        size_t number;
        std::cin >> label >> number;
        nodes[i] = {label, number};
    }

    for (size_t i = 0; i < node_number; ++i) {
        size_t number_of_adjacent;
        std::cin >> number_of_adjacent;

        adjacent_list[i].resize(number_of_adjacent);
        for (size_t j = 0; j < number_of_adjacent; ++j) {
            size_t adjacent_node;
            std::cin >> adjacent_node;
            adjacent_list[i][j] = adjacent_node;
        }

        if (number_of_adjacent > 0) {
            std::sort(adjacent_list[i].begin(), adjacent_list[i].end());
        }
    }
    auto graph = Graph<size_t>(std::move(nodes), std::move(adjacent_list));
    return graph;
}

} // end namespace graph
