import json
from pathlib import Path

DATA = Path('plants.json')

PATCHES = {
    'Vasa': {
        'status': 'needs_text_level_verification',
        'source': {'type': 'classical_text_verification', 'title': 'Bhavaprakasha Nighantu searchable PDF — Vasa passage', 'url': 'https://www.paruluniversity.ac.in/parul-institute-of-ayurved/pdf/PIA-Institute/E%20Shamhita/Bhavapraksha/bhava_prakash_nighantu.pdf', 'reference': 'Vasa passage around verses 68–69 in the searchable PDF; OCR is imperfect, so exact Devanagari quotation is intentionally not imported.'},
        'note': 'Previous Gemini verse/numbering was not accepted. The Sanskrit quotation is withheld until checked against a clean e-Nighantu or print edition.'
    },
    'Nimba': {
        'status': 'verified_text_location_edition_numbering_may_vary',
        'shlokas': [
            'निम्बः शीतो लघुग्राही कटुपाकोऽग्निवातनुत् ।\nस्रध्रः श्रमद्वाक्स्वरार्चिचक्रिमिप्रघ्नुत् ।\nव्रणपित्तकफच्छर्दिकुष्ठलासमेहनुत् ॥७४॥',
            'निम्बपर्णं स्मृतं नेत्र्यं कृमिपित्तविषप्रघुत् ।\nवातलं कटुपाकं च सवरीचकुष्ठनुत् ॥७५॥',
            'निम्बफलं रसे तिक्तं पाके तु कटुभेदनम् ।\nस्निग्धं लघुष्णं कुष्ठघ्नं गुल्मार्शःकृमिमेहनुत् ॥७६॥'
        ],
        'reference': 'Bhavaprakasha Nighantu, Nimba passage, verses 74–76 in the searchable Parul University PDF recension; edition numbering may vary.',
        'source': {'type': 'classical_text_verification', 'title': 'Bhavaprakasha Nighantu searchable PDF — Nimba', 'url': 'https://www.paruluniversity.ac.in/parul-institute-of-ayurved/pdf/PIA-Institute/E%20Shamhita/Bhavapraksha/bhava_prakash_nighantu.pdf', 'reference': 'Verses 74–76 in the searchable recension.'},
        'note': 'Gemini numbering 14–15 was rejected; the searchable recension places the Nimba material at 73–76.'
    },
    'Bhallataka': {
        'status': 'verified_text_location_edition_numbering_may_vary',
        'shlokas': [
            'भल्लातकं त्रिषु प्रोक्तमरुष्कोऽष्करोऽग्निकः ।\nतथैवाग्निमुखी भल्ली वीरवृक्षश्च शोफकृत् ॥२००॥',
            'भल्लातकफलं पक्वं स्वादुपाकरसं लघु ।\nकषायं पाचनं स्निग्धं तीक्ष्णोष्णं चेदि भेदनम् ॥२०१॥',
            'मेध्यं वह्निकरं हन्ति कफवातव्रणोदरम् ।\nकुष्ठार्शोग्रहणीगुल्मशोफानाहज्वरक्रिमीन् ॥२०२॥',
            'तन्मज्जा मधुरो वृष्यो बृंहणो वातपित्तहा ।\nवृन्तमारुष्करं स्वादु पित्तघ्नं केश्यमग्निकृत् ॥२०३॥',
            'भल्लातकः कषायोष्णः शुक्रलो मधुरो लघुः ।\nवातश्लेष्मोदरानाहकुष्ठार्शोग्रहणीगदान् ।\nहन्ति गुल्मज्वरश्वित्रवह्निमान्द्यकृमिव्रणान् ॥२०४॥'
        ],
        'reference': 'Bhavaprakasha Nighantu, Bhallataka passage, verses 200–204 in the Vishvasa searchable transcription; printed editions/recensions may number this passage differently.',
        'source': {'type': 'classical_text_verification', 'title': 'Bhava Mishra — Bhavaprakasha Haritakyadi Varga searchable transcription', 'url': 'https://vishvasa.github.io/sanskrit/koshaH/AyurvedaH/bhava-mishraH_bhAva-prakAshaH/02_2_harItakyAdivarga/', 'reference': 'Bhallataka verses 200–204.'},
        'note': 'Gemini quotation was rejected because its wording and numbering did not match the independently searchable classical passage.'
    },
    'Katuki': {
        'status': 'verified_text_location_edition_numbering_may_vary',
        'shlokas': [
            'कट्वी तु कटुका तिक्ता कृष्णभेदा कटम्भरा ।\nअशोका मत्स्यशकला चक्राङ्गी शकुलादनी ।\nमत्स्यपित्ता काण्डरुहा रोहिणी कटुरोहिणी ॥१३४॥',
            'कट्वी तु कटुका पाके तिक्ता रूक्षा हिमा लघुः ।\nभेदिनी दीपनी हृद्या कफपित्तज्वरापहा ।\nप्रमेहश्वासकासास्रदाहकुष्ठकृमिप्रणुत् ॥१३५॥'
        ],
        'reference': 'Bhavaprakasha Nighantu, Haritakyadi Varga, verses 134–135 in the NIIMH-linked searchable recension; edition numbering may vary.',
        'source': {'type': 'classical_text_verification', 'title': 'Bhavaprakasha Nighantu — Katuki passage', 'url': 'https://ayurveda360.in/ebooks-enighantu-bhavaprakasha-nighantu-haritakyadivarga/', 'reference': 'Verses 134–135; source page identifies the NIIMH e-Nighantu reference.'},
        'note': 'Gemini numbering 141–142 was rejected. The searchable recension supports 134–135 and the spelling कट्वी.'
    },
    'Arjuna': {
        'status': 'verified_text_location_edition_numbering_may_vary',
        'shlokas': [
            'ककुभोऽर्जुननामाख्यो नदीसर्जश्च कीर्तितः ।\nइन्द्रद्रुर्वीरवृक्षश्च वीरश्च धवलः स्मृतः ॥२५॥',
            'ककुभः शीतलो हृद्यः क्षतक्षयविषास्त्रजित् ।\nमेदोमेहव्रणान्हन्ति तुवरः कफपित्तहत् ॥२६॥'
        ],
        'reference': 'Bhavaprakasha Nighantu, Haritakyadi Varga, verses 25–26 in the Jain Quantum searchable scan; edition numbering may vary.',
        'source': {'type': 'classical_text_verification', 'title': 'Harit Kyadi Nighant searchable scan — Arjuna passage', 'url': 'https://jainqq.org/booktext/Harit_Kyadi_Nighant/020370', 'reference': 'Arjuna/Kakubha passage at verses 25–26 in this scan.'},
        'note': 'Gemini numbering 27–28 and its wording were rejected. Other editions may shift numbering; the text is independently corroborated.'
    }
}


def main():
    plants = json.loads(DATA.read_text(encoding='utf-8'))
    by_name = {p.get('identity', {}).get('name'): p for p in plants}
    for name, patch in PATCHES.items():
        if name not in by_name:
            raise SystemExit(f'Missing expected NCISM record: {name}')
        p = by_name[name]
        cr = p.setdefault('classical_reference', {})
        cr['shlokas'] = patch.get('shlokas', [])
        cr['nighantu_references'] = [patch['reference']]
        cr['shloka_reference_status'] = patch['status']
        cr['verification_note'] = patch['note']
        cr.setdefault('samhita_references', [])
        cr['verified_classical_sources'] = [patch['source']]
        sources = p.setdefault('sources', [])
        if not any(s.get('url') == patch['source']['url'] and s.get('type') == patch['source']['type'] for s in sources):
            sources.append(patch['source'])
        metadata = p.setdefault('metadata', {})
        metadata['classical_review_batch'] = '14-18 reviewed 2026-09-16'
        metadata['status'] = patch['status']
        metadata['last_verified'] = '2026-09-16'
        metadata['verified_by'] = 'independent searchable classical-text cross-check'
    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Classical verification pass applied: records 14–18.')


if __name__ == '__main__':
    main()
