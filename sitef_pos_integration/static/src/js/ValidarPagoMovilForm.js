/** @odoo-module **/

import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
import Registries from 'point_of_sale.Registries';
import { useRef } from "@odoo/owl";
import { _lt } from 'web.core';

class ValidarPagoMovilForm extends AbstractAwaitablePopup {
    setup() {
        super.setup();
        
        this.referencia = useRef('referenciaInput');
        this.telefono = useRef('telefonoInput');
        this.banco = useRef('bancoSelect');
    }

    btAceptar() {
        let referencia = this.referencia.el.value;
        let telefono = this.telefono.el.value;
        let banco = this.banco.el.value;
        let monto = this.props.amount;
        telefono = '58' + telefono.substring(1);

        console.log('Referencia:', referencia);
        console.log('Telefono:', telefono);
        console.log('Banco:', banco);
        console.log('Monto:', monto);
    }
}

ValidarPagoMovilForm.defaultProps = {
    cancelText: _lt('Cancel'),
};

ValidarPagoMovilForm.template = 'ValidarPagoMovilForm';

Registries.Component.add(ValidarPagoMovilForm);
export default ValidarPagoMovilForm;