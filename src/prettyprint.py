import compiler.ast
import astvisitor

class PrettyPrint(astvisitor.ASTVisitor):
    """This class pretty prints ASTs
    """

    # Configure how many spaces per indent
    _INDENT_NUM = 2
    # How many characters in a line before it's broken down.
    _LINE_LENGTH = 100

    def prettyPrint(self, ast):
        prettyStr = ""
        if isinstance(ast, list):
            for func in ast:
                prettyStr += self.visit(func, 0, "")
        else:
            prettyStr = self.visit(ast, 0, "")
        return prettyStr

    def _appendIndents(self, str, indent):
        return str + " " * indent * self._INDENT_NUM

    def _appendNodeName(self, str, node):
        return str + node.__class__.__name__ + "(\n"

    def _appendCloseParen(self, str):
        return str + ")\n"

    def default(self, ast, indent, ast_str):
        """The default method for printing a node.
           If the string representation for the current node (ast) is longer
           than _LINE_LENGTH the node gets broken down into parts (its
           children).
        """
        if len(str(ast)) < self._LINE_LENGTH:
            return self._visit_OneLine(ast, indent, ast_str)

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

    def visit_Assign(self, ast, indent, ast_str):
        """This customizes the way Assign nodes are printed.

           This is necessary because getChildNodes doesn't return the tailCall
           attribute. This is added in the tailcallanalysis phase.
        """
        # If the assign has tailCall set to True, then say so:
        if getattr(ast, "tailCall", False):
            ast_str = self._appendIndents(ast_str, indent)
            ast_str += "TAIL CALL. CallerArgNum: %d\n" % ast.callerArgNum
            ast_str = self._visit_OneLine(ast, indent, ast_str)
            return ast_str
        # Otherwise, use the default print routine.
        else:
            return self.default(ast, indent, ast_str)
