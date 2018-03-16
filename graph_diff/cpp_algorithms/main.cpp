#include "baseline_algorithm.hpp"
#include "baseline_with_chop_algorithm.hpp"

using graph_diff::graph::read_graph;
using namespace std;
using graph_diff::algorithm::BaselineAlgorithm;
using graph_diff::algorithm::BaselineWithChopAlgorithm;

int main() {
	auto graph1 = read_graph<int>();
	auto graph2 = read_graph<int>();

	auto best_choice = Algorithm().construct_diff(graph1, graph2);

	for (int i = 0; i < best_choice.size(); ++i) {
		cout << i << ' ' << best_choice[i] << endl;
	}

	return 0;
}
