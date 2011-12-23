import astvisitor

class PrettyPrint(astvisitor.ASTVisitor):
    """This class pretty prints ASTs
    """

    def prettyPrint(self, ast):
        self.visit(ast, 0, "")

    def _appendIndents(self, str, indent):
        return str + "\t" * indent

    def _appendNodeName(self, str, node):
        return str + node.__class__.__name__ + "(\n"

    def _appendCloseParen(self, str):
        return str + ")\n"

    def visit_Module(self, ast, indent, ast_str):
        ast_str = self._appendIndents(str, indent)
        ast_str = self._appendNodeName(str, ast)
        ast_str = self.visit(ast.node, indent + 1, ast_str)
        ast_str = self._appendCloseParen(ast_str)
        return ast_str

    def visit_Stmt(self, ast, indent, ast_str):
        ast_str = self._appendIndents(ast_str, indent)
        ast_str = self._appendNodeName(ast_str, ast)
        for node in ast.nodes:
            ast_str += self.visit(node, indent + 1, ast_str)
        ast_str = self._appendCloseParen(ast_str)
        return ast_str

    def visit_list(self, ast, indent, ast_str):
        pass #TODO: Finish this!
