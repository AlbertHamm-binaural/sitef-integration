from odoo import models, api
from odoo.exceptions import UserError
import logging
import requests
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):

    _inherit = 'account.move'

    def AsignarNumeracion(self):
        url, token = self.GenerarToken()
        hasta, inicio = self.ConsultaNumeracion()
        fin = inicio + 20
        
        _logger.info(f"URL: {url} / TOKEN: {token}")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.post(url + "/AsignarNumeraciones", json={
            "token": token,
            "serie": "",
            "tipoDocumento": "01",
            "numeroDocumentoInicio": inicio,
            "numeroDocumentoFin": fin
        }, headers=headers)
        
        if inicio <= hasta:
            if response.status_code == 200:
                _logger.info("Rango asignado correctamente")
                return
            elif response.status_code == 203:
                _logger.warning(f"Error al asignar el rango: {response.status_code}")
                raise UserError("Error al asignar el rango.")
            else:
                _logger.error(f"Error: {response.status_code}")
                raise UserError(f"Error: {response.status_code}")
        else:
            _logger.error("El rango de numeración asignado ha sido superado.")
            raise UserError("El rango de numeración asignado ha sido superado.")

    def ConsultaNumeracion(self):
        url, token = self.GenerarToken()
        _logger.info(f"URL: {url} / TOKEN: {token}")

        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.post(url + "/ConsultaNumeraciones", json={
                "token": token,
                "serie": "",
                "tipoDocumento": "",
                "prefix": ""
            }, headers=headers)
        
        if response.status_code == 200:
            _logger.info("Numeración consultada correctamente")
            respuesta_json = response.json()
            if respuesta_json.get("codigo") == "200" and "numeraciones" in respuesta_json:
                numeracion = respuesta_json["numeraciones"][0]
                hasta = numeracion.get("hasta")
                inicio = numeracion.get("correlativo")
                return hasta, inicio
            else:
                _logger.error("No existen numeraciones que coincidan con los criterios aplicados o que cuenten con disponibilidad.")
                raise UserError("Error al obtener numeraciones.")
        else:
            _logger.error(f"Error: {response.status_code}")
            raise UserError(f"Error: {response.status_code}")

    def GenerarToken(self):           
        username, password, url, maximaNumeracion = self.ObtenerCredenciales()
        
        respuesta = requests.post(url + "/Autenticacion", json={
            "usuario": username,
            "clave": password
        })
        respuesta_json = respuesta.json()
        _logger.warning(respuesta_json)
                
        if respuesta.status_code == 200:
            if "token" in respuesta_json:
                token = respuesta_json["token"]
                _logger.info(token)
                return token, url, maximaNumeracion
            else:
                _logger.error("La respuesta no contiene el token.")
            if respuesta_json.get("codigo") == 403:
                mensaje = respuesta_json.get("mensaje")
                _logger.warning(mensaje)
                raise UserError(mensaje)
            else:
                _logger.error(f"Error: {respuesta.status_code}")
        else: 
            _logger.error(f"Error: {respuesta.status_code}")
            raise UserError(f"Error: {respuesta.status_code}")
        
    def ObtenerCredenciales(self):
        
        username = None
        password = None
        url = None
        
        for move in self:
            if move.company_id.username_tfhka and move.company_id.password_tfhka and move.company_id.url_tfhka:
                username = move.company_id.username_tfhka
                password = move.company_id.password_tfhka
                url = move.company_id.url_tfhka
            
                return username, password, url
            else:
                _logger.error("USERNAME o PASSWORD vacío.")
                raise UserError("USERNAME o PASSWORD vacío.")
            
        _logger.info(f"Username: {username}, Password: {password}, URL: {url}")