import streamlit as st
import random

# ─── Configuration de la page ────────────────────────────────────────────────
st.set_page_config(
    page_title="Wordle 1v1",
    page_icon="🟩",
    layout="centered",
)

# ─── CSS personnalisé ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    .title { text-align: center; font-size: 2.5rem; font-weight: 800; letter-spacing: 0.15em; margin-bottom: 0.2em; }
    .subtitle { text-align: center; color: #888; margin-bottom: 1.5em; font-size: 0.95rem; }
    .grid-row { display: flex; gap: 6px; justify-content: center; margin: 4px 0; }
    .cell {
        width: 52px; height: 52px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem; font-weight: 800;
        border-radius: 4px; color: white;
        text-transform: uppercase;
    }
    .green  { background-color: #538d4e; }
    .yellow { background-color: #b59f3b; }
    .gray   { background-color: #3a3a3c; }
    .empty  { background-color: #121213; border: 2px solid #3a3a3c; }
    .player-header {
        text-align: center; font-size: 1.2rem; font-weight: 700;
        padding: 8px 0; margin-bottom: 8px;
        border-bottom: 2px solid #333;
    }
    .winner-box {
        background: linear-gradient(135deg, #538d4e, #3a7a40);
        border-radius: 12px; padding: 20px; text-align: center;
        color: white; font-size: 1.1rem; margin: 16px 0;
    }
    .tie-box {
        background: linear-gradient(135deg, #b59f3b, #9a862e);
        border-radius: 12px; padding: 20px; text-align: center;
        color: white; font-size: 1.1rem; margin: 16px 0;
    }
    .turn-badge {
        display: inline-block; padding: 4px 14px;
        border-radius: 20px; font-weight: 700;
        background: #538d4e; color: white;
        font-size: 0.9rem; margin-bottom: 8px;
    }
    .word-reveal {
        text-align: center; font-size: 1.4rem; font-weight: 800;
        letter-spacing: 0.2em; color: #538d4e; margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ─── Liste de mots français de 5 lettres ─────────────────────────────────────
MOTS = [
    "ABIME", "ABLER", "ABOLI", "ABORD", "ABOUT", "ABRIS", "ACCES", "ACIER",
    "ACUTE", "ADIEU", "ADOBE", "ADORE", "AGILE", "AGIOS", "AGITE", "AGONI",
    "AGREE", "AIGLE", "AIMER", "ALBUM", "ALLEE", "ALTER", "AMOUR", "ANCRE",
    "ANGEL", "ANGLE", "ANODE", "APNEE", "APPEL", "ARBRE", "ARCHE", "ARDRE",
    "ARENE", "ARMET", "AROBE", "ARQUE", "ARRET", "ASIDE", "ASILE", "ASTRE",
    "ATOME", "ATOUT", "ATRIO", "ATOUT", "AVANT", "AVION", "AVOIR", "AVORI",
    "AXONE", "AZOTE", "BAGUE", "BALLE", "BANJO", "BARBE", "BARON", "BASER",
    "BATIR", "BICHE", "BIJOU", "BISON", "BOMBE", "BOTTE", "BOULE", "BOXON",
    "BRAVE", "BRAVO", "BREVE", "BRIDE", "BRISE", "BRUME", "BULLE", "BUTIN",
    "CABLE", "CACHE", "CALME", "CARRE", "CARTE", "CEDER", "CHALE", "CHAMP",
    "CHANT", "CHAOS", "CHAUD", "CHIEN", "CHOSE", "CIBLE", "CITER", "CLORE",
    "COBRA", "COEUR", "COLON", "CONTE", "CORDE", "CORNE", "CORPS", "COUPE",
    "COURS", "CRANE", "CRIME", "CROIX", "CUIRE", "DANSE", "DEBUT", "DECOR",
    "DELTA", "DEMON", "DENTS", "DEPOT", "DESIR", "DETTE", "DOIGT", "DORER",
    "DROIT", "DUVET", "ECLAT", "ECOLE", "ECRAN", "EFFET", "ELEVE", "ELIRE",
    "ELOGE", "EMAIL", "ENCRE", "ENGIN", "ENVIE", "ENVOL", "EPAIS", "EPICE",
    "EPOUX", "ESSOR", "ETANG", "ETAPE", "ETUDE", "EVEIL", "EXACT", "EXCES",
    "EXIGE", "EXODE", "FABLE", "FAIRE", "FAUVE", "FEMME", "FENTE", "FERRE",
    "FEUIL", "FICHE", "FILET", "FLAIR", "FLEUR", "FOLIE", "FORCE", "FORET",
    "FORME", "FOSSE", "FOYER", "FRAIS", "FRANC", "FROID", "FRUIT", "FUMEE",
    "FUSEE", "GALET", "GARDE", "GENRE", "GILET", "GIVRE", "GLACE", "GLOBE",
    "GORGE", "GOSSE", "GRACE", "GRAIN", "GRAND", "GRAVE", "GREVE", "GUIDE",
    "HERBE", "HERON", "HEURE", "HIBOU", "HOMME", "HOTEL", "HUILE", "IDEAL",
    "IMAGE", "JARDIN", "JEUNE", "JOKER", "JOLIE", "JOUET", "LACET", "LAPIN",
    "LASER", "LATTE", "LECON", "LEVRE", "LIANE", "LINGE", "LIVRE", "LOCAL",
    "LOUPE", "LOURD", "LUEUR", "LUTIN", "MAGIE", "MAINS", "MALIN", "MAMAN",
    "MARIN", "MASSE", "MATIN", "MECHE", "MELON", "METAL", "METRO", "MEUTE",
    "MONDE", "MORAL", "MORSE", "MOTIF", "MOULE", "MOYEN", "MULET", "MUSEE",
    "NACRE", "NAPPE", "NATTE", "NEIGE", "NERFS", "NICHE", "NIECE", "NOEUD",
    "NOIRE", "NOYER", "NUAGE", "OBJET", "OCEAN", "OLIVE", "OMBRE", "OPALE",
    "ORAGE", "ORDRE", "ORGUE", "OTAGE", "OUTIL", "OVALE", "OZONE", "PAIRE",
    "PANDA", "PASSE", "PATTE", "PAUSE", "PECHE", "PELLE", "PENTE", "PERLE",
    "PERTE", "PHARE", "PIANO", "PIECE", "PINCE", "PISTE", "PIXEL", "PIZZA",
    "PLACE", "PLAGE", "PLUME", "POIDS", "POINT", "POKER", "POMME", "PORTE",
    "POULE", "PREUX", "PRISE", "PROSE", "PRUNE", "QUEUE", "RADIO", "RAFLE",
    "RAVIN", "RECIT", "REGLE", "REINE", "REPAS", "REVER", "RIDER", "ROBOT",
    "ROCHE", "ROMAN", "ROTOR", "ROUGE", "RUBAN", "RUCHE", "RUGBY", "RUINE",
    "SABLE", "SABOT", "SAPIN", "SAUCE", "SAULE", "SAVON", "SCENE", "SERRE",
    "SIEGE", "SIGNE", "SIROP", "SOBRE", "SOCLE", "SOEUR", "SOLDE", "SOMME",
    "SONDE", "SONGE", "SORTE", "SOUCI", "SOUPE", "SPORT", "STADE", "STYLE",
    "SUEUR", "SUITE", "SURGE", "TABLE", "TACHE", "TALON", "TAPIS", "TASSE",
    "TAUPE", "TAXER", "TEMPO", "TENTE", "TERME", "TERRE", "THESE", "TIGRE",
    "TITRE", "TOILE", "TOMBE", "TONNE", "TRACE", "TRAIN", "TRAME", "TREVE",
    "TUILE", "TUYAU", "UNION", "UNITE", "USAGE", "VALSE", "VALVE", "VEINE",
    "VENTE", "VERBE", "VERRE", "VESTE", "VIEUX", "VIGNE", "VILLA", "VIRUS",
    "VITRE", "VIVRE", "VOILE", "VOLER", "VOTER", "VOUTE", "WAGON", "YACHT",
    "ZEBRE", "ZESTE",
]

# Filtre de sécurité : exactement 5 lettres alphabétiques
MOTS = sorted(set(m for m in MOTS if len(m) == 5 and m.isalpha()))


# ─── Initialisation du session_state ─────────────────────────────────────────
def init_state():
    defaults = {
        "secret_word": random.choice(MOTS),
        "current_player": "A",
        "guesses_a": [],
        "guesses_b": [],
        "finished_a": False,
        "finished_b": False,
        "won_a": False,
        "won_b": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─── Fonctions utilitaires ────────────────────────────────────────────────────
def evaluate_guess(secret: str, guess: str) -> list:
    result = ["gray"] * 5
    secret_chars = list(secret.upper())
    guess_chars  = list(guess.upper())
    for i in range(5):
        if guess_chars[i] == secret_chars[i]:
            result[i] = "green"
            secret_chars[i] = None
            guess_chars[i]  = None
    for i in range(5):
        if guess_chars[i] is not None and guess_chars[i] in secret_chars:
            result[i] = "yellow"
            secret_chars[secret_chars.index(guess_chars[i])] = None
    return result


def render_grid(guesses, secret, max_rows=6):
    html = ""
    for i in range(max_rows):
        html += '<div class="grid-row">'
        if i < len(guesses):
            colors = evaluate_guess(secret, guesses[i])
            for j, letter in enumerate(guesses[i].upper()):
                html += f'<div class="cell {colors[j]}">{letter}</div>'
        else:
            for _ in range(5):
                html += '<div class="cell empty"> </div>'
        html += "</div>"
    return html


def reset_game():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    init_state()


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎮 Wordle 1v1")
    st.markdown("---")
    st.markdown("Le mot secret est tiré **aléatoirement** au début de chaque partie.")
    st.markdown(f"**Mots disponibles :** {len(MOTS)}")
    st.markdown("---")
    st.markdown("**Légende**")
    st.markdown("🟩 Lettre bien placée")
    st.markdown("🟨 Lettre présente, mal placée")
    st.markdown("⬛ Lettre absente")
    st.markdown("---")
    if st.button("🔄 Nouvelle partie", use_container_width=True):
        reset_game()
        st.rerun()


# ─── Titre ────────────────────────────────────────────────────────────────────
st.markdown('<div class="title">🟩 WORDLE 1v1</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Même mot secret pour les deux joueurs — qui le trouve en moins de coups ?</div>', unsafe_allow_html=True)

secret = st.session_state.secret_word
MAX_TRIES = 6
game_over = st.session_state.finished_a and st.session_state.finished_b


# ─── Phase de jeu ─────────────────────────────────────────────────────────────
if not game_over:
    player = st.session_state.current_player
    guesses = st.session_state[f"guesses_{player.lower()}"]
    finished = st.session_state[f"finished_{player.lower()}"]

    st.markdown(f'<div style="text-align:center"><span class="turn-badge">🎯 Tour du Joueur {player}</span></div>', unsafe_allow_html=True)
    st.markdown("")

    col_grid, col_input = st.columns([1.2, 1])

    with col_grid:
        st.markdown(f'<div class="player-header">Joueur {player}</div>', unsafe_allow_html=True)
        st.markdown(render_grid(guesses, secret, MAX_TRIES), unsafe_allow_html=True)

    with col_input:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if not finished:
            remaining = MAX_TRIES - len(guesses)
            st.markdown(f"**Essais restants :** {remaining}")
            guess_input = st.text_input(
                "Votre mot",
                max_chars=5,
                placeholder="5 lettres...",
                key=f"input_{player}_{len(guesses)}",
                label_visibility="collapsed",
            )
            if st.button("✅ Valider", use_container_width=True, key=f"submit_{player}"):
                g = guess_input.strip().upper()
                if len(g) != 5 or not g.isalpha():
                    st.error("Entrez exactement 5 lettres.")
                else:
                    guesses.append(g)
                    st.session_state[f"guesses_{player.lower()}"] = guesses
                    if g == secret:
                        st.session_state[f"won_{player.lower()}"] = True
                        st.session_state[f"finished_{player.lower()}"] = True
                    elif len(guesses) >= MAX_TRIES:
                        st.session_state[f"finished_{player.lower()}"] = True
                    st.rerun()
        else:
            won = st.session_state[f"won_{player.lower()}"]
            if won:
                st.success(f"🎉 Bravo Joueur {player} !")
            else:
                st.error(f"❌ Joueur {player} n'a pas trouvé.")

            other = "B" if player == "A" else "A"
            if not st.session_state[f"finished_{other.lower()}"]:
                if st.button(f"➡️ Passer au Joueur {other}", use_container_width=True):
                    st.session_state.current_player = other
                    st.rerun()


# ─── Récapitulatif final ───────────────────────────────────────────────────────
if game_over:
    st.markdown("---")
    st.markdown("## 🏆 Récapitulatif")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="player-header">Joueur A</div>', unsafe_allow_html=True)
        st.markdown(render_grid(st.session_state.guesses_a, secret, MAX_TRIES), unsafe_allow_html=True)
        nb_a = len(st.session_state.guesses_a) if st.session_state.won_a else None
        if st.session_state.won_a:
            st.success(f"✅ Trouvé en **{nb_a}** coup{'s' if nb_a > 1 else ''}")
        else:
            st.error("❌ N'a pas trouvé")

    with col_b:
        st.markdown('<div class="player-header">Joueur B</div>', unsafe_allow_html=True)
        st.markdown(render_grid(st.session_state.guesses_b, secret, MAX_TRIES), unsafe_allow_html=True)
        nb_b = len(st.session_state.guesses_b) if st.session_state.won_b else None
        if st.session_state.won_b:
            st.success(f"✅ Trouvé en **{nb_b}** coup{'s' if nb_b > 1 else ''}")
        else:
            st.error("❌ N'a pas trouvé")

    st.markdown("---")
    won_a, won_b = st.session_state.won_a, st.session_state.won_b

    if won_a and won_b:
        if nb_a < nb_b:
            msg, box = f"🥇 Joueur A gagne ! ({nb_a} vs {nb_b} coups)", "winner-box"
        elif nb_b < nb_a:
            msg, box = f"🥇 Joueur B gagne ! ({nb_b} vs {nb_a} coups)", "winner-box"
        else:
            msg, box = f"🤝 Égalité ! Les deux ont trouvé en {nb_a} coup{'s' if nb_a > 1 else ''}.", "tie-box"
    elif won_a:
        msg, box = "🥇 Joueur A gagne — Joueur B n'a pas trouvé !", "winner-box"
    elif won_b:
        msg, box = "🥇 Joueur B gagne — Joueur A n'a pas trouvé !", "winner-box"
    else:
        msg, box = "😅 Personne n'a trouvé...", "tie-box"

    st.markdown(f'<div class="{box}">{msg}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="word-reveal">Le mot était : {secret}</div>', unsafe_allow_html=True)

    if st.button("🔄 Nouvelle partie", use_container_width=True):
        reset_game()
        st.rerun()
