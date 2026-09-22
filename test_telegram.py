from notifiers.telegram_notifier import TelegramNotifier

def probar_alerta():
    notificador = TelegramNotifier()
    mensaje = (
        "🚀 <b>¡Alerta del Sistema ec-job-pipeline!</b>\n\n"
        "El módulo de notificaciones se ha conectado con éxito.\n"
        "A partir de ahora, las vacantes de Quito llegarán por esta vía."
    )
    
    print("Enviando mensaje de prueba a Telegram...")
    exito = notificador.send_message(mensaje)
    
    if exito:
        print("✅ ¡Mensaje entregado con éxito! Revisa tu aplicación de Telegram.")
    else:
        print("❌ No se pudo entregar el mensaje. Revisa tu token y chat_id.")

if __name__ == "__main__":
    probar_alerta()