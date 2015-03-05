
from enum import Enum


class EnumRepresentation(Enum):
    """
    Reprents a Enum with a string
    """
    def __str__(self):
        if self.value:
            return str(self.value)
        else:
            return super(EnumRepresentation, self).__str__()


class Status(EnumRepresentation):
    normal = 1
    cancelado = 2


class OperationNature(EnumRepresentation):
    no_municipio = 1
    fora_do_municipio = 2
    isencao = 3
    imune = 4
    suspensa_decisao_judicial = 5
    suspensa_procedimento_administrativo = 6


class TaxRegime(EnumRepresentation):
    microempresa_municipal = 1
    estimativa = 2
    sociedade_profissionais = 3
    cooperativa = 4
    mei = 5
    meepp = 6


class YesNo(EnumRepresentation):
    yes = 1
    no = 2


class RpsType(EnumRepresentation):
    rps = 1
    nota_conjugada = 2
    cupom = 3


class CpfCnpj(EnumRepresentation):
    cpf = 1
    cnpj = 2
    nao_informado = 3


NFSE_PROCESS = {
    'processing': 'processing',
    'accepted': 'accepted',
    'rejected': 'rejected',
    'cancelled': 'cancelled'
}
