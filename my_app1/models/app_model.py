from odoo import models, fields, api

class AppModel(models.Model):
    _name = "app.model"
    _description = "Basic app model"

    text = fields.Text(string='Text field')
    check1 = fields.Boolean(string='Test 1')
    check2 = fields.Boolean(string='Test 2')
    check_all = fields.Boolean(string='Select all')

    select1 = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ], string='Select 1,2,3')

    select2 = fields.Selection([
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    ], string='Select 4,5,6')

    boolean1 = fields.Boolean(string='1')
    boolean2 = fields.Boolean(string='2')
    boolean3 = fields.Boolean(string='3')
    boolean4 = fields.Boolean(string='4')
    boolean5 = fields.Boolean(string='5')
    boolean6 = fields.Boolean(string='6')
    boolean7 = fields.Boolean(string='7')
    boolean8 = fields.Boolean(string='8')
    boolean9 = fields.Boolean(string='9')

    char = fields.Char(string='Char field', size=100)
    integer = fields.Integer(string='Integer number')
    float_num = fields.Float(string='Float number', digits=(16, 2))
    monetary = fields.Monetary(string='Monetary field', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency')

    date = fields.Date(string='Date')
    datetime = fields.Datetime(string='Date and time', default=fields.Datetime.now)

    html = fields.Html(string='HTML')
    binary = fields.Binary(string='File')
    image = fields.Image(string='Image', max_width=720, max_height=720)
    active = fields.Boolean(string='Active', default=True)

    user_id = fields.Many2one('res.users', string='User')

    partner_ids = fields.Many2many('res.partner', string='Partners')
    computed_field = fields.Char(string='Computed Title', compute='_compute_title')
    is_company = fields.Boolean(string='Is Company')
    @api.depends('text')
    def _compute_title(self):
        for record in self:
            record.computed_field = f"Title: {record.text or 'Empty'}"

    @api.onchange('check_all')
    def _onchange_check_all(self):
        """select all sets check1 and check2"""

        if self.check_all:
            self.check1 = True
            self.check2 = True
        else:
            if self.check1 and self.check2:
                self.check1 = False
                self.check2 = False

    @api.onchange('check1', 'check2')
    def _onchange_checks(self):
        """'select all' sets on check1 and check2 changes
            text displays current active checks
        """
        if self.check1 and self.check2:
            self.check_all = True
        else:
            self.check_all = False
        current_text = self.text or ""
        label1 = "[Test 1]"
        label2 = "{Test 2}"

        if self.check1:
            if label1 not in current_text:
                current_text = f"{current_text} {label1}".strip()
        else:
            current_text = current_text.replace(label1, "").replace("  ", " ").strip()

        if self.check2:
            if label2 not in current_text:
                current_text = f"{current_text} {label2}".strip()
        else:
            current_text = current_text.replace(label2, "").replace("  ", " ").strip()

        self.text = current_text


    def action_create_partner(self):
        """Header buttons logic"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Contact',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_name': self.text,
                'default_is_company': self.is_company,
            }
        }

    def action_open_wizard(self):
        """Open partner wizard window"""
        return {
            'name': 'Create Partner Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'create.partner.wizard',
            'view_mode': 'form',
            'target': 'new',  # Открывает как модальное окно
        }