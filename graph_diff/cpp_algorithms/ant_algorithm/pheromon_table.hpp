#include "utils.hpp" // std::hash for tuples
#include <cassert>
#include <map>

#include "ant_parameters.hpp"

namespace graph_diff::algorithm {

template <typename T>
class PheromonTable {
public:
    using contained_choice = std::tuple<T, T, T, T>;

    PheromonTable() :
        table(),
        last_update(),
        pows(),
        current_iteration(0)
    {
        // table.reserve(ant_parameters::NUMBER_OF_ITERATIONS * 10000);
        // last_update.reserve(ant_parameters::NUMBER_OF_ITERATIONS * 10000);
        pows.reserve(ant_parameters::NUMBER_OF_ITERATIONS);
        pows.push_back(1);
    }

    double get_element(T u, T u1, T v, T v1) const {
        contained_choice choice = {u, u1, v, v1};
        if (!table.count(choice)) {
            return pows[current_iteration];
        }
        return table.at(choice) * pows[current_iteration - last_update.at(choice)];
    }

    void add_update(T u, T u1, T v, T v1, double value) {
        contained_choice choice = {u, u1, v, v1};
        if (table.find(choice) == table.cend() || last_update.find(choice) == last_update.cend()) {
            table.emplace(choice, 1);
            last_update.emplace(choice, 0);
        }
        assert(table.find(choice) != table.cend());
        assert(last_update.find(choice) != last_update.cend());
        table.at(choice) *= pows[current_iteration - last_update.at(choice)];
        table.at(choice) += value;
        last_update.at(choice) = current_iteration;
    }

    void next_interation() {
        current_iteration++;
        pows.push_back(pows.back() * (1 - ant_parameters::P));
    }

private:
    std::map<contained_choice, double> table;
    std::map<contained_choice, size_t> last_update;
    std::vector<double> pows;
    size_t current_iteration;
};

}