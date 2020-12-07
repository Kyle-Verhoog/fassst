import ast
import dis
import functools
import inspect
import textwrap
import types
import typing


__all__ = ["fast"]


def is_call_of_name(node, name):
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == name
    )


def is_constant_range(node):
    return is_call_of_name(node, "range") and all(
        isinstance(arg, ast.Constant) for arg in node.args
    )


def iterator_elements(iter_node):
    if isinstance(iter_node, (ast.List, ast.Tuple)):
        return iter_node.elts
    if is_constant_range(iter_node):
        args = [a.value for a in iter_node.args]
        return [ast.Constant(n) for n in range(*args)]
    if is_call_of_name(iter_node, "enumerate"):
        inner_elems = iterator_elements(iter_node.args[0])
        return [
            # See FIXME below about expression locations
            ast.Tuple(
                elts=[
                    ast.fix_missing_locations(ast.Constant(i)),
                    ast.fix_missing_locations(el),
                ],
                ctx=ast.Load(),
            )
            for i, el in enumerate(inner_elems)
        ]
    raise NotImplementedError(ast.dump(iter_node))


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

        new_body = []
        for x in iterator_elements(node.iter):
            # FIXME: this should probably use the location the expression
            # actually appeared in (the range(n) call or the element in a
            # literal list/tuple).
            ast.fix_missing_locations(x)
            new_body.append(
                ast.copy_location(ast.Assign(targets=[node.target], value=x), node)
            )
            new_body.extend(node.body)
        return new_body


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

    # Return a new function to leave the original unaltered.
    args = [
        new_fn_code.co_argcount,
        new_fn_code.co_nlocals,
        new_fn_code.co_stacksize,
        new_fn_code.co_flags,
        new_fn_code.co_code,
        new_fn_code.co_consts,
        new_fn_code.co_names,
        new_fn_code.co_varnames,
        new_fn_code.co_filename,
        new_fn_code.co_name,
        new_fn_code.co_firstlineno,
        new_fn_code.co_lnotab,
        new_fn_code.co_freevars,
        new_fn_code.co_cellvars,
    ]
    try:
        args.insert(1, new_fn_code.co_kwonlyargcount)  # Py3
        args.insert(1, new_fn_code.co_posonlyargcount)  # Py38+
    except AttributeError:
        pass

    return functools.update_wrapper(
        types.FunctionType(
            types.CodeType(*args),
            fn.__globals__,
            fn.__name__,
            fn.__defaults__,
            fn.__closure__,
        ),
        fn,
    )
