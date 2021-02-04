# -*- coding: utf-8 -*-
import base64
import locale
from datetime import datetime

import pytz
from dateutil.parser import parse
from erpbrasil.base.fiscal.cnpj_cpf import formata as formata_CNPJ
from erpbrasil.base.fiscal.cnpj_cpf import formata as formata_CPF
from erpbrasil.base.misc import format_zipcode
from genshi import Markup
from reportlab.graphics.barcode import createBarcodeDrawing


def formata_decimal(numero, digitos):
    numero = float(numero)

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    formato = '%.' + str(digitos) + 'f'
    return locale.format(formato, numero, grouping=True)


def formata_duas_casas(valor):
    return formata_decimal(valor, 2)


def formata_tres_casas(valor):
    return formata_decimal(valor, 3)


def formata_cinco_casas(valor):
    return formata_decimal(valor, 5)


formata_vBC = formata_duas_casas
formata_vICMS = formata_duas_casas
formata_vBCST = formata_duas_casas
formata_vST = formata_duas_casas
formata_vTotTrib = formata_duas_casas
formata_vProd = formata_duas_casas
formata_vFrete = formata_duas_casas
formata_vSeg = formata_duas_casas
formata_vDesc = formata_duas_casas
formata_vOutro = formata_duas_casas
formata_vIPI = formata_duas_casas
formata_vNF = formata_duas_casas
formata_qCom = formata_tres_casas
formata_vUnCom = formata_cinco_casas
formata_vProd = formata_duas_casas
formata_pIPI = formata_duas_casas
formata_vOrig = formata_duas_casas
formata_vDesc = formata_duas_casas
formata_vLiq = formata_duas_casas
formata_vDup = formata_duas_casas
formata_pesoB = formata_duas_casas
formata_pesoL = formata_duas_casas
formata_pICMS = formata_duas_casas


def formata_fone(fone):
    if not fone or not len(fone.strip()):
        return ''

    if fone.strip() == '0':
        return ''

    if len(fone) <= 8:
        formatado = fone[:-4] + '-' + fone[-4:]
    elif len(fone) <= 10:
        ddd = fone[0:2]
        fone = fone[2:]
        formatado = '(' + ddd + ') ' + fone[:-4] + '-' + fone[-4:]

    elif len(fone) <= 11:
        ddd = fone[0:3]
        fone = fone[3:]
        formatado = '(' + ddd + ') ' + fone[-9:-6] + '-' + fone[-6:-4] + '-' + fone[-4:]

    #
    # Assume 8 dígitos para o número, 2 para o DD, e o restante é o DDI
    #
    else:
        numero = fone[4:]
        if len(numero) == 9:
            numero = numero[0] + ' ' + numero[1:4] + '-' + numero[4:]
        else:
            numero = numero[0:4] + '-' + numero[4:]
        ddd = fone[2:4]
        ddi = fone[:2]
        formatado = '+' + ddi + ' (' + ddd + ') ' + numero

    return formatado


def modFrete_formatado(NFe):
    modFrete = int(NFe.infNFe.transp.modFrete.text)

    if modFrete == 0:
        formatado = '0-Emitente'

    elif modFrete == 1:
        if int(NFe.infNFe.ide.tpNF.text) == 0:
            formatado = '1-do Remetente'
        else:
            formatado = '1-do Destinatário'

    elif modFrete == 2:
        formatado = '2-de Terceiros'

    elif modFrete == 9:
        formatado = '9-sem frete'

    else:
        formatado = ''

    return formatado


def formata_placa(placa):
    placa = placa[:-4] + '-' + placa[-4:]
    return placa


def formata_dhRecbto(dhRecbto):
    dhRecbto = str(dhRecbto)
    if dhRecbto is None:
        return ''
    else:
        dhRecbto = parse(dhRecbto)
        brasilia = pytz.timezone('America/Sao_Paulo')
        dhRecbto = brasilia.normalize(dhRecbto.astimezone(pytz.utc)).strftime(
            '%d/%m/%Y %H:%M:%S')
        #
        # Troca as siglas:
        # BRT - Brasília Time -> HOB - Horário Oficial de Brasília
        # BRST - Brasília Summer Time -> HVOB - Horário de Verão Oficial de Brasília
        # AMT - Amazon Time -> HOA - Horário Oficial da Amazônia
        # AMST - Amazon Summer Time -> HVOA - Horário de Verão Oficial da Amazônia
        # FNT - Fernando de Noronha Time -> HOFN - Horário Oficial de Fernando de Noronha
        #
        dhRecbto = dhRecbto.replace('(-0100)', '(-01:00)')
        dhRecbto = dhRecbto.replace('(-0200)', '(-02:00)')
        dhRecbto = dhRecbto.replace('(-0300)', '(-03:00)')
        dhRecbto = dhRecbto.replace('(-0400)', '(-04:00)')
        dhRecbto = dhRecbto.replace('BRT', 'HOB')
        dhRecbto = dhRecbto.replace('BRST', 'HVOB')
        dhRecbto = dhRecbto.replace('AMT', 'HOA')
        dhRecbto = dhRecbto.replace('AMST', 'HVOA')
        dhRecbto = dhRecbto.replace('FNT', 'HOFN')
        return dhRecbto


def formata_hora(data):
    return data[11:19]


def formata_dVenc(dVenc):
    dVenc = datetime.strptime(str(dVenc), '%Y-%m-%d')
    return dVenc.strftime("%d/%m/%Y")

##
# -----------------------------------------------------------------------------
##


def endereco_emitente_formatado(NFe):
    formatado = str(NFe.infNFe.emit.enderEmit.xLgr)
    formatado += ', ' + str(NFe.infNFe.emit.enderEmit.nro)

    if (hasattr(NFe.infNFe.emit.enderEmit, 'xCpl') and
            len(str(NFe.infNFe.emit.enderEmit.xCpl).strip())):
        formatado += ' - ' + str(NFe.infNFe.emit.enderEmit.xCpl)

    return formatado


def endereco_destinatario_formatado(NFe):
    formatado = str(NFe.infNFe.dest.enderDest.xLgr)
    formatado += ', ' + str(NFe.infNFe.dest.enderDest.nro)

    if hasattr(NFe.infNFe.dest.enderDest, 'xCpl'):
        formatado += ' - ' + str(NFe.infNFe.dest.enderDest.xCpl)

    return formatado


def endereco_retirada_formatado(NFe):
    if hasattr(NFe.infNFe, 'retirada'):
        formatado = NFe.infNFe.retirada.xLgr
        formatado += ', ' + NFe.infNFe.retirada.nro

        if len(NFe.infNFe.retirada.xCpl.strip()):
            formatado += ' - ' + NFe.infNFe.retirada.xCpl

        formatado += ' - ' + NFe.infNFe.retirada.xBairro
        formatado += ' - ' + NFe.infNFe.retirada.xMun
        formatado += '-' + NFe.infNFe.retirada.UF
        return formatado
    else:
        return ''


def endereco_entrega_formatado(NFe):
    if hasattr(NFe.infNFe, 'entrega'):
        formatado = str(NFe.infNFe.entrega.xLgr)
        formatado += ', ' + str(NFe.infNFe.entrega.nro)

        if len(str(NFe.infNFe.entrega.xCpl).strip()):
            formatado += ' - ' + str(NFe.infNFe.entrega.xCpl)

        formatado += ' - ' + str(NFe.infNFe.entrega.xBairro)
        formatado += ' - ' + str(NFe.infNFe.entrega.xMun)
        formatado += '-' + str(NFe.infNFe.entrega.UF)
        return formatado
    else:
        return ''


def endereco_emitente_formatado_linha_1(NFe):
    formatado = endereco_emitente_formatado(NFe)
    formatado += ' - ' + str(NFe.infNFe.emit.enderEmit.xBairro)
    return formatado


def endereco_emitente_formatado_linha_2(NFe):
    formatado = str(NFe.infNFe.emit.enderEmit.xMun)
    formatado += ' - ' + str(NFe.infNFe.emit.enderEmit.UF)
    formatado += ' - ' + format_zipcode(NFe.infNFe.emit.enderEmit.CEP, 'BR')
    return formatado


def endereco_emitente_formatado_linha_3(NFe):
    if formata_fone(NFe.infNFe.emit.enderEmit.fone).strip() != '':
        formatado = 'Fone: ' + NFe.infNFe.emit.enderEmit.fone
    else:
        formatado = ''
    return formatado


def endereco_emitente_formatado_linha_4(NFe):
    # return NFe.site or NFe.infNFe.emit.email.valor or '' # TODO: De onde vem o site
    if hasattr(NFe.infNFe.emit, 'email'):
        return str(NFe.infNFe.emit.email)
    else:
        return ''


def numero_formatado(NFe):
    num = str(NFe.infNFe.ide.nNF).zfill(9)
    num_formatado = '.'.join((num[0:3], num[3:6], num[6:9]))

    if str(NFe.infNFe.ide.mod) == '65':
        return 'nº ' + num_formatado
    elif str(NFe.infNFe.ide.mod) == '55':
        return 'Nº ' + num_formatado
    else:
        return num_formatado


def serie_formatada(NFe):
    if str(NFe.infNFe.ide.mod) == '65':
        return 'Série ' + str(NFe.infNFe.ide.serie).zfill(3)
    elif str(NFe.infNFe.ide.mod) == '55':
        return 'SÉRIE ' + str(NFe.infNFe.ide.serie).zfill(3)
    else:
        return str(NFe.infNFe.ide.serie).zfill(3)


def monta_chave(NFe):
    chave = str(NFe.infNFe.ide.cUF).strip().rjust(2, '0')
    chave += (str(NFe.infNFe.ide.dhEmi)[2:4] + str(NFe.infNFe.ide.dhEmi)[5:7]
              ).strip().rjust(4, '0')
    chave += str(NFe.infNFe.emit.CNPJ).strip().rjust(14, '0')
    chave += str(NFe.infNFe.ide.mod).zfill(2)
    chave += str(NFe.infNFe.ide.serie).strip().rjust(3, '0')
    chave += str(NFe.infNFe.ide.nNF).strip().rjust(9, '0')
    chave += str(NFe.infNFe.ide.tpEmis).strip().rjust(1, '0')
    chave += str(NFe.infNFe.ide.cNF).strip().rjust(8, '0')
    chave += str(NFe.infNFe.ide.cDV).strip().rjust(1, '0')
    return chave


def chave_formatada(NFe):
    chave = monta_chave(NFe)
    chave = chave.replace('.', '').replace('-', '').replace('/', '')
    chave_formatada = ' '.join((
        chave[0:4], chave[4:8], chave[8:12], chave[12:16], chave[16:20],
        chave[20:24], chave[24:28], chave[28:32], chave[32:36],
        chave[36:40], chave[40:44]))
    return chave_formatada


def chave_imagem(NFe):
    chave = monta_chave(NFe)
    chave = chave = chave.replace('.', '').replace('-', '').replace('/', '')
    #
    # Para converter centímetros para o tamanho do reportlab, use a
    # seguinte fórmula:
    # cm × 128 ÷ 2,75
    #
    # Assim: 0,8 cm = 0,8 × 128 ÷ 2,75 = 37,2 = 37
    # Assim: 0,02 cm = 0,02 × 128 ÷ 2,75 = 0,9 = 1
    #
    imagem = createBarcodeDrawing('Code128', value=chave,
                                  barHeight=37, barWidth=1)
    return base64.b64encode(imagem.asString('png')).decode('utf-8')


def cnpj_transportadora_formatado(NFe):
    try:
        return NFe.infNFe.transp.transporta.CPF
    except AttributeError:
        return NFe.infNFe.transp.transporta.CNPJ


def formata_protocolo(protNFe):
    if not hasattr(protNFe.infProt, 'nProt'):
        return ''

    formatado = str(protNFe.infProt.nProt)
    formatado += ' - '
    formatado += protNFe.infProt.dhRecbto
    return formatado


def dados_adicionais_libreoffice(NFe):
    da = ''

    if hasattr(NFe.infNFe, 'infAdic'):
        if hasattr(NFe.infNFe.infAdic, 'infAdFisco'):
            da = NFe.infNFe.infAdic.infAdFisco.text.replace('| ', '<text:line-break/>')

        if hasattr(NFe.infNFe.infAdic, 'infCpl'):
            if len(da) > 0:
                da += '<text:line-break/>'

            da += NFe.infNFe.infAdic.infCpl.text.replace('| ', '<text:line-break/>')

    return Markup(da)


def cnpj_destinatario_formatado(NFe):
    if hasattr(NFe.infNFe.dest, 'CPF'):
        return formata_CPF(NFe.infNFe.dest.CPF)
    elif hasattr(NFe.infNFe.dest, 'CNPJ'):
        return formata_CNPJ(NFe.infNFe.dest.CNPJ)
    elif hasattr(NFe.infNFe.dest, 'idEstrangeiro'):
        return NFe.infNFe.dest.idEstrangeiro
    else:
        return ''


def cnpj_emitente_formatado(NFe):
    if 'NFe.infNFe.emit.CPF' in locals() and len(NFe.infNFe.emit.CPF):
        return formata_CPF(str(NFe.infNFe.emit.CPF))
    else:
        return formata_CNPJ(str(NFe.infNFe.emit.CNPJ))


def fatura_a_prazo(NFe):
    if not (len(str(NFe.infNFe.cobr.fat.nFat)) or
            len(str(NFe.infNFe.cobr.fat.vOrig)) or
            len(str(NFe.infNFe.cobr.fat.vDesc)) or
            len(str(NFe.infNFe.cobr.fat.vLiq))):
        return False

    if (str(NFe.infNFe.ide.indPag) == '1' or
        len(str(NFe.infNFe.cobr.dup)) > 1 or
        ((len(str(NFe.infNFe.cobr.dup)) == 1) and
         (datetime.strptime(str(NFe.infNFe.cobr.dup[0].dVenc),
                            '%Y-%m-%d').toordinal() > datetime.strptime(
             str(NFe.infNFe.ide.dEmi.toordinal()),
             '%Y-%m-%d').toordinal()))):
        return True

    return False


def fatura_a_vista(NFe):
    if not (len(str(NFe.infNFe.cobr.fat.nFat)) or
            len(str(NFe.infNFe.cobr.fat.vOrig)) or
            len(str(NFe.infNFe.cobr.fat.vDesc)) or
            len(str(NFe.infNFe.cobr.fat.vLiq))):
        return False

    fatura = fatura_a_prazo(NFe)

    return not fatura


def numero_item(det):
    return int(det.attrib['nItem'])


def regime_tributario(NFe):
    return int(NFe.infNFe.emit.CRT.text)


def cst_formatado(det):
    formatado = str(det.imposto.ICMS.tipoICMS.orig).zfill(1)

    if hasattr(det.imposto, 'ISSQN'):
        if str(det.imposto.ISSQN.regime_tributario.text) == 1:
            formatado += '400'
        else:
            formatado += '41'

    elif det.imposto.ICMS.regime_tributario == 1:
        formatado += str(det.imposto.ICMS.tipoICMS.CSOSN).zfill(3)
    else:
        formatado += str(det.imposto.ICMS.tipoICMS.CST).zfill(2)

    return formatado


def crt_descricao(NFe):
    texto = 'Regime tributário: '

    if int(NFe.infNFe.emit.CRT.text) == 1:
        texto += 'SIMPLES Nacional'
    elif int(NFe.infNFe.emit.CRT.text) == 2:
        texto += 'SIMPLES Nacional - excesso de sublimite de receita bruta'
    else:
        texto += 'regime normal'

    return texto


def cst_descricao(NFe):
    if int(NFe.infNFe.emit.CRT.text) == 1:
        return 'CSOSN'
    else:
        return 'CST'


def versao(NFe):
    return NFe.infNFe.attrib['versao']


def informacoes_adicionais_formatadas(det):
    formatado = str(det.infAdProd).replace('|', '<text:line-break/>')
    return Markup(formatado)


def formata_data(data):
    if data == '':
        return ''
    else:
        return '{}/{}/{}'.format(data[8:10], data[5:7], data[0:4])


def dEmi(ide):
    return formata_data(str(ide.dhEmi))


def hEmi(ide):
    return formata_hora(str(ide.dhEmi))


def dSaiEnt(ide):
    return formata_data(str(ide.dhSaiEnt))


def hSaiEnt(ide):
    return formata_hora(str(ide.dhSaiEnt))


def base_icms(det):
    if str(det.imposto.ICMS.tipoICMS.CST) == '60':
        return formata_decimal(det.imposto.ICMS.tipoICMS.vBCSTRet.text, 2)
    return det.imposto.ICMS.tipoICMS.vBC


def valor_icms(det):
    if str(det.imposto.ICMS.tipoICMS.CST) == '60':
        return formata_decimal(det.imposto.ICMS.tipoICMS.vICMSSTRet.text, 2)
    return det.imposto.ICMS.tipoICMS.vICMS


def aliquota_icms(det):
    if str(det.imposto.ICMS.tipoICMS.CST) == '60':
        return formata_decimal(det.imposto.ICMS.tipoICMS.pST.text, 2)
    return det.imposto.ICMS.tipoICMS.pICMS
