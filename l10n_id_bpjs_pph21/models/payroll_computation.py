from odoo import api, fields, models


class IndonesiaPayrollComputation(models.AbstractModel):
    _name = 'indonesia.payroll.computation'
    _description = 'Indonesia BPJS and PPh 21 Computation Engine'

    # Official rates & caps (as of early 2026 – verify before use)
    BPJS_RATES = {
        'jht_ee': 0.02,
        'jht_er': 0.037,
        'jp_ee': 0.01,
        'jp_er': 0.02,
        'jkm_er': 0.003,
        'kesehatan_ee': 0.01,
        'kesehatan_er': 0.04,
    }
    JKK_RATES = {
        '1': 0.0024,
        '2': 0.0054,
        '3': 0.0089,
        '4': 0.0127,
        '5': 0.0174,
    }
    CAP_JP = 11086300          # March 2026 – verify annually
    CAP_KESEHATAN = 12000000

    # TER Category A (TK/0, TK/1, K/0) - based on PMK 168/2023
    TER_A = [
        (5400000, 0.0),
        (5650000, 0.0025),
        (5950000, 0.005),
        (6300000, 0.0075),
        (6750000, 0.01),
        (7500000, 0.0125),
        (8550000, 0.015),
        (9650000, 0.0175),
        (10050000, 0.02),
        (10350000, 0.0225),
        (10700000, 0.025),
        (11050000, 0.03),
        (11600000, 0.035),
        (12500000, 0.04),
        (13750000, 0.05),
        (15100000, 0.06),
        (16950000, 0.07),
        (19750000, 0.08),
        (24150000, 0.09),
        (26450000, 0.10),
        (28000000, 0.11),
        (30050000, 0.12),
        (32400000, 0.13),
        (35400000, 0.14),
        (39100000, 0.15),
        (43850000, 0.16),
        (47800000, 0.17),
        (51400000, 0.18),
        (56300000, 0.19),
        (62200000, 0.20),
        (68600000, 0.21),
        (77500000, 0.22),
        (89000000, 0.23),
        (103000000, 0.24),
        (125000000, 0.25),
        (157000000, 0.26),
        (206000000, 0.27),
        (337000000, 0.28),
        (454000000, 0.29),
        (550000000, 0.30),
        (695000000, 0.31),
        (910000000, 0.32),
        (1400000000, 0.33),
        (float('inf'), 0.34),
    ]

    # TER Category B (TK/2, TK/3, K/1, K/2) - based on PMK 168/2023
    TER_B = [
        (6200000, 0.0),
        (6500000, 0.0025),
        (6850000, 0.005),
        (7300000, 0.0075),
        (9200000, 0.01),
        (10750000, 0.015),
        (11250000, 0.02),
        (11600000, 0.025),
        (12600000, 0.03),
        (13600000, 0.04),
        (14950000, 0.05),
        (16400000, 0.06),
        (18450000, 0.07),
        (21850000, 0.08),
        (26000000, 0.09),
        (27700000, 0.10),
        (29350000, 0.11),
        (31450000, 0.12),
        (33950000, 0.13),
        (37100000, 0.14),
        (41100000, 0.15),
        (45800000, 0.16),
        (49500000, 0.17),
        (53800000, 0.18),
        (58500000, 0.19),
        (64000000, 0.20),
        (71000000, 0.21),
        (80000000, 0.22),
        (93000000, 0.23),
        (109000000, 0.24),
        (129000000, 0.25),
        (163000000, 0.26),
        (211000000, 0.27),
        (374000000, 0.28),
        (459000000, 0.29),
        (555000000, 0.30),
        (704000000, 0.31),
        (957000000, 0.32),
        (1405000000, 0.33),
        (float('inf'), 0.34),
    ]

    # TER Category C (K/3) - based on PMK 168/2023
    TER_C = [
        (6600000, 0.0),
        (6950000, 0.0025),
        (7350000, 0.005),
        (7800000, 0.0075),
        (8850000, 0.01),
        (9800000, 0.0125),
        (10950000, 0.015),
        (11250000, 0.0175),
        (11600000, 0.02),
        (12050000, 0.0225),
        (12950000, 0.03),
        (14150000, 0.04),
        (15550000, 0.05),
        (17050000, 0.06),
        (19500000, 0.07),
        (22700000, 0.08),
        (26600000, 0.09),
        (28100000, 0.10),
        (30100000, 0.11),
        (32600000, 0.12),
        (35400000, 0.13),
        (38900000, 0.14),
        (43000000, 0.15),
        (47400000, 0.16),
        (51250000, 0.17),
        (55850000, 0.18),
        (60400000, 0.19),
        (66700000, 0.20),
        (74500000, 0.21),
        (83250000, 0.22),
        (95600000, 0.23),
        (110000000, 0.24),
        (134000000, 0.25),
        (169000000, 0.26),
        (221000000, 0.27),
        (390000000, 0.28),
        (463000000, 0.29),
        (561000000, 0.30),
        (709000000, 0.31),
        (965000000, 0.32),
        (1419000000, 0.33),
        (float('inf'), 0.34),
    ]

    @api.model
    def get_ter_rate(self, category, gross):
        """Return TER rate for the given category and monthly gross."""
        if category == 'B':
            table = self.TER_B
        elif category == 'C':
            table = self.TER_C
        else:
            table = self.TER_A
        for max_gross, rate in table:
            if gross <= max_gross:
                return rate
        return 0.34

    @api.model
    def _get_bpjs_rates(self):
        """Get BPJS rates from system parameters (with defaults)."""
        icp = self.env['ir.config_parameter'].sudo()
        return {
            'jht_ee': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_jht_ee', 2.0)) / 100,
            'jht_er': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_jht_er', 3.7)) / 100,
            'jp_ee': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_jp_ee', 1.0)) / 100,
            'jp_er': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_jp_er', 2.0)) / 100,
            'jkm_er': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_jkm_er', 0.3)) / 100,
            'kesehatan_ee': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_kes_ee', 1.0)) / 100,
            'kesehatan_er': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_kes_er', 4.0)) / 100,
            'jp_cap': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_jp_cap', 11086300)),
            'kes_cap': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_kes_cap', 12000000)),
            'jkk': {
                '1': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_jkk_1', 0.24)) / 100,
                '2': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_jkk_2', 0.54)) / 100,
                '3': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_jkk_3', 0.89)) / 100,
                '4': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_jkk_4', 1.27)) / 100,
                '5': float(icp.get_param('l10n_id_bpjs_pph21.bpjs_jkk_5', 1.74)) / 100,
            }
        }

    @api.model
    def compute_bpjs(self, employee, gross_salary):
        """Return dict of BPJS amounts (employee deductions and employer costs)."""
        if not employee.has_bpjs_ketenagakerjaan and not employee.has_bpjs_kesehatan:
            return {}

        rates = self._get_bpjs_rates()
        result = {}

        if employee.has_bpjs_ketenagakerjaan:
            result['jht_ee'] = gross_salary * rates['jht_ee']
            result['jht_er'] = gross_salary * rates['jht_er']

            jp_base = min(gross_salary, rates['jp_cap'])
            result['jp_ee'] = jp_base * rates['jp_ee']
            result['jp_er'] = jp_base * rates['jp_er']

            jkk_rate = rates['jkk'].get(employee.bpjs_risk_class or '1', rates['jkk']['1'])
            result['jkk_er'] = gross_salary * jkk_rate
            result['jkm_er'] = gross_salary * rates['jkm_er']

        if employee.has_bpjs_kesehatan:
            kes_base = min(gross_salary, rates['kes_cap'])
            result['kesehatan_ee'] = kes_base * rates['kesehatan_ee']
            result['kesehatan_er'] = kes_base * rates['kesehatan_er']

        return result

    @api.model
    def compute_pph21_ter(self, employee, gross_salary):
        """Monthly PPh 21 using TER method (Jan–Nov)."""
        if not employee.ter_category:
            return 0.0
        rate = self.get_ter_rate(employee.ter_category, gross_salary)
        return gross_salary * rate

