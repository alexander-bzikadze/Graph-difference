#include "utils.hpp" // std::hash for tuples
#include <cassert>

namespace graph_diff::algorithm {

template <typename T>
class PheromonTable {
public:
    using contained_choice = std::tuple<T, T, T, T>;

    PheromonTable() :
        table(),
        last_update(),
        current_iteration(0)
    {}

    double get_element(T u, T u1, T v, T v1) {
        contained_choice choice = {u, u1, v, v1};
        if (!table.count(choice)) {
            return pow(1 - ant_parameters::P, current_iteration);
        }
        return table.at(choice) * pow(1 - ant_parameters::P, current_iteration - last_update.at(choice));
    }

    void add_update(T u, T u1, T v, T v1, double value) {
        contained_choice choice = {u, u1, v, v1};
        if (!table.count(choice) || !last_update.count(choice)) {
            table[choice] = 1;
            last_update[choice] = 0;
        }
        assert(table.find(choice) != table.cend());
        assert(last_update.find(choice) != last_update.cend());
        table[choice] *= pow(1 - ant_parameters::P, current_iteration - last_update.at(choice));
        table[choice] += value;
        last_update[choice] = current_iteration;
    }

    void next_interation() {
        current_iteration++;
    }

private:
    std::unordered_map<contained_choice, double> table;
    std::unordered_map<contained_choice, int> last_update;
    int current_iteration;
};

}