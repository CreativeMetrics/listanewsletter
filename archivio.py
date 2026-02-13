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
		<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
		<style>
			body {{ font-family: 'Inter', sans-serif; background-color: #f4f7f9; color: #333; margin: 0; padding: 40px 20px; }}
			.container {{ max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
			h1 {{ color: #0070f3; margin-bottom: 10px; }}
			p.subtitle {{ color: #666; margin-bottom: 30px; font-size: 0.9em; }}
			table {{ width: 100%; border-collapse: collapse; }}
			th {{ text-align: left; padding: 12px; border-bottom: 2px solid #eee; color: #888; text-transform: uppercase; font-size: 0.8em; }}
			td {{ padding: 15px 12px; border-bottom: 1px solid #eee; }}
			tr:hover {{ background-color: #f9fbff; }}
			.date {{ color: #999; font-size: 0.9em; white-space: nowrap; }}
			.link {{ text-decoration: none; color: #0070f3; font-weight: 600; }}
			.link:hover {{ text-decoration: underline; }}
			footer {{ margin-top: 30px; font-size: 0.8em; color: #bbb; text-align: center; }}
		</style>
	</head>
	<body>
		<div class="container">
			<h1>Archivio Newsletter</h1>
			<p class="subtitle">Ultimo aggiornamento: {now}</p>
			<table>
				<thead>
					<tr>
						<th>Data</th>
						<th>Oggetto della Campagna</th>
					</tr>
				</thead>
				<tbody>
	"""

	for c in campaigns:
		# Formattazione data
		date_obj = datetime.fromisoformat(c['sentDate'].replace('Z', '+00:00'))
		formatted_date = date_obj.strftime("%d %b %Y")
		
		name = c.get('subject') or c.get('name')
		link = c.get('shareLink')
		
		if link:
			html += f"""
				<tr>
					<td class="date">{formatted_date}</td>
					<td><a href="{link}" class="link" target="_blank">{name}</a></td>
				</tr>
			"""

	html += """
				</tbody>
			</table>
			<footer>Generato automaticamente via Brevo API</footer>
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