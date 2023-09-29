# Example: 80S ribosome

## Dynamo
### 1. Initial particle alignment
- Reference = EMD-5592_10.825Apx_48px_lp70A_inv.mrc
- alignment steps = "Global search" then "Refinement"

## RELION-4.0

### 2. 3D classification with exhaustive angular search

Goal: remove "junk" particles

- Reference = EMD-5592 low pass filtered to 70 A
- Mask = spherical mask
- Vary K and T
- exhaustive search