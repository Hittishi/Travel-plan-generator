# Travel-plan-generator

Implemented a travel plan according to the user's needs. The user can request a specific travel route in the form of a graph, then request the best possible route according to
a) Price: The path that is low at cost
b) Time: The route that takes the least amount of time
c) Directness: The route with the fewest number of connections
The user will request routes through text prompts, according to their needs. When a user is required to find the cheapest route, we change the weights of the graph into prices, similarly when they require for the shortest path, the weights are updated as distances. Utilized Prim's and Kruskal's graph algorithms to optimize travel routes.
