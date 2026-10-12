from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # BPJS Rates
    bpjs_jht_ee = fields.Float(string='JHT Employee Rate (%)', default=2.0, config_parameter='l10n_id_bpjs_pph21.bpjs_jht_ee')
    bpjs_jht_er = fields.Float(string='JHT Employer Rate (%)', default=3.7, config_parameter='l10n_id_bpjs_pph21.bpjs_jht_er')
    bpjs_jp_ee = fields.Float(string='JP Employee Rate (%)', default=1.0, config_parameter='l10n_id_bpjs_pph21.bpjs_jp_ee')
    bpjs_jp_er = fields.Float(string='JP Employer Rate (%)', default=2.0, config_parameter='l10n_id_bpjs_pph21.bpjs_jp_er')
    bpjs_jkm_er = fields.Float(string='JKM Employer Rate (%)', default=0.3, config_parameter='l10n_id_bpjs_pph21.bpjs_jkm_er')
    bpjs_kes_ee = fields.Float(string='Kesehatan Employee Rate (%)', default=1.0, config_parameter='l10n_id_bpjs_pph21.bpjs_kes_ee')
    bpjs_kes_er = fields.Float(string='Kesehatan Employer Rate (%)', default=4.0, config_parameter='l10n_id_bpjs_pph21.bpjs_kes_er')

    # Caps
    bpjs_jp_cap = fields.Float(string='JP Salary Cap', default=11086300, config_parameter='l10n_id_bpjs_pph21.bpjs_jp_cap')
    bpjs_kes_cap = fields.Float(string='Kesehatan Salary Cap', default=12000000, config_parameter='l10n_id_bpjs_pph21.bpjs_kes_cap')

    # JKK Rates
    bpjs_jkk_1 = fields.Float(string='JKK Class 1 Rate (%)', default=0.24, config_parameter='l10n_id_bpjs_pph21.bpjs_jkk_1')
    bpjs_jkk_2 = fields.Float(string='JKK Class 2 Rate (%)', default=0.54, config_parameter='l10n_id_bpjs_pph21.bpjs_jkk_2')
    bpjs_jkk_3 = fields.Float(string='JKK Class 3 Rate (%)', default=0.89, config_parameter='l10n_id_bpjs_pph21.bpjs_jkk_3')
    bpjs_jkk_4 = fields.Float(string='JKK Class 4 Rate (%)', default=1.27, config_parameter='l10n_id_bpjs_pph21.bpjs_jkk_4')
    bpjs_jkk_5 = fields.Float(string='JKK Class 5 Rate (%)', default=1.74, config_parameter='l10n_id_bpjs_pph21.bpjs_jkk_5')
