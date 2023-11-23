from fluprodia import FluidPropertyDiagram
import numpy as np
from CoolProp.CoolProp import PropsSI
from matplotlib import pyplot as plt


fluid = "R290"

T_1 = 273.15
T_cond = 333.15

p_1 = 5e5
h_1 = PropsSI("H", "P", p_1, "Q", 1, fluid)
s_1 = PropsSI("S", "P", p_1, "Q", 1, fluid)

p_2 = PropsSI("P", "T", T_cond, "Q", 1, fluid)
h_2s = PropsSI("H", "P", p_2, "S", s_1, fluid)
h_2 = h_1 + (h_2s - h_1) / 0.8
s_2 = PropsSI("S", "P", p_2, "H", h_2, fluid)

isentropic = {
    'isoline_property': 's',
    'isoline_value': s_1,
    'starting_point_property': 'p',
    'starting_point_value': p_1 / 1e5,
    'ending_point_property': 'p',
    'ending_point_value': p_2 / 1e5
}
polytropic = {
    'isoline_property': 's',
    'isoline_value': s_1,
    'isoline_value_end': s_2,
    'starting_point_property': 'p',
    'starting_point_value': p_1 / 1e5,
    'ending_point_property': 'p',
    'ending_point_value': p_2 / 1e5
}


diagram = FluidPropertyDiagram(fluid)
diagram.set_unit_system(T='°C', p='bar', h='kJ/kg')
diagram.set_isolines()
diagram.calc_isolines()


fig, ax = plt.subplots(1, figsize=(8, 5))

diagram.draw_isolines(fig, ax, "logph", x_min=200, x_max=800, y_min=1, y_max=100)

data = diagram.calc_individual_isoline(**isentropic)
ax.plot(data['s'], data['T'], label="isentropic")

data = diagram.calc_individual_isoline(**polytropic)
ax.plot(data['s'], data['T'], label="$\eta_\\text{s,cmp}=0.8$")

ax.legend(loc="upper right")
ax.set_ylabel("temperature in °C")
ax.set_xlabel("specific entropy in J/kgK")
ax.set_title(f"T-s diagram with adiabatic compression of {fluid}")
plt.tight_layout()
fig.savefig("compressor.pdf")


T_1 = PropsSI("T", "P", p_2, "H", h_2, fluid)
T_cond = 333.15

p_1 = PropsSI("P", "T", T_cond, "Q", 1, fluid)
h_1 = PropsSI("H", "T", T_1, "P", p_1, fluid)

h_2 = PropsSI("H", "P", p_1, "Q", 0, fluid)

isobaric = {
    'isoline_property': 'p',
    'isoline_value': p_1 / 1e5,
    'starting_point_property': 'h',
    'starting_point_value': h_1 / 1e3,
    'ending_point_property': 'h',
    'ending_point_value': h_2 / 1e3
}


fig, ax = plt.subplots(1, 2, figsize=(8, 5), sharey=True)

diagram.draw_isolines(fig, ax[0], "Ts", x_min=1250, x_max=2500, y_min=0, y_max=120)

data = diagram.calc_individual_isoline(**isobaric)
ax[0].plot(data['s'], data['T'])

ax[0].set_ylabel("temperature in °C")
ax[0].set_xlabel("specific entropy in J/(kgK)")
ax[0].set_title(f"Ts-diagram of {fluid}")

T_1_water = 50 + 273.15
T_2_water = T_cond - 2

h_1_water = PropsSI("H", "T", T_1_water, "P", 2e5, "water")
h_2_water = PropsSI("H", "T", T_2_water, "P", 2e5, "water")

m_working_fluid = 2

Q_working_fluid = m_working_fluid * (h_2 - h_1) / 1e3
h_sat = PropsSI("H", "P", p_1, "Q", 1, fluid)
Q_wf_desup = m_working_fluid * (h_sat - h_1) / 1e3
Q_wf_cond = m_working_fluid * (h_2 - h_sat) / 1e3
m_water = -Q_working_fluid / (h_2_water - h_1_water)

ax[1].plot([0, -Q_wf_desup, -Q_working_fluid], [T - 273.15 for T in [T_1, T_cond, T_cond]], label=fluid)
ax[1].plot([0, -Q_working_fluid], [T - 273.15 for T in [T_2_water, T_1_water]], label="Water")
ax[1].legend()
ax[1].set_title(f"TQ diagram")
ax[1].set_xlabel("transferred heat in kW")
plt.tight_layout()
fig.savefig("heat-exchanger-example.pdf")

p_1 = PropsSI("P", "T", T_cond, "Q", 1, fluid)
h_1 = PropsSI("H", "T", T_1, "P", p_1, fluid)

h_2 = PropsSI("H", "P", p_1, "Q", 0, fluid)

isenthalpic = {
    'isoline_property': 'h',
    'isoline_value': h_2 / 1e3,
    'starting_point_property': 'p',
    'starting_point_value': p_1 / 1e5,
    'ending_point_property': 'p',
    'ending_point_value': 5
}

fig, ax = plt.subplots(1, figsize=(8, 5))

diagram.draw_isolines(fig, ax, "Ts", x_min=1250, x_max=2500, y_min=0, y_max=120)

data = diagram.calc_individual_isoline(**isenthalpic)
ax.plot(data['s'], data['T'])

ax.set_ylabel("temperature in °C")
ax.set_xlabel("specific entropy in J/(kgK)")
ax.set_title(f"Ts-diagram with isenthalpic throttling of {fluid}")
plt.tight_layout()
fig.savefig("valve.pdf")
