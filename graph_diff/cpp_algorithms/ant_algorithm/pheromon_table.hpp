#pragma once

#include "utils.hpp" // std::hash for tuples
#include <cassert>
#include <map>

#include "ant_parameters.hpp"


namespace graph_diff::algorithm {

/**
 * Interface class for PhermonTable used in AntAlgorithm
 * Update method is crutial to be implemented by the successors
 */
template <typename ...Args>
class PheromonTable {
public:
    using contained_choice = std::tuple<Args...>;

    PheromonTable() :
        table(),
        last_update(),
        pows(),
        current_iteration(0) {
        pows.reserve(graph_diff::algorithm::ant_parameters::NUMBER_OF_ITERATIONS);
        pows.push_back(1);
    }

    /**
     * @param   coordinates in the table
     * @return  return contained there value as lazy as possible
     */
    double get_element(Args... args) const {
        auto choice = std::forward_as_tuple(args...);
        if (!table.count(choice)) {
            return pows[current_iteration];
        }
        return table.at(choice) * pows[current_iteration - last_update.at(choice)];
    }

protected:
    /**
     * Add given value to given coordinates lazy as possible
     * @param   coordinates
     * @param   value to add
     */
    void add_update(Args... args, double value) {
        auto choice = std::forward_as_tuple(args...);
        if (table.find(choice) == table.cend() || last_update.find(choice) == last_update.cend()) {
            table.emplace(choice, 1);
            last_update.emplace(choice, 0);
        }
        assert(table.find(choice) != table.cend());
        assert(last_update.find(choice) != last_update.cend());
        table.at(choice) *= pows[current_iteration - last_update.at(choice)];
        table[choice] += value;
        last_update.at(choice) = current_iteration;
    }

    /**
     * Lazy travel to next iteration
     */
    void next_interation() {
        current_iteration++;
        pows.push_back(pows.back() * (1 - graph_diff::algorithm::ant_parameters::P));
    }

private:
    std::map<contained_choice, double> table;
    std::map<contained_choice, size_t> last_update;
    std::vector<double> pows;
    size_t current_iteration;
};

}