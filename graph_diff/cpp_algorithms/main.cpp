#include "baseline_algorithms_using.hpp"
#include "ant_algorithm_using.hpp"
#include <random>

using graph_diff::algorithm::AntAlgorithm;
using std::cout;
using std::endl;

int main() {
	auto graph1 = graph_diff::graph::read_graph<size_t>();
	auto graph2 = graph_diff::graph::read_graph<size_t>();

	for (int i = 0; i < 1; ++i) {
		auto best_choice = Algorithm().construct_diff(graph1, graph2);

		for (size_t i = 0; i < best_choice.size(); ++i) {
			cout << i << ' ' << best_choice[i] << endl;
		}
	}
	return 0;
}
