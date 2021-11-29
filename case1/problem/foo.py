from bar import bar1


def foo1():
  print("Inside foo1")
  b = bar1()
  return "foo1 " + str(b)
