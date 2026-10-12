{
    'name': 'Indonesia BPJS & PPh 21 Payroll',
    'version': '20.0.1.1.0',
    'category': 'Human Resources/Payroll',
    'summary': 'Indonesia BPJS + PPh 21 TER with configurable rates',
    'description': """
Indonesia BPJS & PPh 21
=======================

Complete localization module for Indonesian payroll compliance on Odoo 20 Community.

Features:
- Employee fields for PTKP status, BPJS risk class, NPWP
- Automatic BPJS calculation (employee + employer shares) with official caps
- PPh 21 monthly TER calculation (categories A/B/C based on PMK 168/2023)
- Sample salary rules ready to use
- Configurable rates (update via code or future settings)

**Important**: Tax and BPJS rates/caps can change. Always verify against the latest regulations (PP, PMK, Perpres) before production use. Test thoroughly with real scenarios.
    """,
    'author': 'Your Name',
    'website': 'https://example.com',
    'depends': [
        'hr',
        'base_setup',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/res_config_settings_views.xml',
        'data/salary_rules.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
    'price': 119.00,
    'currency': 'EUR',
}
