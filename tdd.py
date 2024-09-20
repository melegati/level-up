import sys
import argparse
import os

from DeveloperAIHandler import DeveloperAIHandler, TEST_FAILED, TEST_PASSED
from utils import str2bool, how_many_to_skip

sys.path.append("..")

class TDDRunner():

    def __init__(self, test_file, code_file, full_context, print_context, print_message, max_number_repetitions):

        # Use variables
        openAI_key = os.getenv('OPEN_AI_KEY')
        self.handler = DeveloperAIHandler(
            openAI_key,
            test_file,  
            code_file,
            full_context,  # send always the full context
            print_context,  # print the context
            print_message  # print the message from OpenAI
        )
        self.max_number_repetitions = max_number_repetitions
        self.skip = how_many_to_skip(code_file) + 1

    def run(self):
        result = self.handler.execute_tests()

        if result == TEST_PASSED:
            print("The test case is already fulfilled, the code was not modified by ChatGPT.")
            return

        counter = 0
        self.handler.backup_code_file(self.skip)
        while counter < self.max_number_repetitions:
            counter += 1
            self.handler.send_message(self.handler.create_tdd_prompt(), "{}_{}".format(self.skip, counter))
            self.handler.save_response_to_code_file()
            result = self.handler.execute_tests()

            if result == TEST_PASSED:
                print("Test case passed! You can inspect the updated code now!")
                break
            if result == TEST_FAILED:
                print("Test failed! Resending it to ChatGPT...")

        if result == TEST_FAILED:
            self.handler.restore_code_file(self.skip)


def params():
    parser = argparse.ArgumentParser(description='Description of your program.')

    # Add arguments
    parser.add_argument('--test_file', type=str, help='Path to the file with the tests.', default='test.py')
    parser.add_argument('--code_file', type=str, help='Path to the file with the code.', default='prod.py')
    parser.add_argument('--full_context', type=str2bool, help='sending the full context to OpenAI.', default=False)
    parser.add_argument('--print_context', type=str2bool, help='Printing the context before the it is send.',
                        default=False)
    parser.add_argument('--print_message', type=str2bool, help='Printing the message received from OpenAI.',
                        default=False)
    parser.add_argument('--max_number_repetitions', type=int,
                        help='Maximum number of chances given to OpenAI for solving a test case.', default=5)

    # Parse the command-line arguments
    return parser.parse_args()


if __name__ == '__main__':
    parser = params()

    runner = TDDRunner(
        parser.test_file,
        parser.code_file,
        parser.full_context,
        parser.print_context,
        parser.print_message,
        parser.max_number_repetitions
    )

    runner.run()