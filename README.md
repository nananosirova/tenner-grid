# Tenner Grid Constraint Satisfaction

### What I did
Created Forward Checking and Generalized Arc Consistency contraint propagators, as well as two different CSP encodings to solve the Tenner Grid puzzle. 

### Tenner Grid description

Tenner Grid (also known as “From 1 to 10”, “Zehnergitter”, “Grid Ten”) consists of a rectangular
grid of width ten cells, i.e., the grid with dimensions n rows by 10 columns, and a special (n+1)-th
row. The task is to fill in the first n rows so that every row contains the digits 0 through 9. In columns
the numbers may be repeated.

### The Propagators

The propagators are located in the file propagators.py. The functions are:
  * propFC: A propagator function that propagates according to the Forward Checking (FC) algorithm that
          check constraints that have exactly one uninstantiated variable in their scope, and prune appropriately.
          If newVar is None, forward check all constraints. Else, if newVar=var only check constraints containing
          newVar.
        
          
  * propGAC: A propagator function that propagates according to the Generalized Arc Consistency (GAC)
          algorithm, as covered in lecture. If newVar is None, run GAC on all constraints. Else, if newVar=var
          only check constraints containing newVar.

### Tenner Grid models

  * tenner_csp_model_1: A model built using only binary not-equal constraints for the row and contiguous
cells constraints, and n-ary sum constraints.

  * tenner_csp_model_2: A model built using a combination of n-ary all-different constraints for the row
constraints, n-ary sum constraints, as well as binary not-equal constraints for the contiguous cells
constraints.




