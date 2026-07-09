# Import libraries
from pysat.formula import IDPool, CNF
from pysat.solvers import Solver
from itertools import combinations

# ------------------------------------------------------------------------------

# Build constraints 1-2
def build_exactly_one_color(cnf, idpool, N, r, v_name = "v"):
  """
  Adds:
    1) Each number gets assigned one color: N CNF clauses
    2) Each number cannot have more than one color: N * C(r, 2) CNF clauses

  Variable naming: v_n_c means "number n has color c" and returns v(n, c)
  """
  # Define v for a reusable variable for all constraints
  def v(n,c):
    return idpool.id(f"{v_name}_{n}_{c}")

  # Create constraint 1
  for n in range(1, N + 1):
    cnf.append([v(n, c) for c in range(1, r + 1)])

  # Create constraint 2
  for n in range(1, N + 1):
    for c1, c2 in combinations(range(1, r + 1), 2):
      cnf.append([-v(n, c1), -v(n, c2)])

  return v

# ------------------------------------------------------------------------------

# Build constraints 3-5
def build_no_mst(cnf, idpool, v, N, r):
  """
  Adds:
    3) No mst's can be the same color
    4) No mmst's can be the same color (wraparound)
    5) Fixes symmetry by forcing "1" to be the first color,
       cutting down by a factor of r(r-1)
  """
  # Create constraint 3
  count = 0
  for x in range(1, N + 1):
    for y in range(x, N + 1):
      z = x + y
      if z > N:
        continue
      for c in range(1, r + 1):
        cnf.append([-v(x, c), -v(y, c), -v(z, c)])
        count += 1
  return count

# Create constraint 4
def build_no_mmst(cnf, idpool, v, N, r):
  count = 0
  for x in range(1, N + 1):
    for y in range(x, N + 1):
      s = x + y
      if s <= N:
        continue
      z = s - (N + 1)
      if z == 0:
        continue
      for c in range(1, r + 1):
        cnf.append([-v(x, c), -v(y, c), -v(z, c)])
        count += 1
  return count

# Create constraint 5
def fix_symmetry(cnf, v):
  cnf.append([v(1, 1)])

# ------------------------------------------------------------------------------

# Set problem size: N numbers in [N] and r colors
N = 45
r = 4

# ------------------------------------------------------------------------------

# Initialize variable pool and empty CNF formula
idpool = IDPool()
cnf = CNF()

# Build all five constraints into cnf
v = build_exactly_one_color(cnf, idpool, N, r)
build_no_mst(cnf, idpool, v, N, r)
build_no_mmst(cnf, idpool, v, N, r)
fix_symmetry(cnf, v)

# ------------------------------------------------------------------------------

# Decode a raw SAT model into a {number: color} dictionary for readability
def decode_coloring(model, idpool, N, r, v_name = "v"): # Gives all boolean variables either positive (True) or negative (False)
  true_int = set(val for val in model if val > 0) # Takes only positive integers and puts them into a set
  coloring = {}
  for n in range(1, N + 1):
    assigned = [c for c in range(1, r + 1)
      if idpool.id(f"{v_name}_{n}_{c}") in true_int]
    coloring[n] = assigned[0] if len(assigned) == 1 else assigned
  return coloring

# Solve CNF with the CaDiCaL SAT solver and give result
with Solver(name='cadical153', bootstrap_with=cnf.clauses) as S:
  sat = S.solve() # Loads clauses into CaDiCaL
  if sat:
    print("Satisfiable!")
    model = S.get_model()
    coloring = decode_coloring(model, idpool, N, r)

    invalid = {n: c for n, c in coloring.items() if not isinstance(c, int)}
    if invalid:
      print("Invalid assignment(s) found:", invalid)
    else:
      print("There exists coloring(s) without an mmst.")

    # Prints out valid color combinations up to r times
    color_classes = {c: [] for c in range(1, r + 1)}
    for n, c in coloring.items():
      color_classes[c].append(n)
    for c in range(1, r + 1):
      print(f"color {c}: {color_classes[c]}")
  else:
    print("Unsatisfiable!")

# Use cnf.to_file("i.e. your downloads folder.cnf") to download CNF file