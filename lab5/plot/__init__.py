import numpy as np


def phasePortrait(ax, f, u_range, v_range, args=(), n_grid=100):
    # function from webside:
    # http://be150.caltech.edu/2017/handouts/dynamical_systems_approaches.html
    """
    Plots the flow field with line thickness proportional to speed.

    Parameters
    ----------
    ax : Matplotlib Axis instance
        Axis on which to make the plot
    f : function for form f(y, t, *args)
        The right-hand-side of the dynamical system.
        Must return a 2-array.
    u_range : array_like, shape (2,)
        Range of values for u-axis.
    v_range : array_like, shape (2,)
        Range of values for v-axis.
    args : tuple, default ()
        Additional arguments to be passed to f
    n_grid : int, default 100
        Number of grid points to use in computing
        derivatives on phase portrait.

    Returns
    -------
    output : Matplotlib Axis instance
        Axis with streamplot included.
    """

    # Set up u,v space
    u = np.linspace(u_range[0], u_range[1], n_grid)
    v = np.linspace(v_range[0], v_range[1], n_grid)
    uu, vv = np.meshgrid(u, v)

    # Compute derivatives
    u_vel = np.empty_like(uu)
    v_vel = np.empty_like(vv)
    for i in range(uu.shape[0]):
        for j in range(uu.shape[1]):
            u_vel[i, j], v_vel[i, j] = f(np.array([uu[i, j], vv[i, j]]), None, *args)

    # Compute speed
    speed = np.sqrt(u_vel ** 2 + v_vel ** 2)

    # Make linewidths proportional to speed,
    # with minimal line width of 0.5 and max of 3
    lw = 0.5 + 2.5 * speed / speed.max()

    # Make stream plot
    ax.streamplot(uu, vv, u_vel, v_vel, linewidth=lw, arrowsize=1.2,
                  density=1, color='grey')

    # Steady states if there is no change, so if dS**2+dI**2=0
    cords = np.argwhere(u_vel**2 == -v_vel**2)
    ax = plotSteadyStates(ax, cords, u, v)

    return ax


def plotSteadyStates(ax, cords, u, v):

    if cords.any():  # if any steady state exists
        points_x = []
        points_y = []
        for cord in cords:
            points_x.append(u[cord[0]])
            points_y.append(v[cord[1]])

        ax.plot(points_x, points_y, 'o', color='red', markersize=5, label=' steady states')

    return ax