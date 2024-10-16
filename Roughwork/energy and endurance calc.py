#This code is used to identify, given a certain energy capacity, how much volume is required in the AUV. 
import math as math
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
o2_vol_density_m3_per_h2_mol = 0.5*(ideal_gas_constant * h2_tank_temperature_K)/h2_tank_pressure_Pa #0.5 multiplier because half the h2 moles are required
total_vol_density_m3_per_h2_mol = h2_vol_density_m3_per_h2_mol + o2_vol_density_m3_per_h2_mol
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
fuel_vol_limit_m = fuel_allocation_factor_vol * AUV_vol_m3


######################################
## Capacity Calculations ##
######################################
h2_moles_from_mass_limit = fuel_mass_limit_kg/total_mass_density_kg_per_h2_mol
h2_moles_from_vol_limit = fuel_vol_limit_m/total_vol_density_m3_per_h2_mol

print("With the following configurations: ")
print(f"Hydrogen Tank Pressure (Pa): {h2_tank_pressure_Pa}")
print(f"Hydrogen Tank Temperature (K): {h2_tank_temperature_K}")
print(f"Oxygen Tank Pressure (Pa): {o2_tank_pressure_Pa}")
print(f"Oxygen Tank Temperature (K): {o2_tank_temperature_K}")
print(f"AUV length (m): {AUV_length_m}")
print(f"AUV diameter (m): {AUV_diameter_m}")
print(f"AUV mass (kg): {AUV_mass_kg}")
print(f"AUV vol (m3): {AUV_vol_m3}")


if h2_moles_from_mass_limit < h2_moles_from_vol_limit:
    print("Mass is the limiting factor")
    final_h2_moles = h2_moles_from_mass_limit
else:
    print("Volume is the limiting factor")
    final_h2_moles = h2_moles_from_vol_limit

final_h2_mass_kg = final_h2_moles * 2.01568 * 0.001
final_o2_mass_kg = final_h2_moles * 0.5 * 31.999 * 0.001

final_h2_vol_m3 = (final_h2_moles * ideal_gas_constant * h2_tank_temperature_K)/h2_tank_pressure_Pa
final_o2_vol_m3 = (final_h2_moles * 0.5 * ideal_gas_constant * o2_tank_temperature_K)/o2_tank_pressure_Pa

#h2_tank_volume = final_h2_mass_kg/



#This equation is assuming 50% energy efficiency
total_energy_capacity_kWh = final_h2_mass_kg * 0.5 * 33

#Hotel loads from relevant sensors in Watts
mbes = 130 #SeaBat T50-S
sss = 12 #SeaKing SSS for AUV/ROV
ctd = 0.046 #RBR Leganto CTD

#Hotel load from control electronics
pcb = 5 #RP4
ai_board = 15 #NVIDIA Jetson Orin Nano

hotel_load = mbes+sss+ctd+pcb+ai_board
#Propellor power draw
propellor = 402 #Blue Robotics T500

A = 2*math.pi*(AUV_diameter_m/2)*AUV_length_m + 2*math.pi*((AUV_diameter_m/2)**2)#area of the vehicle 
cd = 0.0075 #drag coefficient of Tethys AUV
velocity = 2
n = 0.7 #typical efficiency of propulsive system on Tethys AUV

propulsive_power = 0.5*((cd * A * 1025 * (velocity)**3))/n

total_power_draw = (hotel_load+propulsive_power)/1000
print('Total power draw is', total_power_draw, 'Watts')

#Endurance in hours

Endurance = total_energy_capacity_kWh/total_power_draw 
Distance_travelled = ((2*(total_energy_capacity_kWh*3.6e6))/3)*(((n/(cd*A*1025*(hotel_load**2))))**0.333) #this calculation takes Joules as the energy capacity onboard, hence the multiplying factor I have included

fuel_consumption_rate = total_power_draw/(33*0.5)


print("")
print("Giving the following storage capacities")
print(f"Hydrogen storage mass (Kg): {final_h2_mass_kg}")
print(f"Oxygen storage mass (Kg): {final_o2_mass_kg}")
print(f"Hydrogen storage volume (m3): {final_h2_vol_m3}")
print(f"Oxygen storage volume (m3): {final_o2_vol_m3}")
print(f"Energy Capacity (kWh)= {total_energy_capacity_kWh}")
print(f"Total Power Draw (kW)= {total_power_draw}")
print(f"Number of hours AUV can run for = {Endurance}")
print(f"Alternative endurance calculation = {Distance_travelled/1000}")
