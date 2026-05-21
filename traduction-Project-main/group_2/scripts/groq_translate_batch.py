import pandas as pd
from groq import Groq
import time, os

# ============================================
# CONFIG — Ajoute tes clés Groq ici
# ============================================
API_KEYS = [
    'PUT_YOUR_GROQ_API_KEY_HERE',  # remplace par ta clé Groq
    'PUT_YOUR_GROQ_API_KEY_HERE',
    'PUT_YOUR_GROQ_API_KEY_HERE',
    'PUT_YOUR_GROQ_API_KEY_HERE',
]

INPUT_FILE  = 'unlabeled_dataset.csv'   # ton fichier CSV exporté depuis Label Studio
OUTPUT_FILE = 'silver_shard_2_translated.csv'  # fichier de sortie dans le même dossier

# ============================================
# INITIALISATION
# ============================================
key_index = 0
client = Groq(api_key=API_KEYS[key_index])
print(f'Clé API active : clé n°{key_index + 1}')

def switch_key():
    """Passe à la clé suivante si la courante est épuisée."""
    global key_index, client
    key_index += 1
    if key_index >= len(API_KEYS):
        print('Toutes les cles epuisees — attente 10 minutes...')
        time.sleep(600)  # 10 minutes puis on recommence avec cle 1
        key_index = 0
    client = Groq(api_key=API_KEYS[key_index])
    print(f'Passage a la cle n°{key_index + 1}')

# ============================================
# FONCTION TRADUCTION
# ============================================
def translate_darija(darija_arabic, darija_arabizi, retries=3):
    if not darija_arabic or pd.isna(darija_arabic):
        return '', ''

    prompt = f"""Agis comme un traducteur expert marocain.
1. Traduis cette phrase Darija en Anglais (Direct & Meaningful).
2. Traduis cette phrase en Arabe Standard (MSA) formel.
Phrase Darija : '{str(darija_arabic).strip()}'

Reponds UNIQUEMENT sous ce format exact (deux lignes) :
ENGLISH: ta traduction anglais ici
MSA: الترجمة بالعربية الفصحى هنا"""

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model='llama-3.1-8b-instant',
                messages=[{'role': 'user', 'content': prompt}],
                temperature=0.3,
                max_tokens=300
            )
            text = response.choices[0].message.content.strip()
            english, msa = '', ''
            for line in text.split('\n'):
                line = line.strip()
                if line.startswith('ENGLISH:'):
                    english = line.replace('ENGLISH:', '').strip()
                elif line.startswith('MSA:'):
                    msa = line.replace('MSA:', '').strip()
            return english, msa

        except Exception as e:
            error = str(e)
            if '429' in error or 'quota' in error.lower() or 'rate' in error.lower():
                print(f'  Rate limit cle n°{key_index + 1} — passage cle suivante...')
                switch_key()  # changer de cle immediatement sans attendre
            else:
                print(f'  Tentative {attempt+1}/{retries} : {e}')
                time.sleep(2)

    return '', ''

# ============================================
# CHARGEMENT DU DATASET
# ============================================
df = pd.read_csv(INPUT_FILE)
print(f'Total lignes : {len(df)}')

# ============================================
# TEST SUR 3 LIGNES
# ============================================
print('\nTest sur 3 lignes...\n')
for i, row in df.head(3).iterrows():
    en, msa = translate_darija(row['darija_arabic'], row['darija_arabizi'])
    print(f'--- Ligne {i+1} ---')
    print(f'Darija  : {row["darija_arabic"]}')
    print(f'English : {en}')
    print(f'MSA     : {msa}')
    print()
    time.sleep(1)

confirm = input('\nLe test est bon ? (oui/non) : ').strip().lower()
if confirm != 'oui':
    print('Script arrete. Verifie le prompt et relance.')
    exit()

# ============================================
# REPRISE AUTOMATIQUE
# ============================================
if os.path.exists(OUTPUT_FILE):
    df_done = pd.read_csv(OUTPUT_FILE)
    done_ids = set(df_done['id'].unique())
    results = df_done.to_dict('records')
    print(f'\nReprise : {len(done_ids)} lignes deja traduites')
else:
    done_ids = set()
    results = []
    print('\nNouveau depart')

df_remaining = df[~df['id'].isin(done_ids)]
print(f'Lignes restantes : {len(df_remaining)}\n')

# ============================================
# BATCH COMPLET
# ============================================
for i, (_, row) in enumerate(df_remaining.iterrows()):
    en, msa = translate_darija(row['darija_arabic'], row['darija_arabizi'])

    results.append({
        'data_id':                row['data_id'],
        'id':                     row['id'],
        'classe':                 row['classe'],
        'darija_arabic':          row['darija_arabic'],
        'darija_arabizi':         row['darija_arabizi'],
        'english':                en if en else row.get('english', ''),
        'modern_standard_arabic': msa if msa else row.get('modern_standard_arabic', ''),
        'english_word_count':     row['english_word_count'],
        'status':                 'GENERATED'
    })

    # Sauvegarde toutes les 10 lignes
    if (i + 1) % 10 == 0:
        pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
        print(f'{i + 1}/{len(df_remaining)} traduits... (cle n°{key_index + 1} active)')

    time.sleep(2)  # 2s entre chaque requete = ~30 req/min max

# Sauvegarde finale
pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
print(f'\nTermine ! {len(results)} lignes sauvegardees dans {OUTPUT_FILE}')
