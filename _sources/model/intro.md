# Introduction

There are different ways to calculate the operation of thermal energy conversion
plants, i.e. the sequential-modular (SM) and the equation-oriented (EO)
approach. Both approaches exist since the 1970s and have been discussed many
times, e.g. the papers {cite}`Biegler1983`, {cite}`Shacham1982`,
{cite}`Rosen1980` or by textbooks {cite}`Auzinger1988`, {cite}`Dimian2016`,
{cite}`Walter2017`.

In general, equations are applied to model the physical processes happening in
the plant's components. A solution is found, if mass and energy balances across
all components are solved. In short: SM is the more "straightforward" approach,
which starts at a specific point of the plant and solves for the next state
equation by equation. After all equations have been solved once, further
iteration might be required, i.e. if recirculations are required of if equations
affect multiple parts of the plant at the same time. On top of that, if the user
specifications change for a setup, the order of solving changes as well. This
makes this approach less flexible compared to the EO approach.

```{note}
The SM approach will be the approach we implement in this course manually. In
the exercise you will see its advantages and shortcomings at a concrete example.
```

In contrast, the EO approach sets up a linear system of non-linear equations and
solves all equations simultaneously. For example, a multidimensional
Newton-Raphson algorithm can then be employed to solve these equations
iteratively. The system of equations is built from the topology of the plant and
the parameters applied by the user. Additional iterations in case of
recirculations are not required. Furthermore, the user is free in the
specification of topology and parameters as long as the system of equations is
well determined with respect to its variables. The main disadvantage is that
troubleshooting requires more experience as the solver cannot point out a
specific reason for failure. In addition, the solver requires starting values
for all variables. An initial guess for generic topologies and generic fluids is
challenging to implement and thus might require user inputs. However, running
additional simulations based on a converged solution leads to faster
convergence.
