import warnings
# 1. Silenciar advertencias matemáticas internas para tener una consola limpia
warnings.filterwarnings("ignore")

import time
from scrapers.job_scraper import JobScraper
from database.db_manager import DatabaseManager
from notifiers.telegram_notifier import TelegramNotifier

# Perfiles profesionales a rastrear en Quito
TARGET_ROLES = [
    "Analista de datos",
    "Auditor de TI",
    "Analista de sistemas",
    "Docente informática"
]

def format_telegram_alert(job: dict) -> str:
    """Diseña la tarjeta de presentación con formato HTML para Telegram."""
    return (
        f"💼 <b>Nueva Vacante Detectada</b>\n\n"
        f"📌 <b>Puesto:</b> {job['title']}\n"
        f"🏢 <b>Empresa:</b> {job['company']}\n"
        f"📍 <b>Ubicación:</b> {job['location']}\n"
        f"🌐 <b>Portal:</b> {job['source']}\n\n"
        f"🔗 <a href='{job['job_url']}'>Postularme a la oferta</a>"
    )

def run_pipeline():
    print("=" * 60)
    print("🚀 INICIANDO PIPELINE DE VACANTES - QUITO, ECUADOR")
    print("=" * 60)

    # Inicializar base de datos, buscador y notificador
    db = DatabaseManager(db_path="jobs_tracker.db")
    scraper = JobScraper(location="Quito, Ecuador")
    notifier = TelegramNotifier()

    total_nuevas = 0

    for role in TARGET_ROLES:
        # Busca vacantes de las últimas 72 horas
        jobs = scraper.search_jobs(query=role, hours_old=72, results_wanted=5)

        for job in jobs:
            job_hash = db.generate_hash(
                title=job["title"],
                company=job["company"],
                job_url=job["job_url"]
            )

            if db.is_new_job(job_hash):
                mensaje = format_telegram_alert(job)
                enviado = notifier.send_message(mensaje)

                if enviado:
                    db.save_job(
                        job_hash=job_hash,
                        title=job["title"],
                        company=job["company"],
                        location=job["location"],
                        source=job["source"],
                        job_url=job["job_url"]
                    )
                    total_nuevas += 1
                    print(f"  ✉️ Alerta enviada: {job['title']} en {job['company']}")
                    time.sleep(1.5)  # Pausa preventiva para no saturar la API
            else:
                print(f"  ⏭️ Vacante omitida (ya registrada): {job['title']}")

    print("\n" + "=" * 60)
    print(f"🏁 PIPELINE FINALIZADO. Total nuevas enviadas: {total_nuevas}")
    print("=" * 60)

if __name__ == "__main__":
    print("\n⚡ Encendiendo el motor...")
    run_pipeline()