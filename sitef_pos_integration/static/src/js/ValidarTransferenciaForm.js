/** @odoo-module **/

import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
import Registries from 'point_of_sale.Registries';
import { useRef } from "@odoo/owl";
import { _lt } from 'web.core';

const ajax = require('web.ajax');

class ValidarTransferenciaForm extends AbstractAwaitablePopup {
    setup() {
        super.setup();
        this.tipDoc = useRef('tipDocSelect');
        this.doc = useRef('docInput');
        this.ref = useRef('refInput');
        this.banco = useRef('bancoSelect');
        this.fecha = useRef('fecha');
    }
    
    async confirm() {
        if (this.doc.el.value != "" && this.ref.el.value != "" && this.banco.el.value != "" && this.fecha.el.value != "" ) {
            let username = this.env.pos.config.username_sitef;
            let password = this.env.pos.config.encrypted_password;
            let url = this.env.pos.config.url_sitef;
            let idbranch = this.env.pos.config.idbranch_sitef;        
            let codestall = this.env.pos.config.codestall_sitef;
            let receivingbank = parseInt(this.env.pos.config.issuingbank_sitef, 10);
    
            let tipDoc = this.tipDoc.el.value;
            let doc = this.doc.el.value;
            let paymenreference = this.ref.el.value;
            let trxdate = this.fecha.el.value;
    
            let origenbank = parseInt(this.banco.el.value, 10);
            let amount = this.props.amount;
            let origendni = tipDoc + doc;
            
            const token = await this.generarToken(url, username, password);
            if (token) {
                const cambio = await this.validarTransferencia(url, username, token, idbranch, codestall, amount, paymenreference, origenbank, origendni, trxdate, receivingbank);
            }
        } else {
            this.showPopup('ErrorPopup', {
                title: this.env._t('Campos vacíos'),
                body: this.env._t('Debe ingresar TODOS los campos')
            });
        }
    }

    async generarToken(url, username, password) {
        const result = await ajax.jsonRpc(
            "/sitef_pos_integration/get_token", "call",
            { url, username, password }
        );
        if (result.error) {
            this.showPopup('ErrorPopup', {
                title: this.env._t('Error al generar token'),
                body: this.env._t(result.error),
            });
            return null
        } else{
            return result;
        }
    }
    
    async validarTransferencia(url, username, token, idbranch, codestall, amount, paymenreference, origenbank, origendni, trxdate, receivingbank) {
        try {    
            const result = await ajax.jsonRpc(
                "/sitef_pos_integration/validarTransferencia_sitef", "call",
                { url, username, token, idbranch, codestall, amount, paymenreference, origenbank, origendni, trxdate, receivingbank}
            );
            if (result == "marcada") {
                this.showPopup('ConfirmPopup', {
                    title: this.env._t('Validación de transferencia'),
                    body: this.env._t('La transferencia fue validada con éxito')
                });
                this.env.posbus.trigger('close-popup', {
                    popupId: this.props.id,
                    response: { confirmed: true, payload: await this.getPayload() },
                });    
                return result;
            } 
            if (result == "verified") {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Validación de transferencia'),
                    body: this.env._t('La transferencia ya fue validada anteriormente'),
                });
                return result;
            } else {
                this.showPopup('ErrorPopup', {
                    title: this.env._t(result.error_code),
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


ValidarTransferenciaForm.defaultProps = {
    cancelText: _lt('Cancel'),
    confirmText: _lt('Confirm'),
};

ValidarTransferenciaForm.template = 'ValidarTransferenciaForm';

Registries.Component.add(ValidarTransferenciaForm);
export default ValidarTransferenciaForm;