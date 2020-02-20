# -*- coding: utf-8 -*-
import locale

import pytz
from erpbrasil.base.fiscal import cnpj_cpf
import base64

from genshi import Markup
from reportlab.graphics.barcode import createBarcodeDrawing
from datetime import datetime
from dateutil.parser import parse


def formata_CNPJ(cnpj):
    return cnpj_cpf.formata(cnpj)


def formata_CPF(cpf):
    return cnpj_cpf.formata(cpf)


def formata_CEP(cep):
    if not len(cep.strip()):
        return ''

    return cep[0:5] + '-' + cep[5:8]


def formata_fone(fone):
    if not len(fone.strip()):
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
            numero  = numero[0] + ' ' + numero[1:4] + '-' + numero[4:]
        else:
            numero = numero[0:4] + '-' + numero[4:]
        ddd = fone[2:4]
        ddi = fone[:2]
        formatado = '+' + ddi + ' (' + ddd + ') ' + numero

    return formatado


def formata_modFrete(modFrete):
    modFrete = int(modFrete)
    if modFrete == 0:
        formatado = '0-Emitente'

    elif modFrete == 1:
        if modFrete == 0:
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
    if data is '':
        return ''
    else:
        return data.text[11:19]


def formata_decimal(numero, digitos):
    formato = '%.' + str(digitos) + 'f'

    return locale.format(formato, float(numero), grouping=True)


def formata_vBC(vBC):
    return formata_decimal(vBC, 2)


def formata_vICMS(vICMS):
    return formata_decimal(vICMS, 2)


def formata_vBCST(vBCST):
    return formata_decimal(vBCST, 2)


def formata_vST(vST):
    return formata_decimal(vST, 2)


def formata_vTotTrib(vTotTrib):
    return formata_decimal(vTotTrib, 2)


def formata_vProd(vProd):
    return formata_decimal(vProd, 2)


def formata_vFrete(vFrete):
    return formata_decimal(vFrete, 2)


def formata_vSeg(vSeg):
    return formata_decimal(vSeg, 2)


def formata_vDesc(vDesc):
    return formata_decimal(vDesc, 2)


def formata_vOutro(vOutro):
    return formata_decimal(vOutro, 2)


def formata_vIPI(vIPI):
    return formata_decimal(vIPI, 2)


def formata_vNF(vNF):
    return formata_decimal(vNF, 2)


def formata_qCom(qCom):
    return formata_decimal(qCom, 4)


def formata_vUnCom(vUmCom):
    return formata_decimal(vUmCom, 4)


def formata_vProd(vProd):
    return formata_decimal(vProd, 2)


def formata_vBC(vBC):
    return formata_decimal(vBC, 2)


def formata_vIPI(vIPI):
    return formata_decimal(vIPI, 2)


def formata_pIPI(pIPI):
    return formata_decimal(pIPI, 2)

##
# -----------------------------------------------------------------------------
##


def endereco_emitente_formatado(NFe):
    formatado = str(NFe.infNFe.emit.enderEmit.xLgr)
    formatado += ', ' + str(NFe.infNFe.emit.enderEmit.nro)

    if hasattr(NFe.infNFe.emit.enderEmit, 'xCpl') and \
        len(str(NFe.infNFe.emit.enderEmit.xCpl).strip()):
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
    formatado += ' - ' + NFe.infNFe.emit.enderEmit.CEP
    return formatado


def endereco_emitente_formatado_linha_3(NFe):
    if formata_fone(NFe.infNFe.emit.enderEmit.fone).strip() != '':
        formatado = 'Fone: ' + NFe.infNFe.emit.enderEmit.fone
    else:
        formatado = ''
    return formatado


def endereco_emitente_formatado_linha_4(NFe):
    #return NFe.site or NFe.infNFe.emit.email.valor or '' # TODO: De onde vem o site
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
    chave = chave.replace('.', '').replace('-','').replace('/','')
    chave_formatada = ' '.join((chave[0:4], chave[4:8], chave[8:12], chave[12:16], chave[16:20], chave[20:24], chave[24:28], chave[28:32], chave[32:36], chave[36:40], chave[40:44]))
    return chave_formatada


def chave_imagem(NFe):
    chave = monta_chave(NFe)
    chave = chave = chave.replace('.', '').replace('-','').replace('/','')
    #
    # Para converter centímetros para o tamanho do reportlab, use a
    # seguinte fórmula:
    # cm × 128 ÷ 2,75
    #
    # Assim: 0,8 cm = 0,8 × 128 ÷ 2,75 = 37,2 = 37
    # Assim: 0,02 cm = 0,02 × 128 ÷ 2,75 = 0,9 = 1
    #
    imagem = createBarcodeDrawing('Code128', value= chave,
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
         (datetime.strptime(str(NFe.infNFe.cobr.dup[0].dVenc), '%Y-%m-%d').toordinal() > datetime.strptime(str(NFe.infNFe.ide.dEmi.toordinal()), '%Y-%m-%d').toordinal()))):
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


def cst_formatado(det):
    formatado = str(det.imposto.ICMS.ICMSSN102.orig).zfill(1)
    formatado += str(det.imposto.IPI.IPITrib.CST).zfill(2)
    return formatado


def crt_descricao(NFe):
    return ''


def versao(NFe):
    return NFe.infNFe.attrib['versao']


def formata_hora(hora):
    return hora[11:19]


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
