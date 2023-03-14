odoo.define('qs_account.form_no_edit', function (require) {
    const FormController = require('web.FormController');
    const rpc = require('web.rpc');

    FormController.include({
        updateButtons: function () {
            this._super.apply(this, arguments);
            if (this.renderer.state.model === 'account.move' && this.renderer.state.data.state === 'posted') {
                rpc.query({
                    model:'account.move',
                    method: 'get_spec',
                    args: [],
                }).then(result => {
                    if (result == true){
                        this.$buttons.find('.o_form_button_edit').hide()
                    }
                    else {
                        this.$buttons.find('.o_form_button_edit').show()
                    }
                }
                    
                )
                
            } else {
                this.$buttons.find('.o_form_button_edit').show()
            }
        }
    })
});