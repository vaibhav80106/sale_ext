from odoo import models, api, fields
from datetime import datetime, date, timedelta


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    @api.depends('list_price', 'discount_percentage')
    def _compute_prod_discount_price(self):
        for product in self:
            if product.list_price and product.discount_percentage:
                product.discounted_price = product.list_price * (1 - (product.discount_percentage / 100))
            else:
                product.discounted_price = product.list_price

    discount_percentage = fields.Float(string="Discount Percentage", default=0.0)
    discounted_price = fields.Float(string="Discounted Price", compute='_compute_prod_discount_price')
    
    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        """Set discounted price for optional products
        """
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)

        if combination_info['product_id']:
            product = self.env['product.product'].sudo().browse(combination_info['product_id'])
            if product.discount_percentage:
                price = product.discounted_price
            else:
                price = combination_info['price']
                
            combination_info.update(
                price=price,
            )
        return combination_info
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line with the discount applied.
        """
        for line in self:
            # Apply the discount percentage from the product template
            discount_percentage = line.product_id.discount_percentage / 100.0
            discounted_price = line.price_unit * (1 - discount_percentage) if discount_percentage > 0 else line.price_unit

            # Prepare the tax calculation with the discounted price
            line.price_unit = discounted_price
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax']

            # Update the amounts on the sale order line
            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': amount_untaxed + amount_tax,
            })
