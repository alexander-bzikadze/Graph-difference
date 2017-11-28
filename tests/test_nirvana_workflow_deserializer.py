import json
import unittest

from nirvana_object_model import workflow_deserializer


class NirvanaWorkflowDeserializerTest(unittest.TestCase):
    def deserialization_should_work_correctly_with_repeating_blocks(self):
        actual = ''
        with open('process_instance.json') as f:
            workflow = workflow_deserializer.deserialize(json.loads(f.read()))
            for connection in workflow.items():
                (source_block, source_block_count, source_name) = connection[0]
                for target in connection[1]:
                    (target_block, target_block_count, target_name) = target
                    actual += '%s (№%s) %s -> %s (№%s) %s\n' % (
                        source_block.operation.operation_id, source_block_count, source_name,
                        target_block.operation.operation_id, target_block_count, target_name
                    )
        print(actual)
        with open('process_instance_pretty.txt', 'r') as f:
            expected = f.read()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
