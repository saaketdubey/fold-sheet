#!/usr/bin/env python3
"""Builds devi_sukta_spec.json for fold_sheet.py (Rigveda 10.125, 10 panels / 5 pages)."""
import json

TITLE = "Devi Sukta"
SUB = "Rigveda 10.125 | Vagambhrini Sukta | Spoken by Vak"

KEY = [
    "a = u in but; i = sit; u = put. AA = father; EE = see; OO = food; OH = go; AY = say; AI = eye; OW = cow. Capitals mark long vowels: hold them. Sanskrit has no stress.",
    "ri (as in hri, dhri, pri) = one quick syllable. kh / chh / th / dh / bh = the consonant + a puff of air (th is never English “th”). Final h = a soft breath echoing the vowel before it. gny (for jn) is often gy in North Indian usage.",
    "Vedic pitch accents are not marked. Sanskrit split into reading units (one pada each); sandhi resolved where a word runs across a unit break.",
    "Rigveda 10.125, unaccented text. English translation is original to this sheet.",
]

INTRO = """<p><b>The Goddess speaks.</b> This hymn is voiced by Vak — Speech — daughter of the seer Ambhrina. Every verse begins with <i>aham</i>, “I”: She carries the Gods, feeds the one who offers, makes seers and sages, draws the bow for Rudra, gives birth to the Father, and reaches beyond Sky and Earth.</p>
<p>It stands in the tenth mandala of the Rigveda, among the cosmological hymns, and is one of the few Vedic hymns spoken wholly in a goddess's own voice. The Shakta tradition reads it as the earliest scriptural statement of the Goddess as supreme power; it is recited at the close of the Devi Mahatmya.</p>
<p class="h2">Seer: Vak Ambhrini · Deity: Vak · Metre: Trishtubh (verse 2 is Jagati)</p>"""

# (dev, translit, phonetic, english) — four padas per verse
V = [
 [("अहं रुद्रेभिर्वसुभिश्चरामि", "aham rudrebhir vasubhish charami", "a-ham rud-RAY-bhir va-su-bhish cha-RAA-mi", "I move with the Rudras and the Vasus,"),
  ("अहमादित्यैरुत विश्वदेवैः ।", "aham adityair uta vishvadevaih |", "a-ham AA-dit-YAIR u-ta vish-va-DAY-VAIH", "I with the Adityas and all the Gods;"),
  ("अहं मित्रावरुणोभा बिभर्मि", "aham mitravarunobha bibharmi", "a-ham mit-RAA-va-ru-NOH-BHAA bi-bhar-mi", "I bear both Mitra and Varuna,"),
  ("अहमिन्द्राग्नी अहमश्विनोभा ॥", "aham indragni aham ashvinobha ||", "a-ham in-DRAAG-NEE a-ham ash-vi-NOH-BHAA", "I bear Indra and Agni, I both Ashvins.")],
 [("अहं सोममाहनसं बिभर्मि", "aham somam ahanasam bibharmi", "a-ham SOH-mam AA-ha-na-sam bi-bhar-mi", "I bear the swelling Soma,"),
  ("अहं त्वष्टारमुत पूषणं भगम् ।", "aham tvashtaram uta pushanam bhagam |", "a-ham tvash-TAA-ram u-ta POO-sha-nam bha-gam", "I bear Tvashtar, Pushan and Bhaga;"),
  ("अहं दधामि द्रविणं हविष्मते", "aham dadhami dravinam havishmate", "a-ham da-DHAA-mi dra-vi-nam ha-vish-ma-TAY", "I bestow wealth on the one who offers,"),
  ("सुप्राव्ये यजमानाय सुन्वते ॥", "supravye yajamanaya sunvate ||", "su-PRAAV-YAY ya-ja-MAA-NAA-ya sun-va-TAY", "on the devout patron who presses the Soma.")],
 [("अहं राष्ट्री संगमनी वसूनां", "aham rashtri sangamani vasunam", "a-ham RAASH-TREE san-ga-ma-NEE va-SOO-NAAM", "I am the Queen, gatherer of treasures,"),
  ("चिकितुषी प्रथमा यज्ञियानाम् ।", "chikitushi prathama yajniyanam |", "chi-ki-tu-SHEE pra-tha-MAA yag-nyi-YAA-NAAM", "the knowing one, first among those worthy of worship;"),
  ("तां मा देवा व्यदधुः पुरुत्रा", "tam ma deva vyadadhuh purutra", "TAAM MAA DAY-VAA vya-da-dhuh pu-rut-RAA", "the Gods set Me in many places,"),
  ("भूरिस्थात्रां भूर्यावेशयन्तीम् ॥", "bhuristhatram bhury aveshayantim ||", "BHOO-ris-THAAT-RAAM BHOOR-YAA-VAY-sha-yan-TEEM", "abiding in many, entering into many.")],
 [("मया सो अन्नमत्ति यो विपश्यति", "maya so annam atti yo vipashyati", "ma-YAA SOH an-nam at-ti YOH vi-pash-ya-ti", "Through Me eats whoever eats, whoever sees,"),
  ("यः प्राणिति य ईं शृणोत्युक्तम् ।", "yah praniti ya im shrinoty uktam |", "yah PRAA-ni-ti ya EEM shri-NOHT-yuk-tam", "whoever breathes, whoever hears what is spoken;"),
  ("अमन्तवो मां त उप क्षियन्ति", "amantavo mam ta upa kshiyanti", "a-man-ta-VOH MAAM ta u-pa kshi-yan-ti", "not knowing Me, they still dwell in Me."),
  ("श्रुधि श्रुत श्रद्धिवं ते वदामि ॥", "shrudhi shruta shraddhivam te vadami ||", "shru-dhi shru-ta shrad-dhi-vam TAY va-DAA-mi", "Hear, O' one who hears: what I tell you is worthy of faith.")],
 [("अहमेव स्वयमिदं वदामि", "aham eva svayam idam vadami", "a-ham AY-va sva-yam i-dam va-DAA-mi", "I Myself proclaim this,"),
  ("जुष्टं देवेभिरुत मानुषेभिः ।", "jushtam devebhir uta manushebhih |", "jush-tam DAY-VAY-bhir u-ta MAA-nu-SHAY-bhih", "welcomed by Gods and by humans;"),
  ("यं कामये तंतमुग्रं कृणोमि", "yam kamaye tam-tam ugram krinomi", "yam KAA-ma-YAY tam-tam ug-ram kri-NOH-mi", "whomever I love, that one I make mighty,"),
  ("तं ब्रह्माणं तमृषिं तं सुमेधाम् ॥", "tam brahmanam tam rishim tam sumedham ||", "tam brah-MAA-nam tam ri-shim tam su-MAY-DHAAM", "a Brahman, a seer, a sage.")],
 [("अहं रुद्राय धनुरा तनोमि", "aham rudraya dhanur a tanomi", "a-ham rud-RAA-ya dha-nur AA ta-NOH-mi", "I stretch the bow for Rudra,"),
  ("ब्रह्मद्विषे शरवे हन्तवा उ ।", "brahmadvishe sharave hantava u |", "brah-mad-vi-SHAY sha-ra-VAY han-ta-VAA u", "so the arrow strikes the hater of prayer;"),
  ("अहं जनाय समदं कृणोमि", "aham janaya samadam krinomi", "a-ham ja-NAA-ya sa-ma-dam kri-NOH-mi", "I make battle for the people,"),
  ("अहं द्यावापृथिवी आ विवेश ॥", "aham dyavaprithivi a vivesha ||", "a-ham DYAA-VAA-pri-thi-VEE AA vi-VAY-sha", "I have entered Sky and Earth.")],
 [("अहं सुवे पितरमस्य मूर्धन्", "aham suve pitaram asya murdhan", "a-ham su-VAY pi-ta-ram as-ya MOOR-dhan", "I give birth to the Father at the summit of this world;"),
  ("मम योनिरप्स्वन्तः समुद्रे ।", "mama yonir apsv antah samudre |", "ma-ma YOH-nir aps-van-tah sa-mud-RAY", "My womb is within the Waters, in the ocean;"),
  ("ततो वि तिष्ठे भुवनानु विश्वा", "tato vi tishthe bhuvananu vishva", "ta-TOH vi tish-THAY bhu-va-NAA-nu vish-VAA", "from there I spread through all beings,"),
  ("उतामूं द्यां वर्ष्मणोप स्पृशामि ॥", "utamum dyam varshmanopa sprishami ||", "u-TAA-MOOM DYAAM varsh-ma-NOH-pa spri-SHAA-mi", "and touch that Sky with My height.")],
 [("अहमेव वात इव प्र वामि", "aham eva vata iva pra vami", "a-ham AY-va VAA-ta i-va pra VAA-mi", "I Myself blow forth like the Wind,"),
  ("आरभमाणा भुवनानि विश्वा ।", "arabhamana bhuvanani vishva |", "AA-ra-bha-MAA-NAA bhu-va-NAA-ni vish-VAA", "taking hold of all beings;"),
  ("परो दिवा पर एना पृथिव्या", "paro diva para ena prithivya", "pa-ROH di-VAA pa-ra AY-NAA pri-thiv-YAA", "beyond the Sky, beyond this Earth,"),
  ("एतावती महिना सं बभूव ॥", "etavati mahina sam babhuva ||", "AY-TAA-va-TEE ma-hi-NAA sam ba-BHOO-va", "so great have I become by My greatness.")],
]

panels = [{"subtitle": SUB, "prose_html": INTRO, "footer": KEY}]
for n, verse in enumerate(V, 1):
    p = {"subtitle": f"Rigveda 10.125 | Verse {n}",
         "units": [{"dev": d, "iast": t, "phon": ph, "en": e} for d, t, ph, e in verse]}
    panels.append(p)
eng = "".join(f"<p style='margin:0 0 7pt;font-size:10.5pt;line-height:1.5'><b>{n}.</b> {' '.join(e for _,_,_,e in verse)}</p>" for n, verse in enumerate(V, 1))
panels.append({"title": "Devi Sukta in English", "subtitle": "Rigveda 10.125 | Translation", "prose_html": eng})

CSS = ".u{margin-bottom:15pt}.dev{font-size:20pt;line-height:1.4;margin-bottom:2pt}.iast,.phon,.en{font-size:11pt}.sub{margin-bottom:20pt}.prose{font-size:11pt;line-height:1.6}.prose p{margin:0 0 11pt}"
here = __import__("pathlib").Path(__file__).parent

# --- single-sided sheet: key on every even-indexed panel (left side); no page numbers ---
single = [dict(p) for p in panels]
for i, p in enumerate(single):
    p["footer"] = KEY if i % 2 == 0 else []
spec = {"title": TITLE, "footer": [], "panels_per_page": 2, "folio": False, "panels": single, "css": CSS}
json.dump(spec, open(here / "devi_sukta_spec.json", "w"), ensure_ascii=False, indent=1)
print(len(single), "panels (single-sided)")

# --- booklet: title panel + the same 10 panels + blank = 12 panels, 3 duplex sheets ---
title = {"title": "", "subtitle": "", "folio": False, "prose_html":
         '<div class="tp"><p class="tt">Devi Sukta</p><p class="ts">Rigveda 10.125</p></div>'}
blank = {"title": "", "subtitle": "", "prose_html": ""}
booklet = [title] + [dict(p) for p in panels] + [blank]
for i, p in enumerate(booklet):          # key on the left page of each opened spread = odd indices
    p["footer"] = KEY if (i % 2 == 1 and i < len(booklet) - 1) else []
spec = {"title": TITLE, "footer": [], "panels_per_page": 2, "imposition": "booklet", "panels": booklet,
        "css": CSS + ".tp{margin-top:2.6in;text-align:center}.tp .tt{font-size:26pt;font-weight:700;margin:0 0 8pt}.tp .ts{font-size:11pt;color:#555;margin:0}"}
json.dump(spec, open(here / "devi_sukta_booklet_spec.json", "w"), ensure_ascii=False, indent=1)
print(len(booklet), "panels (booklet)")
