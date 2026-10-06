from erpbrasil.edoc.pdf.danfe_formata import formata_decimal, formata_duas_casas, formata_tres_casas


def test_formata_decimal_separadores_brasileiros():
    assert formata_decimal("1234567.891", 2) == "1.234.567,89"
    assert formata_decimal(0, 2) == "0,00"
    assert formata_decimal("999.5", 0) == "1.000"
    assert formata_duas_casas("12.5") == "12,50"
    assert formata_tres_casas(1.0005) == "1,001"
