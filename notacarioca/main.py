import requests
import suds
import suds.client
import suds_requests

from lxml import etree
from suds.sax.text import Raw
from xml.sax.saxutils import escape

from notacarioca import settings, models


class NotaCarioca(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.key = kwargs.pop("key")
        self.certificate = kwargs.pop("certificate")
        self.city_code = kwargs.pop("city_code")
        self.env = kwargs.pop("env")
        self.base_url = settings.URL[self.city_code][self.env]
        self.rps = models.RPS(**self.kwargs)

    def _get_rps(self, method):
        return models.RPS(template=method, method=method, **self.kwargs)

    def _get_credentials(self, credential):
        filename = '%s-%s.pem' % (self.rps.emitter.cnpj, credential)
        file_obj = open('/tmp/%s' % filename, 'w+')
        file_obj.write(getattr(self, credential))

        return '/tmp/%s' % filename

    def _get_client(self):
        cache_requests = False
        cache_location = '/tmp/suds'
        cache = suds.cache.DocumentCache(location=cache_location)

        session = requests.Session()
        session.cert = (self._get_credentials("certificate"),
            self._get_credentials("key"))

        return suds.client.Client(
            self.base_url,
            cache=cache,
            transport=suds_requests.RequestsTransport(session)
        )

    def send(self):
        client = self._get_client()
        response = client.service.GerarNfse(self.rps.generate_xml("send_rps"))

        return models.ResponseRPS(self.rps, response)

    def status(self, nfse=False):
        if nfse:
            return self.update_nfse()

        client = self._get_client()

        try:
            response = client.service.ConsultarNfse(
                self.rps.generate_xml("status"))
        except:
            return models.ResponseRPS(self.rps, in_process=True)

        return models.ResponseRPS(self.rps, response)

    def download_nfse(self):
        client = self._get_client()
        response = client.service.ConsultarNfse(
            self.rps.generate_xml("get_nfse"))

        return models.NFSeXML(response)

    def update_nfse(self):
        client = self._get_client()
        response = client.service.ConsultarNfse(
            self.rps.generate_xml("get_nfse"))

        return models.ResponseRPS(self.rps, response)

    def cancel(self):
        client = self._get_client()
        response = client.service.CancelarNfse(
            self.rps.generate_xml("cancel"))

        return models.ResponseCancel(response)
