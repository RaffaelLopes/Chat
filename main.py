# Importação do framework Flet, utilizado para criar interfaces gráficas
import flet as ft 

def main(pagina):
    # Criação de um objeto de texto
    texto = ft.Text("AwesomeChat")

    # Criação de uma coluna para exibir mensagens do chat
    chat = ft.Column()

    # Campo de entrada para o nome do usuário
    nome_usuario = ft.TextField(label="Escreva seu nome")

    def enviar_mensagem_tunel(mensagem):
        # Verifica o tipo de mensagem recebida e atualiza o chat
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"))
        else:
            usuario_mensagem = mensagem["usuario"]
            # Adiciona uma mensagem especial quando um usuário entra no chat
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat", size=22, italic=True, color=ft.colors.ORANGE_ACCENT))
        
        # Atualiza a página para refletir as mudanças no chat
        pagina.update()

    # Inscreve a função de envio de mensagem no sistema de publicação e subscrição
    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def enviar_mensagem(evento):
        # Envia a mensagem digitada para todos os usuários no chat
        pagina.pubsub.send_all({"texto":campo_mensagem.value, "usuario": nome_usuario.value, "tipo":"mensagem"})

        # Limpa o campo de mensagem após o envio
        campo_mensagem.value = ""
        # Atualiza a página para refletir as mudanças no chat
        pagina.update()

    # Campo de entrada para digitar mensagens
    campo_mensagem = ft.TextField(label="Digite uma mensagem")
    # Botão para enviar mensagens
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)

    def entrar_popup(evento):
        # Envia uma mensagem indicando a entrada do usuário no chat
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})

        # Adiciona a coluna do chat à página e configurações adicionais
        pagina.add(chat)
        popup.open = False
        pagina.remove(botao_iniciar)
        pagina.remove(texto)
        pagina.add(ft.Row([campo_mensagem, botao_enviar_mensagem]))
        pagina.add(botao_enviar_mensagem)
        # Atualiza a página para refletir as mudanças
        pagina.update()

    # Configuração do popup para entrada do nome do usuário
    popup = ft.AlertDialog(
        open = False,
        modal = True,
        title = ft.Text("Bem vindo ao CrazyHorseZap"),
        content = nome_usuario,
        actions = [ft.ElevatedButton("Entrar", on_click=entrar_popup)],
    )

    def entrar_chat(evento):
        # Configuração do diálogo para entrada do nome do usuário
        pagina.dialog = popup
        popup.open = True
        # Atualiza a página para refletir as mudanças
        pagina.update()

    # Botão para iniciar o chat
    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)

    # Adiciona o texto inicial e o botão de iniciar à página
    pagina.add(texto)
    pagina.add(botao_iniciar)

# Inicia a aplicação utilizando o navegador da web como interface
ft.app(target=main, view=ft.WEB_BROWSER)
