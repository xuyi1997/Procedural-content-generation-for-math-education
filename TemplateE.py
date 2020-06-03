import matplotlib.pyplot as plt
import random
import matplotlib.patches as patches

def kc_354():
    # calculate the perimeter of a rectangle with the aid of the formula 2 x (l + b) or 2 x l + 2 x b
    N = random.choice([10, 20])
    #width = random.randint(1, N-2)
    #height = random.randint(1, N-2)
    width = 4
    height = 2
    return N, width, height


def show_grid(fig, N, width, height):
    ax = fig.add_subplot(111)
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1.0))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1.0))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1.0))  
    ax.yaxis.set_minor_locator(plt.MultipleLocator(1.0))
    ax.grid(which='major', axis='x', linewidth=0.5, linestyle='-', color='0.25')
    ax.grid(which='minor', axis='x', linewidth=0.5, linestyle='-', color='0.25')
    ax.grid(which='major', axis='y', linewidth=0.5, linestyle='-', color='0.25')
    ax.grid(which='minor', axis='y', linewidth=0.5, linestyle='-', color='0.25')
    ax.set_xticklabels([i for i in range(N+2)])
    ax.set_yticklabels([i for i in range(N+2)])

    x1 = int((N - width) / 2)
    y1 = int((N - height) / 2)
    rec = patches.Rectangle((float(x1), float(y1)), width, height, linewidth=1, color='r')
    ax.add_patch(rec)
    ax.set_aspect(1. / ax.get_data_ratio())
    plt.show()


if __name__ == "__main__":
    N, width, height = kc_354()
    fig = plt.figure()
    show_grid(fig, N,  width, height)
    print("width: ", width, "height: ", height, "perimeter: ", 2 * (width + height), "area: ", width * height)
