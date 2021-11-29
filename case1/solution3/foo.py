def foo1():
  print("Inside foo1")
  b = bar1()
  return "foo1 " + str(b)


def bar1():
  print("Inside bar1")
  return "bar1"


def bar2():
  print("Inside bar2")
  a = foo1()
  return "bar2 " + str(a)
