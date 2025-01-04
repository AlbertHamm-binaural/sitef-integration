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

    async btAceptar() {
        // let tipDoc = this.tipDoc.el.value;
        // let doc = this.doc.el.value;
        // let telefono = this.telefono.el.value;
        // let banco = this.banco.el.value;
        // let monto = this.props.amount;
        // doc = tipDoc + doc;
        // telefono = '58' + telefono.substring(1);

        this.generarToken();
    }

    generarToken() {
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        
        var raw = JSON.stringify({
            "username": this.env.pos.config.username,
            "password": this.env.pos.config.encrypter_password
        });
        
        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };
        
        fetch("https://api.sitefdevenezuela.com/prod/s4/sitef/apiToken", requestOptions)
            .then(response => response.text())
            .then(result => console.log(result))
            .catch(error => console.log('error', error));    
    }
}

CambioForm.defaultProps = {
    cancelText: _lt('Cancel'),
};

CambioForm.template = 'CambioForm';

Registries.Component.add(CambioForm);
export default CambioForm;

