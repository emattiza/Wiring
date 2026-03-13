require 'minitest/autorun'

# Wiring: Simulating Digital Logic with Ruby
#
# Our goal is to build digital primitives (Wires) and combine them
# into Gates (NOR3), eventually building complex logic like XOR.

# --------------------
# The Wire
# --------------------
# A wire holds a charge (0 or 1). It should also be pretty in the repl
# like Wire(0)
class Wire
end

# --------------------
# The Connection
# --------------------
# Ties two wires together so that a change in one propagates to the other.
def connect(wire_a, wire_b)
end

# --------------------
# The NOR3 Gate
# --------------------
# This is our universal primitive. 
# Output is 1 ONLY if all three inputs are 0.

def nor3(a, b, c)
  rval = a == 0 && b == 0 && c == 0 ? 1 : 0
  return rval
end

class NOR3
  def initialize(a, b, c, out)
  end
end

# --------------------
# Derived Logic Gates
# --------------------
# These gates are built strictly by composing NOR3 gates.

def NOT(input, output)
  
end

def OR(a, b, output)
  
end

def AND(a, b, output)

end

def XOR(a, b, output)

end

# --------------------
# Minitest Suite (Pure Nix / No Gems Required)
# --------------------

class TestWiringSimulation < Minitest::Test
  def test_basic_wire
    a = Wire.new
    assert_equal 0, a.value
    a.value = 1
    assert_equal 1, a.value
  end

  def test_basic_connection
    a = Wire.new
    b = Wire.new
    connect(a, b)
    a.value = 1
    assert_equal 1, b.value
    b.value = 0
    assert_equal 0, a.value
  end

  def test_nor3_gate
    a, b, c, out = Wire.new, Wire.new, Wire.new, Wire.new
    NOR3.new(a, b, c, out)

    assert_equal 1, out.value # 0,0,0 -> 1
    a.value = 1
    assert_equal 0, out.value # 1,0,0 -> 0
  end

  def test_logic_gates
    a = Wire.new(0)
    b = Wire.new(0)
    out = Wire.new

    # Test OR
    OR(a, b, out)
    assert_equal 0, out.value
    a.value = 1
    assert_equal 1, out.value

    # Test AND (re-using wires)
    a.value = 0; b.value = 0
    and_out = Wire.new
    AND(a, b, and_out)
    assert_equal 0, and_out.value
    a.value = 1; b.value = 1
    assert_equal 1, and_out.value

    # Test XOR
    a.value = 1; b.value = 1
    xor_out = Wire.new
    XOR(a, b, xor_out)
    assert_equal 0, xor_out.value # 1 XOR 1 = 0
    a.value = 0
    assert_equal 1, xor_out.value # 0 XOR 1 = 1

    # Test NOT
    a.value = 0;
    not_out = Wire.new
    NOT(a, not_out)
    assert_equal 1, not_out.value # NOT 0 = 1
    a.value = 1
    assert_equal 0, not_out.value # NOT 1 = 0
  end
end