import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import streamlit.components.v1 as components
import altair as alt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Sobry TURPE CU4", page_icon="⚡", layout="centered")

# --- TIME ---
tz = ZoneInfo("Europe/Paris")
maintenant = datetime.now(tz)
date_aujourdhui = maintenant.strftime("%Y-%m-%d")
date_demain = (maintenant + timedelta(days=1)).strftime("%Y-%m-%d")

# --- FUNCTION ---
def charger_donnees(date_str):
    chemin_fichier = os.path.join("data", f"tarifs_{date_str}.json")
    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, "r") as fichier:
            contenu = json.load(fichier)
            return contenu.get('prices') or contenu.get('data')
    return None

def calculer_moyenne_hebdo():
    tous_les_prix = []
    for i in range(1, 8):
        date_passee = (maintenant - timedelta(days=i)).strftime("%Y-%m-%d")
        donnees_jour = charger_donnees(date_passee)
        if donnees_jour:
            tous_les_prix.extend([p['price_ttc_eur_kwh'] * 100 for p in donnees_jour])
    return sum(tous_les_prix) / len(tous_les_prix) if tous_les_prix else None

def obtenir_couleurs(prix):
    if prix < 12.0: return "#1B5E20", "white"
    if prix < 15.79: return "#4CAF50", "white"
    if prix < 18.22: return "#FBC02D", "black"
    if prix < 20.65: return "#F57C00", "white"
    return "#D32F2F", "white"

def formater_dataframe(liste_prix, granularite):
    df = pd.DataFrame(liste_prix)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['prix_c'] = df['price_ttc_eur_kwh'] * 100
    
    if "1 heure" in granularite:
        df = df.resample('1h', on='timestamp').mean().reset_index()
        
    df['heure_str'] = df['timestamp'].dt.strftime("%H:%M")
    df['couleur_fond'] = df['prix_c'].apply(lambda x: obtenir_couleurs(x)[0])
    df['couleur_texte'] = df['prix_c'].apply(lambda x: obtenir_couleurs(x)[1])
    return df

def creer_bandeau_defilant(df, granularite, est_aujourdhui=True):
    if "1 heure" in granularite:
        heure_actuelle_str = maintenant.strftime("%H:00")
    else:
        minute_arrondie = (maintenant.minute // 15) * 15
        heure_actuelle_str = maintenant.replace(minute=minute_arrondie).strftime("%H:%M")

    cases_html = ""
    for _, ligne in df.iterrows():
        heure_case = ligne['heure_str']
        valeur_prix = ligne['prix_c']
        couleur_fond = ligne['couleur_fond']
        couleur_texte = ligne['couleur_texte']
        
        est_heure_actuelle = (heure_case == heure_actuelle_str)
        
        bordure = "3px solid #000" if (est_heure_actuelle and est_aujourdhui) else "1px solid transparent"
        
        id_balise = 'id="case-actuelle"' if est_heure_actuelle else ""
        
        cases_html += f"""
        <div {id_balise} style="display:inline-block; min-width:80px; padding:10px; margin:5px; border-radius:10px; background-color:{couleur_fond}; color:{couleur_texte}; border:{bordure}; text-align:center; font-family:sans-serif;">
            <div style="font-size:0.8em; opacity:0.9;">{heure_case}</div>
            <div style="font-weight:bold; font-size:1.1em;">{valeur_prix:.1f}</div>
        </div>
        """
        
    code_complet = f"""
    <div style="overflow-x: auto; white-space: nowrap; padding-bottom:10px; scroll-behavior: smooth;">
        {cases_html}
    </div>
    <script>
        const caseActuelle = document.getElementById('case-actuelle');
        if (caseActuelle) {{
            caseActuelle.scrollIntoView({{ behavior: 'smooth', inline: 'center', block: 'nearest' }});
        }}
    </script>
    """
    components.html(code_complet, height=100)

def afficher_graphique_barres(df):
    graphique = alt.Chart(df).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X('heure_str:N', title=None, axis=alt.Axis(labelAngle=-90)),
        y=alt.Y('prix_c:Q', title='c€ / kWh'),
        color=alt.Color('couleur_fond:N', scale=None), 
        tooltip=[
            alt.Tooltip('heure_str:N', title='Heure'),
            alt.Tooltip('prix_c:Q', title='Prix', format='.2f')
        ]
    ).properties(height=300)
    st.altair_chart(graphique, use_container_width=True)


# --- INITAL LOAD ---
prix_aujourdhui = charger_donnees(date_aujourdhui)
prix_demain = charger_donnees(date_demain)
moyenne_semaine = calculer_moyenne_hebdo()

# --- USER INTERFACE ---
st.title("⚡ Tarif Sobry TURPE CU4 TTC")
st.caption("ℹ️ Les prix affichés incluent le Tarif Spot France + TURPE (CU4) + Toutes Taxes Comprises (TTC).")

# AVERAGE
col1, col2, col3 = st.columns(3)
if prix_aujourdhui:
    moyenne_j = sum([p['price_ttc_eur_kwh'] * 100 for p in prix_aujourdhui]) / len(prix_aujourdhui)
    col1.metric("Moy. Aujourd'hui", f"{moyenne_j:.2f} c€")
if prix_demain:
    moyenne_j1 = sum([p['price_ttc_eur_kwh'] * 100 for p in prix_demain]) / len(prix_demain)
    col2.metric("Moy. Demain", f"{moyenne_j1:.2f} c€")
if moyenne_semaine:
    col3.metric("Moy. 7 Jours", f"{moyenne_semaine:.2f} c€")

st.divider()

# GRANULARITY SELECTOR
choix_affichage = st.radio("Affichage des graphiques et bandeaux :", ["15 minutes", "1 heure"], horizontal=True)

# TODAY
if prix_aujourdhui:
    df_aujourdhui = formater_dataframe(prix_aujourdhui, choix_affichage)
    
    index_actuel = 0
    for i, p in enumerate(prix_aujourdhui):
        dt = datetime.fromisoformat(p['timestamp'])
        if dt.hour == maintenant.hour and dt.minute <= maintenant.minute < dt.minute + 15:
            index_actuel = i
            break
            
    valeur_actuelle = prix_aujourdhui[index_actuel]['price_ttc_eur_kwh'] * 100
    fond_actuel, texte_actuel = obtenir_couleurs(valeur_actuelle)
    
    st.markdown(f'<div style="background-color:{fond_actuel}; padding:20px; border-radius:15px; text-align:center; margin-bottom: 20px;"><h3 style="color:{texte_actuel}; margin:0; font-weight:normal;">Prix Actuel</h3><h1 style="color:{texte_actuel}; margin:0; font-size: 3em;">{valeur_actuelle:.2f} c€/kWh</h1></div>', unsafe_allow_html=True)

    st.subheader(f"La journée ({choix_affichage})")
    creer_bandeau_defilant(df_aujourdhui, choix_affichage, est_aujourdhui=True)

    st.subheader("Graphique d'aujourd'hui")
    afficher_graphique_barres(df_aujourdhui)

else:
    st.warning("⚠️ Les données d'aujourd'hui ne sont pas disponibles.")

st.divider()

# TOMORROW
if prix_demain:
    st.subheader(f"Demain ({date_demain})")
    
    df_demain = formater_dataframe(prix_demain, choix_affichage)
    
    creer_bandeau_defilant(df_demain, choix_affichage, est_aujourdhui=False)
    
    st.subheader("Graphique de demain")
    afficher_graphique_barres(df_demain)
else:
    st.info("🕒 Les tarifs de demain seront disponibles après 13h10.")

# --- FOOTER ---
st.write("")
st.divider()

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">', unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align: center; color: grey; font-size: 0.85em; line-height: 2em;">
        Une app de <b>Juste Une Dev</b><br>
        <a href="https://github.com/justeundev/" target="_blank" style="color: grey; text-decoration: none; margin-right: 15px;">
            <i class="fab fa-github"></i> GitHub
        </a>
        <a href="https://justeunedev.arniael.eu" style="color: grey; text-decoration: none;">
            <i class="fa-solid fa-envelope"></i> Contact
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
