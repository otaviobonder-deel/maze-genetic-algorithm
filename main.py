from genetic_algorithm import GA
from graph import Graph
from a_star import a_star_search, reconstruct_path
import argparse


def main():

    parser = argparse.ArgumentParser(
        description="Solve a maze problem with genetic algorithm"
    )
    parser.add_argument("maze", help="The maze file to run the algorithm", type=str)
    parser.add_argument(
        "-p", "--population", help="Population size (must be an odd number)", type=int
    )
    parser.add_argument(
        "-m",
        "--mutation",
        help="The mutation chance (must be between 0 and 1)",
        type=float,
    )
    parser.add_argument(
        "-ml", "--move", help="Number of moves allowed to the chromosome", type=int
    )
    parser.add_argument(
        "-i",
        "--iterations",
        help="Number of iterations the algorithm will execute to try to find the exit",
        type=int,
    )

    args = parser.parse_args()

    if not args.population:
        population = 501
    else:
        if args.population % 2 == 0:
            population = args.population + 1
            print("Population must be an odd number. Rounding up to " + str(population))
        else:
            population = args.population

    if not args.mutation:
        mutation = 0.5
    else:
        if args.mutation > 1:
            mutation = 0.5
            print("Mutation must be between 0 and 1. Setting to " + str(mutation))
        else:
            mutation = args.mutation

    if not args.move:
        move = 40
    else:
        move = args.move

    if not args.iterations:
        iterations = 5000
    else:
        iterations = args.iterations

    print("Starting maze")
    print(
        "Maze solving started with variables population="
        + str(population)
        + ", mutation="
        + str(mutation)
        + ", moves="
        + str(move)
        + ", iterations="
        + str(iterations)
    )
    ga1 = GA(move, population, mutation, args.maze)
    x = ga1.search_optional_moves(ga1.population, iterations)
    if x is None:
        print("Solução não encontrada")
    else:
        print("Exit found!")
        print("Chromosome with moves: " + str(x[0]))
        print("Start: " + str(x[1][0]) + " End: " + str(x[1][1]))
        print("Starting A*")
        print("Creating graph")
        graph = Graph(ga1.maze1.Board)
        print("Graph created")
        print("Starting algorithm processing")
        came_from, cost_so_far = a_star_search(graph, x[1][0], x[1][1])
        best_path = reconstruct_path(came_from, x[1][0], x[1][1])
        print("Best path found! It's:")
        print(best_path)


main()
