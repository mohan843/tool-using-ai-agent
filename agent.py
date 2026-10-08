'''Safe, dependency-free mini-agent with calculator, search, and file tools.'''
import argparse
import ast
import math
import operator
import re
from pathlib import Path


class ToolError(ValueError):
    '''Invalid or unsafe tool request.'''


class SafeCalculator:
    OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod, ast.Pow: operator.pow}
    UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}

    def calculate(self, expression):
        if len(expression) > 160:
            raise ToolError('Expression is too long (max 160 characters).')
        try:
            value = self._eval(ast.parse(expression, mode='eval').body)
        except (SyntaxError, ZeroDivisionError, OverflowError, TypeError) as exc:
            raise ToolError(f'Invalid arithmetic expression: {exc}') from exc
        if not math.isfinite(float(value)):
            raise ToolError('Result must be finite.')
        return value

    def _eval(self, node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if abs(node.value) > 10**12:
                raise ToolError('Numeric literals are limited to 1e12.')
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in self.UNARY:
            return self.UNARY[type(node.op)](self._eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in self.OPS:
            left, right = self._eval(node.left), self._eval(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 12:
                raise ToolError('Exponent magnitude is limited to 12.')
            result = self.OPS[type(node.op)](left, right)
            if abs(result) > 10**100:
                raise ToolError('Result is too large.')
            return result
        raise ToolError('Only numbers, arithmetic operators, and parentheses are allowed.')


class ToolUsingAgent:
    def __init__(self, data_dir=None):
        self.data_dir = Path(data_dir or Path(__file__).parent / 'data').resolve()
        self.calculator = SafeCalculator()
        self.tools = {'calc': self._calculate, 'search': self._search, 'read': self._read}

    def run(self, request):
        request = request.strip()
        if not request:
            return 'Please provide a request, e.g. calc: 12 * 4'
        match = re.match(r'^(calc|calculate|search|find|read|open)\s*:\s*(.*)$', request, re.I)
        if not match:
            match = re.match(r'^(calculate|compute)\s+(.+)$', request, re.I)
            if match:
                tool, argument = 'calc', match.group(2)
            else:
                return "I can use three tools. Try 'calc: 12 * 4', 'search: RAG', or 'read: sample_notes.txt'."
        else:
            alias = {'calculate': 'calc', 'find': 'search', 'open': 'read'}
            tool = alias.get(match.group(1).lower(), match.group(1).lower())
            argument = match.group(2).strip()
        try:
            return self.tools[tool](argument)
        except ToolError as exc:
            return f'Tool error: {exc}'

    def _calculate(self, expression):
        if not expression:
            raise ToolError('Provide an arithmetic expression.')
        return f'{expression} = {self.calculator.calculate(expression)}'

    def _search(self, query):
        if not query:
            raise ToolError('Provide a search term.')
        hits = []
        for path in sorted(self.data_dir.glob('*.txt')):
            for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
                if query.casefold() in line.casefold():
                    hits.append(f'{path.name}:{number}: {line.strip()}')
        return '\n'.join(hits) if hits else f"No matches found for '{query}'."

    def _read(self, relative_path):
        if not relative_path:
            raise ToolError('Provide a relative file path, e.g. sample_notes.txt.')
        path = (self.data_dir / relative_path).resolve()
        if path != self.data_dir and self.data_dir not in path.parents:
            raise ToolError('File access is limited to the project data directory.')
        if not path.is_file():
            raise ToolError(f'File not found in data directory: {relative_path}')
        if path.suffix.lower() not in {'.txt', '.md', '.csv'}:
            raise ToolError('Only .txt, .md, and .csv files can be read.')
        return path.read_text(encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Run a safe tool-using mini-agent.')
    parser.add_argument('request', nargs='*', help='calc: EXPR | search: TERM | read: FILE')
    args = parser.parse_args()
    if not args.request:
        parser.print_help()
        return
    print(ToolUsingAgent().run(' '.join(args.request)))


if __name__ == '__main__':
    main()
