/*cppimport
<%
setup_pybind11(cfg)
cfg['compiler_args'] = ['-std=c++1z', '-stdlib=libc++']
cfg['compiler_args'] += ['-Xpreprocessor', '-fopenmp']
cfg['linker_args'] = ['-lomp']
cfg['include_dirs'] = ['ant_algorithm', 'baseline_algorithm']
cfg['dependencies'] = ['baseline_algorithms_using.hpp',
                       'baseline_algorithms.hpp',
                       'baseline_algorithms/baseline_algorithm.hpp',
                       'baseline_algorithms/baseline_algorithm_omp.hpp',
                       'baseline_algorithms/baseline_with_chop_algorithm.hpp',
                       'baseline_algorithms/baseline_with_chop_algorithm_omp.hpp']
cfg['dependencies'] += ['ant_algorithm/ant_parameters.hpp',
                        'ant_algorithm/ant_algorithm.hpp',
                        'ant_algorithm/graph_stat.hpp',
                        #'ant_algorithm/cubed_pathfinder/pathfinder.hpp',
                        #'ant_algorithm/cubed_pathfinder/pheromon_table.hpp',
                        'ant_algorithm/utils.hpp']
%>
*/
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "graph.hpp"
#include "baseline_algorithms_using.hpp"
#include "ant_algorithm_using.hpp"


using graph_diff::algorithm::AntAlgorithm;

template <typename T> using node = std::pair<T, size_t>;

/**
 * Runs given algorithm on passed graphs. Graphs are represented
 *  in two vectors
 * @param   nodes1          nodes of the first graph
 * @param   adjacent_list2  list of adjacency of the first graph
 * @param   nodes1          nodes of the second graph
 * @param   adjacent_list2  list of adjacency of the second graph
 */
template <typename Algorithm>
auto algorithm(std::vector<node<size_t>> nodes1,
               std::vector<std::vector<size_t>> adjacent_list1,
               std::vector<node<size_t>> nodes2,
               std::vector<std::vector<size_t>> adjacent_list2) {
    auto graph1 = graph_diff::graph::Graph<size_t>(nodes1, adjacent_list1);
    auto graph2 = graph_diff::graph::Graph<size_t>(nodes2, adjacent_list2);

    auto best_choice = Algorithm().construct_diff(graph1, graph2);

    return best_choice;
}

/**
 * Imported into python module. All functions take arguments as {algorithm} function
 * Functions provided by the module:
 *  - baseline_algorithm
 *  - baseline_with_chop_algorithm
 *  - baseline_algorithm_omp
 *  - baseline_with_chop_algorithm_omp
 *  - ordered_ant_algorithm
 *  - unordered_ant_algorithm
 */
PYBIND11_MODULE(cpp_algorithms, m) {
    m.doc() = "Cpp graph diff algorithms imported into python";
    m.def("baseline_algorithm",                 &algorithm<BaselineAlgorithm>);
    m.def("baseline_with_chop_algorithm",       &algorithm<BaselineWithChopAlgorithm>);
    m.def("baseline_algorithm_omp",             &algorithm<BaselineAlgorithmOmp>);
    m.def("baseline_with_chop_algorithm_omp",   &algorithm<BaselineWithChopAlgorithmOmp>);
    m.def("ordered_ant_algorithm",              &algorithm<AntAlgorithm<OrderedPathfinder>>);
    m.def("unordered_ant_algorithm",            &algorithm<AntAlgorithm<UnorderedPathfinder>>);
}

