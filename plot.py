import matplotlib.pyplot as plt

def plot_map(normal, manic, depressed, elated, down, description, date):
    # create data
    normal = normal[::-1]
    manic = manic[::-1]
    depressed = depressed[::-1]
    elated = elated[::-1]
    down = down[::-1]
    x = date[::-1]
    description = description[::-1]
    # plot
    for i in range(len(normal)):
        if int(depressed[i]):
            y = "depressed"
            plt.plot(x[i], y, 'bo')
        elif int(manic[i]):
            y = "manic"
            plt.plot(x[i], y, 'ro')
        elif int(elated[i]):
            y = "elated"
            plt.plot(x[i], y, 'yo')
        elif int(down[i]):
            y = "down"
            plt.plot(x[i], y, 'co')
        else:
            y = "neutral"
            plt.plot(x[i], y, 'go')
        plt.annotate(description[i], (x[i], y))
    plt.ylabel("Mood Rating")
    plt.xlabel("Time")
    plt.title("Emotion Recognition Chart")
    plt.gcf().autofmt_xdate()
    axes = plt.gca()
    axes.set_yticks(["depressed", "down", "neutral", "elated", "manic"])
    plt.show()
    plt.savefig("results/result.png")