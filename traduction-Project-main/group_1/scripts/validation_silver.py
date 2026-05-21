import pandas as pd
import time
import json
from openai import OpenAI

# =========================
# 1. CONFIGURATION
# =========================

OPENAI_API_KEY = "PUT_YOUR_OPENAI_API_KEY_HERE"
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL_ID = "gpt-4.1-mini"  # recommandé pour darija

# =========================
# 2. CHARGEMENT DES DONNÉES
# =========================

nom_fichier_sortie = '/content/drive/MyDrive/Colab Notebooks/silver_shard_1_EN_COURS.csv'

try:
    df_silver = pd.read_csv(nom_fichier_sortie)
    print(" Reprise du travail en cours...")
except FileNotFoundError:
    df_silver = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/silver_shard_1_clean.csv')
    print("Nouveau départ.")

# =========================
# 3. FONCTION DE CORRECTION
# =========================

def get_smart_correction(row):
    prompt = f"""
You are an expert Moroccan linguist. Correct, normalize, and validate this Darija entry.

### STRICT RULES:
1. darija_arabic (Arabic script only), darija_arabizi (Latin: ع=3, 7=ح, 9=ق, 5=خ, gh=غ, ch=ش), english (Fluent), msa (Standard Arabic).
2. Fidelity: Preserve exact meaning. Translate intent, not word-for-word.
3. Normalization: Fix spelling and fill missing fields.
4. Use authentic Moroccan dialect only (no Egyptian or Levantine words).

### GOLD EXAMPLES:
1. {{"darija_arabic": "عجبني الحال بزاف هنا", "darija_arabizi": "3jbni l7al bzaf hna", "english": "I really enjoyed it here", "msa": "أعجبني الحال كثيراً هنا"}}
2. {{"darija_arabic": "ما كاينش مشكل، هانية", "darija_arabizi": "ma kaynch mouchkil, hanyia", "english": "No problem, it's fine", "msa": "لا توجد مشكلة، بأس"}}
3. {{"darija_arabic": "واش تقدر تعاوني خاي؟", "darija_arabizi": "wach t9dr t3awni khay?", "english": "Can you help me, brother?", "msa": "هل يمكنك مساعدتي يا أخي؟"}}

### INPUT TO CORRECT:
{{"darija_arabic": "{row['darija_arabic']}", "darija_arabizi": "{row.get('darija_arabizi', '')}", "english": "{row['english']}", "msa": "{row['modern_standard_arabic']}"}}

### OUTPUT FORMAT:
Return only valid JSON with keys:
darija_arabic, darija_arabizi, english, msa
"""

    for attempt in range(3):
        try:
            response = client.chat.completions.create(  # ✅ bonne méthode
                model=MODEL_ID,
                messages=[
                    {"role": "system", "content": "You output only valid JSON. No markdown, no backticks, no explanation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            text = response.choices[0].message.content.strip()  # ✅ bon chemin

            # ✅ Nettoyage des backticks si présents
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip()

            if not text:
                raise ValueError("Réponse vide du modèle")

            return json.loads(text)

        except Exception as e:
            wait = 10 * (2 ** attempt)
            print(f"⚠️ Erreur API (tentative {attempt+1}): {e}")
            time.sleep(wait)

    return None

# =========================
# 4. BOUCLE PRINCIPALE
# =========================

lignes_modifiees = 0
DELAI_ENTRE_REQUETES = 1  # ~60 RPM

for index, row in df_silver.iterrows():
    try:
        if row.get('status') in ['GENERATED', 'PARTIALLY VALIDATED']:
            print(f"Ligne {index}...", end=" ", flush=True)

            data = get_smart_correction(row)

            if data:
                df_silver.at[index, 'darija_arabic'] = data.get('darija_arabic', row['darija_arabic'])
                df_silver.at[index, 'darija_arabizi'] = data.get('darija_arabizi', row.get('darija_arabizi', ''))
                df_silver.at[index, 'english'] = data.get('english', row['english'])
                df_silver.at[index, 'modern_standard_arabic'] = data.get('msa', row['modern_standard_arabic'])
                df_silver.at[index, 'status'] = 'AI_REVIEWED'

                lignes_modifiees += 1
                print("✅")
            else:
                print("Erreur correction")

            time.sleep(DELAI_ENTRE_REQUETES)

        if lignes_modifiees > 0 and lignes_modifiees % 10 == 0:
            df_silver.to_csv(nom_fichier_sortie, index=False)
            print(f" Sauvegarde intermédiaire ({lignes_modifiees} lignes)")

    except Exception as e:
        print(f"Erreur ligne {index}: {e}")

# =========================
# 5. SAUVEGARDE FINALE
# =========================

final_path = '/content/drive/MyDrive/Colab Notebooks/silver_shard_1_FULL_corrected.csv'
df_silver.to_csv(final_path, index=False)

print(f"\n Terminé ! {lignes_modifiees} lignes corrigées.")
print(f"Fichier final : {final_path}")