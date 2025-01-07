/** @odoo-module **/

import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
import Registries from 'point_of_sale.Registries';
import { useRef } from "@odoo/owl";
import { _lt } from 'web.core';

const ajax = require('web.ajax');

class ValidarPagoMovilForm extends AbstractAwaitablePopup {
    setup() {
        super.setup();
        this.referencia = useRef('referenciaInput');
        this.telefono = useRef('telefonoInput');
        this.banco = useRef('bancoSelect');
    }

    async confirm() {
        if (this.referencia.el.value != "" && this.telefono.el.value != "") {
            let username = this.env.pos.config.username;
            let password = this.env.pos.config.encrypted_password;

            let idbranch = this.env.pos.config.idbranch;        
            let codestall = this.env.pos.config.codestall;
            let receivingbank = parseInt(this.env.pos.config.issuingbank, 10);
    
            let paymentreference = this.referencia.el.value;
            let telefono = this.telefono.el.value;
            let origenbank = parseInt(this.banco.el.value, 10);
            let amount = this.props.amount;
            let debitphone = '58' + telefono.substring(1);
            let trxdate = new Date().toISOString().slice(0, 10);
            
            const token = await this.generarToken(username, password);
            if (token) {
                const pago = await this.validarPago(username, token, idbranch, codestall, amount, paymentreference, debitphone, origenbank, receivingbank, trxdate);
            }
        } else {
            this.showPopup('ErrorPopup', {
                title: this.env._t('Campos vacíos'),
                body: this.env._t('Debe ingresar la referencia y el teléfono del cliente')
            });
        }
    }

    async generarToken(username, password) {
        const result = await ajax.jsonRpc(
            "/sitef_pos_integration/get_token", "call",
            { username, password }
        );
        if (result.error) {
            this.showPopup('ErrorPopup', {
                title: this.env._t('Error al generar token'),
                body: this.env._t(result.error),
            });
        } else{
            return result;
        }
    }
    
    async validarPago(username, token, idbranch, codestall, amount, paymentreference, debitphone, origenbank, receivingbank, trxdate) {
        try {
            const result = await ajax.jsonRpc(
                "/sitef_pos_integration/validarPago_sitef", "call",
                { username, token, idbranch, codestall, amount, paymentreference, debitphone, origenbank, receivingbank, trxdate }
            );
            if (result == "marcada") {
                this.showPopup('ConfirmPopup', {
                    title: this.env._t('Validación de pago móvil'),
                    body: this.env._t('El pago móvil fue validado con éxito')
                });
                this.env.posbus.trigger('close-popup', {
                    popupId: this.props.id,
                    response: { confirmed: true, payload: await this.getPayload() },
                });    
                return result;
            } 
            if (result == "verified") {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Validación de pago móvil'),
                    body: this.env._t('El pago móvil ya fue validado anteriormente'),
                });
                return result;
            } else {
                this.showPopup('ErrorPopup', {
                    title: this.env._t("Error: ") + result.error_code,
                    body: this.env._t(result.description),
                });
                return null;
            }
        } catch (error) {
            this.showPopup('ErrorPopup', {
                title: this.env._t('Error de validación'),
                body: this.env._t(error),
            });
            return null;
        }
    }
}

ValidarPagoMovilForm.defaultProps = {
    cancelText: _lt('Cancel'),
    confirmText: _lt('Confirm'),
};

ValidarPagoMovilForm.template = 'ValidarPagoMovilForm';

Registries.Component.add(ValidarPagoMovilForm);
export default ValidarPagoMovilForm;