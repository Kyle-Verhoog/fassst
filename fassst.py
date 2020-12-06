import ast
import dis

# import functools
import inspect
import textwrap
import types
import typing

# fn.__code__ = types.CodeType(
#         code.co_argcount,
#         code.co_posonlyargcount,
#         code.co_kwonlyargcount,
#         code.co_nlocals,
#         code.co_stacksize,
#         code.co_flags,
#         code.co_code,
#         code.co_consts,
#         code.co_names,
#         code.co_varnames,
#         code.co_filename,
#         code.co_name,
#         code.co_firstlineno,
#         code.co_lnotab,
#         code.co_freevars,
#         code.co_cellvars,
# )


class InlineFor(ast.NodeTransformer):
    def __init__(self, code, filename):
        self.code = code
        self.filename = filename
        super()

    def visit_For(self, node):
        def is_pure(node):
            # TODO
            return True

        if not is_pure(node.iter):
            return node

        iter_code = ast.get_source_segment(self.code, node.iter)
        target_code = ast.get_source_segment(self.code, node.target)
        new_code = ""
        for x in eval(iter_code):
            new_code += f"{target_code} = {repr(x)}\n"
            for l in node.body:
                new_code += ast.get_source_segment(self.code, l) + "\n"
        new_ast = ast.parse(new_code, filename=self.filename)
        return new_ast.body


def fast(fn):
    code = fn.__code__
    # bcode = dis.dis(code)
    src = textwrap.dedent(inspect.getsource(fn))
    tree = ast.parse(src)

    # Before
    # print(ast.dump(tree, indent=2))

    new_tree = InlineFor(src, code.co_filename).visit(tree)

    # After
    # print(ast.dump(new_tree.body[0], indent=2))
    new_code = compile(new_tree, filename=code.co_filename, mode="exec")
    new_fn_code = new_code.co_consts[0]

    def new_fn():
        pass

    new_fn.__code__ = new_fn_code
    return new_fn

    # code = new_code
    # # Return a new function to leave the original unaltered.
    # args = [
    #         code.co_argcount,  code.co_nlocals,     code.co_stacksize,
    #         code.co_flags,     fn.__code__.co_code, code.co_consts,
    #         code.co_names,     code.co_varnames,    code.co_filename,
    #         code.co_name,      code.co_firstlineno, code.co_lnotab,
    #         code.co_freevars,  code.co_cellvars,
    # ]
    # try:
    #     args.insert(1, code.co_kwonlyargcount)
    # except AttributeError:
    #     pass

    # return functools.update_wrapper(types.FunctionType(
    #         types.CodeType(
    #             *args
    #         ),
    #         fn.__globals__,
    #         fn.__name__,
    #         fn.__defaults__,
    #         fn.__closure__,
    # ))
