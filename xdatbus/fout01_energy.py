

def extract_total_energies(outcar_file):
    total_energies = []

    with open(outcar_file, "r") as file:
        for line in file:
            if "free  energy   TOTEN" in line:
                energy = float(line.split()[-2])  # Convert the energy value to a float
                total_energies.append(energy)

    return total_energies


outcar_path = "OUTCAR"  # Replace with the path to your OUTCAR file
energies = extract_total_energies(outcar_path)

if energies:
    print("Total Energies at Each Step (eV):")
    for i, energy in enumerate(energies):
        print(f"Step {i+1}: {energy} eV")
else:
    print("Total Energy values not found in the OUTCAR file.")
