import os
import sys
import requests
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

# --- INIT ---
# .env LOAD
load_dotenv()

NTFY_URL = os.getenv("NTFY_URL").rstrip('/')
NTFY_USER = os.getenv("NTFY_USER")
NTFY_PASS = os.getenv("NTFY_PASS")

TOPIC_15MIN = os.getenv("NTFY_TOPIC_15MIN")
TOPIC_HOURLY = os.getenv("NTFY_TOPIC_HOURLY")
TOPIC_3H = os.getenv("NTFY_TOPIC_3H")
TOPIC_RECAPS = os.getenv("NTFY_TOPIC_RECAPS")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data/particular/cu4")

TZ = ZoneInfo("Europe/Paris")

# --- TOOLS FOR NOTIFICATIONS ---
def send_ntfy(topic, message, title, tags="zap,bulb", priority=3):
    if not topic:
        print("Erreur : Topic non défini dans le .env")
        return

    try:
        url = f"{NTFY_URL}/{topic}"
        response = requests.post(
            url,
            data=message.encode('utf-8'),
            auth=(NTFY_USER, NTFY_PASS),
            headers={
                "Title": title.encode('utf-8'),
                "Priority": str(priority),
                "Tags": tags
            },
            timeout=10
        )
        response.raise_for_status()
        print(f"✅ Notification envoyée sur {topic} : {title}")
    except Exception as e:
        print(f"❌ Erreur d'envoi ntfy sur {topic} : {e}")

def get_prices(date_obj):
    path = os.path.join(DATA_DIR, f"tarifs_{date_obj.strftime('%Y-%m-%d')}_cu4_particulier.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            d = json.load(f)
            return d.get('prices') or d.get('data', [])
    return []

def get_avg(prices, start_h, end_h):
    if not prices: return 0
    relevant = [p['price_ttc_eur_kwh'] * 100 for p in prices 
                if start_h <= datetime.fromisoformat(p['timestamp']).astimezone(TZ).hour < end_h]
    return sum(relevant) / len(relevant) if relevant else 0

# --- NOTIFICATION PART ---
if __name__ == "__main__":
    now = datetime.now(TZ)
    action = sys.argv[1] if len(sys.argv) > 1 else "none"

    prices_today = get_prices(now)
    prices_tomorrow = get_prices(now + timedelta(days=1))

    if not prices_today and action not in ["recap_demain"]:
        print("⚠️ Pas de données disponibles pour aujourd'hui.")
        sys.exit(0)

    # ==========================================
    # TOPIC 1 : QUARTERLY NOTIFICATION
    # ==========================================
    elif action == "quarterly":
        current_hour = now.hour
        current_minute = now.minute
        quarter_index = current_minute // 15
        
        current_prices = [p['price_ttc_eur_kwh'] * 100 for p in prices_today 
                          if datetime.fromisoformat(p['timestamp']).astimezone(TZ).hour == current_hour]
        
        if len(current_prices) >= 4:
            price_now = current_prices[quarter_index]
            
            if quarter_index < 3:
                price_next = current_prices[quarter_index + 1]
                label_next = f"{current_hour}h{(quarter_index + 1) * 15:02d}"
            else:
                next_hour = (now + timedelta(hours=1)).hour
                next_prices = [p['price_ttc_eur_kwh'] * 100 for p in prices_today 
                               if datetime.fromisoformat(p['timestamp']).astimezone(TZ).hour == next_hour]
                price_next = next_prices[0] if next_prices else None
                label_next = f"{next_hour}h00"

            msg = f"⏱️ Actuel : {price_now:.2f} c€/kWh"
            if price_next is not None:
                msg += f"\n⏭️ Prochain ({label_next}) : {price_next:.2f} c€/kWh"
            
            send_ntfy(TOPIC_15MIN, msg, f"Tarif {current_hour}h{quarter_index * 15:02d}", tags="timer_clock")

    # ==========================================
    # TOPIC 2 : HOURLY NOTIFICATION
    # ==========================================
    if action == "hourly":
        target_hour = (now + timedelta(hours=1)).hour
        next_prices = [p['price_ttc_eur_kwh'] * 100 for p in prices_today 
                       if datetime.fromisoformat(p['timestamp']).astimezone(TZ).hour == target_hour]
        
        if next_prices:
            msg = "\n".join([f"• {target_hour}h{i*15:02d} : {val:.2f} c€" for i, val in enumerate(next_prices)])
            send_ntfy(TOPIC_HOURLY, msg, f"Tarifs {target_hour}h - {target_hour+1}h", tags="hourglass")

    # ==========================================
    # TOPIC 3 : FUTURE 3 HOURS NOTIFICATION
    # ==========================================
    elif action == "3h" and prices_today:
        target_hour = (now + timedelta(hours=1)).hour
    
        h1 = get_avg(prices_today, target_hour, target_hour + 1)
        h2 = get_avg(prices_today, target_hour + 1, target_hour + 2)
        h3 = get_avg(prices_today, target_hour + 2, target_hour + 3)
    
        avg_3h = (h1 + h2 + h3) / 3
        
        msg = (
            f"Moyenne globale : {avg_3h:.2f} c€\n"
            f"{target_hour}h - {target_hour + 1}h : {h1:.2f} c€\n"
            f"{target_hour + 1}h - {target_hour + 2}h : {h2:.2f} c€\n"
            f"{target_hour + 2}h - {target_hour + 3}h : {h3:.2f} c€"
        )
    
        send_ntfy(TOPIC_3H, msg, f"Tarifs {target_hour}h - {target_hour + 3}h")

    # ==========================================
    # TOPIC 4 : GENERAL NOTIFICATION
    # ==========================================
    elif action == "recap_matin":
        moy_jour = get_avg(prices_today, 0, 24)
        moy_matin = get_avg(prices_today, 8, 13)
        msg = f"🌅 Moyenne de la journée : {moy_jour:.2f} c€\n☕ Moyenne Matinée (8h-13h) : {moy_matin:.2f} c€"
        send_ntfy(TOPIC_RECAPS, msg, "Récap Matin", tags="sunrise")

    elif action == "recap_midi":
        moy_aprem = get_avg(prices_today, 13, 18)
        send_ntfy(TOPIC_RECAPS, f"☀️ Moyenne Après-midi (13h-18h) : {moy_aprem:.2f} c€", "Récap Midi", tags="sun_with_face")

    elif action == "recap_demain":
        if prices_tomorrow:
            moy_jour_demain = get_avg(prices_tomorrow, 6, 22)
            
            nuit_matin = [p['price_ttc_eur_kwh'] * 100 for p in prices_tomorrow if datetime.fromisoformat(p['timestamp']).astimezone(TZ).hour < 6]
            nuit_soir = [p['price_ttc_eur_kwh'] * 100 for p in prices_tomorrow if datetime.fromisoformat(p['timestamp']).astimezone(TZ).hour >= 22]
            nuit_complete = nuit_matin + nuit_soir
            moy_nuit_demain = sum(nuit_complete) / len(nuit_complete) if nuit_complete else 0

            msg = f"📅 Moyenne Jour (06h-22h) : {moy_jour_demain:.2f} c€\n🌙 Moyenne Nuit (22h-06h) : {moy_nuit_demain:.2f} c€"
            send_ntfy(TOPIC_RECAPS, msg, "Prix de Demain Disponibles !", tags="calendar")
        else:
            print("⚠️ Les prix de demain ne sont pas encore téléchargés.")

    elif action == "recap_soir":
        moy_soir = get_avg(prices_today, 18, 22)
        send_ntfy(TOPIC_RECAPS, f"🌆 Moyenne Soirée (18h-22h) : {moy_soir:.2f} c€", "Récap Soir", tags="city_sunset")

    elif action == "recap_nuit":
        nuit_ce_soir = [p['price_ttc_eur_kwh'] * 100 for p in prices_today if datetime.fromisoformat(p['timestamp']).astimezone(TZ).hour >= 22] if prices_today else []
        nuit_demain_matin = [p['price_ttc_eur_kwh'] * 100 for p in prices_tomorrow if datetime.fromisoformat(p['timestamp']).astimezone(TZ).hour < 6] if prices_tomorrow else []
        
        nuit_totale = nuit_ce_soir + nuit_demain_matin
        moy_nuit = sum(nuit_totale) / len(nuit_totale) if nuit_totale else 0
        send_ntfy(TOPIC_RECAPS, f"🛌 Moyenne Nuit (22h-06h) : {moy_nuit:.2f} c€", "Récap Nuit", tags="crescent_moon")
        
    else:
        print(f"Action '{action}' non reconnue ou ignorée.")
