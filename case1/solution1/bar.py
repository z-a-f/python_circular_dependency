from foo import foo1


def bar1():
  print("Inside bar1")
  return "bar1"


def bar2():
  print("Inside bar2")
  a = foo1()
  return "bar2 " + str(a)
