odoo.define('qs_account.FollowupFormController', function (require) {
"use strict";

var FollowupFormController = require ('account_followup.FollowupFormController')
const rpc = require("web.rpc");

FollowupFormController.include({
    // events: _.extend({}, FollowupFormController.prototype.events, {
    //     'click .o_account_followup_get_all': '_get_all',
    //     'click .o_account_followup_get_late': '_get_late'
    // }),
    
    /**
     * @override
     */
    renderButtons: function () {
        this._super.apply(this, arguments);
        this.$buttons.on('click', '.o_account_followup_get_all',
            this._get_all.bind(this));
        this.$buttons.on('click', '.o_account_followup_get_late',
            this._get_late.bind(this));
    },
    // /**
    //  * Update the buttons according to followup_level.
    //  *
    //  * @override
    //  */
    // updateButtons: function () {
    //     if (!this.$buttons) {
    //         return;
    //     }
    //     this._super.apply(this, arguments);
    //     var followupLevel = this.model.localData[this.handle].data.followup_level;
    //     if (followupLevel.send_letter) {
    //         this.$buttons.find('button.o_account_followup_send_letter_button')
    //         .removeClass('btn-secondary').addClass('btn-primary');
    //     } else {
    //         this.$buttons.find('button.o_account_followup_send_letter_button')
    //         .removeClass('btn-primary').addClass('btn-secondary');
    //     }
    // },


    /**
     *
     * @private
     */
    _get_all: function () {
        var self = this;
        var records = {
            ids: [this._getPartner()],
        };
        this._rpc({
            model:'account.followup.report',
            method: 'get_all',
            args: [records],
        }).then(function () {
            self.reload();
        });
    },

    /**
     *
     * @private
     */
    _get_late: function () {
        var self = this;
        var records = {
            ids: [this._getPartner()],
        };
        this._rpc({
            model:'account.followup.report',
            method: 'get_late',
            args: [records],
        }).then(function () {
            self.reload();
        });
    },

    
    
})

});