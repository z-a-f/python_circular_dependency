from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from bar import Bar


class Foo:
  def __init__(self, b: Bar):
    self.b = b


def foo1():
  from bar import bar1
  b: Bar = bar1()
  ...
