from __future__ import annotations


class Foo:
  def __init__(self, b: Bar):
    self.b = b


def foo1():
  from bar import bar1
  b: Bar = bar1()
  ...
