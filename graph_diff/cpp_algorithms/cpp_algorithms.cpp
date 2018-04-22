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
                        'ant_algorithm/cubed_pathfinder/pathfinder.hpp',
                        'ant_algorithm/cubed_pathfinder/pheromon_table.hpp',
                        'ant_algorithm/utils.hpp']
%>
*/
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <iostream>

#include "graph.hpp"
#include "baseline_algorithms_using.hpp"
#include "ant_algorithm_using.hpp"


using graph_diff::algorithm::AntAlgorithm;

template <typename T> using node = std::pair<T, size_t>;

template <typename T, typename Algorithm>
auto algorithm(std::vector<node<size_t>> nodes1,
               std::vector<std::vector<size_t>> adjacent_list1,
               std::vector<node<size_t>> nodes2,
               std::vector<std::vector<size_t>> adjacent_list2) {
    auto graph1 = graph_diff::graph::Graph<T>(nodes1, adjacent_list1);
    auto graph2 = graph_diff::graph::Graph<T>(nodes2, adjacent_list2);

    auto best_choice = Algorithm().construct_diff(graph1, graph2);

    return best_choice;
}

PYBIND11_MODULE(cpp_algorithms, m) {
    m.doc() = "Cpp graph diff algorithms imported into python";
    m.def("baseline_algorithm", &algorithm<size_t, BaselineAlgorithm>);
    m.def("ant_algorithm", &algorithm<size_t, AntAlgorithm<CubedPathfinder>>);
    m.def("lin_ant_algorithm", &algorithm<size_t, AntAlgorithm<LinearPathfinder>>);
    m.def("baseline_with_chop_algorithm", &algorithm<size_t, BaselineWithChopAlgorithm>);
    m.def("baseline_algorithm_omp", &algorithm<size_t, BaselineAlgorithmOmp>);
    m.def("baseline_with_chop_algorithm_omp", &algorithm<size_t, BaselineWithChopAlgorithmOmp>);
}

