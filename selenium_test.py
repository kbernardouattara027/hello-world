from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

url = "https://quotes.toscrape.com"

# Selenium Manager trouve ou télécharge automatiquement le bon ChromeDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

citations = []

try:
    driver.get(url)
    print("super tout roule")

    page = 1
    while True:
        # Attendre que les citations soient chargées
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))

        # Récupérer chaque citation de la page
        for bloc in driver.find_elements(By.CLASS_NAME, "quote"):
            texte = bloc.find_element(By.CLASS_NAME, "text").text
            auteur = bloc.find_element(By.CLASS_NAME, "author").text
            tags = [t.text for t in bloc.find_elements(By.CLASS_NAME, "tag")]
            citations.append({"texte": texte, "auteur": auteur, "tags": tags})

        print(f"Page {page} : {len(citations)} citations au total")

        # Passer à la page suivante s'il y en a une
        suivant = driver.find_elements(By.CSS_SELECTOR, "li.next a")
        if not suivant:
            break
        suivant[0].click()
        page += 1

    # Afficher les résultats
    for c in citations:
        print(f"\n{c['texte']}\n  — {c['auteur']} | tags : {', '.join(c['tags'])}")

    # Enregistrer les citations dans un fichier CSV
    with open("citations.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["texte", "auteur", "tags"])
        writer.writeheader()
        for c in citations:
            writer.writerow({**c, "tags": ", ".join(c["tags"])})
    print("\nFichier citations.csv créé.")

    print(f"Scraping terminé : {len(citations)} citations récupérées.")

except Exception as e:
    print("Une erreur est survenue : ", e)

finally:
    # Fermer le navigateur, même en cas d'erreur
    driver.quit()
    print("Le navigateur s'est fermé correctement")
