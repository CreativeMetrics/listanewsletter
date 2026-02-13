import requests
import os
from datetime import datetime

# --- CONFIGURAZIONE ---
API_KEY = os.getenv("BREVO_API_KEY")
LIMIT = 50  # Quante newsletter mostrare
FILE_OUTPUT = "index.html"

def fetch_campaigns():
	url = f"https://api.brevo.com/v3/emailCampaigns?status=sent&limit={LIMIT}&sort=desc"
	headers = {"accept": "application/json", "api-key": API_KEY}
	
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		return response.json().get('campaigns', [])
	else:
		print(f"Errore API: {response.status_code}")
		return []

def generate_html(campaigns):
		now = datetime.now().strftime("%d/%m/%Y %H:%M")
		
		html = f"""
		<!DOCTYPE html>
		<html lang="it">
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>Archivio Newsletter</title>
			<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
			<style>
				:root {{
					--primary: #0070f3;
					--bg: #f8fafc;
					--text: #1e293b;
					--card-bg: #ffffff;
				}}
				body {{ 
					font-family: 'Inter', sans-serif; 
					background-color: var(--bg); 
					color: var(--text); 
					margin: 0; 
					padding: 40px 20px;
					line-height: 1.6;
				}}
				.container {{ max-width: 700px; margin: auto; }}
				header {{ text-align: center; margin-bottom: 50px; }}
				h1 {{ font-weight: 600; font-size: 2.5rem; margin-bottom: 10px; letter-spacing: -1px; }}
				.last-update {{ color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }}
				
				.archive-list {{ display: flex; flex-direction: column; gap: 16px; }}
				
				.card {{
					background: var(--card-bg);
					padding: 20px;
					border-radius: 16px;
					text-decoration: none;
					color: inherit;
					display: flex;
					align-items: center;
					justify-content: space-between;
					transition: all 0.2s ease;
					border: 1px solid rgba(0,0,0,0.05);
				}}
				
				.card:hover {{
					transform: translateY(-3px);
					box-shadow: 0 10px 25px rgba(0,112,243,0.1);
					border-color: var(--primary);
				}}
				
				.card-content {{ display: flex; flex-direction: column; gap: 4px; }}
				.card-title {{ font-weight: 600; color: var(--text); font-size: 1.1rem; }}
				.card-date {{ color: #64748b; font-size: 0.9rem; }}
				
				.arrow {{
					color: var(--primary);
					font-size: 1.2rem;
					font-weight: bold;
					transition: transform 0.2s ease;
				}}
				.card:hover .arrow {{ transform: translateX(5px); }}
		
				footer {{ margin-top: 60px; text-align: center; color: #94a3b8; font-size: 0.8rem; }}
				
				@media (max-width: 600px) {{
					h1 {{ font-size: 1.8rem; }}
					.card {{ padding: 16px; }}
				}}
			</style>
		</head>
		<body>
			<div class="container">
				<header>
					<h1>Le nostre Newsletter</h1>
					<p class="last-update">Aggiornato il {now}</p>
				</header>
				
				<div class="archive-list">
		"""
		
		for c in campaigns:
			# Gestione data
			date_obj = datetime.fromisoformat(c['sentDate'].replace('Z', '+00:00'))
			formatted_date = date_obj.strftime("%d %B %Y")
			
			# Gestione nomi e link
			name = c.get('subject') or c.get('name')
			link = c.get('shareLink')
			
			if link:
				html += f"""
					<a href="{link}" class="card" target="_blank">
						<div class="card-content">
							<span class="card-date">{formatted_date}</span>
							<span class="card-title">{name}</span>
						</div>
						<div class="arrow">→</div>
					</a>
				"""
		
		html += """
				</div>
				<footer>
					Creato con passione • Alimentato da Brevo API
				</footer>
			</div>
		</body>
		</html>
		"""
		
		with open(FILE_OUTPUT, "w", encoding="utf-8") as f:
			f.write(html)

if __name__ == "__main__":
	data = fetch_campaigns()
	if data:
		generate_html(data)
		print(f"Pagina '{FILE_OUTPUT}' creata con successo!")