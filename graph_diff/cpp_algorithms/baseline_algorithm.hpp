#include <iostream>

#include "graph.hpp"

namespace graph_diff::algorithm {

class BaselineAlgorithm {
public:
	template <typename T>
	std::vector<int> const& construct_diff(
			graph_diff::graph::Graph<T> const& graph1, 
			graph_diff::graph::Graph<T> const& graph2) {
		current_choice.clear();
		current_choice.resize(graph1.get_nodes().size() + graph2.get_nodes().size());

		best_choice.clear();
		best_choice.resize(graph1.get_nodes().size());

		for (int i = 0; i < graph2.get_nodes().size(); ++i) {
			current_choice[i] = i;
		}
		for (int i = 0, k = graph2.get_nodes().size(); i < graph1.get_nodes().size(); ++i) {
			current_choice[i + k] = -1;
		}

		start_brute_search(graph1, graph2);
		return best_choice;
	}

private:
	template <typename T>
	void start_brute_search(
			graph_diff::graph::Graph<T> const& graph1, 
			graph_diff::graph::Graph<T> const& graph2) {
		auto score_function = [this, &graph1, &graph2]() { 
			return this->score(graph1, graph2); 
		};
		auto stop_function = [&graph1, &graph2](int i, int j) { 
			return j != -1 && graph1.get_nodes()[i].first != graph2.get_nodes()[j].first; 
		};
		bruteforce_search(score_function, 
			stop_function, 
			0,
			graph2.get_nodes().size(),
			graph1.get_nodes().size());
	}

	template <typename ScoreFunc, typename StopFunc>
	void bruteforce_search(
			ScoreFunc const& score_function, 
			StopFunc const& stop_function, 
			int current_position,
			int last_position,
			int choice_size) {
		if (current_position == choice_size) {
			auto score = score_function();
			if (score > max_score) {
				copy(current_choice.cbegin(), current_choice.cend(), best_choice.begin());
				max_score = score;
			}
			return;
		}

		for (int i = current_position; i < last_position; ++i) {
			if (stop_function(i, current_choice[i])) {
				continue;
			}

			std::swap(current_choice[i], current_choice[current_position]);
			bruteforce_search( score_function, 
				stop_function, 
				current_position + 1, 
				last_position, 
				choice_size);
			std::swap(current_choice[i], current_choice[current_position]);
		}

		std::swap(current_choice[current_position], current_choice[last_position]);
		bruteforce_search(score_function, 
			stop_function, 
			current_position + 1, 
			last_position + 1, 
			choice_size);
		std::swap(current_choice[current_position], current_choice[last_position]);
	}

	template <typename T>
	int score(
			graph_diff::graph::Graph<T> const& graph1, 
			graph_diff::graph::Graph<T> const& graph2) {
		int score = 0;
		for (int i = 0; i < graph1.get_nodes().size(); ++i) {
			auto first = i;
			auto second = current_choice[i];
			if (second == -1) {
				continue;
			}
			auto& first_adjacent = graph1.get_adjacent_list()[first];
			auto& second_adjacent = graph2.get_adjacent_list()[second];

			for (int j = 0; j < first_adjacent.size(); ++j) {
				auto mapped = current_choice[first_adjacent[j]];
				if (mapped != -1 
					&& std::binary_search(second_adjacent.cbegin(), 
						second_adjacent.cend(), 
						mapped)) {
					score++;
				}
			}
		}
		return score;
	}

	std::vector<int> current_choice;
	std::vector<int> best_choice;
	int max_score = 0;
};

} // end namespace graph_diff::algorithm
