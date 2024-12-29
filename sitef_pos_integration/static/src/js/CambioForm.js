/** @odoo-module **/

import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
import Registries from 'point_of_sale.Registries';
import { useRef } from "@odoo/owl";
import { _lt } from 'web.core';

class CambioForm extends AbstractAwaitablePopup {
    setup() {
        super.setup();
        this.tipDoc = useRef('tipDocSelect');
        this.doc = useRef('docInput');
        this.telefono = useRef('telefonoInput');
        this.banco = useRef('bancoSelect');
    }

    btAceptar() {
        let tipDoc = this.tipDoc.el.value;
        let doc = this.doc.el.value;
        let telefono = this.telefono.el.value;
        let banco = this.banco.el.value;
        let monto = this.props.amount;

        doc = tipDoc + doc;
        telefono = '58' + telefono.substring(1);

        console.log('Documento:', doc);
        console.log('Telefono:', telefono);
        console.log('Banco:', banco);
        console.log('Monto:', monto);
    }
}

CambioForm.defaultProps = {
    cancelText: _lt('Cancel'),
};

CambioForm.template = 'CambioForm';

Registries.Component.add(CambioForm);
export default CambioForm;

