from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(title="API Parrainage")

# --- CONFIGURATION CORS (Crucial pour Lovable) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En production, on mettrait l'URL exacte de Lovable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def calculer_matches():
    df = pd.read_csv("base_etudiants.csv")
    filleuls = df[df['filleul'] == True].to_dict('records')
    parrains = df[df['filleul'] == False].to_dict('records')
    
    paires = []
    
    for filleul in filleuls:
        meilleur_parrain = None
        meilleur_score = -1
        
        for parrain in parrains:
            score = 0
            if filleul['filière'] == parrain['filière']: score += 10
            if parrain['niveau'] > filleul['niveau']: score += 5
            if filleul['nationalité'] == parrain['nationalité']: score += 3
            
            if score > meilleur_score:
                meilleur_score = score
                meilleur_parrain = parrain
                
        if meilleur_parrain:
            paires.append({
                "filleul_nom": f"{filleul['prenom']} {filleul['nom']}",
                "filleul_filiere": filleul['filière'],
                "parrain_nom": f"{meilleur_parrain['prenom']} {meilleur_parrain['nom']}",
                "parrain_filiere": meilleur_parrain['filière']
            })
            parrains.remove(meilleur_parrain)
            
    return paires

@app.get("/api/matches")
def get_matches():
    try:
        resultats = calculer_matches()
        return {"status": "success", "data": resultats}
    except Exception as e:
        return {"status": "error", "message": str(e)}