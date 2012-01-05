import stage
import astvisitor

class x86selector(astvisitor.ASTVisitor, stage.Stage):
    def __init__(self, flags):
        #No flags for this stage.
        #Create generator for tmp var names prefixed with "_is"
        self._makeTmpVarName = self._genName("_is")
        self._makeTmpVar = self._makeTmpVarGen()
        self._calleeSaveRegs = [
                x86.Register('ebx'),
                x86.Register('esi'),
                x86.Register('edi')]

    def do(self):
        return [self.visit(func) for func in self._stageInput]

    def _makeTmpVarGen(self):
        """A generator for making new VarNode objects"""
        while True:
            yield x86.VarNode(self._makeTmpVarName.next())

    def visit_Function(self, ast):
        x86_ast = []
        # Generate the function preamble
        x86_ast.extend(
                [x86.FunctionLabel(ast.name.name),
                 x86.Pushl(x86.Register('ebp')),
                 x86.Movl(x86.Register('esp'), x86.Register('ebp'))
                 ]
        )

        # Allocate space on the stack for spill variables by moving esp.
        local_list = set(P2GetLocals().getLocals(ast))
        spillage_space = len(local_list) * 4
        x86_ast.append(x86.Subl(x86.ConstNode(spillage_space), x86.Register('esp')))

        # Push callee save registers
        for reg in self._calleeSaveRegs:
            x86_ast.append(x86.Pushl(reg))

        # Move arguments to a local location (either a place on the stack or
        # a register). Register allocation will take care of placing the tmp
        # vars that get created.
        offset = 8
        for arg in ast.argnames:
            x86_ast.append(x86.Movl(x86.MemLoc(offset), self._makeTmpVar.next()))
            offset += 4

        # Generate the function body and append
        func_body = self.visit(ast.code)
        x86_ast += func_body

        # Restore callee save
        for reg in reversed(self._calleeSaveRegs):
            x86_ast.append(x86.Popl(reg))

        # Move esp back, and leave, ret.
        x86_ast.extend([
            x86.Addl(x86.ConstNode(spillage_space), x86.Register('esp')),
            x86.Leave(),
            x86.Ret()])

        return x86_ast

    def visit_CallUserDef(self, ast):
        x86_ast = []
        # Push arguments
        for arg in reversed(ast.args):
            (arg_code, result_var) = self.visit(arg)
            x86_ast += arg_code
            x86_ast.append(x86.Pushl(result_var))

        # Call function
        (node_code, result_var) = self.visit(ast.node)
        x86_ast += node_code
        x86_ast.append(x86.CallStar(result_var))

        # Deallocate argument space by moving esp
        arg_space = len(ast.args) * 4
        x86_ast.append( x86.Addl(x86.ConstNode(arg_space), x86.Register('esp')) )

        # Move return value to a temp var
        ret_val = self._makeTmpVar.next()
        x86_ast.append( x86.Movl(x86.Register('eax'), ret_val) )

        return (x86_ast, ret_val)

    def visit_CreateClosure(self, ast):
        x86_ast = []
        # Generate code for the argument
        (env_code, env_result_var) = self.visit(ast.env)
        x86_ast += env_code
        # Generate code for the function call
        arg_list = [
                env_result_var,
                x86.AddressLabel(ast.name.name) ]
        (call_func_code, ret) = self._makeCallFunc('create_closure', arg_list)
        x86_ast += call_func_code
        return (x86_ast, ret)

    def visit_GetFreeVars(self, ast):
        x86_ast = []
        # Generate code for argument
        (name_code, name_result_var) = self.visit(ast.name)
        x86_ast += name_code
        # Generate code for function call
        (call_func_code, ret) = self_makeCallFunc('get_free_vars', [name_result_var])
        x86_ast += call_func_code
        return (x86_ast, ret)

    def _makeCallFunc(self, func_name, args):
        x86_ast = []
        # Push the arguments
        for arg in args:
            x86_ast.append(x86.Pushl(arg))

        # Call the function
        x86_ast.append(x86.Call(func_name))

        # Move the return value to a temp var
        ret_val = self._makeTmpVar.next()
        x86_ast.append(x86.Movl(x86.Register('eax'), ret_val))

        # Deallocate argument space
        arg_space = len(args) * 4
        x86_ast.append(x86.Movl(x86.Addl(x86.ConstNode(arg_space), x86.Register('esp'))))

        return (x86_ast, ret_val)
