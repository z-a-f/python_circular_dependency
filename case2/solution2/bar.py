from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from foo import Foo


class Bar:
  def __init__(self, f: Foo):
    self.f = f


def bar1() -> Bar:
  ...
