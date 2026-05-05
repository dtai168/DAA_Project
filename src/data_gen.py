import random
from cvrp_core import Customer, CVRPInstance


def random_instance(n_customers: int, capacity: int, seed: int = 0) -> CVRPInstance:
    random.seed(seed)
    depot = Customer(0, 50.0, 50.0, 0)
    customers = []
    for i in range(1, n_customers + 1):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        demand = random.randint(1, 10)
        customers.append(Customer(i, x, y, demand))
    return CVRPInstance(depot=depot, customers=customers, capacity=capacity)
