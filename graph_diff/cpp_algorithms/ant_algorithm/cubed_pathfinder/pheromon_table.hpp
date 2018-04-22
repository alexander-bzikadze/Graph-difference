#pragma once

#include "../pheromon_table.hpp"

namespace graph_diff::algorithm::cubed_pathfinder {

template <typename T>
class PheromonTable : public graph_diff::algorithm::PheromonTable<T, T, T, T> {
public:
    using father_class = graph_diff::algorithm::PheromonTable<T, T, T, T>;
    PheromonTable() = default;

    void update(std::vector<long long> const& choice, double addition) {
        for (size_t j = 0; j < choice.size(); ++j) {
            for (size_t k = 0; k < choice.size(); ++k) {
                father_class::add_update(j, choice.at(j), k, choice.at(k), addition);
            }
        }
        father_class::next_interation();
    }
};

}