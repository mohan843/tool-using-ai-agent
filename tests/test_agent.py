import tempfile
import unittest
from pathlib import Path
from agent import SafeCalculator, ToolError, ToolUsingAgent


class SafeCalculatorTests(unittest.TestCase):
    def setUp(self):
        self.calculator = SafeCalculator()

    def test_precedence_and_parentheses(self):
        self.assertEqual(self.calculator.calculate('2 + 3 * (4 - 1)'), 11)

    def test_division(self):
        self.assertEqual(self.calculator.calculate('10 / 4'), 2.5)

    def test_rejects_code_execution(self):
        with self.assertRaises(ToolError):
            self.calculator.calculate("__import__('os').system('echo unsafe')")

    def test_limits_exponent(self):
        with self.assertRaises(ToolError):
            self.calculator.calculate('2 ** 13')


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.data = Path(self.temp.name)
        (self.data / 'notes.txt').write_text('Agents use tools.\nRAG retrieves context.\n', encoding='utf-8')
        self.agent = ToolUsingAgent(self.data)

    def tearDown(self):
        self.temp.cleanup()

    def test_calculator_tool(self):
        self.assertEqual(self.agent.run('calc: 6 * 7'), '6 * 7 = 42')

    def test_search_tool(self):
        self.assertIn('notes.txt:2: RAG retrieves context.', self.agent.run('search: rag'))

    def test_read_tool(self):
        self.assertIn('Agents use tools', self.agent.run('read: notes.txt'))

    def test_blocks_path_traversal(self):
        self.assertIn('limited to the project data directory', self.agent.run('read: ../outside.txt'))

    def test_helpful_unknown_request(self):
        self.assertIn('I can use three tools', self.agent.run('tell me a joke'))


if __name__ == '__main__':
    unittest.main()
