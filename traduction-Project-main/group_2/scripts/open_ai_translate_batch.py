import re
import time
from label_studio_sdk import LabelStudio
from openai import OpenAI

# ── CONFIG ──────────────────────────────────────────────────────────────
LABEL_STUDIO_URL     = "http://localhost:8080"
LABEL_STUDIO_API_KEY = "PUT_YOUR_LABEL_STUDIO_API_KEY_HERE"
PROJECT_ID           = 12
OPENAI_API_KEY       = "PUT_YOUR_OPENAI_API_KEY_HERE"

MODEL_NAME    = "gpt-4o-mini"
BATCH_SIZE    = 20       # augmenté pour aller plus vite
SLEEP_BETWEEN = 0.5      # réduit, safe avec gpt-4o-mini
MAX_RETRIES   = 3        # tentatives par tâche en cas d'erreur
# ────────────────────────────────────────────────────────────────────────

PROMPT = """Tu es un expert en linguistique marocaine et traducteur professionnel Darija vers Anglais et MSA.

Tu reçois une phrase en deux formes :
- Script Arabe   : '{darija_arabic}'
- Arabizi (Latin): '{darija_arabizi}'

RÈGLES DE NETTOYAGE :
1. Supprime les artefacts : @@, @-@, <unk>, #, espaces doubles
2. Si tu vois <unk> -> remplace par le mot logique selon le contexte
3. Si la phrase est tronquée -> simplifie pour garder un sens complet

RÈGLES darija_arabic : zéro caractère latin, mots étrangers en translittération arabe
RÈGLES darija_arabizi : phonétique latine, sons arabes avec chiffres (7, 9, 3)
RÈGLES TRADUCTION : fidélité sémantique, registre naturel, noms propres conservés

Réponds UNIQUEMENT sous ce format exact (4 lignes) :
DARIJA_ARABIC: ...
DARIJA_ARABIZI: ...
ENGLISH: ...
MSA: ..."""


def parse(raw: str) -> dict:
    out = {"darija_arabic": "", "darija_arabizi": "", "english": "", "msa": ""}
    for key, pat in [
        ("darija_arabic",  r"DARIJA_ARABIC:\s*(.+)"),
        ("darija_arabizi", r"DARIJA_ARABIZI:\s*(.+)"),
        ("english",        r"ENGLISH:\s*(.+)"),
        ("msa",            r"MSA:\s*(.+)"),
    ]:
        m = re.search(pat, raw, re.IGNORECASE)
        if m:
            out[key] = m.group(1).strip()
    return out


def build_result(parsed: dict) -> list:
    mapping = [
        ("corrected_darija_arabic",  "task_anchor", parsed["darija_arabic"]),
        ("corrected_darija_arabizi", "task_anchor", parsed["darija_arabizi"]),
        ("corrected_english",        "task_anchor", parsed["english"]),
        ("corrected_msa",            "task_anchor", parsed["msa"]),
    ]
    return [
        {"from_name": fn, "to_name": tn, "type": "textarea", "value": {"text": [val]}}
        for fn, tn, val in mapping if val
    ]


def process_task(oai, ls, task) -> bool:
    d = task.data or {}
    darija_arabic  = str(d.get("darija_arabic",  "") or "").strip()
    darija_arabizi = str(d.get("darija_arabizi", "") or "").strip()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = oai.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": PROMPT.format(
                    darija_arabic=darija_arabic,
                    darija_arabizi=darija_arabizi,
                )}],
                temperature=0.1,
                max_tokens=500,
            )
            parsed = parse(resp.choices[0].message.content.strip())
            result = build_result(parsed)

            ls.predictions.create(
                task=task.id,
                result=result,
                score=0.95,
                model_version=MODEL_NAME,
            )
            return True

        except Exception as e:
            print(f"    Tentative {attempt}/{MAX_RETRIES} échouée : {e}", flush=True)
            if attempt < MAX_RETRIES:
                time.sleep(2 * attempt)  # backoff : 2s, 4s
    return False


def main():
    ls = LabelStudio(base_url=LABEL_STUDIO_URL, api_key=LABEL_STUDIO_API_KEY)
    me = ls.users.whoami()
    print(f"Connecté : {me.username} ({me.email})", flush=True)

    # Chargement avec progression
    print(f"\nChargement des tâches du projet {PROJECT_ID}...", flush=True)
    tasks = []
    for i, task in enumerate(ls.tasks.list(project=PROJECT_ID)):
        tasks.append(task)
        if (i + 1) % 500 == 0:
            print(f"  {i + 1} tâches chargées...", flush=True)
    print(f"Total : {len(tasks)} tâches", flush=True)

    to_process = [t for t in tasks if not t.predictions]
    print(f"Sans prédiction : {len(to_process)} tâches", flush=True)
    print(f"Déjà traitées   : {len(tasks) - len(to_process)} tâches\n", flush=True)

    if not to_process:
        print("Rien à faire — toutes les tâches ont déjà une prédiction.")
        return

    oai = OpenAI(api_key=OPENAI_API_KEY)
    ok = errors = 0
    total = len(to_process)
    start = time.time()

    for i in range(0, total, BATCH_SIZE):
        batch = to_process[i : i + BATCH_SIZE]
        done  = i + len(batch)
        pct   = round(done / total * 100)

        # Estimation temps restant
        elapsed = time.time() - start
        speed   = done / elapsed if elapsed > 0 else 0
        eta_min = round((total - done) / speed / 60) if speed > 0 and done > 0 else "?"

        print(f"\nLot {i // BATCH_SIZE + 1} — {done}/{total} ({pct}%) — ETA : {eta_min} min", flush=True)

        for task in batch:
            success = process_task(oai, ls, task)
            if success:
                ok += 1
                print(f"  ✓ Task {task.id}", flush=True)
            else:
                errors += 1
                print(f"  ✗ Task {task.id} — ignorée après {MAX_RETRIES} tentatives", flush=True)

        if i + BATCH_SIZE < total:
            time.sleep(SLEEP_BETWEEN)

    elapsed_total = round((time.time() - start) / 60, 1)
    print(f"\n{'='*50}")
    print(f"Terminé en {elapsed_total} min : {ok} succès / {errors} erreurs sur {total} tâches", flush=True)
    print("→ Label Studio : sélectionne tout → 'Retrieve Annotations from Predictions'")


if __name__ == "__main__":
    main()