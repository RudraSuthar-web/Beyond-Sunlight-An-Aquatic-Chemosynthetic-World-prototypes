import random
from typing import List, Tuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class ChemicalCompound:
    def __init__(self, name: str, energy: float):
        self.name = name
        self.energy = energy

class GeologicalFeature:
    def __init__(self, name: str, compounds: List[ChemicalCompound], x: int, y: int):
        self.name = name
        self.compounds = compounds
        self.x = x
        self.y = y

class Organism:
    def __init__(self, name: str, energy: float, size: float, x: int, y: int):
        self.name = name
        self.energy = energy
        self.size = size
        self.x = x
        self.y = y

    def metabolize(self, compound: ChemicalCompound, temperature: float, pressure: float) -> float:
        energy_gained = compound.energy * self.size
        efficiency = 1 - (abs(temperature - 10) / 20) - (abs(pressure - 200) / 400)
        energy_gained *= max(0, efficiency)
        self.energy += energy_gained
        return energy_gained

    def move(self, dx: int, dy: int, max_x: int, max_y: int):
        self.x = (self.x + dx) % max_x
        self.y = (self.y + dy) % max_y

class Ecosystem:
    def __init__(self, features: List[GeologicalFeature], organisms: List[Organism], size: Tuple[int, int]):
        self.features = features
        self.organisms = organisms
        self.size = size
        self.temperature_map = self.generate_temperature_map()
        self.pressure_map = self.generate_pressure_map()

    def generate_temperature_map(self):
        return [[random.uniform(5, 15) for _ in range(self.size[1])] for _ in range(self.size[0])]

    def generate_pressure_map(self):
        return [[100 + 10 * y for y in range(self.size[1])] for _ in range(self.size[0])]

    def get_nearby_feature(self, organism: Organism) -> GeologicalFeature:
        return min(self.features, key=lambda f: ((f.x - organism.x) ** 2 + (f.y - organism.y) ** 2) ** 0.5)

    def simulate_cycle(self):
        for organism in self.organisms:
            # Move
            dx, dy = random.randint(-1, 1), random.randint(-1, 1)
            organism.move(dx, dy, self.size[0], self.size[1])

            # Interact
            feature = self.get_nearby_feature(organism)
            compound = random.choice(feature.compounds)
            temperature = self.temperature_map[organism.x][organism.y]
            pressure = self.pressure_map[organism.x][organism.y]
            energy_gained = organism.metabolize(compound, temperature, pressure)

            print(f"{organism.name} at ({organism.x}, {organism.y}) gained {energy_gained:.2f} energy from {compound.name} at {feature.name}")

            # Simple predation
            if organism.name == "Yeti Crab" and organism.energy > 10:
                prey = random.choice([o for o in self.organisms if o.name == "Giant Tubeworm"])
                if ((prey.x - organism.x) ** 2 + (prey.y - organism.y) ** 2) ** 0.5 < 2:
                    organism.energy += prey.energy / 2
                    prey.energy /= 2
                    print(f"{organism.name} preyed on {prey.name}")

    def get_plot_data(self):
        x_features = [f.x for f in self.features]
        y_features = [f.y for f in self.features]
        x_organisms = [o.x for o in self.organisms]
        y_organisms = [o.y for o in self.organisms]
        colors = ['r' if o.name == "Sulfur-oxidizing Microbe" else 'g' if o.name == "Giant Tubeworm" else 'b' for o in self.organisms]
        sizes = [o.size * 100 for o in self.organisms]
        return x_features, y_features, x_organisms, y_organisms, colors, sizes

def create_ocean_world(size: Tuple[int, int]) -> Ecosystem:
    # Define chemical compounds
    hydrogen_sulfide = ChemicalCompound("Hydrogen Sulfide", 0.5)
    methane = ChemicalCompound("Methane", 0.7)
    iron = ChemicalCompound("Iron", 0.3)

    # Define geological features
    features = [
        GeologicalFeature("Hydrothermal Vent", [hydrogen_sulfide, iron], random.randint(0, size[0]-1), random.randint(0, size[1]-1))
        for _ in range(3)
    ] + [
        GeologicalFeature("Methane Seep", [methane], random.randint(0, size[0]-1), random.randint(0, size[1]-1))
        for _ in range(2)
    ]

    # Define organisms
    organisms = [
        Organism("Sulfur-oxidizing Microbe", 1.0, 0.01, random.randint(0, size[0]-1), random.randint(0, size[1]-1))
        for _ in range(50)
    ] + [
        Organism("Giant Tubeworm", 5.0, 0.1, random.randint(0, size[0]-1), random.randint(0, size[1]-1))
        for _ in range(20)
    ] + [
        Organism("Yeti Crab", 3.0, 0.05, random.randint(0, size[0]-1), random.randint(0, size[1]-1))
        for _ in range(10)
    ]

    return Ecosystem(features, organisms, size)

def animate(frame, ecosystem, scatter_organisms, scatter_features):
    ecosystem.simulate_cycle()
    x_features, y_features, x_organisms, y_organisms, colors, sizes = ecosystem.get_plot_data()
    scatter_organisms.set_offsets(list(zip(x_organisms, y_organisms)))
    scatter_organisms.set_color(colors)
    scatter_organisms.set_sizes(sizes)
    return scatter_organisms, scatter_features

def main():
    size = (50, 50)
    ocean_world = create_ocean_world(size)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, size[0])
    ax.set_ylim(0, size[1])

    x_features, y_features, x_organisms, y_organisms, colors, sizes = ocean_world.get_plot_data()
    scatter_organisms = ax.scatter(x_organisms, y_organisms, c=colors, s=sizes)
    scatter_features = ax.scatter(x_features, y_features, c='yellow', marker='^', s=100)

    anim = FuncAnimation(fig, animate, frames=200, interval=100, blit=True, 
                         fargs=(ocean_world, scatter_organisms, scatter_features))
    plt.show()

if __name__ == "__main__":
    main()