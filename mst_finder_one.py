def has_mst(c, N):
  """ has_mst: contains a monochromatic Schur triple """
  for x in range(1, N + 1):
    for y in range (x, N + 1):
      z = x + y
      if z > N:
        break
      if c[x] == c[y] == c[z]:  # Better than c.get()
        return True, (x, y, z)
  return False, None

# Call
mst_exists, triple = has_mst(c, N)

if mst_exists:
  print(f"c has an mst. Schur triple is {triple}.")
else:
  print("c does not have an mst.")

# Create reflection of c
c_reflection = {i: c[N + 1 - i] for i in range(1, N + 1)}

# Call reflection
mst_exists_ref, triple_ref = has_mst(c_reflection, N)

if mst_exists_ref:
  print(f"reflection of c has an mst. Schur triple is {triple_ref}.")
else:
  print("reflection of c does not have an mst.")

# Return only the first mst found, even if multiple exist