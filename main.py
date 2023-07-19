"""
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
  ...


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


def connect(a, b):
  ...


# def test_basic_connection():
#   """
#   >>> a = Wire()
#   >>> b = Wire()
#   >>> connect(a, b)
#   >>> a.value = 1
#   >>> a
#   Wire(0)
#   >>> b
#   Wire(1)
#   >>> b.value = 0
#   >>> a
#   Wire(0)
#   >>> b
#   Wire(0)
#   """
"""
The gate and a single operation

We are going to create a NOR3 gate. Our only constraint is we have access to one operation: a nor3 function. You will not be allowed to do any digital logic unless it passes through this nor3 function. Here it is:
"""


def nor3(a, b, c):
  return not (a or b or c)


# class NOR3:
# or
# def NOR3()
"""
Here is a sample repl Session utilizing this NOR3 gate
"""

# def test_nor3_gate():
#   """
#   >>> a = Wire()
#   >>> b = Wire()
#   >>> c = Wire()
#   >>> out = Wire()
#   >>> NOR3(a, b, c, out)
#   >>> out.value
#   1
#   >>> a.value = 1
#   >>> out.value
#   0
#   """
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


def NOT():
  ...


def AND():
  ...


def OR():
  ...


def XOR():
  ...
