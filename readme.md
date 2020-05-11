# Genetic algorithm to solve a maze problem, with A* to execute the best route

This program was implemented as an exercise to the IA discipline in the course of Software Engineering.

I developed this program using genetic algorithms and refining the solution with A*.

## What you need to run this program

To run this python script you need a maze file. It must be written with strings. 0 represents floor; 1 represents walls; B represents holes (similar to walls); E represents entrance (where the player starts); S represents exit (the final solution). Check the "maze.txt" file for an example.

## How to run this program

To run this program you must have python 3 installed. Then you need the numpy dependency. You can install the required dependencies using:

```
pip3 install -r requirements.txt
```

Then you are ready to run the script:

```
python3 main.py maze.txt
```

The script accepts the following flags:

```
-p = Population size of the algorithm. This represents the amount of chromosomes to test.
-m = The mutation chance of a chromosome after crossover. It basically changes a random move inside a chromosome.
-ml = Move limit. This represents the amount of moves each chromosome contains. It's recommended to set to the amount of empty cells inside the maze.
-i = The amount of iterations the algorithm will try before giving up if no solution is found.
```

Example, to run the maze with a population of 101 chromosomes, run:

```
python3 main.py maze.txt -p 101
```

## What is the heuristic function

This scripts implements the Euclidean Distance if it finds the exit of the maze, plus penalties for hitting holes/walls. If the exit is not found in the chromosome, it sums 1000 to the sum of penalties. The objective is achieve a result of 0 from the heuristic function. This means that the player is at the exit and didn't hit any walls/holes.

## What to expect from this script
This script will show the best path between the entrance and exit of the maze if a solution is found.
