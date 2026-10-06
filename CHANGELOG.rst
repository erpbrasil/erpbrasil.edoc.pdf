
Changelog
=========

0.0.0 (2020-02-20)
------------------

* First release on PyPI.


1.0.0 (2021-05-05)
------------------

* Correção dos imports da biblioteca;
* NF-e Danfe c/ Volumes;


1.3.0 (não publicada)
---------------------

* Biblioteca sem suporte: o README recomenda a migração para a BrazilFiscalReport.
  Esta versão existe para que quem ainda a usa (Odoo 12.0 e 14.0) não quebre o
  namespace das outras libs erpbrasil.
* Empacotamento: ``pyproject.toml`` com hatchling; o pacote vira "portion" PEP 420
  dos namespaces ``erpbrasil`` e ``erpbrasil.edoc`` (não leva mais os
  ``__init__`` de namespace, que apagavam o ``__version__`` da ``erpbrasil.edoc``);
  Python 3.6 a 3.14 declarado e testado no CI; publicação por Trusted Publishing
  com conferência da tag.
* ``sh`` deixa de ser dependência: o LibreOffice é chamado por ``subprocess``,
  procurado como ``libreoffice`` ou ``soffice`` no PATH ou pela variável
  ``ERPBRASIL_LIBREOFFICE``, com erro claro quando não existe (antes falhava em
  silêncio, issue #13).
* Testes independentes do diretório de execução e pulados sem LibreOffice.
* ``reportlab`` fica em ``<4`` até o Python 3.10 (wheel com o renderPM embutido,
  como o Odoo 14 usa); em 3.11+ entra o ``reportlab`` 4 com ``rlPyCairo``, que
  precisa da ``libcairo`` do sistema.
\n
