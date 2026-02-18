import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_menu():
    url = "https://bais.bilkent.edu.tr/menu/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error fetching menu: {e}"

    soup = BeautifulSoup(response.content, 'html.parser')
    
    today_date = datetime.now()
    today_str = today_date.strftime("%d.%m.%Y")
    today_id = today_date.strftime("%Y-%m-%d") # Format for HTML ID: day-2026-02-17-tab-pane
    
    # Check if today is weekend (Saturday=5, Sunday=6)
    # The menu might exist for weekends, but often not.
    # The website shows tabs for the week.
    
    target_pane = soup.find('div', id=f"day-{today_id}-tab-pane")
    
    if not target_pane:
        return f"⚠️ {today_str} tarihi için menü bulunamadı. (Haftasonu olabilir mi?)"

    message = f"📅 *Bilkent Yemekhane Menüsü ({today_str})*\n\n"
    
    menu_types = {
        "Öğle Yemeği (Fiks)": "Tabildot Fiks Menü - Öğlen",
        "Akşam Yemeği (Fiks)": "Tabildot Fiks Menü - Akşam",
        "Seçmeli Menü": "Tabildot Seçmeli Menü"
    }

    found_any = False

    for title, search_text in menu_types.items():
        # Search ONLY within the target pane for today
        header = target_pane.find(lambda tag: tag.name == "h5" and search_text in tag.get_text())
        
        if header:
            found_any = True
            message += f"🛑 *{title}*\n"
            
            card = header.find_parent('div', class_='card')
            if card:
                card_body = card.find('div', class_='card-body')
                if card_body:
                    # Remove nutrition box if it exists
                    nutrition_box = card_body.find('div', class_='nutrition-box')
                    if nutrition_box:
                        nutrition_box.decompose()
                    
                    text_content = card_body.get_text(separator='\n')
                    raw_lines = [line.strip() for line in text_content.split('\n') if line.strip()]
                    
                    seen = set()
                    for line in raw_lines:
                        # Filter unwanted text
                        if "12:00" in line or "17:00" in line or "Verilen enerji" in line or "Sadece ana" in line or "Toplam Enerji" in line:
                            continue
                            
                        # Filter out calories/macros just in case they slipped through
                        if "Enerji" in line or "Karbonhidrat" in line:
                            continue

                        if line not in seen:
                            message += f"• {line}\n"
                            seen.add(line)
            
            message += "\n"
        else:
            message += f"⚠️ *{title}* bulunamadı.\n\n"

    if not found_any:
        return "⚠️ Menü verisi çekilemedi. Web sitesi yapısı değişmiş olabilir."
        
    message += "Afiyet olsun! 🍽️"
    return message

if __name__ == "__main__":
    print(get_menu())
