"""Correct classical references for NCISM drugs 1-8 using searchable classical-text recensions."""
import json
from pathlib import Path

PATH = Path("plants.json")
FIXES = {
    "amalaki": {
        "shloka": "हरीतकीसमं धात्रीफलं किन्तु विशेषतः ।\nरक्तपित्तप्रमेहघ्नं परं वृष्यं रसायनम् ॥\nहन्ति वातं तदम्लत्वात्पित्तं माधुर्यशैत्यतः ।\nकफं रूक्षकषायत्वात्फलं धात्र्यास्त्रिदोषजित् ॥",
        "ref": "Bhavaprakasha Nighantu, Haritakyadi Varga, Amalaki passage (commonly cited around verses 39–40; numbering varies by recension/edition).",
    },
    "guduchi": {
        "shloka": "गुडूची कटुका तिक्ता स्वादुपाका रसायनी ।\nसंग्राहिणी कषायोष्णा लघ्वी बल्याऽग्निदीपनी ।\nदोषत्रयामतृड्दाहमेहकासांश्च पाण्डुताम् ॥\nकामलाकुष्ठवातास्रज्वरकृमिवमीन् हरेत् ।\nप्रमेहश्वासकासार्शःकृच्छ्रहृद्रोगवातनुत् ॥",
        "ref": "Bhavaprakasha Nighantu, Guduchyadi Varga, verses 8–9 in the searchable recension; edition numbering may vary.",
    },
    "vibhitaki": {
        "shloka": "बिभीतकस्त्रिलिङ्गः स्यान्नाक्षः कर्षफलस्तु सः ।\nकलिद्रुमो भूतवासस्तथा कलियुगालयः ॥\nबिभीतकं स्वादुपाकं कषायं कफपित्तनुत् ।\nउष्णवीर्यं हिमस्पर्शं भेदनं कासनाशनम् ॥",
        "ref": "Bhavaprakasha Nighantu, Haritakyadi Varga, verses 33–34 in the searchable recension; edition numbering may vary.",
    },
    "ashwagandha": {
        "shloka": "गन्धान्ता वाजिनामादिरश्वगन्धा हयाह्वया ।\nवराहकर्णी वरदा बलदा कुष्ठगन्धिनी ॥\nअश्वगन्धाऽनिलश्लेष्मश्वित्रशोथक्षयापहा ।\nबल्या रसायनी तिक्ता कषायोष्णाऽतिशुक्रला ॥",
        "ref": "Bhavaprakasha Nighantu, Guduchyadi Varga, verses 161–162 in the searchable recension; edition numbering may vary.",
    },
    "shatavari": {
        "shloka": "शतावरी बहुसुता भीरुरिन्दीवरी वरी ।\nनारायणी शतपदी शतवीर्या च पीवरी ॥\nशतावरी गुरुः शीता तिक्तास्वाद्वी रसायनी ।\nमेधाग्निपुष्टिदा स्निग्धा नेत्र्या गुल्मातिसारजित् ।\nशुक्रस्तन्यकरी बल्या वातपित्तास्रशोथजित् ॥",
        "ref": "Bhavaprakasha Nighantu, Guduchyadi Varga, Shatavari passage; exact verse numbering should be taken from the selected edition before displaying a number.",
    },
    "brahmi": {
        "shloka": "ब्राह्मी हिमा सरा तिक्ता लघुर्मेध्या च शीतला ।\nकषाया मधुरा स्वादुपाकायुष्या रसायनी ।\nस्वर्या स्मृतिप्रदा कुष्ठपाण्डुमेहास्रकासजित् ।\nविषशोथज्वरहरी तद्वन्मण्डूकपर्ण्यपि ॥",
        "ref": "Bhavaprakasha Nighantu, Guduchyadi Varga, Brahmi/Brahmi-shaka passage; exact verse numbering should be taken from the selected edition before displaying a number.",
    },
    "pippali": {
        "shloka": "पिप्पली मागधी कृष्णा वैदेही चपला कणा ।\nउपकुल्योषणा शौण्डी कोला स्यात्तीक्ष्णतण्डुला ॥\nपिप्पली दीपनी वृष्या स्वादुपाका रसायनी ।\nअनुष्णा कटुका स्निग्धा वातश्लेष्महरी लघुः ॥\nपिप्पली रेचनी हन्ति श्वासकासोदरज्वरान् ।\nकुष्ठप्रमेहगुल्मार्शःप्लीहशूलाममारुतान् ॥",
        "ref": "Bhavaprakasha Nighantu, Haritakyadi Varga, Pippali passage (often numbered 50–51 in searchable recensions; other editions differ).",
    },
    "haritaki": {
        "shloka": "हरीतकी पञ्चरसा लवणवर्जिता ।\nरूक्षा चोष्णा सरा मेध्या स्वादुपाका रसायनी ॥",
        "ref": "Bhavaprakasha Nighantu, Haritakyadi Varga, Haritaki properties passage; exact verse numbering varies by edition.",
    },
}

data = json.loads(PATH.read_text(encoding="utf-8"))
for p in data:
    key = p.get("id", "").lower()
    if key not in FIXES:
        continue
    f = FIXES[key]
    cr = p.setdefault("classical_reference", {})
    cr["shlokas"] = [f["shloka"]]
    cr["nighantu_references"] = [f["ref"]]
    cr["shloka_reference_status"] = "classical_text_corrected; edition/numbering explicitly qualified"
    cr["reference_hubs"] = [
        "TDU Indian Medicinal Plants Database — Shlokas",
        "CCRAS/NIIMH e-Nighantu — Bhavaprakasha Nighantu",
    ]
    meta = p.setdefault("metadata", {})
    meta["classical_review_batch"] = "1-8 corrected 2026-09-16"
    meta["status"] = "classical_text_reviewed; edition_numbering_may_vary"

PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Corrected classical references for: " + ", ".join(k for k in FIXES))
