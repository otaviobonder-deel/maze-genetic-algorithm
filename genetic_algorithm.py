import random
from maze import Maze
import numpy as np
import math


class GA:
    def __init__(self, move_limit, population_size, mutation_chance, maze):
        self.MOVE_LIMIT = move_limit
        self.POPULATION_SIZE = population_size
        self.MUTATION_CHANCE = mutation_chance
        self.population = np.random.randint(
            0, 9, (self.POPULATION_SIZE, self.MOVE_LIMIT)
        )
        self.maze1 = Maze(maze)

    def fitness(self, chromosome):
        moves = []
        for i in range(0, chromosome.size):
            if chromosome[i] == 0:
                moves.append(0)
            elif chromosome[i] == 1:
                moves.append(self.maze1.move_player_up())
            elif chromosome[i] == 2:
                moves.append(self.maze1.move_player_down())
            elif chromosome[i] == 3:
                moves.append(self.maze1.move_player_left())
            elif chromosome[i] == 4:
                moves.append(self.maze1.move_player_right())
            elif chromosome[i] == 5:
                moves.append(self.maze1.move_player_up_right())
            elif chromosome[i] == 6:
                moves.append(self.maze1.move_player_up_left())
            elif chromosome[i] == 7:
                moves.append(self.maze1.move_player_down_right())
            elif chromosome[i] == 8:
                moves.append(self.maze1.move_player_down_left())
        score = self.sum_score(moves, chromosome)
        self.maze1.reset_player()
        return score

    def sum_score(self, moves, chromosome):
        score = 0
        for i in range(0, len(moves)):
            if moves[i] == self.maze1.WALL:
                score += 1
            elif moves[i] == self.maze1.FINISH:
                np.put(chromosome, list(range(i + 1, chromosome.size)), 0)
                score += round(
                    math.sqrt(
                        (
                            self.maze1.finishPosition[0]
                            - self.maze1.playerCurrentPosition[0]
                        )
                        ** 2
                        + (
                            self.maze1.finishPosition[1]
                            - self.maze1.playerCurrentPosition[1]
                        )
                        ** 2
                    ),
                    2,
                )
                break
        if self.maze1.FINISH not in moves:
            score += 1000
        return chromosome, score

    def fittest_score(self, population):
        scores = []
        for i in population:
            scores.append(self.fitness(i))
        scores = np.asarray(scores)
        scores = scores[np.argsort(scores[:, 1])]
        return scores

    def selection(self, population):
        new_population_in_numpy = np.array(population[0][0])
        new_population_in_python = []
        for i in range(1, int((population.shape[0] + 1) / 2)):
            first_parent = self.choose_best_between_choices(
                population[random.randrange(0, population.shape[0])],
                population[random.randrange(0, population.shape[0])],
            )
            second_parent = self.choose_best_between_choices(
                population[random.randrange(0, population.shape[0])],
                population[random.randrange(0, population.shape[0])],
            )
            off_spring = self.cross_over(first_parent, second_parent)
            mutated1 = self.mutate(off_spring[0])
            mutated2 = self.mutate(off_spring[1])
            new_population_in_python.append(mutated1[0])
            new_population_in_python.append(mutated2[0])
        new_population_in_python = np.asarray(new_population_in_python)
        new_population = np.vstack([new_population_in_numpy, new_population_in_python])
        return new_population

    def cross_over(self, first_parent, second_parent):
        crossovers = [
            random.randrange(0, self.MOVE_LIMIT),
            random.randrange(0, self.MOVE_LIMIT),
            random.randrange(0, self.MOVE_LIMIT),
        ]
        crossovers.sort()
        off_spring1 = np.concatenate(
            (
                first_parent[: crossovers[0]],
                second_parent[crossovers[0] : crossovers[1]],
                first_parent[crossovers[1] : crossovers[2]],
                second_parent[crossovers[2] :],
            )
        )
        off_spring2 = np.concatenate(
            (
                second_parent[: crossovers[0]],
                first_parent[crossovers[0] : crossovers[1]],
                second_parent[crossovers[1] : crossovers[2]],
                first_parent[crossovers[2] :],
            )
        )
        return off_spring1, off_spring2

    def mutate(self, chromosome):
        mutation_random = round(random.random(), 2)
        if self.MUTATION_CHANCE > mutation_random:
            mutation_index = random.randrange(0, len(chromosome[0]))
            chromosome[0][mutation_index] = random.randrange(1, 9)
        return chromosome

    def get_start_finish_coordinates(self, moves):
        start_coordinates = self.maze1.fixed_start_position
        end_coordinates = [
            self.maze1.fixed_start_position[0],
            self.maze1.fixed_start_position[1],
        ]
        for i in moves:
            if i == 1:
                end_coordinates[0] = end_coordinates[0] - 1
            elif i == 2:
                end_coordinates[0] = end_coordinates[0] + 1
            elif i == 3:
                end_coordinates[1] = end_coordinates[1] - 1
            elif i == 4:
                end_coordinates[1] = end_coordinates[1] + 1
            elif i == 5:
                end_coordinates[0] = end_coordinates[0] - 1
                end_coordinates[1] = end_coordinates[1] + 1
            elif i == 6:
                end_coordinates[0] = end_coordinates[0] - 1
                end_coordinates[1] = end_coordinates[1] - 1
            elif i == 7:
                end_coordinates[0] = end_coordinates[0] + 1
                end_coordinates[1] = end_coordinates[1] + 1
            elif i == 8:
                end_coordinates[0] = end_coordinates[0] + 1
                end_coordinates[1] = end_coordinates[1] - 1
        return [start_coordinates, tuple(end_coordinates)]

    def choose_best_between_choices(self, chromosome1, chromosome2):
        if chromosome1[1] <= chromosome2[1]:
            return chromosome1
        else:
            return chromosome2

    def search_optional_moves(self, population, stop_count):
        for i in range(0, stop_count):
            most_fit_score = self.fittest_score(population)
            if most_fit_score[0][1] == 0:
                return (
                    most_fit_score[0][0],
                    self.get_start_finish_coordinates(most_fit_score[0][0]),
                )
            else:
                print(
                    "Iteration " + str(i) + ", best score " + str(most_fit_score[0][1])
                )
                population = self.selection(most_fit_score)