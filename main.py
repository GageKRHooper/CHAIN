# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 06:42:08 2025

@author: gagek
"""

import numpy as np
import matplotlib.pyplot as plt
import random


class MF:
    @staticmethod
    def Rot2d(pos, angle, length):
        x1, y1 = pos
        rad = angle * (np.pi / 180)
        x2 = round(x1 + length * np.cos(rad), 8)
        y2 = round(y1 + length * np.sin(rad), 8)
        return x2, y2


class Neuron:
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.dendriteCounter = 1
        self.axonCounter = 1
        self.dendrites = {}
        self.axon_terminals = {}  

    def growDendrite(self, pos, parent_angle, length, growthRate):
        newLength = length * growthRate
        angle = parent_angle + random.uniform(-45, 45)  # Slight variation from parent angle
        dendrite_id = f"dendrite_{self.dendriteCounter}"
        self.dendriteCounter += 1
        x, y = MF.Rot2d(pos, angle, newLength)
        self.dendrites[dendrite_id] = {
            "start": pos,
            "end": (x, y),
            "angle": angle,
            "length": newLength
        }

    def branchDendrite(self, pos, parent_angle, length, growthRate, sprouts=2):
        newLength = length * growthRate
        angleOffset = 180  # Fixed offset for branching angles
        for i in range(sprouts):
            dendrite_id = f"dendrite_{self.dendriteCounter}"
            self.dendriteCounter += 1
            sprout_angle = parent_angle + angleOffset * (i - (sprouts - 1) / 2)  # Evenly distribute angles
            x, y = MF.Rot2d(pos, sprout_angle, newLength)
            self.dendrites[dendrite_id] = {
                "start": pos,
                "end": (x, y),
                "angle": sprout_angle,
                "length": newLength
            }
            
    def initAxonTerminal(self, length=20, angle=None):
        """
        Create the initial axon terminal branch.
        If no angle is provided, use the average dendrite angle (if any) and grow in the opposite direction.
        """
        if angle is None:
            if self.dendrites:
                avg_angle = sum([d["angle"] for d in self.dendrites.values()]) / len(self.dendrites)
            else:
                avg_angle = random.uniform(0, 360)
            angle = (avg_angle + 180) % 360

        x, y = MF.Rot2d(self.position, angle, length)
        axon_id = f"axon_{self.axonCounter}"
        self.axonCounter += 1
        self.axon_terminals[axon_id] = {
            "start": self.position,
            "end": (x, y),
            "angle": angle,
            "length": length
        }

    def growAxon(self, pos, parent_angle, length, growthRate):
        """
        Grow a new axon branch from a given position.
        """
        newLength = length * growthRate
        angle = parent_angle + random.uniform(-25, 25)  # Slight variation
        axon_id = f"axon_{self.axonCounter}"
        self.axonCounter += 1
        x, y = MF.Rot2d(pos, angle, newLength)
        self.axon_terminals[axon_id] = {
            "start": pos,
            "end": (x, y),
            "angle": angle,
            "length": newLength
        }

    def branchAxon(self, pos, parent_angle, length, growthRate, sprouts=2):
        """
        Create axon branches (sprouts) from a given position.
        """
        newLength = length * growthRate
        angleOffset = (45 / 2)  # Fixed offset for branching angles
        for i in range(sprouts):
            axon_id = f"axon_{self.axonCounter}"
            self.axonCounter += 1
            sprout_angle = parent_angle + angleOffset * (i - (sprouts - 1) / 2)
            x, y = MF.Rot2d(pos, sprout_angle, newLength)
            self.axon_terminals[axon_id] = {
                "start": pos,
                "end": (x, y),
                "angle": sprout_angle,
                "length": newLength
            }

    def plotDendrites(self):
        labeled = False
        for dendrite in self.dendrites.values():
            start = dendrite["start"]
            end = dendrite["end"]
            if not labeled:
                plt.plot([start[0], end[0]], [start[1], end[1]], 'b-', label='Dendrite')
                labeled = True
            else:
                plt.plot([start[0], end[0]], [start[1], end[1]], 'b-')
            plt.scatter(end[0], end[1], c='g', s=20)
        plt.scatter(self.position[0], self.position[1], c='r', label='Neuron')

    def plotAxonTerminals(self):
        labeled = False
        for branch in self.axon_terminals.values():
            start = branch["start"]
            end = branch["end"]
            if not labeled:
                plt.plot([start[0], end[0]], [start[1], end[1]], 'm-', linewidth=2, label='Axon Terminal')
                labeled = True
            else:
                plt.plot([start[0], end[0]], [start[1], end[1]], 'm-', linewidth=2)
            plt.scatter(end[0], end[1], c='m', s=30)

# Initialize neuron
neuron = Neuron(id=1, position=(0, 0))

# Randomly grow or branch dendrites and create synapses
for _ in range(100):
    choice = random.uniform(0, 1)
    if len(neuron.dendrites) == 0:
        # For the first dendrite, grow directly from the neuron position
        start_pos = neuron.position
        parent_angle = random.uniform(0, 360)
        parent_length = 5
    else:
        # Randomly select a dendrite and get its end position and angle
        parent_dendrite = random.choice(list(neuron.dendrites.values()))
        start_pos = parent_dendrite["end"]
        parent_angle = parent_dendrite["angle"]
        parent_length = parent_dendrite["length"]

    growthRate = random.uniform(0.5, 1)

    if choice > 0.1:
        neuron.growDendrite(start_pos, parent_angle, parent_length, growthRate)
    elif choice > 0.4:
        neuron.branchDendrite(start_pos, parent_angle, parent_length, growthRate)

# Initialize the axon terminal based on dendrite information.
neuron.initAxonTerminal(length=10)

# Now, randomly grow and branch the axon terminal similarly to dendrites.
for _ in range(100):
    # Randomly select an existing axon branch to extend.
    parent_axon = random.choice(list(neuron.axon_terminals.values()))
    pos = parent_axon["end"]
    parent_angle = parent_axon["angle"]
    parent_length = parent_axon["length"]
    growthRate = random.uniform(0.5, 1.1)
    choice = random.uniform(0, 1)
    if choice > 0.2:
        neuron.growAxon(pos, parent_angle, parent_length, growthRate)
    else:
        neuron.branchAxon(pos, parent_angle, parent_length, growthRate)

# Plot dendrites, synapses, and axon terminals
plt.figure(figsize=(10, 10))
neuron.plotDendrites()
neuron.plotAxonTerminals()
plt.title("Neuron: Dendrites, Synapses, and Axon Terminal Branches")
plt.xlabel("X")
plt.ylabel("Y")
plt.axis('equal')
plt.legend()
plt.show()
