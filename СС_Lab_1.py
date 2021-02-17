# Chetrar Eugeniu FAF-193
# Variant: (32 + 1) - 6 = 27
from collections import defaultdict

class Graph():
    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, fr, to, weight):
        if fr not in self.graph:
            self.graph[fr][to] = weight
        elif to not in self.graph[fr]:
            self.graph[fr][to] = weight
        else:
            self.graph[fr][to] += weight


    def check_grammar(self, start_node, input):
        res = f"{start_node}"
        node_current = self.graph[start_node]

        i = 0
        inp_len = len(input)
        while i != inp_len:

            flag = False
            for j in node_current.keys():

                if input[i] == node_current[j]:

                    res += f" -> {j}"
                    flag = True

                    if self.graph[j]:
                        node_current = self.graph[j]
                    break

            if not flag:
                break

            i += 1

        if res[-1] != "*":
            print("This string is not accepted by FA")
        else:
            print(f"This string is accepted by FA\n"
                  f"It can be achieved through travelling next nodes {res}")


g = Graph()
g.add_edge("S", "A", "a")
g.add_edge("A", "S", "b")
g.add_edge("S", "B", "b")
g.add_edge("A", "A", "c")
g.add_edge("A", "B", "a")
g.add_edge("B", "B", "a")
g.add_edge("B", "*", "b")

g.check_grammar("S", "abbb")
g.check_grammar("S", "ac")