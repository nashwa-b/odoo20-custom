# -*- coding: utf-8 -*-

from odoo import fields, models
import requests
from odoo.exceptions import ValidationError


class PurchaseOrderWizard(models.TransientModel):
    """Creation of Wizards for Sales Orders"""
    _name = 'purchase.order.wizard'
    _description = 'Wizard for Purchase Orders'

    api_key = fields.Char('API Key')
    db_name = fields.Char('DB Name')
    url = fields.Char('URL')

    def action_fetch_purchase_orders(self):
        """Fetch and create purchase orders from db of version 19"""
        response = requests.post(
            f"{self.url}/json/2/purchase.order/search_read",
            headers={
                "Authorization": f"bearer {self.api_key}",
                "X-Odoo-Database": self.db_name,
            },
            json={
                "domain": [],
                "fields": [
                    "name", "partner_id", "partner_ref", "date_approve", "date_planned", "state", "id"
                ],
                # "limit": 1
            },
        )
        if response.status_code != 200:
            print("Response text:", response.text)
        response.raise_for_status()
        print(response)
        purchase_orders = response.json()
        print(purchase_orders)

        for po in purchase_orders:
            vendor_name = po["partner_id"][1]
            vendor_id = po["partner_id"][0]
            print("vendor_name:", vendor_name)
            print("vendor_id:", vendor_id)

            vendor = self.env['res.partner'].sudo().search([('name', '=', po['partner_id'][1])], limit=1)
            print("vendor:", vendor)

            existing_po = self.env['purchase.order'].sudo().search([('origin', '=', po.get('name'))], limit=1)

            if existing_po:
                continue

            new_po = self.env['purchase.order'].create({
                'origin': po.get('name'),
                'partner_id': vendor.id,
                'partner_ref': po['partner_ref'],
                'date_approve': po['date_approve'],
                'date_planned': po['date_planned'],
                'state': po['state']
            })
            print('pos', new_po)

            responses = requests.post(
                f"{self.url}/json/2/purchase.order.line/search_read",
                headers={
                    "Authorization": f"bearer {self.api_key}",
                    "X-Odoo-Database": self.db_name,
                },
                json={
                    "domain": [('order_id', '=', po.get('id'))],
                    "fields": [
                        "product_id", "product_qty", "price_unit", "price_subtotal"
                    ],
                    # "limit": 1
                },
            )
            if responses.status_code != 200:
                print("Response text:", responses.text)
            responses.raise_for_status()
            print(responses)
            purchase_order_lines = responses.json()
            print("pol", purchase_order_lines)

            for pl in purchase_order_lines:
                print('p', pl['product_id'][1])
                product = self.env['product.product'].sudo().search([('display_name', '=', pl['product_id'][1])],
                                                                    limit=1)
                print("product:", product)
                if not product:
                    raise ValidationError("Product not found")
                new_pol = self.env['purchase.order.line'].create({
                    'order_id': new_po.id,
                    'product_id': product.id,
                    'product_qty': pl['product_qty'],
                    'price_unit': pl['price_unit'],
                    'price_subtotal': pl['price_subtotal'],
                })
                print('poll', new_pol)
