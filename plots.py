import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import MaxNLocator

plt.rcParams["animation.html"] = "jshtml"
plt.style.use('ggplot')


class Animation2D:
    """
    Create 2D animation

    Parameters
    ----------
    plot_type (str): plot type, the available plots ('line', 'scatter')

    Args
    ----
    fig: plt.figure

    ax:  plt.axes
    """

    def __init__(self, plot_type='line'):
        self.__x = None
        self.__y = None

        self.__xs = None
        self.__ys = None

        self.__plot = None

        self.fig = None
        self.ax = None

        self.__xticker = None
        self.__yticker = None

        self.plot_type = plot_type

        self.types = {'line': self.__line_plot,
                      'scatter': self.__scatter_plot}

    def __points_init(self):
        self.__plot.set_data([], [])
        return self.__plot,

    def __line_plot(self):
        return self.ax.plot([], [])

    def __scatter_plot(self):
        return self.ax.scatter([], [])

    def __animate(self, i):
        self.__xs.append(self.__x[i])
        self.__ys.append(self.__y[i])

        self.__plot.set_data(self.__xs, self.__ys)

        return self.__plot,

    def play_animation(self, x, y, title: str = '', int_axs: bool = False) -> FuncAnimation:
        """
        Parameters
        ----------
        x (np.array or list):

        y (np.array or list):

        title (str): figure title

        int_axs (bool): If True, ticks will take only integer values, provided at least
                        min_n_ticks integers are found within the view limits.

        Returns
        -------
        animation: FuncAnimation
        """
        self.__x = x
        self.__y = y

        self.__xs = []
        self.__ys = []

        self.__xticker = MaxNLocator(integer=int_axs)
        self.__yticker = MaxNLocator(integer=int_axs)

        self.fig = plt.figure()

        self.ax = plt.axes(xlim=(0, x.max() + 1), ylim=(0, y.max() + 1))

        self.ax.xaxis.set_major_locator(self.__xticker)
        self.ax.yaxis.set_major_locator(self.__yticker)
        
        self.ax.set_title(title)

        self.__plot, = self.types[self.plot_type]()

        animation = FuncAnimation(self.fig,
                                  self.__animate,
                                  init_func=self.__points_init,
                                  frames=len(x),
                                  interval=20,
                                  blit=True)
        return animation
