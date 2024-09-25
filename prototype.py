import random
from typing import List, Tuple

class ChemicalCompound:
    def __init__(self, name: str, energy: float):
        self.name = name
        self.energy = energy

class GeologicalFeature:
    def __init__(self, name: str, compounds: List[ChemicalCompound]):
        self.name = name
        self.compounds = compounds

class Organism:
    def __init__(self, name: str, energy: float, size: float):
        self.name = name
        self.energy = energy
        self.size = size

    def metabolize(self, compound: ChemicalCompound) -> float:
        energy_gained = compound.energy * self.size
        self.energy += energy_gained
        return energy_gained

class Ecosystem:
    def __init__(self, features: List[GeologicalFeature], organisms: List[Organism]):
        self.features = features
        self.organisms = organisms

    def simulate_cycle(self):
        for organism in self.organisms:
            feature = random.choice(self.features)
            compound = random.choice(feature.compounds)
            energy_gained = organism.metabolize(compound)
            print(f"{organism.name} gained {energy_gained:.2f} energy from {compound.name} at {feature.name}")

def create_ocean_world() -> Ecosystem:
    # Define chemical compounds
    hydrogen_sulfide = ChemicalCompound("Hydrogen Sulfide", 0.5)
    methane = ChemicalCompound("Methane", 0.7)
    iron = ChemicalCompound("Iron", 0.3)

    # Define geological features
    hydrothermal_vent = GeologicalFeature("Hydrothermal Vent", [hydrogen_sulfide, iron])
    methane_seep = GeologicalFeature("Methane Seep", [methane])

    # Define organisms
    microbe = Organism("Sulfur-oxidizing Microbe", 1.0, 0.01)
    tubeworm = Organism("Giant Tubeworm", 5.0, 0.1)
    crab = Organism("Yeti Crab", 3.0, 0.05)

    return Ecosystem([hydrothermal_vent, methane_seep], [microbe, tubeworm, crab])

def main():
    ocean_world = create_ocean_world()
    for _ in range(10):
        ocean_world.simulate_cycle()

if __name__ == "__main__":
    main()