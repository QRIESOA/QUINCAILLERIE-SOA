odoo.define('qs_sale.TicketScreen', function(require) {
'use strict';

    const TicketScreen = require('point_of_sale.TicketScreen');
    const models = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    var OrderSuper = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attributes, options){
            OrderSuper.initialize.call(this,attributes,options);
            if (options.json){
                this.init_from_JSON(options.json);
            }
            else {
                this.note_client = this.note_client;
            }
            // this.note_client = this.env.pos.get_order().note_client;
            // console.log("note_client", this.note_client)
        },

        init_from_JSON: function(json) {
            OrderSuper.init_from_JSON.apply(this,arguments);
            this.note_client = json.note_client;
        }
    });

    models.load_fields('pos.order', ['note_client']);

    // models.load_models([{
    //     model: 'pos.order',
    //     fields: ['note_client'],
    //     loaded: function (self, note_client) {
    //         self.note_client = note_client;
    //     },
    // }]);
    
    const QsoaTicketScreen = TicketScreen => class extends TicketScreen {
        
        /**
         * @returns {Record<string, { repr: (order: models.Order) => string, displayName: string, modelField: string }>}
         */
        _getSearchFields() {
            const fields = {
                RECEIPT_NUMBER: {
                    repr: (order) => order.name,
                    displayName: this.env._t('Receipt Number'),
                    modelField: 'pos_reference',
                },
                DATE: {
                    repr: (order) => moment(order.creation_date).format('YYYY-MM-DD hh:mm A'),
                    displayName: this.env._t('Date'),
                    modelField: 'date_order',
                },
                CUSTOMER: {
                    repr: (order) => order.get_client_name(),
                    displayName: this.env._t('Customer'),
                    modelField: 'partner_id.display_name',
                },
                // search of note
                NOTE: {
                    repr: (order) => order.note_client,
                    displayName: this.env._t('Note'),
                    modelField: 'note_client',
                },
            };

            if (this.showCardholderName()) {
                fields.CARDHOLDER_NAME = {
                    repr: (order) => order.get_cardholder_name(),
                    displayName: this.env._t('Cardholder Name'),
                    modelField: 'payment_ids.cardholder_name',
                };
            }

            

            return fields;
        }
        
        getNote(order) {
            // return order.note_client;
            return order.note_client;
        }
    }

    Registries.Component.extend(TicketScreen, QsoaTicketScreen);

        
    return TicketScreen;
});
