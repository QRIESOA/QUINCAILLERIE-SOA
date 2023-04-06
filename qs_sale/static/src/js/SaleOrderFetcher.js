odoo. define('qs_sale.SaleOrderFetcher', function (require) {
    'use strict';

    const { EventBus } = owl.core;
    const SaleOrderFetcher = require('pos_sale.SaleOrderFetcher');

    SaleOrderFetcher._getOrderIdsForCurrentPage = async (limit, offset) => {
        let domain = [['currency_id', '=', SaleOrderFetcher.comp.env.pos.currency.id]].concat(SaleOrderFetcher.searchDomain || []);
        return await SaleOrderFetcher.rpc({
            model: 'sale.order',
            method: 'search_read',
            args: [domain, ['name', 'partner_id', 'amount_total', 'date_order', 'state', 'user_id', 'note_client'], offset, limit],
            context: SaleOrderFetcher.comp.env.session.user_context,
        });
    };
    
});
