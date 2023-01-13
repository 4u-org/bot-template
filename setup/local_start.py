import asyncio
from aiogram import Bot, Dispatcher
from aiohttp import web
import os
from OpenSSL import crypto
import ssl

import config as cfg

async def start_local_aiohttp_app(
    dispatcher: Dispatcher, 
    local_aiohttp_app: web.Application
):
    task = asyncio.create_task(web._run_app(
        app=local_aiohttp_app, 
        port=cfg.WEB_SERVER_PORT,
        host=cfg.WEB_SERVER_HOST, 
        ssl_context=setup_ssl()
        ))
    dispatcher["local_aiohttp_task"] = task

async def stop_local_aiohttp_app(dispatcher: Dispatcher):
    local_aiohttp_task: asyncio.Task[None] = dispatcher["local_aiohttp_task"]
    local_aiohttp_task.cancel()

def start_bot(dp: Dispatcher, app: web.Application, bot: Bot):
    dp.startup.register(start_local_aiohttp_app)
    dp.shutdown.register(stop_local_aiohttp_app)
    dp.run_polling(bot, local_aiohttp_app=app)

# Webapp requirements
def setup_ssl() -> ssl.SSLContext:
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.check_hostname = False
    certfile, keyfile = generate_self_signed_cert("setup/self-signed-certs")
    ssl_context.load_cert_chain(certfile, keyfile)
    return ssl_context

def generate_self_signed_cert(cert_dir):
    """Generate a SSL certificate.
 
    If the cert_path and the key_path are present they will be overwritten.
    """
    if not os.path.exists(cert_dir):
        os.makedirs(cert_dir)
    cert_path = os.path.join(cert_dir, "cert-rsa.pem")
    key_path = os.path.join(cert_dir, "key-rsa.pem")
 
    ecert =  os.path.exists(cert_path)
    ekey = os.path.exists(key_path)
    if ecert and ekey:
        return cert_path, key_path
    elif ecert:
        os.unlink(cert_path)
    elif ekey:
        os.unlink(key_path)
 
    # create a key pair
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 1024)
 
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = 'US'
    cert.get_subject().ST = 'Lorem'
    cert.get_subject().L = 'Ipsum'
    cert.get_subject().O = 'Lorem'
    cert.get_subject().OU = 'Ipsum'
    cert.get_subject().CN = 'Unknown'
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60) 
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha1')
 
    with open(cert_path, 'wb') as fd: 
        fd.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
 
    with open(key_path, 'wb') as fd: 
        fd.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
 
    return cert_path, key_path