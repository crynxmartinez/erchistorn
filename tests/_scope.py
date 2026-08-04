"""Per-function scope analysis shared by the integrity tests.

Why per-function and not module-wide: an earlier module-wide version treated a
name bound inside *any* function as bound *everywhere*, which hid two live 500s
(`PROFESSION_RANKS`, `ch`). Scoping to the function is the entire point.
"""
from __future__ import annotations

import ast
import builtins

IMPLICIT = {"__file__", "__name__", "__doc__", "__package__", "__spec__",
            "__loader__", "__builtins__"}


def module_scope(tree: ast.Module) -> set[str]:
    """Names visible at module scope. Does not descend into function bodies."""
    bound = set(dir(builtins)) | IMPLICIT
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                bound.add((a.asname or a.name).split(".")[0])
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign,
                               ast.For, ast.AsyncFor, ast.With, ast.AsyncWith,
                               ast.If, ast.Try, ast.While)):
            # Module-level binding forms, including conditional ones
            # (try/except imports, `if TYPE_CHECKING:` blocks).
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Store):
                    bound.add(sub.id)
                elif isinstance(sub, ast.alias):
                    bound.add((sub.asname or sub.name).split(".")[0])
    return bound


def function_locals(fn: ast.AST) -> set[str]:
    """Names bound anywhere inside one function, including nested scopes.

    Deliberately over-approximates (a name bound in a nested comprehension
    counts for the whole function). Over-approximating keeps this a
    false-negative-prone but false-positive-free check, which is the right
    trade for a gate that must never cry wolf.
    """
    local: set[str] = set()
    args = getattr(fn, "args", None)
    if args is not None:
        for a in (list(args.args) + list(args.kwonlyargs)
                  + list(args.posonlyargs)):
            local.add(a.arg)
        if args.vararg:
            local.add(args.vararg.arg)
        if args.kwarg:
            local.add(args.kwarg.arg)
    for node in ast.walk(fn):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            local.add(node.id)
        elif isinstance(node, ast.alias):
            local.add((node.asname or node.name).split(".")[0])
        elif isinstance(node, ast.arg):
            local.add(node.arg)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            local.add(node.name)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            local.update(node.names)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                               ast.ClassDef)):
            local.add(node.name)
    return local


_SCOPE_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)


def _own_nodes(fn: ast.AST):
    """Yield nodes belonging to `fn` itself, not to functions nested inside it."""
    stack = list(ast.iter_child_nodes(fn))
    while stack:
        node = stack.pop()
        if isinstance(node, _SCOPE_NODES):
            continue  # a nested scope; it is checked separately
        yield node
        stack.extend(ast.iter_child_nodes(node))


def _nested_scopes(fn: ast.AST):
    """Direct function/lambda children of `fn`, skipping deeper nesting."""
    stack = list(ast.iter_child_nodes(fn))
    while stack:
        node = stack.pop()
        if isinstance(node, _SCOPE_NODES):
            yield node
            continue
        stack.extend(ast.iter_child_nodes(node))


def undefined_names(tree: ast.Module) -> dict[str, tuple[str, int]]:
    """Map name -> (function, line) for loads not visible from that function.

    Closures must inherit the enclosing function's locals. A first version
    checked every `FunctionDef` against module scope plus its own locals only,
    which flagged 18 legitimate closures (`_usable`, `do_heal`, `_stat`) that
    read names from the function they were defined in. `visible` therefore
    accumulates down the nesting chain.
    """
    module = module_scope(tree)
    missing: dict[str, tuple[str, int]] = {}

    def walk_scope(fn: ast.AST, enclosing: set[str], name: str) -> None:
        visible = enclosing | function_locals(fn)
        for node in _own_nodes(fn):
            if (isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
                    and node.id not in visible):
                missing.setdefault(node.id, (name, node.lineno))
        for nested in _nested_scopes(fn):
            walk_scope(nested, visible, getattr(nested, "name", name))

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            walk_scope(node, module, node.name)
        elif isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    walk_scope(sub, module, f"{node.name}.{sub.name}")
    return missing
