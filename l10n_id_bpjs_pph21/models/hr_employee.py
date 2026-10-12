from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    ptkp_status = fields.Selection([
        ('tk0', 'TK/0 - Single, no dependents'),
        ('tk1', 'TK/1 - Single, 1 dependent'),
        ('tk2', 'TK/2 - Single, 2 dependents'),
        ('tk3', 'TK/3 - Single, 3 dependents'),
        ('k0', 'K/0 - Married, no dependents'),
        ('k1', 'K/1 - Married, 1 dependent'),
        ('k2', 'K/2 - Married, 2 dependents'),
        ('k3', 'K/3 - Married, 3 dependents'),
    ], string='PTKP Status', default='tk0',
       help='Status Penghasilan Tidak Kena Pajak for PPh 21 TER category')

    bpjs_risk_class = fields.Selection([
        ('1', 'Risk Class 1 (0.24%)'),
        ('2', 'Risk Class 2 (0.54%)'),
        ('3', 'Risk Class 3 (0.89%)'),
        ('4', 'Risk Class 4 (1.27%)'),
        ('5', 'Risk Class 5 (1.74%)'),
    ], string='BPJS JKK Risk Class', default='1')

    npwp = fields.Char(string='NPWP', size=16)
    has_bpjs_kesehatan = fields.Boolean(string='Has BPJS Kesehatan', default=True)
    has_bpjs_ketenagakerjaan = fields.Boolean(string='Has BPJS Ketenagakerjaan', default=True)

    @api.depends('ptkp_status')
    def _compute_ter_category(self):
        for emp in self:
            if emp.ptkp_status in ('tk0', 'tk1', 'k0'):
                emp.ter_category = 'A'
            elif emp.ptkp_status in ('tk2', 'tk3', 'k1', 'k2'):
                emp.ter_category = 'B'
            else:
                emp.ter_category = 'C'

    ter_category = fields.Selection([
        ('A', 'TER Category A'),
        ('B', 'TER Category B'),
        ('C', 'TER Category C'),
    ], string='TER Category', compute='_compute_ter_category', store=True)
