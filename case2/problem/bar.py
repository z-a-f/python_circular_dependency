from foo import Foo


class Bar:
  def __init__(self, f: Foo):
    self.f = f


def bar1() -> Bar:
  ...
