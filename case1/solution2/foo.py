import bar


def foo1():
  print("Inside foo1")
  b = bar.bar1()
  return "foo1 " + str(b)
