def foo1():
  from bar import bar1
  print("Inside foo1")
  b = bar1()
  return "foo1 " + str(b)
