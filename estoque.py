from dados import produtos

def verificar_estoque(produto_id, quantidade):
    produto = produtos.get(produto_id)
    if produto and produto["estoque"] >= quantidade:
        return True
    return False