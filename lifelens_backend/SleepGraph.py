import pandas as pd
import matplotlib.pyplot as plt

class Node:
    def __init__(self, cycle_id, attributes):
        self.cycle_id = cycle_id
        self.attributes = attributes
        
class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        
    def add_node(self, node):
        self.nodes[node.cycle_id] = node
        self.edges[node.cycle_id] = []
        
    def add_edge(self, from_cycle, to_cycle):
        if from_cycle in self.nodes and to_cycle in self.nodes:
            self.edges[from_cycle].append(to_cycle)
            self.edges[to_cycle].append(from_cycle)
            
sleepGraph = Graph()
sleepData = pd.read_csv('sleepData.csv')

##Construct the sleep graph with nodes and edges
for index, row in sleepData.iterrows():
    attributes = {
        "Wake": row["Awake duration (min)"],
        "Light Sleep": row["Light sleep duration (min)"],
        "Deep Sleep": row["Deep (SWS) duration (min)"],
        "REM Sleep": row["REM duration (min)"],
        "Total Sleep": row["Asleep duration (min)"],
        "Sleep Need": row["Sleep need (min)"],
        "Sleep Debt": row["Sleep debt (min)"],
        "Whoop Performance": row["Sleep performance %"],
        "Overall Sleep Performance": None,
        "Light Sleep Performance": None,
        "Deep Sleep Performance": None,
        "REM Sleep Performance": None,
        "Average Sleep Phase Performance": None,
        "Custom Performance": None
    }
    node = Node(cycle_id=index, attributes=attributes)
    sleepGraph.add_node(node)
    
for i in range(len(sleepData)-1):
    sleepGraph.add_edge(i, i+1)
    
# def averageNorms(graph):
#     total_light = 0
#     total_deep = 0
#     total_rem = 0
#     total_sleep = 0
#     node_count = 0
    
#     for node in graph.nodes.values():
#         awake = node.attributes["Wake"]
#         light = node.attributes["Light Sleep"]
#         deep = node.attributes["Deep Sleep"]
#         rem = node.attributes["REM Sleep"]
#         total_sleep = awake+light+deep+rem
        
#         total_light += light/total_sleep
#         total_deep += deep/total_sleep
#         total_rem += rem/total_sleep
#         node_count += 1
        
#     avg_light = total_light/node_count
#     avg_deep = total_deep/node_count
#     avg_rem = total_rem/node_count
#     return avg_light, avg_deep, avg_rem

# avg_light, avg_deep, avg_rem = averageNorms(sleepGraph)

weights = {
    "Light Sleep": 0.55,
    "Deep Sleep": 0.2,
    "REM Sleep": 0.25
}

def sleepPerformance(graph):
    for node in graph.nodes.values():
        awake = node.attributes["Wake"]
        light = node.attributes["Light Sleep"]
        deep = node.attributes["Deep Sleep"]
        rem = node.attributes["REM Sleep"]
        total_sleep = awake+light+deep+rem
        sleep_need = node.attributes.get("Sleep Need", 480)

        overall_sleep_performance = min(total_sleep/sleep_need, 1.0)
        node.attributes["Overall Sleep Performance"] = round(overall_sleep_performance * 100, 2)

def comparePhase(graph):
    for node in graph.nodes.values():
        total_sleep = node.attributes["Total Sleep"]
        
        expected_light = weights["Light Sleep"] * total_sleep
        expected_deep = weights["Deep Sleep"] * total_sleep
        expected_rem = weights["REM Sleep"] * total_sleep
        
        light_sleep = node.attributes["Light Sleep"]
        deep_sleep = node.attributes["Deep Sleep"]
        rem_sleep = node.attributes["REM Sleep"]
        
        light_difference = light_sleep - expected_light
        deep_difference = deep_sleep - expected_deep
        rem_difference = rem_sleep - expected_rem
        
        if(light_difference < 0):
            light_performance = round(abs((light_sleep/expected_light)*100), 2)
        else:
            light_performance = 100
            
        if(deep_difference < 0):
            deep_performance = round(abs((deep_sleep/expected_deep)*100), 2)
        else:
            deep_performance = 100
            
        if(rem_difference < 0):
            rem_performance = round(abs((rem_sleep/expected_rem)*100), 2)
        else:
            rem_performance = 100
        
        averagePhasePerformance = round((light_performance + deep_performance + rem_performance)/3, 0)
        
        node.attributes["Light Sleep Performance"] = {
            "Actual": light_sleep,
            "Expected": round(expected_light, 0),
            "Difference": round(light_difference, 0),
            "Performance": light_performance,
        }
        node.attributes["Deep Sleep Performance"] = {
            "Actual": deep_sleep,
            "Expected": round(expected_deep, 0),
            "Difference": round(deep_difference, 0),
            "Performance": deep_performance,
        }
        node.attributes["REM Sleep Performance"] = {
            "Actual": rem_sleep,
            "Expected": round(expected_rem, 0),
            "Difference": round(rem_difference, 0),
            "Performance": rem_performance,
        }
        node.attributes["Average Sleep Phase Performance"] = {
            "Average Performance": averagePhasePerformance
        }
        
# def customPerformance(graph):
#     for node in graph.nodes.values():
#         awake = node.attributes["Wake"]
#         light = node.attributes["Light Sleep"]
#         deep = node.attributes["Deep Sleep"]
#         rem = node.attributes["REM Sleep"]
#         total_sleep = awake+light+deep+rem
#         sleep_need = node.attributes.get("Sleep Need", 480)
#         sleep_efficiency = node.attributes.get("Sleep Efficiency", 1.0)
        
        
#         if total_sleep < sleep_need:
#             light_norm = light/total_sleep
#             deep_norm = deep/total_sleep
#             rem_norm = rem/total_sleep
#             sleepRatio = min(total_sleep/sleep_need, 1.0)
#             customPerformance = 100 * sleepRatio * (
#                 weights["Light Sleep"] * light_norm +
#                 weights["Deep Sleep"] * deep_norm +
#                 weights["REM Sleep"] * rem_norm
#             )
#             customPerformance = customPerformance * sleep_efficiency
#         else:
#             customPerformance = 100
            
#         node.attributes["Custom Performance"] = round(customPerformance, 0);

# customPerformance(sleepGraph)
sleepPerformance(sleepGraph)
comparePhase(sleepGraph)

for node_id, node in sleepGraph.nodes.items():
    print(f"""
    Cycle {node_id}:
    WHOOP Performance Rating: {node.attributes['Whoop Performance']}
    Sleep Performance: {node.attributes['Overall Sleep Performance']}
    Light Sleep: {node.attributes['Light Sleep Performance']}
    Deep Sleep: {node.attributes['Deep Sleep Performance']}
    REM Sleep: {node.attributes['REM Sleep Performance']}
    Average Sleep Phase Performance: {node.attributes['Average Sleep Phase Performance']}
        """)
    
sleepData['Sleep Date'] = pd.to_datetime(sleepData['Sleep onset']).dt.date

# Update data dictionary with Sleep Date instead of Cycle ID
data = {
    "Sleep Date": [],
    "Average Sleep Phase Performance": [],
    "Sleep Performance": [],
    "WHOOP Performance Rating": []
}

for node_id, node in sleepGraph.nodes.items():
    data["Sleep Date"].append(sleepData.loc[node_id, "Sleep Date"])  # Map node ID to Sleep Date
    data["Average Sleep Phase Performance"].append(node.attributes["Average Sleep Phase Performance"]["Average Performance"])
    data["Sleep Performance"].append(node.attributes["Overall Sleep Performance"])
    data["WHOOP Performance Rating"].append(node.attributes["Whoop Performance"])

df = pd.DataFrame(data)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df["Sleep Date"], df["Average Sleep Phase Performance"], label="Average Sleep Phase Performance", marker='o')
plt.plot(df["Sleep Date"], df["Sleep Performance"], label="Sleep Performance", marker='s')
plt.plot(df["Sleep Date"], df["WHOOP Performance Rating"], label="WHOOP Performance Rating", marker='^')

# Update labels and title
plt.xlabel("Sleep Date")
plt.ylabel("Performance (%)")
plt.title("Comparison of Sleep Metrics Across Dates")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()