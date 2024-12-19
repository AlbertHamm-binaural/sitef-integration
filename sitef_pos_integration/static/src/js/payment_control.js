/** @odoo-module */
import PaymentScreen from "point_of_sale.PaymentScreen";
import Registries from "point_of_sale.Registries";

var Session = require("web.Session");

const ControlSitef = (PaymentScreen) =>
    
class ControlSitef extends PaymentScreen {
    async cambioSitef() {
        console.log("hola"),
        this.showPopup('ConfirmPopup', {
        title: this.env._t("Cambio"),
        body: this.env._t("Hola Miguel."),
        });
    }
};

Registries.Component.extend(PaymentScreen, ControlSitef);