from dados import produtos, pedidos
from estoque import verificar_estoque
from logger import logger


def calcular_total(preco_unitario, quantidade, desconto=0):
    if preco_unitario < 0 or quantidade <= 0:
        logger.error("Parâmetros inválidos para cálculo de total.")
        raise ValueError("Preço e quantidade devem ser positivos.")
    
    total_bruto = preco_unitario * quantidade
    total_final = total_bruto * (1 - desconto)
    
    logger.info(f"Total calculado: {total_final:.2f}")
    return total_final

def processar_pedido(pedido_id, produto_id, quantidade, preco_unitario, desconto=0):
    logger.info(f"Processando pedido {pedido_id}: {quantidade} unidades de '{produto_id}'.")

    if not verificar_estoque(produto_id, quantidade):
        logger.warning(f"Estoque insuficiente para '{produto_id}'.")
        raise RuntimeError("Estoque insuficiente.")
    
    total = calcular_total(preco_unitario, quantidade, desconto)
    pedidos[pedido_id] = {
        "produto_id": produto_id,
        "quantidade": quantidade,
        "total": total,
        "status": "em processamento"
    }
    logger.info(f"Pedido {pedido_id} processado com sucesso. Total: R${total:.2f}")
    return total

def cadastrar_produto(produto_id, nome, preco, estoque):
    try:
        if produto_id in produtos:
            raise ValueError("Produto já cadastrado.")
        produtos[produto_id] = {
            "nome": nome,
            "preco": preco,
            "estoque": estoque
        }
        logger.info(f"Produto {nome} cadastrado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao cadastrar produto {nome}: {e}")
        raise

def finalizar_pedido(pedido_id):
    try:
        if pedido_id not in pedidos:
            raise ValueError("Pedido não encontrado.")
        pedidos[pedido_id]["status"] = "finalizado"
        logger.info(f"Pedido {pedido_id} finalizado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao finalizar pedido {pedido_id}: {e}")
        raise