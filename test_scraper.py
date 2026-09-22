from scrapers.job_scraper import JobScraper

def probar_rastreador():
    # Inicializar el rastreador enfocado en Quito
    buscador = JobScraper(location="Quito, Ecuador")
    
    # Buscar ofertas de los últimos 7 días
    ofertas = buscador.search_jobs("Analista de datos", hours_old=168, results_wanted=5)
    
    print("\n--- OFERTAS ENCONTRADAS EN QUITO ---")
    if not ofertas:
        print("No se encontraron ofertas en esta consulta.")
        return

    for vacante in ofertas:
        titulo = vacante["title"]
        empresa = vacante["company"]
        fuente = vacante["source"]
        link = vacante["job_url"]
        
        print(f"📌 Puesto:  {titulo}")
        print(f"🏢 Empresa: {empresa}")
        print(f"🌐 Fuente:  {fuente}")
        print(f"🔗 Enlace:  {link}")
        print("-" * 50)

if __name__ == "__main__":
    probar_rastreador()