from __future__ import annotations
import bar


class Foo:
  def __init__(self, b: bar.Bar):
    self.b = b


def foo1():
  b: bar.Bar = bar.bar1()
  ...
