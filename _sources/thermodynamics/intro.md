# Introduction

The following sections present a brief summary of the thermodynamic theory we
will apply to model the heat pump in the later sections. First, important
terms and concepts are defined in the overview on
{ref}`thermodynamic systems <thermo-system>`. Then, the respective
fundamentals are outlined in more detail. The theory is applied in a small
exercise at the end of the chapter.

- {ref}`Thermodynamic state <thermo-states>`
- {ref}`Thermodynamic process <thermo-processes>`
- {ref}`Components <thermo-components>`
- {ref}`Exercises <thermo-exercises>`

For in depth theory the following literature might be useful:

- "Thermodynamik" (German) {cite}`Baehr2016`
- "Thermodynamics" {cite}`Klein2011`

(thermo-system)=

## Thermodynamic system

A thermodynamic system is a distinct space which is defined by
*system boundaries*. The system can have various attributes, for example it may
be

- *open* or *close* for mass transport over its boundaries,
- *open* or *close* for transport of energy (e.g. by heat or work)

{numref}`thermodynamic-systems` illustrates these concepts.

```{note}
In this workshop we will only work with open systems with respect to mass
transport. With respect to energy the systems may either be open or close. An
important type of system is a system that does not allow transport of heat over
its boundaries. This type of system is called *adiabatic*. Systems that do not
transfer work over their system boundaries do not get a specific name, examples
are heat exchangers.
```

```{figure} /figures/system.svg
---
name: thermodynamic-systems
---
Illustration of different types of thermodynamic systems
```

If you take a snapshot of the system in time and describe its inner properties,
you describe the *state* of the system. The state includes information like
pressure, temperature, type of fluid or phase (liquid/gaseous) of the fluid.
The state of a system is not fixed, it may change during a
*thermodynamic process*. {numref}`thermodynamic-processes` shows a snapshot of
a closed thermodynamic system before and after a process has taken place. The
system changed its state.

```{figure} /figures/process.svg
---
name: thermodynamic-processes
---
Illustration of a thermodynamic system changing its state through a process
```

Technical systems like a heat pump often consist of many connected *components*
(each component can be considered an individual system), for example, heat
exchangers, compressors, valves, pumps etc.. In these components different
*processes* take place, that change the *state* of a fluid between the inlet of
the component and its outlet. For example, {numref}`thermodynamic-system-open`
shows an electric heater, where a fluid flows through the system. The fluid
changes its state between the inlet and the outlet of the system.

```{figure} /figures/system_open.svg
---
name: thermodynamic-system-open
---
Illustration of a fluid changing its state from 1 to 2 while flowing through an
open system
```
