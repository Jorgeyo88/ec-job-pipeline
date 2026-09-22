from typing import List, Dict
from jobspy import scrape_jobs

class JobScraper:
    """Extrae vacantes laborales multicanal filtradas para la ciudad de Quito."""

    def __init__(self, location: str = "Quito, Ecuador"):
        self.location = location

    def search_jobs(self, query: str, hours_old: int = 168, results_wanted: int = 10) -> List[Dict]:
        """
        Rastrea vacantes en LinkedIn y Google Jobs (que indexa Computrabajo,
        Multitrabajos y bolsas locales) con filtro estricto por ciudad.
        """
        print(f"\n🔎 Rastreador buscando: '{query}' en {self.location}...")

        try:
            raw_jobs = scrape_jobs(
                site_name=["linkedin", "google"],
                search_term=f"{query} Quito",
                location=self.location,
                results_wanted=results_wanted,
                hours_old=hours_old,
                country_indeed="ecuador"
            )

            if raw_jobs is None or raw_jobs.empty:
                print(f"ℹ️ No se hallaron ofertas recientes para: '{query}'")
                return []

            cleaned_jobs: List[Dict] = []

            for _, row in raw_jobs.iterrows():
                title = str(row.get("title", "")).strip()
                company = str(row.get("company", "Empresa no especificada")).strip()
                job_location = str(row.get("location", "")).strip()
                job_url = str(row.get("job_url", "")).strip()
                site = str(row.get("site", "Bolsa de empleo")).strip()

                if not job_url or not title or title.lower() == "nan":
                    continue

                final_location = job_location if job_location and job_location.lower() != "nan" else "Quito, Ecuador"

                cleaned_jobs.append({
                    "title": title,
                    "company": company,
                    "location": final_location,
                    "job_url": job_url,
                    "source": site.capitalize()
                })

            print(f"✅ Se encontraron {len(cleaned_jobs)} vacantes para '{query}'")
            return cleaned_jobs

        except Exception as error:
            print(f"⚠️ Error extrayendo ofertas para '{query}': {error}")
            return []