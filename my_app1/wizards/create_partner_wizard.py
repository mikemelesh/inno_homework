from odoo import models, fields, api

class CreatePartnerWizard(models.TransientModel):
    """wizard to create temporariry partner window"""
    _name = 'create.partner.wizard'
    _description = 'Wizard to create partner'

    name = fields.Char(string='Name', required=True)
    is_company = fields.Boolean(string='Is Company')

    def action_create(self):
        partner = self.env['res.partner'].create({
            'name': self.name,
            'is_company': self.is_company,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': partner.id,
            'view_mode': 'form',
            'target': 'current',
        }