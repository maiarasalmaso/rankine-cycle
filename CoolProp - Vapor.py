import tkinter as tk
from tkinter import ttk
import CoolProp.CoolProp as CP
from iapws import IAPWS97
from ttkthemes import ThemedStyle

class SteamCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rankine Calculator")
        self.root.minsize(400, 200)
        self.style = ThemedStyle(root)
        self.style.set_theme("radiance")

        # Variáveis de entrada
        self.temperature_1_var = tk.DoubleVar(value=450)
        self.pressure_1_var = tk.DoubleVar(value=7)
        self.pressure_2s_var = tk.DoubleVar(value=2.5)
        self.temperature_3_var = tk.DoubleVar(value=420)
        self.pressure_3_var = tk.DoubleVar(value=2.5)
        self.pressure_4_var = tk.DoubleVar(value=1)
        self.pressure_5s_var = tk.DoubleVar(value=0.007)
        self.pressure_6_var = tk.DoubleVar(value=0.007)
        self.pressure_8_var = tk.DoubleVar(value=1)

        # Variáveis de saída
        self.enthalpy_1_var = tk.StringVar(value="")
        self.T1sat_var = tk.StringVar(value="")
        self.enthalpy_2s_var = tk.StringVar(value="")
        self.temperature_T2s_var = tk.StringVar(value="")
        self.enthalpy_3_var = tk.StringVar(value="")
        self.T3sat_var = tk.StringVar(value="")
        self.enthalpy_4_var = tk.StringVar(value="")
        self.T4sat_var = tk.StringVar(value="")
        self.enthalpy_5s_var = tk.StringVar(value="")
        self.temperature_T5s_var = tk.StringVar(value="")
        self.T5sat_var = tk.StringVar(value="")
        self.enthalpy_6_var = tk.StringVar(value="")
        self.T6sat_var = tk.StringVar(value="")
        self.enthalpy_8_var = tk.StringVar(value="")
        self.T8sat_var = tk.StringVar(value="")
        self.work_turbine_var = tk.StringVar(value="")
        self.n_var = tk.StringVar(value="")
        self.h4_var = tk.StringVar(value="")
        self.h5_var = tk.StringVar(value="")
        self.h2_var = tk.StringVar(value="")
        self.m_var = tk.StringVar(value="")
        self.ncycle_var = tk.StringVar(value="")

        self.create_input_widgets()
        self.create_output_widgets()

    def calculate_enthalpies(self):
        # State 1 calculations
        fluid_name = 'water'
        temperature_1 = self.temperature_1_var.get()
        pressure_1 = self.pressure_1_var.get()
        temperature_1K = temperature_1 + 273.15
        h1 = CP.PropsSI('H', 'T', temperature_1K, 'P', pressure_1 * 1e6, fluid_name) / 1000  # Convert J/kg to kJ/kg
        self.enthalpy_1_var.set(f"Enthalpy (h1): {h1:.2f} kJ/kg")
        T1sat = CP.PropsSI('T', 'P', pressure_1 * 1e6, 'Q', 0, fluid_name) - 273.15
        self.T1sat_var.set(f"Saturation Temperature (T1sat): {T1sat:.2f} °C")

        # State 2s calculations
        pressure_2s = self.pressure_2s_var.get()
        sat_steam_2s = IAPWS97(P=pressure_2s, x=1)
        h2s = sat_steam_2s.h
        T2s = sat_steam_2s.T
        self.enthalpy_2s_var.set(f"Enthalpy (h2s): {h2s:.2f} kJ/kg")
        self.temperature_T2s_var.set(f"Saturation Temperature (T2s): {T2s:.2f} °C")

        # State 3 calculations
        temperature_3 = self.temperature_3_var.get()
        pressure_3 = self.pressure_3_var.get()
        temperature_3K = temperature_3 + 273.15
        h3 = CP.PropsSI('H', 'T', temperature_3K, 'P', pressure_3 * 1e6, fluid_name) / 1000  # Convert J/kg to kJ/kg
        self.enthalpy_3_var.set(f"Enthalpy (h3): {h3:.2f} kJ/kg")
        T3sat = CP.PropsSI('T', 'P', pressure_3 * 1e6, 'Q', 0, fluid_name) - 273.15
        self.T3sat_var.set(f"Saturation Temperature (T3sat): {T3sat:.2f} °C")

        # State 4 calculations
        pressure_4 = self.pressure_4_var.get()
        sat_steam_4 = IAPWS97(P=pressure_4, x=1)
        h4s = sat_steam_4.h
        self.enthalpy_4_var.set(f"Enthalpy (h4s): {h4s:.2f} kJ/kg")
        T4sat = CP.PropsSI('T', 'P', pressure_4 * 1e6, 'Q', 1, fluid_name) - 273.15
        self.T4sat_var.set(f"Saturation Temperature (T4sats): {T4sat:.2f} °C")

        # State 5s calculations
        pressure_5s = self.pressure_5s_var.get()
        sat_steam_5s = IAPWS97(P=pressure_5s, x=1)
        h5s = sat_steam_5s.h
        self.enthalpy_5s_var.set(f"Enthalpy (h5s): {h5s:.2f} kJ/kg")
        T5s = sat_steam_5s.T
        self.temperature_T5s_var.set(f"Saturation Temperature (T5s): {T5s:.2f} °C")
        T5sat = CP.PropsSI('T', 'P', pressure_5s * 1e6, 'Q', 1, fluid_name) - 273.15
        self.T5sat_var.set(f"Saturation Temperature (T5sat): {T5sat:.2f} °C")

        # State 6 calculations
        pressure_6 = self.pressure_6_var.get()
        sat_water = IAPWS97(P=pressure_6, x=0)
        h6 = sat_water.h
        self.enthalpy_6_var.set(f"Enthalpy (h6=h7): {h6:.2f} kJ/kg")
        T6sat = sat_water.T - 273.15
        self.T6sat_var.set(f"Saturation Temperature (T6sat = T7sat): {T6sat:.2f} °C")
        
        # State 8 calculations
        pressure_8 = self.pressure_8_var.get()
        sat_water_8 = IAPWS97(P=pressure_8, x=0)
        h8 = sat_water_8.h
        T8sat = sat_water_8.T - 273.15
        self.enthalpy_8_var.set(f"Enthalpy (h8): {h8:.2f} kJ/kg")
        self.T8sat_var.set(f"Saturation Temperature (T8sat): {T8sat:.2f} °C")
        
        # Calculations of final values
        h3 = float(self.enthalpy_3_var.get().split(":")[1].split()[0])
        h4 = float(self.enthalpy_4_var.get().split(":")[1].split()[0])
        h4s = float(self.enthalpy_4_var.get().split(":")[1].split()[0])
        h5s = float(self.enthalpy_5s_var.get().split(":")[1].split()[0])

        work_turbine = h3 - h4
        self.work_turbine_var.set(f"work_turbine: {work_turbine:.2f} kJ/kg")

        n = 0.83  # assuming a constant value for 'n' for now

        h4 = h3 - n * (h3 - h4s)
        self.h4_var.set(f"Enthalpy (h4): {h4:.4f} kJ/kg")

        h5 = h4 - n * (h4 - h5s)
        self.h5_var.set(f"Enthalpy(h5): {h5:.2f} kJ/kg")

        h2 = (h1) - (0.785) * (h1 - h2s)
        self.h2_var.set(f"Enthalpy(h2): {h2:.2f} kJ/kg")

        m = (h8 - h6) / (h4 - h6)
        self.m_var.set(f"m: {m:.5f} kg/s")

        ncycle = (((h1 - h2) + (h3 - h4s) + (1 - m) * (h4s - h5)) / ((h1 - h8) + (h3 - h2)))*100
        self.ncycle_var.set(f"ncycle: {ncycle:.4f} %")

    def create_input_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="State 1 :").grid(row=0, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(frame, text="Temperature (°C):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.temperature_1_var).grid(row=1, column=1, sticky=tk.W)

        ttk.Label(frame, text="Pressure (MPa):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.pressure_1_var).grid(row=2, column=1, sticky=tk.W)

        ttk.Label(frame, text="State 2s:").grid(row=3, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(frame, text="Pressure (MPa):").grid(row=4, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.pressure_2s_var).grid(row=4, column=1, sticky=tk.W)

        ttk.Label(frame, text="State 3:").grid(row=5, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(frame, text="Temperature (°C):").grid(row=6, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.temperature_3_var).grid(row=6, column=1, sticky=tk.W)

        ttk.Label(frame, text="Pressure (MPa):").grid(row=7, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.pressure_3_var).grid(row=7, column=1, sticky=tk.W)

        ttk.Label(frame, text="State 4s:").grid(row=9, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(frame, text="Pressure (MPa):").grid(row=10, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.pressure_4_var).grid(row=10, column=1, sticky=tk.W)

        ttk.Label(frame, text="State 5s:").grid(row=11, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(frame, text="Pressure (MPa):").grid(row=12, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.pressure_5s_var).grid(row=12, column=1, sticky=tk.W)

        ttk.Label(frame, text="State 6:").grid(row=13, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(frame, text="Pressure (MPa):").grid(row=14, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.pressure_6_var).grid(row=14, column=1, sticky=tk.W)

        ttk.Label(frame, text="State 8:").grid(row=15, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Label(frame, text="Pressure (MPa):").grid(row=16, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.pressure_8_var).grid(row=16, column=1, sticky=tk.W)

        ttk.Button(frame, text="Calculate", command=self.calculate_enthalpies).grid(row=18, column=0, columnspan=2, pady=10)

    def create_output_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
    
        ttk.Label(frame, textvariable=self.enthalpy_1_var).grid(row=1, column=2, sticky=tk.W)
        ttk.Label(frame, textvariable=self.T1sat_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Label(frame, textvariable=self.enthalpy_2s_var).grid(row=2, column=2, sticky=tk.W)
        ttk.Label(frame, textvariable=self.temperature_T2s_var).grid(row=2, column=0, sticky=tk.W)
        ttk.Label(frame, textvariable=self.enthalpy_3_var).grid(row=3, column=2, sticky=tk.W)
        ttk.Label(frame, textvariable=self.T3sat_var).grid(row=3, column=0, sticky=tk.W)
        ttk.Label(frame, textvariable=self.enthalpy_4_var).grid(row=4, column=2, sticky=tk.W)
        ttk.Label(frame, textvariable=self.T4sat_var).grid(row=4, column=0, sticky=tk.W)
        ttk.Label(frame, textvariable=self.enthalpy_5s_var).grid(row=5, column=2, sticky=tk.W)
        ttk.Label(frame, textvariable=self.temperature_T5s_var).grid(row=5, column=0, sticky=tk.W)
        ttk.Label(frame, textvariable=self.T5sat_var).grid(row=6, column=0, sticky=tk.W)
        ttk.Label(frame, textvariable=self.enthalpy_6_var).grid(row=6, column=2, sticky=tk.W)
        ttk.Label(frame, textvariable=self.T6sat_var).grid(row=7, column=0, sticky=tk.W)
        ttk.Label(frame, textvariable=self.enthalpy_8_var).grid(row=7, column=2, sticky=tk.W)
        ttk.Label(frame, textvariable=self.T8sat_var).grid(row=8, column=0, sticky=tk.W)
        ttk.Label(frame, textvariable=self.work_turbine_var).grid(row=4, column=3, sticky=tk.W)
        ttk.Label(frame, textvariable=self.n_var).grid(row=1, column=3, sticky=tk.W)
        ttk.Label(frame, textvariable=self.h5_var).grid(row=8, column=2, sticky=tk.W)
        ttk.Label(frame, textvariable=self.h2_var).grid(row=9, column=2, sticky=tk.W)
        ttk.Label(frame, textvariable=self.h4_var).grid(row=10, column=2, sticky=tk.W)  # Ajuste para a linha 8, coluna 0
        ttk.Label(frame, textvariable=self.m_var).grid(row=2, column=3, sticky=tk.W)
        ttk.Label(frame, textvariable=self.ncycle_var).grid(row=3, column=3, sticky=tk.W)


if __name__ == "__main__":
    root = tk.Tk()
    app = SteamCalculatorApp(root)
    root.mainloop()
