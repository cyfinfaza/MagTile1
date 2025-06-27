import matplotlib.pyplot as plt
import csv

# === Configuration ===
FILENAME = "trajectory.csv"  # CSV file with indices
ROWS = 15                    # Number of grid rows
COLS = 15                    # Number of grid columns

def load_indices(filename):
    indices = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            for cell in row:
                cell = cell.strip()
                if cell:
                    indices.append(int(cell))
    return indices

def index_to_coord(index, cols):
    return divmod(index-1, cols)  # returns (row, col)

def plot_trajectory(indices, rows, cols):
    coords = [index_to_coord(idx, cols) for idx in indices]
    xs, ys = zip(*[(col, row) for row, col in coords])  # transpose for plotting

    plt.figure(figsize=(6, 6))
    ax = plt.gca()
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(-0.5, rows - 0.5)
    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))
    ax.grid(True)

    # Draw trajectory arrows (blue)
    for i in range(len(xs) - 1):
        dx = xs[i+1] - xs[i]
        dy = ys[i+1] - ys[i]
        ax.arrow(xs[i], ys[i], dx, dy, head_width=0.3, length_includes_head=True, color='blue')

    # Plot intermediate points (black)
    if len(xs) > 2:
        ax.plot(xs[1:-1], ys[1:-1], 'o', color='black', markersize=8)

    # Plot start/end points
    if len(xs) > 0:
        if len(xs) > 1 and xs[0] == xs[-1] and ys[0] == ys[-1]:
            # Start and end are the same: yellow
            ax.plot(xs[0], ys[0], 'o', color='yellow', markersize=12, label='Start/End')
        else:
            # Start (green)
            ax.plot(xs[0], ys[0], 'o', color='green', markersize=10, label='Start')
            # End (red)
            if len(xs) > 1:
                ax.plot(xs[-1], ys[-1], 'o', color='red', markersize=10, label='End')

    ax.invert_yaxis()
    ax.set_title("Electromagnet Grid Trajectory")
    plt.show()

# === Run ===
indices = load_indices(FILENAME)
plot_trajectory(indices, ROWS, COLS)

