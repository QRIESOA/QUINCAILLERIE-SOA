odoo. define('qs_sale.SaleOrderFetcher', function (require) {
    'use strict';

    var SaleOrderFetcher = require('pos_sale.SaleOrderFetcher');

    SaleOrderFetcher.include({
        async _getOrderIdsForCurrentPage(limit, offset) {
            let domain = [['currency_id', '=', this.comp.env.pos.currency.id]].concat(this.searchDomain || []);
            return await this.rpc({
                model: 'sale.order',
                method: 'search_read',
                args: [domain, ['name', 'partner_id', 'amount_total', 'date_order', 'state', 'user_id', 'note_client'], offset, limit],
                context: this.comp.env.session.user_context,
            });
        }
    });
});