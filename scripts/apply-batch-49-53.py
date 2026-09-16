import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'plants.json'

# Gemini batch IDs are matched by drug name, not NCISM order number.
# Classical verses supplied in this batch are retained as pending verification
# unless independently checked; structured drug data is still imported.
BATCH = {
    'Guggulu': {
        'identity': {'botanical_name': 'Commiphora wightii (Arn.) Bhandari', 'family': 'Burseraceae', 'english_name': 'Indian Bdellium / Guggul', 'synonyms': ['Devadhupa', 'Koushika', 'Pura', 'Mahishaksha', 'Palankasha']},
        'therapeutics': {'useful_part': ['purified oleo-gum resin (Shodhita Niryasa)'], 'indications': ['Amavata', 'Vatarakta', 'Medoroga', 'Sandhivata', 'Granthi/Arbuda', 'Kushta']},
        'dravya_guna': {'rasa': ['tikta', 'katu', 'kashaya', 'madhura'], 'guna': ['laghu', 'ruksha', 'tikshna', 'vishada', 'sukshma', 'sara'], 'virya': 'ushna', 'vipaka': 'katu', 'prabhava': 'Vedanasthapana / Medohara / Rasayana', 'karma': ['Medohara', 'Rasayana', 'Shothahara', 'Vedanasthapana', 'Vranaropana', 'Lekhana', 'Bhangasandhanakara']},
        'dosha': {'vata': 'generally pacifies', 'pitta': 'may increase; use according to context', 'kapha': 'pacifies'},
        'formulations': [{'name':'Yogaraja Guggulu'}, {'name':'Kaishora Guggulu'}, {'name':'Kanchanara Guggulu'}, {'name':'Triphala Guggulu'}, {'name':'Simhanada Guggulu'}],
        'identification': {'description': 'Irregular brownish-yellow translucent or sticky oleo-gum resin masses with strong balsamic aromatic odor.'},
        'classical_reference': {'shlokas': ['गुग्गुलुर्विशदस्तिक्तो वीर्योष्णः पित्तलः सरः ।\\nकषायः कटुकः पाके कटू रूक्षो लघुः परः ॥३५॥'], 'nighantu_references': ['Bhavaprakasha Nighantu, Karpuradi Varga, verses 35–36 (edition numbering may vary)'], 'shloka_reference_status': 'verified text/reference in searchable Bhavaprakasha recension; edition/page should be recorded separately'},
        'metadata': {'status': 'classical_text_checked'}
    },
    'Ashoka': {
        'identity': {'botanical_name': 'Saraca asoca (Roxb.) Willd.', 'family': 'Fabaceae', 'english_name': 'Ashoka Tree', 'synonyms': ['Hemapushpa', 'Kankelli', 'Vamadhara', 'Pindapushpa']},
        'therapeutics': {'useful_part': ['stem bark (Twak)', 'seeds (Bija)', 'flowers (Pushpa)'], 'indications': ['Asrigdara', 'Pradara', 'Yoniroga', 'Daha', 'Trishna', 'Apachi']},
        'dravya_guna': {'rasa': ['kashaya', 'tikta'], 'guna': ['laghu', 'ruksha'], 'virya': 'sheeta', 'vipaka': 'katu', 'prabhava': 'Asrigdarahara / Stri-rogahara', 'karma': ['Asrigdarahara', 'Garbhashaya-shothahara', 'Varnya', 'Hridya', 'Vranaropana', 'Sangrahi']},
        'dosha': {'vata': 'generally not aggravating', 'pitta': 'pacifies', 'kapha': 'pacifies'},
        'formulations': [{'name':'Ashokarishta'}, {'name':'Ashoka Ghrita'}, {'name':'Ashokaksheerapaka'}, {'name':'Chandanasava'}],
        'identification': {'description': 'Stem bark pieces are channelled or curved, with rough greyish-brown outer surface and reddish-brown inner surface; strongly astringent.'},
        'classical_reference': {'shlokas': ['अशोकः शीतलस्तिक्तो ग्राही वर्ण्यः कषायकः ।\\nदोषापचीतृषादाहकृमिशोषविषापहः ॥'], 'nighantu_references': ['Bhavaprakasha Nighantu, Vatadi Varga, verses 47–48'], 'shloka_reference_status': 'reference verified; searchable text supports the core verse, but edition-level transcription should be checked'},
        'metadata': {'status': 'classical_text_checked'}
    },
    'Bala': {
        'identity': {'botanical_name': 'Sida cordifolia L.', 'family': 'Malvaceae', 'english_name': 'Country Mallow', 'synonyms': ['Vatyalika', 'Batyala', 'Kharayashtika', 'Bhadra']},
        'therapeutics': {'useful_part': ['root', 'seeds', 'whole plant (Panchanga)'], 'indications': ['Vatavyadhi', 'Kshaya', 'Klaibya', 'Raktapitta', 'Daurbalya']},
        'dravya_guna': {'rasa': ['madhura'], 'guna': ['guru', 'snigdha', 'picchila'], 'virya': 'sheeta', 'vipaka': 'madhura', 'prabhava': 'Balya / Vrishya / Vataharanam', 'karma': ['Balya', 'Brimhana', 'Vrishya', 'Vatashamaka', 'Prajasthapana', 'Ojavardhaka']},
        'dosha': {'vata': 'pacifies', 'pitta': 'generally pacifies', 'kapha': 'may increase'},
        'formulations': [{'name':'Balarishta'}, {'name':'Bala Taila'}, {'name':'Kshirabala Taila'}, {'name':'Baladi Kwatha'}],
        'identification': {'description': 'Subshrub with cylindrical taproot, cordate velvety leaves and yellow solitary flowers; seeds are characteristic.'},
        'classical_reference': {'shlokas': [], 'nighantu_references': ['Bhavaprakasha Nighantu, Guduchyadi Varga — exact verse requires edition-level verification'], 'shloka_reference_status': 'needs_verification'},
        'metadata': {'status': 'structured_data_added_classical_text_pending'}
    },
    'Punarnava': {
        'identity': {'botanical_name': 'Boerhavia diffusa L.', 'family': 'Nyctaginaceae', 'english_name': 'Spreading Hogweed', 'synonyms': ['Shothaghni', 'Raktapunarnava', 'Varshabhu', 'Kathillaka', 'Prithvi']},
        'therapeutics': {'useful_part': ['root', 'whole plant (Panchanga)'], 'indications': ['Shotha', 'Pandu', 'Vrikkaroga', 'Hridroga with swelling', 'Udara Roga']},
        'dravya_guna': {'rasa': ['madhura', 'tikta', 'kashaya'], 'guna': ['laghu', 'ruksha'], 'virya': 'ushna', 'vipaka': 'madhura', 'prabhava': 'Shothahara / Mutrala', 'karma': ['Shothahara', 'Mutrala', 'Hridya', 'Deepana', 'Anulomana', 'Rasayana', 'Panduhara']},
        'dosha': {'vata': 'generally pacifies', 'pitta': 'generally pacifies', 'kapha': 'pacifies'},
        'formulations': [{'name':'Punarnavarishta'}, {'name':'Punarnavadi Kwatha'}, {'name':'Punarnavadi Mandoora'}, {'name':'Punarnavasava'}, {'name':'Punarnavadi Guggulu'}],
        'identification': {'description': 'Diffusely branched perennial herb with stout root, green upper leaf surface, pale/whitish lower surface and small pinkish-red flowers.'},
        'classical_reference': {'shlokas': [], 'nighantu_references': ['Bhavaprakasha Nighantu, Guduchyadi Varga — exact verse requires edition-level verification'], 'shloka_reference_status': 'needs_verification'},
        'metadata': {'status': 'structured_data_added_classical_text_pending'}
    },
    'Eranda': {
        'identity': {'botanical_name': 'Ricinus communis L.', 'family': 'Euphorbiaceae', 'english_name': 'Castor Oil Plant', 'synonyms': ['Gandharvahasta', 'Vatari', 'Rubu', 'Chitra', 'Urubuka']},
        'therapeutics': {'useful_part': ['root', 'leaves', 'seeds', 'seed oil (Eranda Taila)'], 'indications': ['Amavata', 'Vatavyadhi', 'Vibandha', 'Udavarta', 'Gulma']},
        'dravya_guna': {'rasa': ['madhura', 'katu', 'kashaya'], 'guna': ['sukshma', 'tikshna', 'snigdha', 'sara', 'guru'], 'virya': 'ushna', 'vipaka': 'madhura', 'prabhava': 'Virechana / Vataharanam', 'karma': ['Virechana', 'Vatashamaka', 'Vedanasthapana', 'Shothahara', 'Vrishya', 'Vayasthapana']},
        'dosha': {'vata': 'pacifies', 'pitta': 'may increase with excessive use', 'kapha': 'generally pacifies'},
        'formulations': [{'name':'Eranda Saptaka Kwatha'}, {'name':'Gandharvahastadi Taila'}, {'name':'Eranda Taila'}, {'name':'Rasnasaptaka Kwatha'}, {'name':'Simhanada Guggulu'}],
        'identification': {'description': 'Tall shrub with palmately lobed leaves, prickly three-celled fruits and smooth mottled seeds.'},
        'classical_reference': {'shlokas': [], 'nighantu_references': ['Bhavaprakasha Nighantu, Guduchyadi Varga — exact verse requires edition-level verification'], 'shloka_reference_status': 'needs_verification'},
        'metadata': {'status': 'structured_data_added_classical_text_pending'}
    },
    'Haridra': {
        'identity': {'botanical_name': 'Curcuma longa L.', 'family': 'Zingiberaceae', 'english_name': 'Turmeric', 'synonyms': ['Kanchani', 'Nisha', 'Gauri', 'Krimighni', 'Varavarnini']},
        'therapeutics': {'useful_part': ['rhizome (Kanda)'], 'indications': ['Prameha', 'Kushta', 'Pandu', 'Vrana', 'Sheetapitta', 'Pratishyaya']},
        'dravya_guna': {'rasa': ['tikta', 'katu'], 'guna': ['ruksha', 'laghu'], 'virya': 'ushna', 'vipaka': 'katu', 'prabhava': 'Varnya / Vishaghna / Pramehara', 'karma': ['Varnya', 'Krimighna', 'Kushtaghna', 'Vishaghna', 'Pramehara', 'Vranaropana', 'Raktashodhaka']},
        'dosha': {'vata': 'may increase when excessive', 'pitta': 'may increase when excessive', 'kapha': 'generally pacifies'},
        'formulations': [{'name':'Haridra Khanda'}, {'name':'Nisha Amalaki Churna'}, {'name':'Haridradi Ghrita'}, {'name':'Nimbadi Churna'}],
        'identification': {'description': 'Primary ovate or secondary cylindrical branched rhizomes with deep orange-yellow interior and characteristic aromatic odor.'},
        'classical_reference': {'shlokas': ['हरिद्रा कटुका तिक्ता वर्ण्योष्णा कफपित्तनुत् ।\\nविषदोषहरी कुष्ठकण्डूव्रणापहा ॥'], 'nighantu_references': ['Bhavaprakasha Nighantu, Haritakyadi Varga, verses 196–197; edition numbering should be checked'], 'shloka_reference_status': 'text checked against searchable recension; edition/page may vary'},
        'metadata': {'status': 'structured_data_added_classical_text_checked'}
    },
    'Aragvadha': {
        'identity': {'botanical_name': 'Cassia fistula L.', 'family': 'Fabaceae (Caesalpiniaceae)', 'english_name': 'Golden Shower Tree / Purging Cassia', 'synonyms': ['Rajavriksha', 'Shampaka', 'Chaturangula', 'Kritamala', 'Vyadhighata']},
        'therapeutics': {'useful_part': ['fruit pulp (Phala Majja)', 'stem bark (Twak)'], 'indications': ['Vibandha', 'Kushta', 'Jwara', 'Hridroga', 'Udarasula']},
        'dravya_guna': {'rasa': ['madhura'], 'guna': ['guru', 'mridu', 'snigdha'], 'virya': 'sheeta', 'vipaka': 'madhura', 'prabhava': 'Sramsi / Mridu Virechana', 'karma': ['Mridu Virechana', 'Sramsana', 'Kushtaghna', 'Jwarahara', 'Hridya', 'Kandughna']},
        'dosha': {'vata': 'generally not aggravating when appropriately used', 'pitta': 'pacifies', 'kapha': 'may reduce'},
        'formulations': [{'name':'Aragvadharishta'}, {'name':'Aragvadhadi Kwatha'}, {'name':'Aragvadhadi Leha'}, {'name':'Maha Manjisthadi Kwatha'}],
        'identification': {'description': 'Long cylindrical pendulous dark brown pods with transverse septa and sticky dark pulp.'},
        'classical_reference': {'shlokas': ['कर्णिकारो दीर्घफलः स्वर्णाङ्गः स्वर्णभूषणः ।\\nआरग्वधो गुरुः स्वादुः शीतलः स्रंसनोत्तमः ॥१४९॥\\nज्वरहृद्रोगपित्तास्रवातोदावर्त्तशूलनुत् ।\\nतत्फलं स्रंसनं रुच्यं कुष्ठपित्तकफापहम् ॥१५०॥\\nज्वरे तु सततं पथ्यं कोष्ठशुद्धिकरं परम् ॥१५१॥'], 'nighantu_references': ['Bhavaprakasha Nighantu, Haritakyadi Varga, verses 149–151'], 'shloka_reference_status': 'verified text/reference in searchable recension; edition numbering may vary'},
        'metadata': {'status': 'classical_text_checked'}
    },
    'Katuki': {
        'identity': {'botanical_name': 'Picrorhiza kurroa Royle ex Benth.', 'family': 'Plantaginaceae (Scrophulariaceae)', 'english_name': 'Hellebore / Picrorhiza', 'synonyms': ['Tikta', 'Katurohini', 'Matsyashakala', 'Chakrangi', 'Shataparva']},
        'therapeutics': {'useful_part': ['rhizome and root (Kanda / Mula)'], 'indications': ['Kamala', 'Jwara', 'Kushta', 'Prameha', 'Vibandha']},
        'dravya_guna': {'rasa': ['tikta'], 'guna': ['laghu', 'ruksha'], 'virya': 'sheeta', 'vipaka': 'katu', 'prabhava': 'Bhedana / Yakrit-rakshaka', 'karma': ['Bhedana', 'Deepana', 'Pachana', 'Jwarahara', 'Kamalahara', 'Hridya', 'Raktashodhaka']},
        'dosha': {'vata': 'may increase when excessive', 'pitta': 'pacifies', 'kapha': 'pacifies'},
        'formulations': [{'name':'Arogyavardhini Vati'}, {'name':'Katutrayadi Kwatha'}, {'name':'Katukadi Churna'}, {'name':'Mahatiktaka Ghrita'}],
        'identification': {'description': 'Cylindrical greyish-brown rhizomes with dark scale-leaf crowns and root scars; intensely bitter persistent taste.'},
        'classical_reference': {'shlokas': ['कट्वी तु कटुका तिक्ता कृष्णभेदा कटुम्भरा ।\\nकटुका कटुका पाके तिक्ता रूक्षा हिमा लघुः ।\\nभेदिनी दीपनी हृद्या कफपित्तज्वरापहा ॥'], 'nighantu_references': ['Bhavaprakasha Nighantu, Haritakyadi Varga; searchable recensions place the principal properties around verses 135–136, with edition variation'], 'shloka_reference_status': 'text/reference checked against searchable recension; supplied batch wording/numbering corrected'},
        'metadata': {'status': 'classical_text_checked'}
    },
    'Trivrit': {
        'identity': {'botanical_name': 'Operculina turpethum (L.) Silva Manso', 'family': 'Convolvulaceae', 'english_name': 'Indian Jalap / Turpeth', 'synonyms': ['Triputa', 'Sarala', 'Nishotra', 'Kumbha', 'Kuta']},
        'therapeutics': {'useful_part': ['root bark (Mula Twak)'], 'indications': ['Vibandha', 'Udara Roga', 'Shotha', 'Arsha', 'Pandu']},
        'dravya_guna': {'rasa': ['tikta', 'katu'], 'guna': ['laghu', 'ruksha', 'tikshna'], 'virya': 'ushna', 'vipaka': 'katu', 'prabhava': 'Sukha-Virechana', 'karma': ['Virechana', 'Sukha-Virechana', 'Kaphahara', 'Pittahara', 'Shothahara']},
        'dosha': {'vata': 'may increase if excessive', 'pitta': 'pacifies through virechana when appropriately used', 'kapha': 'pacifies'},
        'formulations': [{'name':'Avipattikar Churna'}, {'name':'Trivrit Lehyam'}, {'name':'Trivritadi Kwatha'}, {'name':'Abhayarishta'}],
        'identification': {'description': 'Long fleshy roots with central woody core, longitudinally furrowed dark reddish-brown bark and faint odor.'},
        'classical_reference': {'shlokas': ['त्रिवृत् तु कटुका तिक्ता रूक्षा सूक्ष्मा हिमाऽग्निजित् ।\\nसुखं विरेचयत्याशु पित्तश्लेष्मानिलापहा ॥'], 'nighantu_references': ['Bhavaprakasha Nighantu, Haritakyadi Varga; verse numbering varies by edition and should be checked'], 'shloka_reference_status': 'text/reference pending final edition-level verification'},
        'metadata': {'status': 'structured_data_added_classical_text_pending'}
    },
    'Kumari': {
        'identity': {'botanical_name': 'Aloe vera (L.) Burm.f. (syn. Aloe barbadensis Mill.)', 'family': 'Asphodelaceae (Liliaceae)', 'english_name': 'Indian Aloe / Aloe Vera', 'synonyms': ['Kanya', 'Grihakanya', 'Tarani', 'Vipulasrava']},
        'therapeutics': {'useful_part': ['leaf gel/pulp', 'dried resinous leaf juice (Elua)'], 'indications': ['Artavadosha / Rajorodha', 'Yakrit-Pleeharoga', 'Gulma', 'Vrana', 'Kushta']},
        'dravya_guna': {'rasa': ['tikta', 'madhura'], 'guna': ['guru', 'snigdha', 'picchila'], 'virya': 'sheeta', 'vipaka': 'madhura', 'prabhava': 'Bhedana / Artavajanana / Rasayana', 'karma': ['Bhedana', 'Brimhana', 'Vrishya', 'Rasayana', 'Artavajanana', 'Yakrit-Pleehadhara', 'Chakshushya']},
        'dosha': {'vata': 'generally pacifies', 'pitta': 'pacifies', 'kapha': 'may increase when excessive'},
        'formulations': [{'name':'Kumariasava'}, {'name':'Rajapravartini Vati'}, {'name':'Kumari Ghrita'}, {'name':'Kumari Taila'}],
        'identification': {'description': 'Sessile rosette succulent with thick fleshy lanceolate leaves, spiny margins and abundant translucent inner gel.'},
        'classical_reference': {'shlokas': ['कुमारी भेदनी शीता तिक्ता स्वाद्वी रसायनी ।\\nनेत्र्या वृष्या बल्या च वातपित्तविषापहा ॥'], 'nighantu_references': ['Bhavaprakasha Nighantu, Guduchyadi Varga; principal verse around 229–230 in searchable recensions'], 'shloka_reference_status': 'text/reference pending final edition-level verification'},
        'metadata': {'status': 'structured_data_added_classical_text_pending'}
    },
    'Vasa': {
        'identity': {'botanical_name': 'Adhatoda vasica Nees (syn. Justicia adhatoda L.)', 'family': 'Acanthaceae', 'english_name': 'Malabar Nut', 'synonyms': ['Vasaka', 'Vasika', 'Singhasya', 'Vajradanti', 'Bhishagmata']},
        'therapeutics': {'useful_part': ['leaves', 'root', 'flowers'], 'indications': ['Kasa', 'Shwasa', 'Raktapitta', 'Kshayaja Kasa', 'Jwara']},
        'dravya_guna': {'rasa': ['tikta', 'kashaya'], 'guna': ['laghu', 'ruksha'], 'virya': 'sheeta', 'vipaka': 'katu', 'prabhava': 'Kasahara / Shwasahara / Raktapittahara', 'karma': ['Kasahara', 'Shwasahara', 'Raktapittahara', 'Kaphaghna', 'Hridya', 'Swarya', 'Jwarahara']},
        'dosha': {'vata': 'may increase when excessive', 'pitta': 'pacifies', 'kapha': 'pacifies'},
        'formulations': [{'name':'Vasavaleha'}, {'name':'Vasarishta'}, {'name':'Vasadi Kwatha'}, {'name':'Vasakasava'}, {'name':'Vasadi Ghrita'}],
        'identification': {'description': 'Broad lanceolate leaves with prominent pinnate venation and white two-lipped flowers resembling a lion mouth.'},
        'classical_reference': {'shlokas': [], 'nighantu_references': ['Bhavaprakasha Nighantu, Guduchyadi Varga; searchable recensions place the principal Vasa properties around verses 68–78 depending on edition'], 'shloka_reference_status': 'needs_verification'},
        'metadata': {'status': 'structured_data_added_classical_text_pending'}
    },
    'Nimba': {
        'identity': {'botanical_name': 'Azadirachta indica A. Juss.', 'family': 'Meliaceae', 'english_name': 'Neem / Margosa Tree', 'synonyms': ['Picumarda', 'Arishta', 'Niyanta', 'Ravipriya', 'Netravi']},
        'therapeutics': {'useful_part': ['bark', 'leaves', 'seeds', 'seed oil', 'whole plant (Panchanga)'], 'indications': ['Kushta', 'Krimi', 'Vrana', 'Jwara', 'Prameha']},
        'dravya_guna': {'rasa': ['tikta', 'kashaya'], 'guna': ['laghu', 'ruksha'], 'virya': 'sheeta', 'vipaka': 'katu', 'prabhava': 'Kushtaghna / Kandughna / Krimighna', 'karma': ['Kushtaghna', 'Krimighna', 'Kandughna', 'Vrana-shodhaka', 'Vrana-ropana', 'Jwaraghna', 'Raktashodhaka']},
        'dosha': {'vata': 'may increase when excessive', 'pitta': 'pacifies', 'kapha': 'pacifies'},
        'formulations': [{'name':'Nimbadi Churna'}, {'name':'Nimbaharidradi Churna'}, {'name':'Nimbadi Kwatha'}, {'name':'Nimbadi Taila'}, {'name':'Jatyadi Taila'}],
        'identification': {'description': 'Large evergreen tree with pinnate leaves, serrated leaflets, small fragrant white flowers and yellow ripe drupes.'},
        'classical_reference': {'shlokas': [], 'nighantu_references': ['Bhavaprakasha Nighantu, Guduchyadi Varga; searchable recension places Nimba properties around verses 73–76'], 'shloka_reference_status': 'needs_verification'},
        'metadata': {'status': 'structured_data_added_classical_text_pending'}
    },
    'Bhringaraja': {
        'identity': {'botanical_name': 'Eclipta alba (L.) Hassk. (syn. Eclipta prostrata (L.) L.)', 'family': 'Asteraceae (Compositae)', 'english_name': 'False Daisy', 'synonyms': ['Markava', 'Kesharaja', 'Pitripriya', 'Bhringa', 'Angaraka']},
        'therapeutics': {'useful_part': ['whole plant (Panchanga)'], 'indications': ['Palita / Khalitya', 'Shiro-roga', 'Yakrit-Pleeha Roga', 'Pandu', 'Kushta']},
        'dravya_guna': {'rasa': ['katu', 'tikta'], 'guna': ['ruksha', 'laghu'], 'virya': 'ushna', 'vipaka': 'katu', 'prabhava': 'Keshya / Rasayana', 'karma': ['Keshya', 'Rasayana', 'Shothahara', 'Yakrit-uttejaka', 'Shirorogahara', 'Varnya']},
        'dosha': {'vata': 'may increase when excessive', 'pitta': 'generally pacifies', 'kapha': 'pacifies'},
        'formulations': [{'name':'Bhringaraja Taila'}, {'name':'Mahabhringaraja Taila'}, {'name':'Bhringarajasava'}, {'name':'Shadbindu Taila'}],
        'identification': {'description': 'Small erect or prostrate annual herb with lanceolate sessile hairy leaves and small white solitary capitula.'},
        'classical_reference': {'shlokas': [], 'nighantu_references': ['Bhavaprakasha Nighantu, Guduchyadi Varga; exact Bhringaraja verse and edition numbering require text-level verification'], 'shloka_reference_status': 'needs_verification'},
        'metadata': {'status': 'structured_data_added_classical_text_pending'}
    },
    'Yashtimadhu': {
        'identity': {'botanical_name': 'Glycyrrhiza glabra L.', 'family': 'Fabaceae (Papilionaceae)', 'english_name': 'Licorice / Liquorice', 'synonyms': ['Madhuka', 'Klitaka', 'Yashtyahva', 'Madhuvana', 'Jalamadhuka']},
        'therapeutics': {'useful_part': ['stolons and roots'], 'indications': ['Swarabheda', 'Vrana', 'Kasa', 'Daha', 'Vatarakta', 'Daurbalya']},
        'dravya_guna': {'rasa': ['madhura'], 'guna': ['guru', 'snigdha'], 'virya': 'sheeta', 'vipaka': 'madhura', 'prabhava': 'Varnya / Keshya / Swarya / Vrishya', 'karma': ['Swarya', 'Varnya', 'Keshya', 'Vrishya', 'Chakshushya', 'Balya', 'Vranaropana', 'Pittashamaka']},
        'dosha': {'vata': 'pacifies', 'pitta': 'pacifies', 'kapha': 'may increase when excessive'},
        'formulations': [{'name':'Yashtimadhu Churna'}, {'name':'Yashtimadhu Taila'}, {'name':'Yashtimadhu Kwatha'}, {'name':'Shatavari Ghrita'}, {'name':'Chandanasava'}],
        'identification': {'description': 'Cylindrical yellowish-brown roots and stolons with longitudinal striations, fibrous fracture and intensely sweet taste.'},
        'classical_reference': {'shlokas': [], 'nighantu_references': ['Bhavaprakasha Nighantu, Haritakyadi Varga; principal Yashtimadhu passage around verses 145–146 in searchable recensions'], 'shloka_reference_status': 'needs_verification'},
        'metadata': {'status': 'structured_data_added_classical_text_pending'}
    },
    'Bhallataka': {
        'identity': {'botanical_name': 'Semecarpus anacardium L.f.', 'family': 'Anacardiaceae', 'english_name': 'Marking Nut', 'synonyms': ['Arushkara', 'Agnimukha', 'Tapana', 'Dahana', 'Shoshana']},
        'therapeutics': {'useful_part': ['fruit; purified drug only (Shodhita Phala)'], 'indications': ['Arsha', 'Gulma', 'Kaphaja Roga', 'Kushta', 'Krimi', 'Amavata']},
        'dravya_guna': {'rasa': ['katu', 'tikta', 'kashaya'], 'guna': ['laghu', 'snigdha', 'tikshna'], 'virya': 'ushna', 'vipaka': 'madhura', 'prabhava': 'Kapha-Vatahara / Rasayana / Bhedana', 'karma': ['Rasayana', 'Deepana', 'Pachana', 'Bhedana', 'Krimighna', 'Vrana-shodhana', 'Chedana', 'Arshoghna']},
        'dosha': {'vata': 'pacifies', 'pitta': 'may increase; strong care required', 'kapha': 'pacifies'},
        'formulations': [{'name':'Bhallataka Rasayana'}, {'name':'Sanjeevani Vati'}, {'name':'Amrita Bhallataka Leha'}, {'name':'Bhallataka Parpati'}, {'name':'Bhallataka Taila'}],
        'identification': {'description': 'Ovoid black drupe seated on a fleshy orange-yellow receptacle; pericarp contains acrid oily juice that can severely irritate skin when unprocessed.'},
        'classical_reference': {'shlokas': [], 'nighantu_references': ['Bhavaprakasha Nighantu, Haritakyadi Varga; supplied verse/citation requires text-level verification'], 'shloka_reference_status': 'needs_verification'},
        'metadata': {'status': 'structured_data_added_classical_text_pending'}
    }
}

def merge(dst, src):
    for key, value in src.items():
        if isinstance(value, dict):
            merge(dst.setdefault(key, {}), value)
        else:
            dst[key] = value

plants = json.loads(DATA.read_text(encoding='utf-8'))
found = set()
for plant in plants:
    name = plant.get('identity', {}).get('name', '')
    if name in BATCH:
        merge(plant, BATCH[name])
        plant.setdefault('metadata', {})['batch_54_63_added'] = True
        found.add(name)

missing = sorted(set(BATCH) - found)
if missing:
    raise SystemExit(f'Missing expected drug records: {missing}')

DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Applied batch 54–63 data to:', ', '.join(sorted(found)))
