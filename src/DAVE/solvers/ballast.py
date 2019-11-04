"""
Ballasting
"""
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

class tank:
    def __init__(self):
        self.name = "noname"
        self.max = 0
        self.pct = 0
        self.position = np.array((0.,0.,0.))

    def weight(self):
        return self.max *  self.pct / 100

    def is_full(self):
        return self.pct>=100-1e-5

    def is_empty(self):
        return self.pct<=1e-5

    def is_partial(self):
        return (not self.is_empty() and not self.is_full())

    def mxmymz(self):
        return self.position * self.weight()

class system:

    def __init__(self):
        self.tanks = []
        self._target_cog = np.array((0.,0.,0.))
        self._target_wt = 0

    def xyzw(self):
        """Gets the current ballast cog and weight

        Returns:
            ((x,y,z), weight)
        """
        mxmymz = np.array((0.,0.,0.))
        wt = 0

        for tank in self.tanks:
            mxmymz += tank.mxmymz()
            wt += tank.weight()

        if wt==0:
            return (np.array((0.,0.,0.)), 0)
        xyz = mxmymz / wt

        return (xyz, wt)

    def _error(self):
        (cog, wt) = self.xyzw()

        dx = cog[0] - self._target_cog[0]
        dy = cog[1] - self._target_cog[1]
        dw = wt - self._target_wt

        return dx**2 + dy**2 + dw **2

    def optimize_tank(self, tank):
        E0 = self._error()
        p0 = tank.pct

        # fill tank
        tank.pct = 100
        if self._error() < E0:
            return True

        # empty tank
        tank.pct = 0
        if self._error() < E0:
            return True

        # optimum must be somewhere in between

        def fun(x):
            tank.pct = x
            return self._error()


        res = minimize(fun, x0=np.array((50.)), bounds=[(0.,100.)])

        if not res.success:
            raise ArithmeticError('Optimization failed')

        # Did the optimization result in a different tank fill
        if abs(p0-res.x) > 0.0001:
            print('Tank {} set to {}'.format(tank.name, res.x))
            tank.pct = res.x
            return True

        return False

    def optimize_multiple_partial(self, tanks):

        E0 = self._error()


        n_tanks = len(tanks)

        # See if it is possible to empty one of the tanks and get an result that is at least as good
        if n_tanks > 2:
            # two slack tanks should be enough in most cases
            for i_empty in reversed(range(n_tanks)):
                subset = []
                for i in range(n_tanks):
                    if i == i_empty:
                        tanks[i].pct = 0
                    else:
                        subset.append(tanks[i])

                if self.optimize_multiple_partial(subset):
                    if self._error() <= E0:
                        print('Removed one of the slack tanks')
                        return True

        # See if it is possible to fill one of the tanks and get an result that is at least as good
        if n_tanks>2:
            # two slack tanks should be enough in most cases
            for i_full in range(n_tanks):
                subset = []
                for i in range(n_tanks):
                    if i==i_full:
                        tanks[i].pct=100
                    else:
                        subset.append(tanks[i])

                if self.optimize_multiple_partial(subset):
                    if self._error() <= E0:
                        print('Removed one of the slack tanks')
                        return True



        def fun(x):
            for i,tank in enumerate(tanks):
                tank.pct = x[i]
            return self._error()

        x0 = []
        bnds = []

        for tank in tanks:
            x0.append(tank.pct)
            bnds.append((0., 100.))

        res = minimize(fun, x0=np.array(x0), bounds=bnds)

        if not res.success:
            raise ArithmeticError('Optimization failed')


        # apply the result
        fun(res.x)

        # Did the optimization result in a different tank fill
        if self._error() < E0:
            print('multi-opt result = ', res.x)
            return True

        return False

    def ballast_to(self, cogx, cogy, weight):

        _log = []

        self._target_wt = weight
        self._target_cog[0] = cogx
        self._target_cog[1] = cogy

        while True:

            _log.append([tank.pct for tank in self.tanks])
            print(_log[-1])

            if self._error() < 1e-5:
                break

            # optimize partially filled tanks
            partials = []
            for tank in self.tanks:
                if tank.is_partial():
                    partials.append(tank)

            if len(partials) == 1:
                if self.optimize_tank(partials[0]):
                    continue


            if len(partials) > 1:
                if self.optimize_multiple_partial(partials):
                    continue

            changed = False

            for tank in self.tanks:
                if self.optimize_tank(tank):
                    changed = True
                    break

            if changed:
                continue

            raise ArithmeticError('Optimization failed')

        print(self._error())
        print(self.xyzw())
        print([t.pct for t in self.tanks])
        plt.plot(_log)
        plt.show()

# ====== main code ======

if __name__ == '__main__':

    # make four tanks
    t1 = tank()
    t1.position = np.array((10.,10.,0))
    t1.max = 500


    t2 = tank()
    t2.position = np.array((10., -10., 0))
    t2.max = 500

    t3 = tank()
    t3.position = np.array((-10., -10., 0))
    t3.max = 500

    t4 = tank()
    t4.position = np.array((-10., 10., 0))
    t4.max = 500

    t5 = tank()
    t5.position = np.array((10., 10., 0))
    t5.max = 500

    t6 = tank()
    t6.position = np.array((10., -10., 0))
    t6.max = 500

    t7 = tank()
    t7.position = np.array((-10., -10., 0))
    t7.max = 500

    t8 = tank()
    t8.position = np.array((-10., 10., 0))
    t8.max = 500

    t1.name = 't1'
    t2.name = 't2'
    t3.name = 't3'
    t4.name = 't4'
    t5.name = 't5'
    t6.name = 't6'
    t7.name = 't7'
    t8.name = 't8'

    s = system()
    s.tanks.extend([t1,t2,t3,t4,t5,t6,t7,t8])

    s.ballast_to(0,5,2100)

"""
If more than three slack tanks

Fill the fullest one
or empty the emptiest one

and resolve

"""

