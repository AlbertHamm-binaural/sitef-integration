from odoo import models, api, fields
from odoo.exceptions import UserError
import logging
import requests
from datetime import datetime as DateTime

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):

    _inherit = 'account.move'
    
    fecha_token_tfhka = fields.Datetime()
    token_actual_tfhka = fields.Char()

    def Emision(self):   
        url,token = self.GenerarToken()
        hasta, inicio = self.ConsultaNumeracion(url, token)

        numeroDocumento = self.UltimoDocumento(url, token)
        if numeroDocumento is inicio:
            self.AsignarNumeracion(self, url, token, hasta, inicio)
        
        _logger.info(f"Se esta ejecturando emision")
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.post(url + "/Emision", json={
            "documentoElectronico": {
            "encabezado": {
            "identificacionDocumento": {
                "tipoDocumento": "01",
                "numeroDocumento": str(numeroDocumento + 1),
                "tipoTransaccion": "01",
                "fechaEmision": "07/09/2023",
                "fechaVencimiento": "08/09/2023",
                "horaEmision": "01:36:22 pm",
                "tipoDePago": "CONTADO",
                "serie": "",
                "tipoDeVenta": "EN LINEA",
                "moneda": "BsD"
            },
            "comprador": {
                "tipoIdentificacion": "V",
                "numeroIdentificacion": "005534237",
                "razonSocial": "NELSON IVAN, LINARES OROPEZA",
                "direccion": "CRRT VIA LA UNION CALLE EL YAGRUMAL, QTA VILLA VIRGINIA, URB EL HATILLO, EL HATILLO-1083,CARACAS, EDO. DISTRITO CAPITAL, VENEZUELA",
                "pais": "VE",
                "telefono": [
                "+58-4142369327"
                ],
                "notificar": "Si",
                "correo": [
                "miguel@binauraldev.com"
                ]
            }
            },
            "detallesItems":[
                {
                "numeroLinea": "1",
                "codigoPLU": "03-2023",
                "indicadorBienoServicio": "2",
                "descripcion": "CUOTA MANTENIMIENTO",
                "cantidad": "1",
                "precioUnitario": "1400",
                "precioItem": "1400",
                "codigoImpuesto": "G",
                "tasaIVA": "16",
                "valorIVA": "224",
                "valorTotalItem": "1624"
                }
            ]
        }

        },headers=headers)
         
        if response.status_code is 200:
            respuesta_json = response.json()
            if respuesta_json.get("codigo") == "200":
                _logger.info("Documento emitido correctamente")
                return
            elif respuesta_json.get("codigo") == "201":
                _logger.error("Numero de documento duplicado")
                raise UserError("Numero de documento duplicado")
            else:
                _logger.error(f"Error al emitir documento: { respuesta_json}")
                raise UserError(f"Error al emitir documento: { respuesta_json}")
        else:
            _logger.error(f"Error: {response.status_code}")
            raise UserError(f"Error: {response.status_code}")
            
    def UltimoDocumento(self, url, token):
        _logger.info(f"Se esta ejecutando ultimodocumento")

        headers = {
            "Authorization": f"Bearer {token}"
        }
          
        response = requests.post(url + "/UltimoDocumento", json={
                "token": token,
                "serie": "",
                "tipoDocumento": "01",
            }, headers=headers)
        
        if response.status_code == 200:
            _logger.info("Ultimo documento consultado correctamente")
            respuesta_json = response.json()
            if respuesta_json.get("codigo") == "200":
                numeroDocumento = respuesta_json["numeroDocumento"]
                return numeroDocumento
            else:
                _logger.error("Error al obtener numeroDocumento.")
        else:
            _logger.error(f"Error: {response.status_code}")
            raise UserError(f"Error: {response.status_code}")

    def AsignarNumeracion(self, url, token, hasta, inicio):
        fin = inicio + 20
        inicio += 1
        
        _logger.info(f"Se esta ejecutando asignar numeracion")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        if inicio <= hasta:
            response = requests.post(url + "/AsignarNumeraciones", json={
            "token": token,
            "serie": "",
            "tipoDocumento": "01",
            "numeroDocumentoInicio": inicio,
            "numeroDocumentoFin": fin
        }, headers=headers)
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

    def ConsultaNumeracion(self, url, token):
        _logger.info(f"Se esta ejecutando consulta numeracion")

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
        username, password, url = self.ObtenerCredencial()
        fecha_token_tfhka = self.fecha_token_tfhka 
        fecha_actual = DateTime.now()
        
        if not isinstance(fecha_token_tfhka, DateTime) or fecha_token_tfhka < fecha_actual:
            respuesta = requests.post(url + "/Autenticacion", json={
                "usuario": username,
                "clave": password
            })
            respuesta_json = respuesta.json()
            _logger.warning(respuesta_json)
              
            if respuesta.status_code == 200:
                if "token" in respuesta_json:
                    token = respuesta_json["token"]
                    _logger.info(f"El token es: {token}")
                    
                    expiracion_str = respuesta_json["expiracion"]
                    expiracion_str = expiracion_str[:26] + 'Z' 
                    expiracion = DateTime.strptime(expiracion_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    
                    self.fecha_token_tfhka = expiracion
                    self.token_actual_tfhka = token
                    return url, token
                elif "token" not in respuesta_json:
                    mensaje = respuesta_json.get("mensaje")
                    _logger.warning(mensaje)
                    raise UserError(F"Error {mensaje}")
                else:
                    _logger.error(f"Error: {respuesta.status_code}")
            else: 
                _logger.error(f"Error: {respuesta.status_code}")
                raise UserError(f"Error: {respuesta.status_code}")
        else:
            _logger.info("El token aún es válido.")
            token = self.token_actual_tfhka
            return url, token
        
    def ObtenerCredencial(self):
        
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
            