import compiler.ast
import astvisitor

class PrettyPrint(astvisitor.ASTVisitor):
    """This class pretty prints ASTs
    """

    # Configure how many spaces per indent
    _INDENT_NUM = 2

    def prettyPrint(self, ast):
        return self.visit(ast, 0, "")

    def _appendIndents(self, str, indent):
        return str + " " * indent * self._INDENT_NUM

    def _appendNodeName(self, str, node):
        return str + node.__class__.__name__ + "(\n"

    def _appendCloseParen(self, str):
        return str + ")\n"

    def default(self, ast, indent, ast_str):
        ast_str = self._appendIndents(ast_str, indent)
        ast_str = self._appendNodeName(ast_str, ast)
        for child in ast.getChildNodes():
            ast_str = self.visit(child, indent + 1, ast_str)
        ast_str = self._appendIndents(ast_str, indent)
        ast_str = self._appendCloseParen(ast_str)
        return ast_str

    def _visit_OneLine(self, ast, indent, ast_str):
        """A helper function that prints out a node in one line"""
        ast_str= self._appendIndents(ast_str, indent)
        ast_str += str(ast) + "\n"
        return ast_str

    def visit_Const(self, *args):
        return self._visit_OneLine(*args)

    def visit_Name(self, *args):
        return self._visit_OneLine(*args)

    def visit_AssName(self, *args):
        return self._visit_OneLine(*args)

    def visit_Add(self, *args):
        return self._visit_OneLine(*args)

