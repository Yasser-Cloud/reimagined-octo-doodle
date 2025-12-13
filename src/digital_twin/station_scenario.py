import pypsa
import pandas as pd
import numpy as np

def create_substation_alpha():
    """
    Creates a detailed PyPSA network representing 'Substation Alpha'.
    Components:
    - External Grid (High Voltage Source)
    - HV Bus (110kV)
    - Transformer (110kV -> 20kV)
    - MV Bus (20kV)
    - 3 Outgoing Feeders (Lines to loads)
    - 3 Loads (Residential, Commercial, Industrial)
    """
    network = pypsa.Network()

    # 1. Add Buses
    network.add("Bus", "HV_Grid_Bus", v_nom=110.0)
    network.add("Bus", "MV_Station_Bus", v_nom=20.0)
    # Feeder endpoints
    network.add("Bus", "Feeder_1_End", v_nom=20.0)
    network.add("Bus", "Feeder_2_End", v_nom=20.0)
    network.add("Bus", "Feeder_3_End", v_nom=20.0)

    # 2. Add External Grid Connection (Slack Bus)
    network.add("Generator", "External_Grid",
                bus="HV_Grid_Bus",
                p_nom=100.0, # 100 MW capabilities
                control="Slack") # Maintains voltage/frequency

    # 3. Add Main Transformer (The Critical Asset)
    # 3. Add Main Transformer (The Critical Asset)
    # Changed from Link to Transformer to support Linear Power Flow (LPF)
    network.add("Transformer", "T1_Transformer",
                bus0="HV_Grid_Bus",
                bus1="MV_Station_Bus",
                s_nom=40.0, # 40 MVA Rating (s_nom for transformers)
                x=0.1, r=0.01) # Reactance/Resistance for physics calc


    # 4. Add Feeders (Lines)
    # Modeled as typical 20kV underground cables
    line_data = {"x": 0.1, "r": 0.05} # Simplified impedance

    network.add("Line", "Feeder_1_Res",
                bus0="MV_Station_Bus",
                bus1="Feeder_1_End",
                x=line_data["x"], r=line_data["r"],
                s_nom=10.0, length=5.0) # 5km

    network.add("Line", "Feeder_2_Comm",
                bus0="MV_Station_Bus",
                bus1="Feeder_2_End",
                x=line_data["x"], r=line_data["r"],
                s_nom=10.0, length=3.0) # 3km

    network.add("Line", "Feeder_3_Ind",
                bus0="MV_Station_Bus",
                bus1="Feeder_3_End",
                x=line_data["x"], r=line_data["r"],
                s_nom=15.0, length=8.0) # 8km

    # 5. Add Static Loads (Base case)
    # We will modify these dynamically in the application
    network.add("Load", "Load_Residential",
                bus="Feeder_1_End",
                p_set=5.0) # 5 MW

    network.add("Load", "Load_Commercial",
                bus="Feeder_2_End",
                p_set=4.0) # 4 MW

    network.add("Load", "Load_Industrial",
                bus="Feeder_3_End",
                p_set=8.0) # 8 MW

    return network

if __name__ == "__main__":
    n = create_substation_alpha()
    print("Substation Alpha Created Successfully")
    print(n.bfs())
