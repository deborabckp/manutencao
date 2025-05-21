import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import cadastrar_produto, finalizar_pedido, processar_pedido, produtos, pedidos

def test_cadastrar_produto_sucesso():
    cadastrar_produto("p1", "Produto 1", 10.0, 100)
    assert "p1" in produtos
    assert produtos["p1"]["nome"] == "Produto 1"

def test_cadastrar_produto_duplicado():
    cadastrar_produto("p2", "Produto 2", 15.0, 50)
    with pytest.raises(ValueError):
        cadastrar_produto("p2", "Produto 2", 15.0, 50)

def test_processar_pedido_sucesso():
    cadastrar_produto("p3", "Produto 3", 20.0, 100)
    total = processar_pedido("pedido1", "p3", 5, 20.0)
    assert total == 100.0
    assert pedidos["pedido1"]["status"] == "em processamento"

def test_processar_pedido_estoque_insuficiente():
    cadastrar_produto("p4", "Produto 4", 30.0, 2)
    with pytest.raises(RuntimeError):
        processar_pedido("pedido2", "p4", 5, 30.0)

def test_finalizar_pedido_sucesso():
    cadastrar_produto("p5", "Produto 5", 12.0, 20)
    processar_pedido("pedido3", "p5", 2, 12.0)
    finalizar_pedido("pedido3")
    assert pedidos["pedido3"]["status"] == "finalizado"

def test_finalizar_pedido_inexistente():
    with pytest.raises(ValueError):
        finalizar_pedido("pedido_inexistente")