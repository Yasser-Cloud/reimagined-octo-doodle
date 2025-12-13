import pypsa
import pandas as pd
from src.digital_twin.station_scenario import create_substation_alpha

try:
    print("Creating Network...")
    n = create_substation_alpha()
    print("Running LPF...")
    n.lpf()
    
    print("\n--- DEBUG INFO ---")
    print(f"Snapshots: {n.snapshots}")
    
    print("\nChecking Static 'p0' in n.links:")
    if "p0" in n.links.columns:
        print(n.links["p0"])
    else:
        print("Column 'p0' NOT found in n.links (Static Config)")

    print("\nChecking Time-Series 'p0' in n.links_t.p0:")
    print(n.links_t.p0)
    
except Exception as e:
    print(f"\nCRITICAL ERROR: {e}")
