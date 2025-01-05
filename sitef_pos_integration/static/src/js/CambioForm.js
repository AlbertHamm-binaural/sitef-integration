/** @odoo-module **/

import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
import Registries from 'point_of_sale.Registries';
import { useRef } from "@odoo/owl";
import { _lt } from 'web.core';

const ajax = require('web.ajax');

class CambioForm extends AbstractAwaitablePopup {
    setup() {
        super.setup();
        this.tipDoc = useRef('tipDocSelect');
        this.doc = useRef('docInput');
        this.telefono = useRef('telefonoInput');
        this.banco = useRef('bancoSelect');
    }
    
    async btAceptar() {
        let username = this.env.pos.config.username;
        let password = this.env.pos.config.encrypted_password;
        let idbranch = this.env.pos.config.idbranch;        
        let codestall = this.env.pos.config.codestall;
        let issuingbank = parseInt(this.env.pos.config.issuingbank, 10);

        let tipDoc = this.tipDoc.el.value;
        let doc = this.doc.el.value;
        let telefono = this.telefono.el.value;

        let destinationbank = parseInt(this.banco.el.value, 10);
        let amount = this.props.amount;
        let destinationid = tipDoc + doc;
        let destinationmobilenumber = '58' + telefono.substring(1);

        const token = await this.generarToken(username, password);
        const cambio = await this.generarCambio(username, token, idbranch, codestall, destinationid, destinationmobilenumber, destinationbank, issuingbank, amount);
    }

    async generarToken(username, password) {
        try {
            const result = await ajax.jsonRpc(
                "/sitef_pos_integration/get_token", "call",
                { username, password }
            );
            return result;
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    }
    async generarCambio(username, token, idbranch, codestall, destinationid, destinationmobilenumber, destinationbank, issuingbank, amount) {
        try {
            const result = await ajax.jsonRpc(
                "/sitef_pos_integration/cambio_sitef", "call",
                { username, token, idbranch, codestall, destinationid, destinationmobilenumber, destinationbank, issuingbank, amount}
            );
            if (result.trx_status == "approved") {
                this.showPopup('ConfirmPopup', {
                    title: this.env._t('Pago Móvil realizado con éxito'),
                    body: this.env._t('Referencia: ') + result.payment_reference
                });
                return result;
            } else {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Error: ') + result.error_code,
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

CambioForm.defaultProps = {
    cancelText: _lt('Cancel'),
};

CambioForm.template = 'CambioForm';

Registries.Component.add(CambioForm);
export default CambioForm;