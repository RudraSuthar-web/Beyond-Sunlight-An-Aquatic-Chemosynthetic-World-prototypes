from typing import List, Tuple
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Patch

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
            dx, dy = random.randint(-1, 1), random.randint(-1, 1)
            organism.move(dx, dy, self.size[0], self.size[1])

            feature = self.get_nearby_feature(organism)
            compound = random.choice(feature.compounds)
            temperature = self.temperature_map[organism.x][organism.y]
            pressure = self.pressure_map[organism.x][organism.y]
            energy_gained = organism.metabolize(compound, temperature, pressure)

            print(f"{organism.name} at ({organism.x}, {organism.y}) gained {energy_gained:.2f} energy from {compound.name} at {feature.name}")

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
        energies = {
            'Microbe': sum(o.energy for o in self.organisms if o.name == "Sulfur-oxidizing Microbe") / sum(1 for o in self.organisms if o.name == "Sulfur-oxidizing Microbe"),
            'Tubeworm': sum(o.energy for o in self.organisms if o.name == "Giant Tubeworm") / sum(1 for o in self.organisms if o.name == "Giant Tubeworm"),
            'Crab': sum(o.energy for o in self.organisms if o.name == "Yeti Crab") / sum(1 for o in self.organisms if o.name == "Yeti Crab")
        }
        return x_features, y_features, x_organisms, y_organisms, colors, sizes, energies

def create_ocean_world(size: Tuple[int, int]) -> Ecosystem:
    hydrogen_sulfide = ChemicalCompound("Hydrogen Sulfide", 0.5)
    methane = ChemicalCompound("Methane", 0.7)
    iron = ChemicalCompound("Iron", 0.3)

    features = [
        GeologicalFeature("Hydrothermal Vent", [hydrogen_sulfide, iron], random.randint(0, size[0]-1), random.randint(0, size[1]-1))
        for _ in range(3)
    ] + [
        GeologicalFeature("Methane Seep", [methane], random.randint(0, size[0]-1), random.randint(0, size[1]-1))
        for _ in range(2)
    ]

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

def animate(frame, ecosystem, scatter_organisms, scatter_features, title, energy_text):
    ecosystem.simulate_cycle()
    x_features, y_features, x_organisms, y_organisms, colors, sizes, energies = ecosystem.get_plot_data()
    scatter_organisms.set_offsets(list(zip(x_organisms, y_organisms)))
    scatter_organisms.set_color(colors)
    scatter_organisms.set_sizes(sizes)
    title.set_text(f"Ocean World Ecosystem Simulation - Cycle: {frame+1}")
    
    energy_text.set_text(f"Avg. Energy: Microbe: {energies['Microbe']:.2f}, Tubeworm: {energies['Tubeworm']:.2f}, Crab: {energies['Crab']:.2f}")
    
    return scatter_organisms, scatter_features, title, energy_text

def main():
    size = (50, 50)
    ocean_world = create_ocean_world(size)

    fig, (ax, ax_energy) = plt.subplots(2, 1, figsize=(12, 14), gridspec_kw={'height_ratios': [3, 1]})
    fig.suptitle("Chemosynthetic Ocean World Ecosystem", fontsize=16)
    
    ax.set_xlim(0, size[0])
    ax.set_ylim(0, size[1])
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")

    x_features, y_features, x_organisms, y_organisms, colors, sizes, _ = ocean_world.get_plot_data()
    scatter_organisms = ax.scatter(x_organisms, y_organisms, c=colors, s=sizes, alpha=0.7)
    scatter_features = ax.scatter(x_features, y_features, c='yellow', marker='^', s=100)

    legend_elements = [
        Patch(facecolor='r', edgecolor='r', label='Sulfur-oxidizing Microbe', alpha=0.7),
        Patch(facecolor='g', edgecolor='g', label='Giant Tubeworm', alpha=0.7),
        Patch(facecolor='b', edgecolor='b', label='Yeti Crab', alpha=0.7),
        Patch(facecolor='yellow', edgecolor='yellow', label='Geological Feature')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    title = ax.text(0.5, 1.05, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5},
                    transform=ax.transAxes, ha="center")

    energy_text = ax_energy.text(0.5, 0.5, "", ha='center', va='center')
    ax_energy.axis('off')

    anim = FuncAnimation(fig, animate, frames=200, interval=200, blit=True, 
                         fargs=(ocean_world, scatter_organisms, scatter_features, title, energy_text))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()