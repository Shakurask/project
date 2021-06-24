import datetime
import matplotlib.pyplot as plt




def get_timeline(sub_g):
    
    date_timeline = {}
    for j in range(1, 112):
        date_timeline[j]=0

    dates = sub_g.vs["Date"]
    dates = list(map(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d'),dates))

    for date in dates:
        diff = int((date - datetime.datetime(1993, 1, 1)).days/30)
        date_timeline[diff] = date_timeline[diff] + 1
    c = 0
    for (m, count) in date_timeline.items():
        c+=count
        date_timeline[m] = c
    return date_timeline;



def plot_timeline(date_timeline):
    fig, ax = plt.subplots()

    ax.bar(date_timeline.keys(), date_timeline.values())

    ax.set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    fig.set_figwidth(12)    #  ширина Figure
    fig.set_figheight(6)    #  высота Figure

    plt.show()



def get_child_timeline(cluster, timeline):
    child_timeline = get_timeline(cluster)
    for (m, c) in child_timeline.items():
        if timeline[m] != 0:
            child_timeline[m] = c#/timeline[m]
        else:
            child_timeline[m] = 0
    return  child_timeline