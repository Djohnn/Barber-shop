from rolepermissions.roles import AbstractUserRole


class Gerente(AbstractUserRole):
    available_permissions = {
        'cadastrar_produtos': True,
        'liberar_desconto': True,
        'cadastrar_vendedor': True,
        
    }

class Vendedor(AbstractUserRole):
    available_permissions = {
        'realizar_vendas': True
        
    }

class Caixa(AbstractUserRole):
    available_permissions = {
        'visualir_comissão': True,
        'visualizar_serviço_realizado': True,
        'acessar_agendamentos': True,
        'finalizar_venda': True,
        'add_produto_agendamento': True,
    }

class Caixa(AbstractUserRole):
    available_permissions = {
        'dashbord': True,
        'comissão': True,
        'servico_realizado': True,
    }
