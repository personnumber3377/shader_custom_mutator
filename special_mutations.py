
# shader_mutator.py
from __future__ import annotations

from dataclasses import replace
from typing import Dict, List, Optional, Tuple, Union
import copy
import random

from shader_ast import *

# For the builtin functions etc...
from builtin_data import BUILTIN_FUNCTIONS

# Debugging???

# DEBUG = True

DEBUG = False

# if DEBUG:# Originally was conditional
import shader_unparser



# THESE NEXT ONES ARE FOR SPECIAL HAVOC!!!



# Chooses a function which returns a scalar value. This is used in the special mutation of return values and function calls...
def pick_function_for_array_return(items, env, rng):
    candidates = []
    for item in items:
        if isinstance(item, FunctionDef):
            ret = typename_to_typeinfo(item.return_type)
            if ret.name in ("int", "uint", "float", "bool"):
                candidates.append(item)
    return rng.choice(candidates) if candidates else None


def rewrite_call_sites(items, fn_name, array_len, rng):
    def visit_expr(e):
        if isinstance(e, CallExpr) and isinstance(e.callee, Identifier):
            if e.callee.name == fn_name:
                idx = rng.choice([0, 0, 1, array_len - 1])
                return IndexExpr(e, IntLiteral(idx))
        # recurse
        for attr in vars(e):
            v = getattr(e, attr)
            if isinstance(v, Expr):
                setattr(e, attr, visit_expr(v))
            elif isinstance(v, list):
                setattr(e, attr, [visit_expr(x) if isinstance(x, Expr) else x for x in v])
        return e

    for item in items:
        if isinstance(item, FunctionDef):
            item.body = visit_expr(item.body)


# END SPECIAL HAVOC FUNCTIONS


# ----------------------------
# Special havoc mode with very specific mutations...
# ----------------------------

# TODO: Consider moving these special mutations to another python file???

def _havoc_apply_struct_decl_qualifiers_all(items: List[TopLevel], rng: random.Random, env: Env) -> List[TopLevel]:
    """
    Apply a coordinated qualifier mutation across ALL StructDecl declarators.

    Goal: make it easy to reach bugs that require multiple correlated qualifier changes
    (e.g. BOTH structs getting 'uniform' in the same iteration).
    """
    it_items = deepclone(items)

    # Decide a single global "plan" for this havoc iteration.
    # Keep it biased toward 'uniform' because that's what you care about here.
    plans = [
        "force_uniform",     # add uniform everywhere (keep existing qualifiers too)
        "replace_uniform",   # replace with exactly 'uniform'
        "toggle_uniform",    # flip uniform on/off everywhere
        "replace_random",    # replace with one random storage qualifier (uniform/buffer/const or none)
        "mix_add_remove",    # use mutate_declarator_qualifiers but with aggressive params everywhere
    ]
    plan = rng.choice(plans)

    # Pick a global storage qualifier for plans that need it
    # Heavily bias towards uniform
    storage_choices = ["uniform", "uniform", "uniform", "buffer", "const", None]
    global_storage = rng.choice(storage_choices)

    # Optional: also apply a single global precision choice sometimes
    # (struct declarators probably ignore precision, but it can perturb parser / AST)
    global_precision = rng.choice(PRECISION_QUALIFIERS)

    changed_any = False

    for i, item in enumerate(it_items):
        if not isinstance(item, StructDecl):
            continue
        if not getattr(item, "declarators", None):
            continue

        # Mutate all declarators of this struct decl
        for d in item.declarators:
            old = list(d.qualifiers or [])

            qs = set(old)

            if plan == "force_uniform":
                # Ensure uniform present, keep other qualifiers
                qs.add("uniform")

            elif plan == "replace_uniform":
                qs = {"uniform"}

            elif plan == "toggle_uniform":
                if "uniform" in qs:
                    qs.remove("uniform")
                else:
                    qs.add("uniform")

            elif plan == "replace_random":
                # Replace with exactly one chosen qualifier (or none)
                qs.clear()
                if global_storage is not None:
                    qs.add(global_storage)

            elif plan == "mix_add_remove":
                # Use your existing mutator but crank it up, applied everywhere.
                mutate_declarator_qualifiers(
                    d,
                    rng,
                    storage_pool=["uniform", "buffer", "const", None],
                    precision_pool=PRECISION_QUALIFIERS,
                    p_add=0.90,
                    p_remove=0.60,
                    p_replace=0.80,
                )
                # mutate_declarator_qualifiers already wrote d.qualifiers; continue
                if d.qualifiers != old:
                    changed_any = True
                continue

            # Apply global precision sometimes (harmless if ignored)
            # Note: Declarator has qualifiers; TypeName holds precision.
            # We can only store precision if Declarator supports it; otherwise skip.
            # If your Declarator doesn't have a precision field, this is a no-op.
            if hasattr(d, "precision") and coin(rng, 0.35):
                d.precision = global_precision

            # Commit qualifier set
            d.qualifiers = [q for q in qs if q is not None]

            if d.qualifiers != old:
                changed_any = True

    # Helpful for your assert-chasing debugging hook
    # if changed_any and ("uniform" == global_storage or plan in ("force_uniform", "replace_uniform")):
    #     global stop
    #     stop = True

    return it_items

def mutate_function_return_to_array(fn: FunctionDef, rng):
    # N = rng.choice([2, 3, 4, 8, 16, 32, 64, 123])
    N = rng.choice([0, 2, 3, 4, 8, rng.randrange(0,1000)]) # Generate access index
    
    # Change return type
    fn.return_type = TypeName(fn.return_type.name)
    fn.return_type.array_dims = [IntLiteral(N)]

    # Rewrite return statements
    def rewrite_returns(stmt):
        if isinstance(stmt, ReturnStmt) and stmt.expr:
            base_type = fn.return_type.name
            stmt.expr = CallExpr(
                Identifier(f"{base_type}[{N}]"),
                [stmt.expr]
            )
        elif hasattr(stmt, "stmts"):
            for s in stmt.stmts:
                rewrite_returns(s)

    rewrite_returns(fn.body)

    return N

def _havoc_function_scalar_to_array(items, rng, env):
    items = deepclone(items)
    fn = pick_function_for_array_return(items, env, rng)
    print("fn: "+str(fn))
    if not fn:
        return items
    
    # global stop
    # stop = True
    
    array_len = mutate_function_return_to_array(fn, rng)
    rewrite_call_sites(items, fn.name, array_len, rng)

    return items

def special_havoc(items, rng, env):
    # Check for the thing here...
    # print("special_havoc")
    strats = ["struct_qualifier_all", "function_scalar_to_array"]
    strat = rng.choice(strats)
    if strat == "struct_qualifier_all": # Replace the qualifiers of here with the certain thing.
        return _havoc_apply_struct_decl_qualifiers_all(items, rng, env)
    elif strat == "function_scalar_to_array":
        return _havoc_function_scalar_to_array(items, rng, env)

    return items
