# -*- coding: utf-8 -*-

import re
import flags
from datetime import datetime
import settings
import xmltodict

from lxml import etree
from xml.sax.saxutils import escape
from jinja2 import Environment, PackageLoader

from notacarioca import template_filters as filters


class ErrorMixin(object):

    def _build_errors(self, response):
        self.status = flags.NFSE_PROCESS["rejected"]
        message = response["ListaMensagemRetorno"]["MensagemRetorno"]

        if isinstance(message, dict):
            self.errors.append(Error(**message))
        else:
            for error in message:
                self.errors.append(Error(**error))


class RPS(object):

    def __init__(self, **kwargs):
        self.serie = kwargs.pop("serie")
        self.number = kwargs.pop("number")
        self.rps_type = kwargs.pop("rps_type")
        self.emission_date = kwargs.pop("emission_date",
            datetime.now().isoformat())
        self.operation_nature = kwargs.pop("operation_nature")
        self.status = kwargs.pop("rps_situation")

        # Control fields
        self.protocol = kwargs.pop("protocol", None)
        self.nfse_number = kwargs.pop("nfse_number", None)

        self.taker = None

        if kwargs.get("taker"):
            self.taker = Taker(**kwargs.pop("taker"))

        self.emitter = Emitter(**kwargs.pop("emitter"))
        self.service = Service(**kwargs.pop("service"))

    def _get_template(self, template):
        env = Environment(loader=PackageLoader('notacarioca', 'templates'))
        env.filters["normalize"] = filters.normalize_str
        env.filters["format_percent"] = filters.format_percent
        env.filters["format_datetime"] = filters.format_datetime

        return env.get_template(template)

    def _generate_xml(self, template, **kwargs):
        template = self._get_template(template)
        xml = template.render(kwargs).encode("utf-8")
        xml = re.sub('>\s+<', '><', xml)
        xml = re.sub(u'\ufeff', '', xml)
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        output = etree.fromstring(xml, parser=parser)

        return output

    def generate_xml(self, method):
        tmpl = settings.TEMPLATES[method]
        xml = self._generate_xml(tmpl, rps=self)

        return etree.tostring(xml)


class Emitter(object):

    def __init__(self, **kwargs):
        self.cnpj = kwargs.pop("cnpj")
        self.city_inscription = kwargs.pop("city_inscription")
        self.national_simple = kwargs.pop("national_simple")
        self.cultural_promoter = kwargs.pop("cultural_promoter")


class Service(object):

    def __init__(self, **kwargs):
        self.service_item_list = kwargs.pop("service_item_list")
        self.city_tax_code = kwargs.pop("city_tax_code")
        self.description = kwargs.pop("description")
        self.city_code = kwargs.pop("city_code")

        self.values = Values(**kwargs.pop("values"))


class Values(object):

    def __init__(self, **kwargs):
        self.service_amount = kwargs.pop("service_amount")
        self.pis_amount = kwargs.pop("pis_amount")
        self.inss_amount = kwargs.pop("inss_amount")
        self.cofins_amount = kwargs.pop("cofins_amount")
        self.iss_amount = kwargs.pop("iss_amount")
        self.ir_amount = kwargs.pop("ir_amount")
        self.retained_iss = kwargs.pop("retained_iss")
        self.retained_iss_amount = kwargs.pop("retained_iss_amount")
        self.csll_amount = kwargs.pop("csll_amount")
        self.calculation_base = kwargs.pop("calculation_base")
        self.aliquota = kwargs.pop("aliquota")
        self.liquid_amount = kwargs.pop("liquid_amount")
        self.unconditioned_discount = kwargs.pop("unconditioned_discount")
        self.discount_conditioning = kwargs.pop("discount_conditioning")
        self.deduction_amount = kwargs.pop("deduction_amount")
        self.other_retentions_amount = kwargs.pop("other_retentions_amount")


class Taker(object):

    def __init__(self, **kwargs):
        self.social_reason = kwargs.pop("social_reason")
        self.email = kwargs.pop("email", None)
        self.phone = kwargs.pop("phone", None)
        self.cnpj = kwargs.pop("cnpj", None)
        self.cpf = kwargs.pop("cpf", None)
        self.address = Address(**kwargs.pop("address"))


class Address(object):

    def __init__(self, **kwargs):
        self.street = kwargs.pop('street')
        self.number = kwargs.pop('number')
        self.complement = kwargs.get('complement')
        self.neighborhood = kwargs.pop('neighborhood')
        self.city_code = kwargs.get('city_code')
        self.state = kwargs.pop('state')
        self.zip_code = kwargs.pop('zip_code')


class ResponseRPS(ErrorMixin):

    def __init__(self, rps, response=None, in_process=False, **kwargs):
        self.response = response
        self.rps = rps
        self.nfse = None
        self.status = flags.NFSE_PROCESS["processing"]
        self.errors = []

        if not in_process:
            self._process_response()

    def _build_nfse(self, response):
        nfse_inf = response["CompNfse"]["Nfse"]["InfNfse"]
        self.nfse = NFSe(**nfse_inf)

    def _process_response(self):
        response = xmltodict.parse(self.response)

        if response.get("GerarNfseResposta"):
            response = response["GerarNfseResposta"]

            if "ListaMensagemRetorno" in response.keys():
                self._build_errors(response)

                return None

            self.status = flags.NFSE_PROCESS["accepted"]

        if response.get("ConsultarNfseResposta"):
            response = response["ConsultarNfseResposta"]
            self.status = flags.NFSE_PROCESS["accepted"]

            if response["ListaNfse"]["CompNfse"].get("NfseCancelamento"):
                self.status = flags.NFSE_PROCESS["cancelled"]

        self._build_nfse(response)


class ResponseCancel(ErrorMixin):

    def __init__(self, response):
        self.response = response
        self.status = flags.NFSE_PROCESS["cancelled"]
        self.errors = []

        self._process_response()

    def _process_response(self):
        response = xmltodict.parse(self.response)["CancelarNfseResposta"]

        if "ListaMensagemRetorno" in response.keys():
            self._build_errors(response)


class Error(object):

    def __init__(self, **kwargs):

        self.description = kwargs.pop("Mensagem")
        self.code = kwargs.pop("Codigo")
        self.tip = kwargs.pop("Correcao", None)


class NFSe(object):

    def _format_datetime(self, date):
        if date:
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

        return date

    def __init__(self, **kwargs):
        print kwargs
        self.key = kwargs["CodigoVerificacao"] or None
        self.number = int(kwargs["Numero"]) or None
        self.emission_date_nfse = self._format_datetime(kwargs.get("DataEmissao"))
        self.mirror = None
        self.xml = None


class NFSeXML(object):

    def __init__(self, response, **kwargs):
        self.response = response
        self.xml = None

        self._process_xml()

    def _process_xml(self):
        self.xml = self.response.encode("utf-8")
