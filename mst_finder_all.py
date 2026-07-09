def find_all_mst(c, N):
    """ Find list of all mst's in coloring c of [N] """
    mst_list = []

    for x in range(1, N + 1):
        for y in range(x, N + 1):
            z = x + y
            if z > N:
                break
            if c[x] == c[y] == c[z]:
                mst_list.append((x, y, z))
    return mst_list

# Call
mst_list = find_all_mst(c, N)

if mst_list:
    print(f"c has {len(mst_list)} mst(s). Schur triples are:.")
    for triple in mst_list:
        print(triple)
else:
    print("c does not have an mst.")

# Create reflection of c
c_reflection = {i: c[N + 1 - i] for i in range(1, N + 1)}

mst_list_ref = find_all_mst(c_reflection, N)

if mst_list_ref:
    print(f"Reflection of c has {len(mst_list_ref)} mst(s). Schur triples are:.")
    for triple in mst_list_ref:
        print(triple)
else:
    print("Reflection of c does not have an mst.")
