from generators.helpers.value import UnitValue
from decimal import Decimal

import logging
log = logging.getLogger(__name__)


T_P_Pmm_rho = [
    (0, 0.611, 4.58, 4.84),
    (1, 0.656, 4.92, 5.22),
    (2, 0.705, 5.29, 5.60),
    (3, 0.757, 5.68, 5.98),
    (4, 0.813, 6.10, 6.40),
    (5, 0.872, 6.54, 6.84),
    (6, 0.934, 7.01, 7.3),
    (7, 1.01, 7.57, 7.8),
    (8, 1.07, 8.05, 8.3),
    (9, 1.15, 8.61, 8.8),
    (10, 1.23, 9.21, 9.4),
    (11, 1.31, 9.84, 10.0),
    (12, 1.40, 10.52, 10.7),
    (13, 1.50, 11.23, 11.4),
    (14, 1.59, 11.99, 12.1),
    (15, 1.70, 12.79, 12.8),
    (16, 1.81, 13.63, 13.6),
    (17, 1.94, 14.53, 14.5),
    (18, 2.06, 15.48, 15.4),
    (19, 2.19, 16.48, 16.3),
    (20, 2.34, 17.54, 17.3),
    (21, 2.48, 18.6, 18.3),
    (22, 2.64, 19.8, 19.4),
    (23, 2.81, 21.1, 20.6),
    (24, 2.99, 22.4, 21.8),
    (25, 3.17, 23.8, 23.0),
    (30, 4.24, 31.8, 30.3),
    (40, 7.37, 55.3, 51.2),
    (50, 12.3, 92.5, 83.0),
    (60, 19.9, 149.4, 130),
    (70, 31.0, 233.7, 198),
    (80, 47.3, 355.1, 293),
    (90, 70.1, 525.8, 424),
    (100, 101.3, 760.0, 598),
]

# from http://school-physics.spb.ru/data/labs/Saturated_steam.pdf
T_P_Pmm_rho_2 = [
    (-20, 0.10, 0.8, 1.5),
    (-19, 0.11, 0.9, 1.5),
    (-18, 0.12, 0.9, 1.6),
    (-17, 0.14, 1.0, 1.7),
    (-16, 0.15, 1.1, 1.8),
    (-15, 0.17, 1.2, 1.9),
    (-14, 0.18, 1.4, 2.0),
    (-13, 0.20, 1.5, 2.2),
    (-12, 0.22, 1.6, 2.3),
    (-11, 0.24, 1.8, 2.4),
    (-10, 0.26, 1.9, 2.6),
    (-9, 0.28, 2.1, 2.8),
    (-8, 0.31, 2.3, 2.9),
    (-7, 0.34, 2.5, 3.1),
    (-6, 0.37, 2.8, 3.3),
    (-5, 0.40, 3.0, 3.6),
    (-4, 0.44, 3.3, 3.8),
    (-3, 0.48, 3.6, 4.0),
    (-2, 0.52, 3.9, 4.3),
    (-1, 0.56, 4.2, 4.6),
    (0, 0.61, 4.6, 4.9),
    (1, 0.66, 4.9, 5.3),
    (2, 0.71, 5.3, 5.6),
    (3, 0.76, 5.7, 6.0),
    (4, 0.81, 6.1, 6.4),
    (5, 0.87, 6.5, 6.8),
    (6, 0.93, 7.0, 7.3),
    (7, 1.00, 7.5, 7.7),
    (8, 1.07, 8.1, 8.3),
    (9, 1.15, 8.6, 8.8),
    (10, 1.23, 9.2, 9.4),
    (11, 1.31, 9.8, 10.0),
    (12, 1.40, 10.5, 10.6),
    (13, 1.50, 11.2, 11.3),
    (14, 1.60, 12.0, 12.0),
    (15, 1.71, 12.8, 12.8),
    (16, 1.82, 13.6, 13.6),
    (17, 1.94, 14.5, 14.4),
    (18, 2.06, 15.5, 15.3),
    (19, 2.20, 16.5, 16.3),
    (20, 2.34, 17.5, 17.3),
    (21, 2.49, 18.7, 18.3),
    (22, 2.64, 19.8, 19.4),
    (23, 2.81, 21.1, 20.5),
    (24, 2.98, 22.4, 21.7),
    (25, 3.17, 23.8, 23.0),
    (26, 3.36, 25.2, 24.3),
    (27, 3.57, 26.7, 25.7),
    (28, 3.78, 28.4, 27.2),
    (29, 4.01, 30.0, 28.8),
    (30, 4.24, 31.8, 30.4),
    (31, 4.49, 33.7, 32.0),
    (32, 4.75, 35.7, 33.8),
    (33, 5.03, 37.7, 35.7),
    (34, 5.32, 39.9, 37.6),
    (35, 5.62, 42.2, 39.6),
    (36, 5.94, 44.6, 41.7),
    (37, 6.28, 47.1, 43.9),
    (38, 6.62, 49.7, 46.2),
    (39, 6.99, 52.4, 48.6),
    (40, 7.38, 55.3, 51.2),
    (41, 7.78, 58.3, 53.8),
    (42, 8.20, 61.5, 56.5),
    (43, 8.64, 64.8, 59.4),
    (44, 9.10, 68.3, 62.3),
    (45, 9.58, 71.9, 65.4),
    (46, 10.09, 75.7, 68.6),
    (47, 10.61, 79.6, 72.0),
    (48, 11.16, 83.7, 75.5),
    (49, 11.74, 88.0, 79.1),
    (50, 12.33, 92.5, 82.8),
    (51, 12.96, 97.2, 86.8),
    (52, 13.61, 102.1, 90.8),
    (53, 14.29, 107.2, 95.1),
    (54, 15.00, 112.5, 99.5),
    (55, 15.73, 118.0, 104.0),
    (56, 16.51, 123.8, 108.8),
    (57, 17.31, 129.8, 113.7),
    (58, 18.15, 136.1, 118.8),
    (59, 19.01, 142.6, 124.1),
    (60, 19.92, 149.4, 129.5),
    (61, 20.85, 156.4, 135.2),
    (62, 21.84, 163.8, 141.1),
    (63, 22.85, 171.4, 147.2),
    (64, 23.91, 179.3, 153.5),
    (65, 25.00, 187.5, 160.1),
    (66, 26.15, 196.1, 166.8),
    (67, 27.33, 205.0, 173.9),
    (68, 28.56, 214.2, 181.1),
    (69, 29.83, 223.7, 188.6),
    (70, 31.16, 233.7, 196.4),
    (71, 32.52, 243.9, 204.4),
    (72, 33.95, 254.6, 212.7),
    (73, 35.43, 265.7, 221.3),
    (74, 36.96, 277.2, 230.1),
    (75, 38.55, 289.1, 239.3),
    (76, 40.19, 301.4, 248.7),
    (77, 41.88, 314.1, 258.5),
    (78, 43.64, 327.3, 268.6),
    (79, 45.47, 341.0, 279.0),
    (80, 47.35, 355.1, 289.7),
    (81, 49.29, 369.7, 300.8),
    (82, 51.32, 384.9, 312.2),
    (83, 53.41, 400.6, 324.0),
    (84, 55.57, 416.8, 336.2),
    (85, 57.81, 433.6, 348.7),
    (86, 60.12, 450.9, 361.6),
    (87, 62.49, 468.7, 374.9),
    (88, 64.95, 487.1, 388.6),
    (89, 67.48, 506.1, 402.8),
    (90, 70.10, 525.8, 417.3),
    (91, 72.81, 546.1, 432.3),
    (92, 75.60, 567.0, 447.7),
    (93, 78.48, 588.6, 463.6),
    (94, 81.45, 610.9, 480.0),
    (95, 84.52, 633.9, 496.8),
    (96, 87.68, 657.6, 514.1),
    (97, 90.94, 682.1, 531.9),
    (98, 94.30, 707.3, 550.2),
    (99, 97.76, 733.2, 569.1),
    (100, 101.33, 760.0, 588.5),
]


class Vapor:
    def __init__(self, t_p_pmm_rho):
        self.T_P_Pmm_rho = t_p_pmm_rho

    def _get_rows_pairs(self):
        for index in range(len(self.T_P_Pmm_rho) - 1):
            yield self.T_P_Pmm_rho[index], self.T_P_Pmm_rho[index + 1]

    def _get_index_by_index(self, *, value=None, search_index=None, result_index=None):
        for row, next_row in self._get_rows_pairs():
            if row[search_index] <= value < next_row[search_index]:
                return (value - row[search_index]) / (next_row[search_index] - row[search_index]) * (next_row[result_index] - row[result_index]) + row[result_index]

        if value == self.T_P_Pmm_rho[-1][search_index]:
            return self.T_P_Pmm_rho[-1][result_index]

        # TODO: delete dirty hack
        if search_index == 1 and value < self.T_P_Pmm_rho[0][search_index]:
            return 0

        log.error(f'Failed to find {value} at index {search_index}')
        raise RuntimeError()

    def get_rho_by_t(self, t):
        if isinstance(t, UnitValue):
            s = float((t / UnitValue('С')).SI_Value)
        else:
            assert isinstance(t, (int, float))
            s = t
        value = self._get_index_by_index(value=s, search_index=0, result_index=3)
        return UnitValue(f'{value:.2f} г / м^3')

    def get_p_by_t(self, t):
        if isinstance(t, UnitValue):
            s = float((t / UnitValue('С')).SI_Value)
        else:
            assert isinstance(t, (int, float))
            s = t
        value = self._get_index_by_index(value=s, search_index=0, result_index=1)
        return UnitValue(f'{value:.3f} кПа')

    def get_t_by_rho(self, rho):
        if isinstance(rho, UnitValue):
            s = float((rho / UnitValue('г / м^3')).SI_Value)
        else:
            assert isinstance(rho, (int, float))
            s = rho
        value = self._get_index_by_index(value=s, search_index=3, result_index=0)
        return value

    def get_t_by_p(self, p):
        if isinstance(p, UnitValue):
            s = float((p / UnitValue('кПа')).SI_Value)
        else:
            assert isinstance(p, (int, float))
            s = p
        value = self._get_index_by_index(value=s, search_index=1, result_index=0)
        return value


def test_vapor():
    vapor = Vapor(T_P_Pmm_rho)
    assert vapor.get_rho_by_t(80).SI_Value == Decimal('0.29300')
    assert vapor.get_rho_by_t(65).SI_Value == Decimal('0.16400')
    assert vapor.get_rho_by_t(100).SI_Value == Decimal('0.598')
    assert vapor.get_t_by_rho(293) == 80

    vapor_2 = Vapor(T_P_Pmm_rho_2)
    assert vapor_2.get_rho_by_t(80).SI_Value == Decimal('0.28970')
    assert vapor_2.get_rho_by_t(65).SI_Value == Decimal('0.16010')
    assert vapor_2.get_rho_by_t(100).SI_Value == Decimal('0.58850')
    assert vapor_2.get_t_by_rho(293) == 80.29729729729729

test_vapor()
