#pragma once

#include "../pheromon_table.hpp"


namespace graph_diff::algorithm::cubed_pathfinder {

/**
 * Class used by cubed_pathfinder::Pathfinder
 * Is implementation of graph_diff::algorithm::PheromonTable interface
 *  for cubed ant_algorithm
 */
template <typename T>
class PheromonTable : public graph_diff::algorithm::PheromonTable<T, T, T, T> {
public:
    using father_class = graph_diff::algorithm::PheromonTable<T, T, T, T>;
    PheromonTable() = default;

    /**
     * Updates contained pheromon table
     * Is crutial method of PheromonTable interface
     * @param   choice      choice made on a iteration of ant_algorithm
     * @param   addition    double value given by the algorithm
     */
    void update(std::vector<long long> const& choice, 
                double addition) {
        for (size_t j = 0; j < choice.size(); ++j) {
            for (size_t k = 0; k < choice.size(); ++k) {
                father_class::add_update(j, choice.at(j), k, choice.at(k), addition);
            }
        }
        father_class::next_interation();
    }
};

}