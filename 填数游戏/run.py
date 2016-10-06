import logging

import numpy as np

import itertools


class App:
    def __init__(self):
        self.logger = logging.getLogger("console.app")
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)
        self.mat_size = input("size of matrix:")
        self.mat = np.zeros((self.mat_size, self.mat_size))
        self.point_confirmed = []
        self.points_opt = []
        self.confirm_depth = 1

    # get the input matrix
    def mat_input(self):
        a = input("num of row:")
        b = input("num of col:")
        c = input("num of value")
        if a < 1 or a > self.mat.shape[0]:
            self.logger.error("wrong input of row")
        elif b < 1 or b > self.mat.shape[1]:
            self.logger.error("wrong input of col")
        elif c < 1 or c > self.mat.shape[0]:
            self.logger.error("wrong input of value")
        else:
            self.mat[a - 1, b - 1] = c
            self.point_confirmed.append((a - 1, b - 1, c))
            self.logger.info("matrix updated")

    # generate origin option points matrix
    def points_opt_init(self):
        points_option = []
        for i in range(self.mat_size):
            for j in range(self.mat_size):
                point_option = []
                for k in range(1, self.mat_size + 1):
                    point_option.append((i, j, k))
                points_option.append(point_option)
        self.points_opt = points_option

    # filter the illegal points base on new confirmed points
    def points_filter(self, points_opt, points_exit):
        for point_exit in points_exit:
            points_opt_selected = []
            for point_opt in points_opt:
                point_opt_selected = []
                for point in point_opt:
                    if self.point_compare(point, point_exit):
                        point_opt_selected.append(point)
                points_opt_selected.append(point_opt_selected)
            points_opt = points_opt_selected
        return points_opt

    # confirm the legal points
    def points_confirm(self, points_opt):
        points_confirmed = self.point_confirmed[:]
        for point_opt in points_opt:
            if len(point_opt) == 1 and point_opt[0] not in points_confirmed:
                points_confirmed.append(point_opt[0])
        if points_confirmed == self.point_confirmed:
            for point_opt in points_opt:
                if len(point_opt) > 1:
                    for point in point_opt:
                        if self.confirm_depth > 2 or self.confirm_evaluate(points_opt, points_confirmed, point):
                            points_confirmed.append(point)
                            return points_confirmed
        return points_confirmed

    # judge if it is legal to add the point
    def confirm_evaluate(self, points_opt, point_confirm, point):
        self.confirm_depth += 1
        tmp_confirm = point_confirm[:]
        tmp_confirm.append(point)
        tmp_opt = self.points_filter(points_opt, tmp_confirm)
        points_eva = self.points_confirm(tmp_opt)
        if self.point_evaluate(points_eva):
            return True
        else:
            return False

    # compare the point list if all two combinations obey the rules
    def point_evaluate(self, points):
        if len(points) > 1:
            points_com = itertools.combinations(points, 2)
            for com in points_com:
                if not self.point_compare(com[0], com[1]):
                    return False
        return True

    # compare two point whether obey the rules
    def point_compare(self, point_1, point_2):
        # remove same position values
        if point_1[0] == point_2[0] and point_1[1] == point_2[1] and point_1[2] != point_2[2]:
            return False
        # remove same row values with same value
        if point_1[0] == point_2[0] and point_1[1] != point_2[1] and point_1[2] == point_2[2]:
            return False
        # remove same col values with same value!
        if point_1[0] != point_2[0] and point_1[1] == point_2[1] and point_1[2] == point_2[2]:
            return False
        else:
            return True

    # fill the matrix base on points confirmed
    def matrix_fill(self):
        for item in self.point_confirmed:
            self.mat[item[0], item[1]] = item[2]

    # compute the numbers to fill base on the input
    def compute(self):
        self.points_opt_init()
        while len(self.point_confirmed) < self.mat_size * self.mat_size:
            self.points_opt = self.points_filter(self.points_opt, self.point_confirmed)
            point_exit = self.points_confirm(self.points_opt)
            self.point_confirmed = point_exit
            self.confirm_depth = 1
        self.matrix_fill()
        self.logger.info("compute completed")

    # run the fill number application
    def run(self):
        points_known = input("num of points have known:")
        for i in range(points_known):
            self.mat_input()
        self.logger.info("the input matrix is:")
        self.logger.info("---------------------------------[ input matrix ]-------------------------------------------")
        self.logger.info(self.mat)
        self.logger.info("--------------------------------------------------------------------------------------------")
        self.logger.info("matrix computing, wait for a moment")
        self.compute()
        self.logger.info("matrix completed, output matrix is:")
        self.logger.info("----------------------------------[ output matrix ]-----------------------------------------")
        self.logger.info(self.mat)
        self.logger.info("--------------------------------------------------------------------------------------------")


if __name__ == '__main__':
    app = App()
    app.run()
