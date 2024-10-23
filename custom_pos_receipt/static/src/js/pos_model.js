odoo.define('custom_pos_receipt.models', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var super_order_line_model = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function() {
            var json = super_order_line_model.export_for_printing.apply(this,arguments);
            json.default_code = this.get_product().default_code;
            json.pos_config_id = this.pos.config.id;
            return json;
        },
    });
});