#pragma once

#include <utility>
#include <iostream>
#include <vector>
#include <algorithm>


namespace graph_diff::graph {

/**
 * Class container for labeld graph represented
 * as vector of pairs and vector of adjacency lists
 */
template <typename T>
class Graph {
public:
    using node = std::pair<T, size_t>;

    Graph() = default;
    Graph(std::vector<node> nodes,
          std::vector<std::vector<size_t>> adjacent_list) :
        _nodes(nodes),
        _adjacent_list(adjacent_list) {
            for (auto& vec : _adjacent_list) {
                std::sort(vec.begin(), vec.end());
            }
        }

    Graph(Graph&&) = default;
    Graph& operator=(Graph&&) = default;

    /**
     * @return  vector of contained nodes,
     *  represented as pairs {Label, Number}
     */
    auto const& get_nodes() const {
        return _nodes;
    }

    /**
     * @param   number of node
     * @return  vector of numbers of nodes,
     *  adjacent to given
     */
    auto const& get_adjacent_list(size_t i) const {
        return _adjacent_list[i];
    }

    /**
     * @param   i   number of the first node
     * @param   j   number of the second node
     * @return  if i is adjacent to j
     */
    auto is_adjacent(size_t i, size_t j) const {
        return std::binary_search(_adjacent_list[i].cbegin(),
                                  _adjacent_list[i].cend(),
                                  j);
    }
    /**
     * @return  number of nodes contained
     */
    size_t size() const {
        return _nodes.size();
    }

private:
    std::vector<node> _nodes;
    std::vector<std::vector<size_t>> _adjacent_list;
};


/**
 * Reads graph from console. Graph must be represented as follows:
 *      {number_of_nodes:n}
 *      {Label_1, Node_1}
 *      ...
 *      {Label_n, Node_n}
 *      {Number_of_adjacent_to_1_nodes}
 *      {Number_of_adjacent_node}
 *      ...
 *      {Number_of_adjacent_node}
 *      ...
 *      {Number_of_adjacent_to_n_nodes}
 *      {Number_of_adjacent_node}
 *      ...
 *      {Number_of_adjacent_node}
 * @return  graph object constracted from cin imput
 */
template <typename T> auto read_graph() {
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
    return Graph<size_t>(std::move(nodes), std::move(adjacent_list));
}

} // end namespace graph_diff::graph
