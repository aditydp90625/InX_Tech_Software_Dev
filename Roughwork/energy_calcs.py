#This code is used to identify, given a certain energy capacity, how much volume is required in the AUV. 

######################################
## Storage Calculations ##
######################################

h2_tank_pressure_Pa = 500*100000
h2_tank_temperature_K = 273.15

o2_tank_pressure_Pa = 200*100000
o2_tank_temperature_K = 273.15


## Volumetric Density Calculations ##

# Using pV = nRT
# p = pressure (Pa)
# V = volume (m3)
# n = moles (mol)
# R = 8.3144598 J/(mol*K)
# T = Temperature (Kelvin)
# Rearranged to V/n = RT/p

ideal_gas_constant = 8.3144598 #using mol, Pa, Kelvin, and m3
#All the calculations below are done with reference to 1 h2 mole as then you can account for o2 only requiring 0.5 moles in the reaction
h2_vol_density_m3_per_h2_mol = (ideal_gas_constant * h2_tank_temperature_K)/h2_tank_pressure_Pa
o2_vol_density_m3_per_h2_mol = 0.5*(ideal_gas_constant * o2_tank_temperature_K)/o2_tank_pressure_Pa #0.5 multiplier because half the h2 moles are required

total_vol_density_m3_per_h2_mol = h2_vol_density_m3_per_h2_mol + o2_vol_density_m3_per_h2_mol

# Alternative calculation methodology



print(total_vol_density_m3_per_h2_mol)

## Gravimetric Density Calculations ##

# Using Mass = Mr * mol
# Can figure out how much weight will be taken up by the fuel

# Mr of H2 =  2.01568 g/mol
h2_mass_density_kg_per_h2_mol = 2.01568 * 1 * 0.001
# Mr of O2 = 31.999 g/mol
# Note: 0.5 instead of 1 is used for mol for O2 based on the stoichometry 
o2_mass_density_kg_per_h2_mol = 31.999 * 0.5 * 0.001
total_mass_density_kg_per_h2_mol = h2_mass_density_kg_per_h2_mol + o2_mass_density_kg_per_h2_mol
print(total_mass_density_kg_per_h2_mol)


######################################
## Alternative Fuel Sources ##
######################################

## For Hydrogen ##
# Doing the calculations, what is the ideal gravimetric and volumetric density of hydrogen so that the limit is minimised.
# How exactly to do this?
# It is somethign that has the density of water. Bu this doesn't necessarily mean that energy capacity is maximised. 
# Keeping all options open

# Sodium Borohydride (NaBH4)
# Reversible metal hydride


## For Oxygen ##
# Hydrogen Peroxide
# Chlorate Candles

# https://www.sciencedirect.com/science/article/pii/S0360319919318658

#These are calculations with compressed hydrogen and oxygen

paper_volumetric_density_kg_h2_per_m3_at_700bar = 35
paper_volumetric_density_kg_h2_per_m3_at_350bar = 21
paper_volumetric_density_kg_h2_per_m3_at_200bar = 16

paper_gravimetric_density_kg_h2_per_kg_system_at_700bar = 0.06
paper_gravimetric_density_kg_h2_per_kg_system_at_350bar = 0.032
paper_gravimetric_density_kg_h2_per_kg_system_at_200bar = 0.012

paper_volumetric_density_kg_o2_per_m3_at_153bar = 166.7
paper_gravimetric_density_kg_o2_per_kg_system_at_153bar = 0.213


# For each mole of H2 we need 0.5 mole of O2. 
# This translates to a ratio of 2.01568*1 : 31.999*0.5 = 1:8
# Same ratio can apply for the densities. For every kilo of hydrogen you need roughly 8 times that of oxygen. So the density realistically becomes 1/8 of oxygen

space_required_per_kg_of_h2_and_o2_in_m3 = (1/paper_volumetric_density_kg_h2_per_m3_at_700bar) + 8*(1/paper_volumetric_density_kg_o2_per_m3_at_153bar)
weight_required_per_kg_of_h2_and_o2_in_kg = (1/paper_gravimetric_density_kg_h2_per_kg_system_at_700bar) + 8*(1/paper_gravimetric_density_kg_o2_per_kg_system_at_153bar)


######################################
## AUV Dimensioning Calculations ##
######################################
AUV_diameter_m = 0.5
AUV_length_m = 3

# Using pi*r^2 *l to find the volume of the AUV cylinder
AUV_vol_m3 = 3.141592*((AUV_diameter_m/2)*(AUV_diameter_m/2))*AUV_length_m
# 1025 is the density of saltwater as the AUV has to be neutrally bouyant
AUV_mass_kg = AUV_vol_m3 * 1025

# TODO: The following values need to be checked.
# Is the mass and volume alloc factor the same
fuel_allocation_factor_mass = 0.24  
fuel_allocation_factor_vol = 0.24

fuel_mass_limit_kg = fuel_allocation_factor_mass * AUV_mass_kg
fuel_vol_limit_m3 = fuel_allocation_factor_vol * AUV_vol_m3

print(f"fuel mass limit kg: {fuel_mass_limit_kg}" )
print(f"fuel_vol_limit_m3: {fuel_vol_limit_m3}")


######################################
## Alternative Capacity Calculations ##
######################################
kg_of_h2_volumetric_limit = fuel_vol_limit_m3/space_required_per_kg_of_h2_and_o2_in_m3
kg_of_h2_gravimetric_limit = fuel_mass_limit_kg/weight_required_per_kg_of_h2_and_o2_in_kg

if kg_of_h2_gravimetric_limit>kg_of_h2_volumetric_limit:
    print("Volume is limiting factor")
    final_h2_mass_kg = kg_of_h2_volumetric_limit
else:
    print("weight is limiting factor")
    final_h2_mass_kg = kg_of_h2_gravimetric_limit

final_h2_system_vol_m3 = final_h2_mass_kg/paper_volumetric_density_kg_h2_per_m3_at_700bar
final_h2_system_mass_kg = final_h2_mass_kg/paper_gravimetric_density_kg_h2_per_kg_system_at_700bar

final_o2_mass_kg = final_h2_mass_kg*8 #This is a relatively rough approx
final_o2_system_mass_kg = final_o2_mass_kg/paper_gravimetric_density_kg_o2_per_kg_system_at_153bar
final_o2_system_vol_m3 = final_o2_mass_kg/paper_volumetric_density_kg_o2_per_m3_at_153bar

print(f"Hydrogen mass onboard (kg): {final_h2_mass_kg}")
print(f"Oxygen Mass onboard (kg): {final_o2_mass_kg}")

print(f"H2 system mass: {final_h2_system_mass_kg}")
print(f"H2 system volume:  {final_h2_system_vol_m3}")

print(f"O2 system mass: {final_o2_system_mass_kg}")
print(f"O2 system vol: {final_o2_system_vol_m3}")

total_energy_capacity_kWh = final_h2_mass_kg * 0.5 * 33

print(f"Total energy capacity (kWh): {total_energy_capacity_kWh}")


######################################
## Capacity Calculations ##
######################################

# h2_moles_from_mass_limit = fuel_mass_limit_kg/total_mass_density_kg_per_h2_mol
# h2_moles_from_vol_limit = fuel_vol_limit_m/total_vol_density_m3_per_h2_mol

# print("With the following configurations: ")
# print(f"Hydrogen Tank Pressure (Pa): {h2_tank_pressure_Pa}")
# print(f"Hydrogen Tank Temperature (K): {h2_tank_temperature_K}")
# print(f"Oxygen Tank Pressure (Pa): {o2_tank_pressure_Pa}")
# print(f"Oxygen Tank Temperature (K): {o2_tank_temperature_K}")

# print(f"AUV length (m): {AUV_length_m}")
# print(f"AUV diameter (m): {AUV_diameter_m}")
# print(f"AUV mass (kg): {AUV_mass_kg}")
# print(f"AUV vol (m3): {AUV_vol_m3}")


# if h2_moles_from_mass_limit < h2_moles_from_vol_limit:
#     print("Mass is the limiting factor")
#     final_h2_moles = h2_moles_from_mass_limit
# else:
#     print("Volume is the limiting factor")
#     final_h2_moles = h2_moles_from_vol_limit

# final_h2_mass_kg = final_h2_moles * 2.01568 * 0.001
# final_o2_mass_kg = final_h2_moles * 0.5 * 31.999 * 0.001

# final_h2_vol_m3 = (final_h2_moles * ideal_gas_constant * h2_tank_temperature_K)/h2_tank_pressure_Pa
# final_o2_vol_m3 = (final_h2_moles * 0.5 * ideal_gas_constant * o2_tank_temperature_K)/o2_tank_pressure_Pa

# #This equation is assuming 50% energy efficiency
# total_energy_capacity_kWh = final_h2_mass_kg * 0.5 * 33


######################################
## Alternative Capacity Calculations 2 ##
######################################

# print("")
# print("Giving the following storage capacities")
# print(f"Hydrogen storage mass (Kg): {final_h2_mass_kg}")
# print(f"Oxygen storage mass (Kg): {final_o2_mass_kg}")
# print(f"Hydrogen storage volume (m3): {final_h2_vol_m3}")
# print(f"Oxygen storage volume (m3): {final_o2_vol_m3}")
# print(f"Energy Capacity (kWh)= {total_energy_capacity_kWh}")