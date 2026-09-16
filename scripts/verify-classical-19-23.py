import json
from pathlib import Path

PATH = Path('plants.json')
plants = json.loads(PATH.read_text(encoding='utf-8'))

PATCHES = {
    'Tulasi': {
        'shlokas': [
            'तुलसी सुरसा ग्राम्या सुलभा बहुमञ्जरी ।\nअपेतराक्षसी गौरी भूतघ्नी देवदुन्दुभिः ॥५०॥',
            'तुलसी कटुका तिक्ता हृद्योष्णा दाहपित्तकृत् ।\nदीपनी कुष्ठकृच्छ्रास्रपार्श्वरुक्कफवातजित् ।\nशुक्ला कृष्णा च तुलसी गुणैस्तुल्या प्रकीर्तिता ॥५१॥',
        ],
        'refs': ['Bhavaprakasha Nighantu, Pushpa Varga, 50–51 (UOH/DAV recension; edition numbering may vary)'],
        'sources': ['https://sanskrit.uohyd.ac.in/Corpus/Typed-Texts/bhava-prakash/bhavaprakashaha.html', 'https://davpharmacy.com/e-nighantu/'],
        'status': 'verified_text_location_edition_numbering_may_vary',
        'note': 'Gemini-submitted verses 62–63 were not retained; independently supported text and numbering from searchable Bhavaprakasha recensions are used.'
    },
    'Haridra': {
        'shlokas': [
            'हरिद्रा काञ्चनी पीता निशाख्या वरवर्णिनी ।\nकृमिघ्नी हलदी योषित्प्रिया हट्टविलासिनी ॥१९६॥',
            'हरिद्रा कटुका तिक्ता रूक्षोष्णा कफपित्तनुत् ।\nवर्ण्या त्वग्दोषमेहास्रशोथपाण्डुव्रणापहा ॥१९७॥',
        ],
        'refs': ['Bhavaprakasha Nighantu, Haritakyadi Varga, 196–197 (SanskritDocuments/PCIMH recension; another recension numbers these 171–172)'],
        'sources': ['https://sanskritdocuments.org/~sanskrit/doc_trial/fortransfer/bhAvaprakAshanighaNTu01_sa.html', 'https://pcimh.gov.in/'],
        'status': 'verified_text_location_edition_numbering_may_vary',
        'note': 'Text is independently supported; verse numbering varies among digital/printed recensions.'
    },
    'Twak': {
        'shlokas': [
            'त्वक्पत्रञ्च वराङ्गं स्याद् भृङ्गं चोचं तथोत्कटम् ॥६४॥',
            'त्वचं लघूष्णं कटुकं स्वादु तिक्तञ्च रूक्षकम् ।\nपित्तलं कफवातघ्नं कण्ड्वामारुचिनाशनम् ।\nहृद्बस्तिरोगवातार्शः कृमिपीनसशुक्रहृत् ॥६५॥',
        ],
        'refs': ['Bhavaprakasha Nighantu, Karpuradi Varga, 64–65 (Wikisource recension; another transcription numbers the passage 56–57)'],
        'sources': ['https://sa.wikisource.org/wiki/%E0%A4%AD%E0%A4%BE%E0%A4%B5%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%95%E0%A4%BE%E0%A4%B6%E0%A4%A8%E0%A4%BF%E0%A4%98%E0%A4%A3%E0%A5%8D%E0%A4%9F%E0%A5%81', 'https://vishvasa.github.io/sanskrit/koshaH/AyurvedaH/bhava-mishraH_bhAva-prakAshaH/03_3_karpUrAdivarga/'],
        'status': 'corrected_from_unverified_submission',
        'note': 'The Gemini-submitted Twak quotation was not found in the checked Bhavaprakasha recensions and was replaced by the independently supported passage.'
    },
    'Ela': {
        'shlokas': [
            'सूक्ष्मोपकुञ्चिका तुत्था कोरङ्गी द्राविडी त्रुटिः ।\nएला सूक्ष्मा कफश्वासकासार्शोमूत्रकृच्छ्रहृत् ।\nरसे तु कटुका शीता लघ्वी वातहरी मता ॥६३॥',
        ],
        'refs': ['Bhavaprakasha Nighantu, Karpuradi Varga, 63 (Wikisource/Vishvasa recension; edition numbering may vary)'],
        'sources': ['https://sa.wikisource.org/wiki/%E0%A4%AD%E0%A4%BE%E0%A4%B5%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%95%E0%A4%BE%E0%A4%B6%E0%A4%A8%E0%A4%BF%E0%A4%98%E0%A4%A3%E0%A5%8D%E0%A4%9F%E0%A5%81', 'https://vishvasa.github.io/sanskrit/koshaH/AyurvedaH/bhava-mishraH_bhAva-prakAshaH/03_3_karpUrAdivarga/'],
        'status': 'verified_text_location_edition_numbering_may_vary',
        'note': 'The independently supported Bhavaprakasha passage is used; the Gemini quotation was not retained.'
    },
    'Kutaja': {
        'shlokas': [
            'कुटजः कूटजः कीटो वत्सको गिरिमल्लिका ।\nकालिङ्गः शक्रशाखी च मल्लिकापुष्प इत्यपि ।\nइन्द्रो यवफलः प्रोक्तो वृक्षकः पाण्डुरद्रुमः ॥१०१॥',
            'कुटजः कटुको रूक्षो दीपनस्तुवरो हिमः ।\nअर्शोऽतिसारपित्तास्रकफतृष्णामकुष्ठनुत् ॥१०२॥',
        ],
        'refs': ['Bhavaprakasha Nighantu, Guduchyadi Varga, 101–102 (Vishvasa recension; edition numbering may vary)'],
        'sources': ['https://vishvasa.github.io/sanskrit/koshaH/AyurvedaH/bhava-mishraH_bhAva-prakAshaH/04_4_guDUchyAdivarga/'],
        'status': 'corrected_from_unverified_submission',
        'note': 'Gemini-submitted numbering 116–117 and quotation were not accepted; the independently searchable Bhavaprakasha passage is used.'
    },
}

for p in plants:
    name = p.get('identity', {}).get('name')
    if name not in PATCHES:
        continue
    patch = PATCHES[name]
    cr = p.setdefault('classical_reference', {})
    cr['shlokas'] = patch['shlokas']
    cr['nighantu_references'] = patch['refs']
    cr['verified_classical_sources'] = [
        {'type': 'classical_text_search', 'title': 'Independent searchable Bhavaprakasha recension', 'url': u,
         'note': 'Used for text-level verification; edition/recension numbering may vary.'}
        for u in patch['sources']
    ]
    cr['shloka_reference_status'] = patch['status']
    cr['verification_note'] = patch['note']
    meta = p.setdefault('metadata', {})
    meta['classical_review_batch'] = '19-23'
    meta['classical_review_date'] = '2026-09-16'
    meta['classical_review_method'] = 'independent text-level comparison; Gemini quotations not accepted without source confirmation'

PATH.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Applied independent classical verification for records 19-23.')
