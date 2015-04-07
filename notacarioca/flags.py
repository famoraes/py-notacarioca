# -*- coding: utf-8 -*-

RPS_SITUATION = (
    (1, 'Normal'),
    (2, 'Cancelado')
)

OPERATION_NATURE = (
    (1, 'Tributação no município'),
    (2, 'Tributação fora do município'),
    (3, 'Isenção'),
    (4, 'Imune'),
    (5, 'Exigibilidade suspensa por decisão judicial'),
    (6, 'Exigibilidade suspensa por procedimento Administrativo')
)

TAX_REGIME = (
    (1, "Microempresa Municipal"),
    (2, "Estimativa"),
    (3, "Sociedade Professional"),
    (4, "Cooperativa"),
    (5, 'MEI - Microempresário Individual'),
    (6, 'ME EPP - Microempresário e Empresa de Pequeno Porte')
)

RPS_TYPE = (
    (1, "RPS"),
    (2, "Nota Conjugada"),
    (3, "Cumpom")
)

NFSE_PROCESS = {
    'processing': 'processing',
    'accepted': 'accepted',
    'rejected': 'rejected',
    'cancelled': 'cancelled'
}
