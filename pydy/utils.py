#!/usr/bin/env python

import textwrap

from pkg_resources import parse_version
import sympy as sm
from sympy.core.function import AppliedUndef
from sympy.utilities.iterables import iterable
from sympy.physics.mechanics import dynamicsymbols

SYMPY_VERSION = sm.__version__


def sympy_equal_to_or_newer_than(version, installed_version=None):
    """Returns true if the installed version of SymPy is equal to or newer
    than the provided version string."""
    if installed_version is None:
        v = SYMPY_VERSION
    else:
        v = installed_version
    return cmp(parse_version(v), parse_version(version)) > -1


def wrap_and_indent(lines, indentation=4, width=79):
    """Returns a single string in which the lines have been indented and
    wrapped into a block of text."""
    # TODO : This will indent any lines that only contain a new line. Which
    # may not be preferable.
    new_lines = []
    for line in lines:
        if line != '\n':
            wrapped = textwrap.wrap(line, width=width-indentation)
        else:
            wrapped = [line]
        new_lines += wrapped
    spacer = '\n' + ' ' * indentation
    return ' ' * indentation + spacer.join(new_lines)


# This is a copy of the function in SymPy. It doesn't exist in SymPy 0.7.4
# so we keep it here for now.
def find_dynamicsymbols(expression, exclude=None):
    """Find all dynamicsymbols in expression.

    >>> from sympy.physics.mechanics import dynamicsymbols, find_dynamicsymbols
    >>> x, y = dynamicsymbols('x, y')
    >>> expr = x + x.diff()*y
    >>> find_dynamicsymbols(expr)
    set([x(t), y(t), Derivative(x(t), t)])

    If the optional ``exclude`` kwarg is used, only dynamicsymbols
    not in the iterable ``exclude`` are returned.

    >>> find_dynamicsymbols(expr, [x, y])
    set([Derivative(x(t), t)])
    """
    t_set = set([dynamicsymbols._t])
    if exclude:
        if iterable(exclude):
            exclude_set = set(exclude)
        else:
            raise TypeError("exclude kwarg must be iterable")
    else:
        exclude_set = set()
    return set([i for i in expression.atoms(AppliedUndef, sm.Derivative) if
                i.free_symbols == t_set]) - exclude_set
