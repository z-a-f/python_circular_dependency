from foo import foo1
from bar import bar1, bar2


def main():
  f = foo1()
  b1 = bar1()
  b2 = bar2()
  print(f)


if __name__ == '__main__':
  main()
