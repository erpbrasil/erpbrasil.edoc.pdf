import os
import shutil

import pytest

from erpbrasil.edoc.pdf import base

AQUI = os.path.dirname(os.path.abspath(__file__))
PASTA_XML = os.path.join(AQUI, "xml")

tem_libreoffice = bool(
    os.environ.get("ERPBRASIL_LIBREOFFICE") or shutil.which("libreoffice") or shutil.which("soffice")
)


@pytest.mark.skipif(not tem_libreoffice, reason="LibreOffice nao encontrado")
@pytest.mark.parametrize("arquivo", sorted(os.listdir(PASTA_XML)))
def test_pdf_gen(arquivo, tmp_path):
    saida = str(tmp_path / arquivo.replace(".xml", ".pdf"))
    caminho = base.ImprimirXml.imprimir(caminho_xml=os.path.join(PASTA_XML, arquivo), output_dir=saida)
    assert os.path.getsize(caminho) > 1000
    with open(caminho, "rb") as pdf:
        assert pdf.read(5) == b"%PDF-"
