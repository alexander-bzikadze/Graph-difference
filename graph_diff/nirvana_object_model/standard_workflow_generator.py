import random
from collections import defaultdict

import numpy.random
import math

from graph_diff.nirvana_object_model.block import Block
from graph_diff.nirvana_object_model.operation import Operation
from graph_diff.nirvana_object_model.workflow import Workflow
from graph_diff.nirvana_object_model.workflow_generator import WorkflowGenerator


class StandardWorkflowGenerator(WorkflowGenerator):
    LENGTH_OF_STRINGS = 10

    def __init__(self,
                 min_block_num=2,
                 max_block_num=30,
                 min_input_output_number=0,
                 max_input_output_number=3,
                 min_key_value_number=0,
                 max_key_value_number=10,
                 block_number_expectation=None):
        self.min_block_num = min_block_num
        self.max_block_num = max_block_num
        self.min_key_value_number = min_key_value_number
        self.max_key_value_number = max_key_value_number
        self.min_input_output_number = min_input_output_number
        self.max_input_output_number = max_input_output_number
        if block_number_expectation is None:
            self.node_number_expectation = max_block_num * 0.3
        else:
            self.node_number_expectation = block_number_expectation

    def generate_workflow(self):
        workflow = Workflow()

        # Expectation is equal to self.node_number_expectation
        block_number = numpy.random.geometric(p=1 / self.node_number_expectation) + 1
        block_number = max(self.min_block_num, block_number)
        block_number = min(self.max_block_num, block_number)

        a_label_number = 1
        # Mode for number of labels is 20% of numbers of the nodes.
        mode_label_number = math.ceil((block_number - 1) / 5)
        b_label_number = block_number

        types_of_block_number = int(math.ceil(numpy.random.triangular(
            left=a_label_number,
            mode=mode_label_number,
            right=b_label_number
        )))

        types_of_block = []
        for _ in range(0, types_of_block_number):
            operation_id = str(random.randint(0, types_of_block_number // 2))
            input_number = numpy.random.randint(
                self.max_input_output_number - self.min_input_output_number) + self.min_input_output_number
            output_number = numpy.random.randint(
                self.max_input_output_number - self.min_input_output_number) + self.min_input_output_number
            inputs = [str(random.randint(0, types_of_block_number // 2)) for _
                      in range(0, input_number)]
            outputs = [str(random.randint(0, types_of_block_number // 2)) for _
                       in range(0, output_number)]

            key_value = numpy.random.randint(
                self.max_key_value_number - self.min_key_value_number) + self.min_key_value_number
            key_values = {str(random.randint(0, types_of_block_number // 2)):
                          str(random.randint(0, types_of_block_number // 2))
                          for _ in range(0, key_value)}
            types_of_block.append(Block(
                operation=Operation(
                    operation_id=operation_id,
                    inputs=inputs,
                    outputs=outputs),
                options=key_values
            ))

        print()
        block_types = numpy.random.multinomial(n=block_number,
                                               pvals=[1 / types_of_block_number] * types_of_block_number)

        block_types = sum([
            [i] * value for i, value in enumerate(block_types)
        ], [])
        random.shuffle(block_types)

        for i in block_types:
            block_number = workflow.add_block(types_of_block[i])
            previous_block_numbers = defaultdict(int)
            for prev_block in workflow:
                previous_block_numbers[prev_block] += 1
                if 1 == numpy.random.randint(2) and types_of_block[i] is not prev_block:
                    workflow.add_connection_by_execution(
                        from_block=prev_block,
                        from_number=previous_block_numbers[prev_block],
                        to_block=types_of_block[i],
                        to_number=block_number
                    )
                elif 1 == numpy.random.randint(2) \
                        and types_of_block[i] is not prev_block \
                        and len(types_of_block[i].operation.inputs) > 0 \
                        and len(prev_block.operation.outputs) > 0:
                    input_nest = random.choice(types_of_block[i].operation.inputs)
                    output_nest = random.choice(prev_block.operation.outputs)
                    workflow.add_connection_by_data(
                        from_block=prev_block,
                        from_number=previous_block_numbers[prev_block],
                        output_nest=output_nest,
                        to_block=types_of_block[i],
                        to_number=block_number,
                        input_nest=input_nest
                    )

        return workflow
