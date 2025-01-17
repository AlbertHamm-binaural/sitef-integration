from odoo import models, api
from odoo.exceptions import UserError
import logging
import requests
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):

    _inherit = 'account.move'

    def Emision(self):          
        url,token = self.GenerarToken()
        _logger.info(f"URL: {url} / TOKEN: {token}")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        respuesta = requests.post(url + "/Emision", json={
            "token": token,
        })

    def GenerarToken(self):
            
        username, password, url = self.ObtenerCredenciales()
        
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
                return token, url
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