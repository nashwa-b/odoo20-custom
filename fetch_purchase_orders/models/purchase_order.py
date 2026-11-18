# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseOrder(models.Model):
    """Adding sale order button in product view"""
    _inherit = 'purchase.order'
    #
    # def action_fetch_purchase_order(self):
    #     self.ensure_one()
    #     print(self)
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Fetch Purchase Order',
    #         'res_model': 'purchase.order.wizard',
    #         "views": [[self.env.ref('fetch_purchase_orders.view_purchase_order_wizard_form').id, "form"]],
    #         'target': 'new',
    #         # 'context': {'default_product_id': self.id, 'default_price_unit': self.list_price}
    #     }




