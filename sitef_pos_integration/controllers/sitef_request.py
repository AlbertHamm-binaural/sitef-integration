from odoo import http
import requests
import logging
import hashlib
from bs4 import BeautifulSoup

_logger = logging.getLogger(__name__)

class SitefController(http.Controller):
    @http.route('/sitef_pos_integration/get_token', type='json', methods=['POST'])
    def get_token(self, url, username, password):
        if username != "" and password != "":
            _logger.warning("INSIDE GET TOKEN")
            response = requests.post(url + "/sitef/apiToken", json={
                "username": username,
                "password": password
            })
            response_json = response.json()
            _logger.warning(response_json)
            
            if response.status_code == 200 and "data" in response_json and "token" in response_json["data"]:
                token = response_json["data"]["token"]
                return token
            else:
                return {"error": "Campo username o password incorrecto."}
        else:
            return {"error": "Campo username o password vacío."}
    
    @http.route('/sitef_pos_integration/cambio_sitef', type='json', methods=['POST'])
    def cambio_sitef(self, url, username, token, idbranch, codestall, destinationid, destinationmobilenumber, destinationbank, issuingbank, amount):
        _logger.warning("INSIDE VUELTO SITEF")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        token_md5 = hashlib.md5(token.encode()).hexdigest()
        response = requests.post(url + "/sitefAuth/setVueltoSitef", json={
            "username": username, 
            "token": token_md5, 
            "idbranch": idbranch,
            "codestall": codestall, 
            "destinationid": destinationid,
            "destinationmobilenumber": destinationmobilenumber, 
            "destinationbank": destinationbank,
            "issuingbank": issuingbank, 
            "invoicenumber": "4143320592",
            "amount": amount
        }, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            _logger.warning(response_json)
            
            if "data" in response_json and "transaction_c2p_response" in response_json["data"]:
                return {
                    "trx_status": response_json["data"]["transaction_c2p_response"]["trx_status"],
                    "payment_reference": response_json["data"]["transaction_c2p_response"]["payment_reference"],
                }
            else:
                _logger.error("Error en la solicitud.")
                error_list = response_json["data"]["error_list"]
                if isinstance(error_list, list) and len(error_list) > 0:
                    if (error_list[0]["error_code"] == "500"):
                        return {
                            "error_code": "Cédula o teléfono inválido",
                            "description": error_list[0]["description"]
                        }
                    else:
                        return {
                            "error_code": error_list[0]["error_code"],
                            "description": error_list[0]["description"]
                        }
                else:
                    return {
                        "error_code": "unknown",
                        "description": "Unknown error"
                    }
        else:
            _logger.error(f"Error en la solicitud: {response.status_code} - {response.text}")
            return {"error": f"Error en la solicitud: {response.status_code}"}
    
    @http.route('/sitef_pos_integration/validarPago_sitef', type='json', methods=['POST'])
    def validarPago_sitef(self, url, username, token, idbranch, codestall, amount, paymentreference, debitphone, origenbank, receivingbank, trxdate):
        _logger.warning("INSIDE VALIDAR PAGO SITEF")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        token_md5 = hashlib.md5(token.encode()).hexdigest()
        response = requests.post(url + "/sitefAuth/getBusquedaSitef", json={
            "username": username,
            "token": token_md5,
            "idbranch": idbranch,
            "codestall": codestall,
            "amount": amount,
            "paymentreference": paymentreference,
            "debitphone": debitphone,
            "origenbank": origenbank,
            "invoicenumber": "9491",
            "receivingbank": receivingbank,
            "trxdate": trxdate
        }, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            _logger.warning(response_json)
            
            if "data" in response_json and "marcada" in response_json["data"]:
                return response_json["data"]["marcada"]
            else:
                _logger.error("Error en la solicitud.")
                error_list = response_json["data"]["error_list"]
                if isinstance(error_list, list) and len(error_list) > 0:
                    return {
                        "error_code": "Datos no encontrados",
                        "description": error_list[0]["description"]
                    }
                else:
                    return {
                        "error_code": "unknown",
                        "description": "Unknown error"
                    }
        else:
            _logger.error(f"Error en la solicitud: {response.status_code} - {response.text}")
            return {"error": f"Error en la solicitud: {response.status_code}"}
        
    @http.route('/sitef_pos_integration/validarTransferencia_sitef', type='json', methods=['POST'])
    def validarTransferencia_sitef(self, url, username, token, idbranch, codestall, amount, paymenreference, origenbank, origendni, trxdate, receivingbank):
        _logger.warning("INSIDE VALIDAR TRANSFERENCIA SITEF")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        token_md5 = hashlib.md5(token.encode()).hexdigest()
        response = requests.post(url + "/sitefAuth/getTrfSitef", json={
            "username": username,
            "token": token_md5,
            "idbranch": idbranch,
            "codestall": codestall,
            "amount": amount,
            "paymenreference": paymenreference,
            "origendni": origendni,
            "origenbank": origenbank,
            "receivingbank": receivingbank,
            "origenbank": origenbank,
            "trxdate": trxdate
        }, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            _logger.warning(response_json)
            
            if "data" in response_json and "marcada" in response_json["data"]:
                return response_json["data"]["marcada"]
            else:
                _logger.error("Error en la solicitud.")
                error_list = response_json["data"]["error_list"]
                if isinstance(error_list, list) and len(error_list) > 0:
                    return {
                        "error_code": "Datos no encontrados",
                        "description": error_list[0]["description"]
                    }
                else:
                    return {
                        "error_code": "unknown",
                        "description": "Unknown error"
                    }
        else:
            _logger.error(f"Error en la solicitud: {response.status_code} - {response.text}")
            return {"error": f"Error en la solicitud: {response.status_code}"}
        
    @http.route('/sitef_pos_integration/validarZelle_sitef', type='json', methods=['POST'])
    def validarZelle_sitef(self, url, username, token, idbranch, codestall, amount, trxdate):
        _logger.warning("INSIDE VALIDAR TRANSFERENCIA SITEF")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        token_md5 = hashlib.md5(token.encode()).hexdigest()
        response = requests.post(url + "/sitefAuth/getZelleSitef", json={
            "username": username,
            "token": token_md5,
            "idbranch": idbranch,
            "codestall": codestall,
            "amount": amount,
            "invoicenumber": "ITL-004568",
            "trxdate": trxdate
        }, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            _logger.warning(response_json)
            
            if "data" in response_json and "marcada" in response_json["data"]:
                return response_json["data"]["marcada"]
            else:
                _logger.error("Error en la solicitud.")
                error_list = response_json["data"]["error_list"]
                if isinstance(error_list, list) and len(error_list) > 0:
                    return {
                        "error_code": "Datos no encontrados",
                        "description": error_list[0]["description"]
                    }
                else:
                    return {
                        "error_code": "unknown",
                        "description": "Unknown error"
                    }
        else:
            _logger.error(f"Error en la solicitud: {response.status_code} - {response.text}")
            return {"error": f"Error en la solicitud: {response.status_code}"}

    @http.route('/sitef_pos_integration/obtener_precio_dolar', type='json', methods=['POST'])
    def obtener_precio_dolar(self):
        url = 'https://www.bcv.org.ve'
        respuesta = requests.get(url, verify=False)

        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            
            dolar_divs = soup.find_all('div', class_='centrado')
            
            if len(dolar_divs) >= 5:
                dolar_text = dolar_divs[4].find('strong').text.strip()
                dolar_text = dolar_text.replace(',', '.')
                precio_dolar = float(dolar_text.split(' ')[0])
                return round(precio_dolar, 2)
        else:
            print(f"Error: {respuesta.status_code}")