from __future__ import annotations
import foo


class Bar:
  def __init__(self, f: foo.Foo):
    self.f = f


def bar1() -> Bar:
  ...
