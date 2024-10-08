# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'E-Commerce Product wise Discount',
    'version': '16.0.0..1',
    'summary': '',
    'sequence': 1,
    'description': """
    """,
    'category': 'sale',
    'website': '',
    'images': [],
    'depends': ['base', 'sale', 'sale_management', 'website_sale'],
    'data': [
            'views/product.xml',
            'views/website_sale.xml',
    ],
    'demo': [
        
    ],
    'qweb': [
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
   
}
