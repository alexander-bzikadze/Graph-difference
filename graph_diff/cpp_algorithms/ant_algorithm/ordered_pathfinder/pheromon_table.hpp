#pragma once

#include "../pheromon_table.hpp"

namespace graph_diff::algorithm::ordered_pathfinder {

/**
 * Class used by ordered_pathfinder::Pathfinder
 * Is implementation of graph_diff::algorithm::PheromonTable interface
 *  for ordered ant_algorithm
 */
template <typename T>
class PheromonTable : public graph_diff::algorithm::PheromonTable<T, T> {
public:
    using father_class = graph_diff::algorithm::PheromonTable<T, T>;
    PheromonTable() = default;

    /**
     * Updates contained pheromon table
     * Is crutial method of PheromonTable interface
     * @param   choice      choice made on a iteration of ant_algorithm
     * @param   addition    double value given by the algorithm
     */
    void update(std::vector<long long> const& choice, double addition) {
        for (size_t j = 0; j < choice.size(); ++j) {
        	if (choice[j] != -1) {
            	father_class::add_update(j, choice[j], addition);
        	}
        }
        father_class::next_interation();
    }
};

} // end of graph::algorithm::ordered_pathfinder