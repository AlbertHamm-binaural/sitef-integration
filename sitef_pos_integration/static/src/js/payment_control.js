odoo.define('sitef_pos_integration.payment_control', function (require) {

    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require("point_of_sale.PaymentScreen");

    var Session = require("web.Session");
        
    const ControlSitef = PaymentScreen => class extends PaymentScreen {
        constructor() {
            super(...arguments);

        }

        async cambio() {
            if (this.selectedPaymentLine && this.selectedPaymentLine.amount < 0) {
                this.showPopup('CambioForm', {amount: Math.abs(this.selectedPaymentLine.amount)});
            }
            else {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t('No se puede realizar un cambio.'),
                });
            }
        }
        async validarPagoMovil() {
            if (this.selectedPaymentLine && this.selectedPaymentLine.amount > 0) {
                this.showPopup('ValidarPagoMovilForm', {amount: parseFloat(Math.abs(this.selectedPaymentLine.amount).toFixed(2))});
                
            }
            else {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t('No se puede realizar un pago móvil.'),
                });
            }
        }

        AmountCambio(amount) {        
            if (amount < 0 && amount != 0) {
                return true;
            } else {
                return false;
            }
        }

        AmountPagoMovil(amount) {
            if (amount > 0 && amount != 0) {
                return false;
            } else{
                return true;
            }
        }
    };

    Registries.Component.extend(PaymentScreen, ControlSitef);
    return ControlSitef;
});