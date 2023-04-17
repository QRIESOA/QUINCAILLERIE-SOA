odoo.define('qs_sale.models', function (require) {
    "use strict";

var models = require('point_of_sale.models');

    var super_order_line_model = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        
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

        export_for_printing: function() {
            var json = super_order_line_model.export_for_printing.apply(this,arguments);
            json.down_payment_details =  this.down_payment_details;
            if (this.sale_order_origin_id) {
                json.so_reference = this.sale_order_origin_id.name;
                json.note_client = this.sale_order_origin_id.note_client || this.order.note_client;
            }
            return json;
          },

    });

});
