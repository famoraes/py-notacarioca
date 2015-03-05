URL = {
    3304557: {
        "sandbox": "https://notacarioca.rio.gov.br/WSNacional/nfse.asmx?wsdl",
        "production": "https://homologacao.notacarioca.rio.gov.br/WSNacional/nfse.asmx?wsdl"
    }
}

TEMPLATES = {
    'send_rps': "RecepcionarLoteRps.xml",
    'status': "ConsultarSituacaoLoteRps.xml",
    'get_nfse': "ConsultarNfseEnvio.xml",
    'cancel': "CancelarNfseEnvio.xml"
}

METHODS = {
    'send_rps': "RecepcionarLoteRps",
    'status': "ConsultarSituacaoLoteRps",
    'get_nfse': "ConsultarNfse",
    'cancel': "CancelarNfse"
}
