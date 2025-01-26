from odoo import models, api, fields
from odoo.exceptions import UserError
import logging
import requests
from datetime import datetime as DateTime
import base64
import os

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):

    _inherit = 'account.move'
    
    fecha_token_tfhka = fields.Datetime()
    token_actual_tfhka = fields.Char()


    def Nota(self, numeroDocumento):
           
        data = { 
            "DocumentoElectronico": {
                "Encabezado": {
                    "IdentificacionDocumento": {
                        "TipoDocumento": "02",
                        "NumeroDocumento": numeroDocumento + 1,
                        "TipoProveedor": "",
                        "TipoTransaccion": "02",
                        "SerieFacturaAfectada": "A",
                        "NumeroFacturaAfectada": "10254",
                        "FechaFacturaAfectada": "10/01/2023",
                        "MontoFacturaAfectada": "10.00",
                        "ComentarioFacturaAfectada": "prueba",
                        "FechaEmision": "07/03/2023",
                        "HoraEmision": "01:23:05 pm",
                        "Anulado": False,
                        "TipoDePago": "importado",
                        "Serie": "A",
                        "Sucursal": "0001",
                        "TipoDeVenta": "interna",
                        "Moneda": "VES"
                    },
                    "Vendedor": {
                        "Codigo": "A01",
                        "Nombre": "Moises Parra",
                        "NumCajero": "001"
                    },
                    "Comprador": {
                        "TipoIdentificacion": "V",
                        "NumeroIdentificacion": "26159207",
                        "RazonSocial": "Eduardo Montiel",
                        "Direccion": "Av Principal de algun sitio",
                        "Pais": "VE",
                        "Telefono": [
                            "+582122447664"
                        ],
                        "Correo": [
                            "servidor@servidor.com"
                        ]
                    },
                    "Totales": {
                        "NroItems": "1",
                        "MontoGravadoTotal": "10.00",
                        "MontoExentoTotal": "0",
                        "Subtotal": "10.00",
                        "TotalAPagar": "11.60",
                        "TotalIVA": "1.60",
                        "MontoTotalConIVA": "11.60",
                        "MontoEnLetras": "ONCE BOLIVARES CON SESENTA CENTIMOS",
                        "TotalDescuento": "0",
                        "ImpuestosSubtotal": [
                            {
                                "CodigoTotalImp": "G",
                                "AlicuotaImp": "16.00",
                                "BaseImponibleImp": "10.00",
                                "ValorTotalImp": "1.60"
                            }
                        ],
                        "FormasPago": [
                            {
                                "Forma": "01",
                                "Monto": "11.60",
                                "Moneda": "VES",
                                "TipoCambio": ""
                            }
                        ]
                    }
                },
                "DetallesItems": [
                    {
                        "NumeroLinea": "1",
                        "CodigoPLU": "7591",
                        "IndicadorBienoServicio": "1",
                        "Descripcion": "Refresco PET 500 ml",
                        "Cantidad": "2",
                        "UnidadMedida": "NIU",
                        "PrecioUnitario": "5.00",
                        "PrecioItem": "10.00",
                        "CodigoImpuesto": "G",
                        "TasaIVA": "16.00",
                        "ValorIVA": "1.60",
                        "ValorTotalItem": "11.60"
                    }
                ]
            }
        }
        return data
    
    def FacturaBasica(self, numeroDocumento):
           
        data = {
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
        }
        return data
        

    def Emision(self):   
        url,token = self.GenerarToken() 
        hasta, inicio = self.ConsultaNumeracion(url, token)
        numeroDocumento = self.UltimoDocumento(url, token)
        data = self.FacturaBasica(numeroDocumento)
        
        if numeroDocumento == inicio:
            self.AsignarNumeracion(self, url, token, hasta, inicio)   
        _logger.info(f"Se esta ejecturando emision")
            
        headers = {
            "Authorization": f"Bearer {token}"
        }      
        response = requests.post(url + "/Emision", json=data,headers=headers)     
        if response.status_code == 200:
            respuesta_json = response.json()
            if respuesta_json.get("codigo") == "200":
                _logger.info("Documento emitido correctamente")
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

    
    # def DescargarArchivo(self):
    #     url, token = self.GenerarToken()
        
    #     headers = {
    #         "Authorization": f"Bearer {token}"
    #     }
        
    #     response = requests.post(url + "/DescargaArchivo", json={
    #             "token": token,
    #             "serie": "",
    #             "tipoDocumento": "01",
    #             "numeroDocumento": "1"
    #         }, headers=headers)
        
    #     if response.status_code == 200:
    #         _logger.info("Petición realizada correctamente")
            
    #         try:
    #             respuesta_json = response.json()
                
    #             if respuesta_json.get("codigo") == "200":
    #                 base64_string = respuesta_json.get("archivo")
                    
    #                 if base64_string:
    #                     try:
    #                         # Decodificar el archivo
    #                         decoded_file = base64.b64decode(base64_string)
                            
    #                         # Ruta explícita
    #                         current_directory = ""
    #                         file_path = os.path.join(current_directory, "archivo_descargado.pdf")
                            
    #                         # Guardar el archivo
    #                         with open(file_path, "wb") as file:
    #                             file.write(decoded_file)
                            
    #                         _logger.info(f"Archivo guardado en: {file_path}")
    #                         return file_path
    #                     except Exception as e:
    #                         _logger.error(f"Error al decodificar o guardar el archivo: {e}")
    #                         raise UserError("No se pudo guardar el archivo descargado.")
    #                 else:
    #                     _logger.error("La respuesta no contiene el archivo en base64.")
    #                     raise UserError("La respuesta no contiene el archivo en base64.")
    #             else:
    #                 _logger.error(f"Error en la descarga: {respuesta_json.get('mensaje')}")
    #                 raise UserError(f"Error en la descarga: {respuesta_json.get('mensaje')}")
    #         except Exception as e:
    #             _logger.error(f"Error al procesar la respuesta JSON: {e}")
    #             raise UserError("No se pudo procesar la respuesta JSON.")
    #     else:
    #         _logger.error(f"Error HTTP: {response.status_code}")
    #         raise UserError(f"Error HTTP: {response.status_code}")

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
            