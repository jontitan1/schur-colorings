# Schur Colorings
## Overview
### Schur Numbers
In Ramsey theory, a **Schur number**, typically denoted as $S(k)$, is the smallest integer $n$ such that if the set of integers ${1, 2, ..., n}$ is partitioned into $k$ distinct subsets or "colors", at least one of the subsets contains a solution to the equation $x + y = z$.

These numbers define the threshold where avoiding "monochromatic" solutions to $x + y = z$ is no longer possible. The Known Schur triples are
- $S(1) = 2$
- $S(2) = 5$
- $S(3) = 14$
- $S(4) = 45$
- $S(5) = 161$

On the other hand, a modular monochromatic Schur triple, instead of $x + y = z$, checks for solutions to $x + y$ is congruent to $z(mod N + 1)$.

**mst** is the abbreviation for "monochromatic Schur triple," while **mmst** is the abbreviation for "modular monochromatic Schur triple."

## Repository Contents
### mst_finder_one *and* mst_finder_all
This program accepts
- an integer $N$
- a dictionary $c$
where
```c[n]```
is the color assigned to integer $n$.

Difference between mst_finder_one *and* mst_finder_all:
- mst_finder_one returns only the first mst found in $c$ and its reflection
- mst_finder_all returns all mst's found in $c$ and its reflection

The programs
- find one or all mst's
- construct the reflected coloring
- find one or all mst's in the reflection
An example coloring is included in
```examples/coloring_N160_r5.py```

## mmst_sat_solver.py
This program generates CNF constraints for SAT solvers.
It implements
- exactly one color for each number
- no mst's
- no mmst's
- symmetry breaking

The generated CNF is solved using CaDiCaL through PySAT.
The encoding is completely general and work for arbitrary $N$ and $r$.

## Motivation
This project was developed to investigate modular Schur triples for larger instances.
Although the repository uses smaller examples for demonstration, the implementation was designed to explore challenging cases such as
- `N = 155`,`r = 5`
- `N = 158`,`r = 5`

These produce significantly larger SAT instances.

## Installation
```bash
pip install -r requirements.txt
```

## Running the programs
### mst_finder_one *and* mst_finder_all
```
python mst_finder_one.py
python mst_finder_all.py
```

### SAT encoding
```
python mmst_sat_solver.py
```
