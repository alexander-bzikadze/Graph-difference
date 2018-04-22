#pragma once

#include "../pheromon_table.hpp"

namespace graph_diff::algorithm::linear_pathfinder {

template <typename T>
class PheromonTable : public graph_diff::algorithm::PheromonTable<T, T> {
public:
    using father_class = graph_diff::algorithm::PheromonTable<T, T>;
    PheromonTable() = default;

    void update(std::vector<long long> const& choice, double addition) {
        for (size_t j = 0; j < choice.size(); ++j) {
        	if (choice[j] != -1) {
            	father_class::add_update(j, choice[j], addition);
        	}
        }
        father_class::next_interation();
    }

    int VAR = 0;
};

} // end of graph::algorithm::linear_pathfinder