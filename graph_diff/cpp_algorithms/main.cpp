#include "baseline_algorithm.hpp"
#include "baseline_with_chop_algorithm.hpp"
#include "baseline_algorithm_omp.hpp"
#include "baseline_with_chop_algorithm_omp.hpp"
#include "ant_algorithm/ant_algorithm.hpp"

using graph_diff::graph::read_graph;
using std::cout;
using std::endl;
using graph_diff::algorithm::BaselineAlgorithm;
using graph_diff::algorithm::BaselineWithChopAlgorithm;
using graph_diff::algorithm::BaselineAlgorithmOmp;
using graph_diff::algorithm::BaselineWithChopAlgorithmOmp;
using graph_diff::algorithm::AntAlgorithm;

int main() {
	auto graph1 = read_graph<int>();
	auto graph2 = read_graph<int>();

	auto best_choice = Algorithm<>().construct_diff(graph1, graph2);

	for (int i = 0; i < best_choice.size(); ++i) {
		cout << i << ' ' << best_choice[i] << endl;
	}

	graph_diff::algorithm::PheromonTable<int> table;
	graph_diff::algorithm::Pathfinder<int> p(graph1, graph2, table);

	return 0;
}
