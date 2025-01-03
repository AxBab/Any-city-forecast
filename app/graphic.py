import matplotlib.pyplot as plt

# Function to build a grapchic
def build_graph(times: list, temps: list, data_lenght: int, city: str):
    fig = plt.figure(figsize=(data_lenght / 1.5 + 4, 5))
    fig.tight_layout()

    # Customizing the graphic
    ax = fig.add_subplot()
    ax.set_xticks(range(0, data_lenght*7, 7), times, fontsize=9) # Establishing xticks (for time)
    ax.grid() # Establishing the grid
    ax.set_xlabel("Время", fontsize=12, labelpad=10) # Writing the label near x-axis (Time)
    ax.set_ylabel("Температура в °C", fontsize=12, labelpad=10) # Writing the label near y-axis (Temperature)
    ax.set_title(f"Прогноз погоды в городе {city}", fontsize=14) # Writing the title of the graph

    # Data to making the graphic
    x = range(0, data_lenght*7, 7) # Data for X-axis
    y = list(map(lambda t: int(t[:-1]), temps)) # Data for Y-axis

    ax.set_ylim(min(y) - 1, max(y) + 1) # Establishing limits to do graph more readable for people
    ax.plot(x, y) # Drawing a line on the graphic
    ax.scatter(x, y) # Drawing spots on the grapchic
    fig.savefig("app/forecast.png", bbox_inches='tight', pad_inches=0.2) # Saving cropped picture of graphic

# Call this function if run this file
if __name__ == "__main__":
    # Example run
    build_graph(["10:00", "11:00", "12:00", "13:00", "14:00", "15:00"], ["+37o", "+32o", "+24o", "+22o", "+21o", "+20o"], 6, "Каир")