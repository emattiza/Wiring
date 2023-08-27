"""
$ ls main.py | entr pytest
Wiring: Simulating Digital Logic with Python

Shortened material from day 1 of a course with David Beazley
http://dabeaz.com/courses if you want to learn more

Digital Computers have come a long way, and their synthesis is pretty intricate today and on a much smaller scale physically. However, much was accomplished with less many years ago, and we are going to explore building a system with Python as a DSL or modeling language for a real world hardware design.

To start, we can look to a piece of computer history, the AGC (Apollo Guidance Computer) [Link here](http://www.righto.com/2019/09/a-computer-built-from-nor-gates-inside.html)

Our goal today is to build the primitives, and then some combination of them to make more complex pieces like gates, and if time permits, making an ALU.

Along the way, you can expect to learn some new python tricks you may be less familiar with, and some design patterns to aid in meeting our users preferred style of writing their new models. You'll learn some important reasons why we test software, and how to automate it. You can also just puddle around in the REPL with your newly created objects. This is your playground!

--------------------
The wire
--------------------

Our first piece of reality to model is a wire with charge. For now, this can be a container, but in the next step we will add a notion of "connection" to wires and the propagation of information that happens

Here is a sample REPL experience we would like to have for making independent wires:

>>> a = Wire()
>>> a
Wire(0)
>>> a.value = 1
>>> a
Wire(1)

"""

def test_basic_wire():
  """
  >>> a = Wire()
  >>> a
  Wire(0)
  >>> a.value = 1
  >>> a
  Wire(1)
  """


class Wire:
  """
  Implement your wire here!
  """
  def __init__(self, x=0):
    self._value = x
    self.watchers = set()

  @property
  def value(self):
    return self._value

  @value.setter
  def value(self, new_value):
    # in place tuple reassignment
    # old_value = self._value
    # self._value = new_value
    old_value = self._value
    self._value = new_value
    if new_value != old_value:
      self.notify()

  def notify(self):
    for watcher in self.watchers:
      watcher()
      

  def watch(self, func):
    self.watchers.add(func)
    func()
    
  def __repr__(self):
    return f'Wire({self.value})'

"""
--------------------
The connection
--------------------

What should happen when two wires are connected, and one end becomes charged?

o---A---o---B---o

        +---B---o
        |
o---A---o---C---o
        |
        +---D---o

What kinds of interactions do A and B need to have to communicate their state and let their neighbors know?

See and uncomment test_basic_connection for an example repl session
"""


def connect(a: Wire, b: Wire):
  a.watch(lambda: setattr(b, "value", a.value))
  b.watch(lambda: setattr(a, "value", b.value))


def test_basic_connection():
  """
  >>> a = Wire()
  >>> b = Wire()
  >>> connect(a, b)
  >>> a.value = 1
  >>> a
  Wire(1)
  >>> b
  Wire(1)
  >>> b.value = 0
  >>> a
  Wire(0)
  >>> b
  Wire(0)
  """
  ...
"""
The gate and a single operation

We are going to create a NOR3 gate. Our only constraint is we have access to one operation: a nor3 function. You will not be allowed to do any digital logic unless it passes through this nor3 function. Here it is:
"""


def nor3(a, b, c):
  return not (a or b or c)


class NOR3:
  def __init__(self, a: Wire, b: Wire, c: Wire, out: Wire):
    """1 if all are 0, else 0"""
    self.a = a
    self.b = b
    self.c = c
    self.out = out
    a.watch(self.update)
    b.watch(self.update)
    c.watch(self.update)


  def update(self):
    self.out.value = int(nor3(self.a.value, self.b.value, self.c.value))
    
  def __repr__(self):
    return f"{self.__class__.__name__}({self.a.value}, {self.b.value}, {self.c.value}, {self.out.value})"
  


# or
# def NOR3()
"""
Here is a sample repl Session utilizing this NOR3 gate
"""

def test_nor3_gate():
  """
  >>> a = Wire()
  >>> b = Wire()
  >>> c = Wire()
  >>> out = Wire()
  >>> NOR3(a, b, c, out)
  NOR3(0, 0, 0, 1)
  >>> out.value
  1
  >>> a.value = 1
  >>> out.value
  0
  """
"""
Other Logic Gates

Now go ahead and write some common logic gates! You will only be allowed to use the NOR3 gate you defined above. 

Author Note: Be warned though! If you don't test, how you will be sure they work correctly as a unit and a system when you use them in something larger and more complex?

Some Other Gates:
NOT(x, out)         x      out
                   ---     ---
                    0       1
                    1       0

AND(x, y, out)      x       y      out
                   ---     ---     ---
                    0       0       0
                    0       1       0
                    1       0       0
                    1       1       1

OR(x, y, out)       x       y      out
                   ---     ---     ---
                    0       0       0
                    0       1       1
                    1       0       1
                    1       1       1

XOR(x, y, out)      x       y      out
                   ---     ---     ---
                    0       0       0
                    0       1       1
                    1       0       1
                    1       1       0
"""


class NOT:
  def __init__(self, a, out):
    self.a = a
    self.b = Wire()
    self.c = Wire()
    self.out = out
    NOR3(self.a, self.b, self.c, self.out)

  def __repr__(self):
    return f"NOT({self.a.value}, {self.out.value})"

def test_not_gate():
  """
  >>> a = Wire()
  >>> out = Wire()
  >>> NOT(a, out)
  NOT(0, 1)
  >>> out.value
  1
  >>> a.value = 1
  >>> out.value
  0
  """

class AND:
  def __init__(self, a, b, out):
    self.a = a
    self.b = b
    self.c = Wire()
    self.out = out

    self.aa = Wire()
    NOR3(self.a, self.a, self.c, self.aa)
    self.bb = Wire()
    NOR3(self.b, self.b, self.c, self.bb)

    NOR3(self.aa, self.bb, self.c, self.out)

  def __repr__(self):
    return f"AND({self.a.value}, {self.b.value}, {self.out.value})"
  
class OR:
  def __init__(self, a, b, out):
    self.a = a
    self.b = b
    self.out = out    
    a.watch(self.update)
    b.watch(self.update)

  def update(self):
    self.out.value = int(nor3(nor3(self.a.value, self.b.value, 0), nor3(self.a.value, self.b.value, 0), 0))

  def casey_cheated(self):
    a_gate_out = Wire()
    b_gate_out = Wire()
    NOR3(self.a, self.a, Wire(), a_gate_out)
    NOR3(self.b, self.b, Wire(), b_gate_out)
    NOR3(a_gate_out, b_gate_out, Wire(), self.out)

  def __repr__(self):
    return f"OR({self.a.value}, {self.b.value}, {self.out.value})"

def test_or_gate():
  """
  >>> a = Wire()
  >>> b = Wire()
  >>> out = Wire()
  >>> OR(a, b, out)
  OR(0, 0, 0)
  >>> out.value
  0
  >>> a.value = 1
  >>> b.value = 0
  >>> out.value
  1
  >>> a.value = 0
  >>> b.value = 1
  >>> out.value
  1
  >>> a.value = 1
  >>> b.value = 1
  >>> out.value
  1
  """

class XOR():
  def __init__(self, a, b, out):
    self.a = a
    self.b = b
    self.out = out

    a_nor_a = Wire()
    NOR3(self.a, self.a, Wire(), a_nor_a)
    b_nor_b = Wire()
    NOR3(self.b, self.b, Wire(), b_nor_b)
    aa_nor_bb = Wire()
    NOR3(a_nor_a, b_nor_b, Wire(), aa_nor_bb)
    a_nor_b = Wire()
    NOR3(self.a, self.b, Wire(), a_nor_b)
    NOR3(aa_nor_bb, a_nor_b, Wire(), self.out)
  
  def __repr__(self):
    return f"XOR({self.a.value}, {self.b.value}, {self.out.value})"


def test_xor_gate():
  """
  >>> a = Wire()
  >>> b = Wire()
  >>> out = Wire()
  >>> XOR(a, b, out)
  XOR(0, 0, 0)
  >>> out.value
  0
  >>> a.value = 1
  >>> b.value = 0
  >>> out.value
  1
  >>> a.value = 0
  >>> b.value = 1
  >>> out.value
  1
  >>> a.value = 1
  >>> b.value = 1
  >>> out.value
  0
  """