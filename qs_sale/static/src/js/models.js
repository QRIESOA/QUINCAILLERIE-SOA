odoo.define('qs_sale.models', function (require) {
    "use strict";

var models = require('pos_sale.models');

    models.Orderline = models.Orderline.extend({
        export_as_JSON: function () {
            const json = super_order_line_model.export_as_JSON.apply(this, arguments);
            json.sale_order_origin_id = this.sale_order_origin_id;
            json.sale_order_line_id = this.sale_order_line_id;
            json.down_payment_details = this.down_payment_details && JSON.stringify(this.down_payment_details);
            return json;
        },
        get_sale_order: function(){
            if(this.sale_order_origin_id) {
                let value = {
                    'name': this.sale_order_origin_id.name,
                    'note_client': this.sale_order_origin_id.note_client,
                    'details': this.down_payment_details || false
                }
        
                return value;
            }
            return false;
        },
    });

})