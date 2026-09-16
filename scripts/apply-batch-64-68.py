import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'plants.json'

BATCH = {
    'Pippali': {
        'identity': {'botanical_name':'Piper longum L.','family':'Piperaceae','english_name':'Long Pepper','synonyms':['Magadhi','Vaidehi','Kana','Krishna','Chapala']},
        'therapeutics': {'useful_part':['dried fruit (Phala)','root (Pippalimula)'],'indications':['Kasa','Shwasa','Pleeharoga','Jwara','Amavata','Agnimandya']},
        'dravya_guna': {'rasa':['katu'],'guna':['laghu','snigdha','tikshna'],'virya':'anushnasheeta','vipaka':'madhura','prabhava':'Rasayana / Kasahara / Shwasahara','karma':['Rasayana','Deepana','Pachana','Kasahara','Shwasahara','Vrishya','Pleehara']},
        'formulations':[{'name':'Vardhamana Pippali Rasayana'},{'name':'Pippalyasava'},{'name':'Trikatu Churna'},{'name':'Pippali Churna'},{'name':'Chavyadi Churna'}],
        'identification':{'description':'Cylindrical dark fruit spikes formed by fused berries, characteristically aromatic and pungent.'},
        'classical_reference':{'shlokas':[],'nighantu_references':['Bhavaprakasha Nighantu, Haritakyadi Varga — supplied verse/reference requires edition-level verification'],'shloka_reference_status':'needs_verification'},
    },
    'Shunthi': {
        'identity': {'botanical_name':'Zingiber officinale Roscoe','family':'Zingiberaceae','english_name':'Dry Ginger','synonyms':['Nagara','Vishvabhesaja','Mahoushadha','Shringavera']},
        'therapeutics': {'useful_part':['dried rhizome (Shushka Kanda)'],'indications':['Amavata','Agnimandya','Adhmana','Chhardi','Kasa','Shoola']},
        'dravya_guna': {'rasa':['katu'],'guna':['laghu','snigdha'],'virya':'ushna','vipaka':'madhura','prabhava':'Deepana / Pachana / Vata-Anulomana','karma':['Deepana','Pachana','Anulomana','Vrishya','Hridya','Shothahara','Kasahara']},
        'formulations':[{'name':'Saubhagya Shunthi Paka'},{'name':'Shunthi Churna'},{'name':'Trikatu Churna'},{'name':'Shunthi Ghrita'},{'name':'Rasnadi Kwatha'}],
        'identification':{'description':'Dried, buff to light-grey, branched rhizome with characteristic aromatic pungency.'},
        'classical_reference':{'shlokas':['नागरं दीपनं वृष्यं ग्राहि हृद्यं विबन्धनुत् ॥१६३॥\nरुच्यं लघु स्वादुपाकं स्निग्धोष्णं कफवातजित् ॥१६४॥'],'nighantu_references':[],'samhita_references':['Ashtanga Hridaya, Sutrasthana 6/163–164'],'shloka_reference_status':'verified text/reference; this is an Ashtanga Hridaya citation rather than the supplied Bhavaprakasha numbering'},
    },
    'Maricha': {
        'identity': {'botanical_name':'Piper nigrum L.','family':'Piperaceae','english_name':'Black Pepper','synonyms':['Vellaja','Krishna','Ushana','Dharmapattana']},
        'therapeutics': {'useful_part':['dried unripe fruit (Phala)'],'indications':['Agnimandya','Krimi','Sthoulya','Kasa','Shwasa','Pratishyaya']},
        'dravya_guna': {'rasa':['katu'],'guna':['laghu','ruksha','tikshna'],'virya':'ushna','vipaka':'katu','prabhava':'Pramathi / Deepana / Krimighna','karma':['Deepana','Pachana','Pramathi','Krimighna','Shirovirechana','Chedana','Kaphaghna']},
        'formulations':[{'name':'Trikatu Churna'},{'name':'Marichadi Gutika'},{'name':'Marichadi Taila'},{'name':'Talisadi Churna'},{'name':'Kankayana Vati'}],
        'identification':{'description':'Small globose, dark brown to black, reticulately wrinkled dried fruits with pungent aromatic taste.'},
        'classical_reference':{'shlokas':[],'nighantu_references':['Bhavaprakasha Nighantu, Haritakyadi Varga — supplied verse/reference requires edition-level verification'],'samhita_references':['Ashtanga Hridaya, Sutrasthana 6/161–162 describes Maricha and Pippali'],'shloka_reference_status':'needs_verification'},
    },
    'Twak': {
        'identity': {'botanical_name':'Cinnamomum verum J.Presl','family':'Lauraceae','english_name':'Cinnamon','synonyms':['Darusita','Utkata','Vara','Mukhashodhaka']},
        'therapeutics': {'useful_part':['inner stem bark (Twak)'],'indications':['Mukhadurgandhya','Agnimandya','Hridroga','Chhardi','Kasa','Pinasa']},
        'dravya_guna': {'rasa':['katu','tikta','madhura'],'guna':['laghu','ruksha','tikshna'],'virya':'ushna','vipaka':'katu','prabhava':'Mukhashodhaka / Hridya / Chhardighna','karma':['Deepana','Pachana','Mukhashodhaka','Hridya','Vata-anulomana','Vishaghna','Chhardighna']},
        'formulations':[{'name':'Sitopaladi Churna'},{'name':'Chaturjata Churna'},{'name':'Eladi Churna'},{'name':'Twak Kwatha'},{'name':'Khadiradi Vati'}],
        'identification':{'description':'Thin inner bark, usually in rolled or quilled pieces, yellowish-brown and strongly aromatic.'},
        'classical_reference':{'shlokas':['त्वक्पत्त्रं च वराङ्गं स्याद्भृङ्गं चोचं तथोत्कटं ।\nत्वचं लघूष्णं कटुकं स्वादु तिक्तं च रूक्षकं ॥६४॥\nपित्तलं कफवातघ्नं कण्ड्वामारुचिनाशनं ॥६५॥'],'nighantu_references':['Bhavaprakasha Nighantu, Karpuradi Varga, verses 64–65'],'shloka_reference_status':'verified searchable text; edition/page may vary'},
    },
    'Ela': {
        'identity': {'botanical_name':'Elettaria cardamomum (L.) Maton','family':'Zingiberaceae','english_name':'Small Cardamom','synonyms':['Sukshma','Dravidi','Truti','Korangi']},
        'therapeutics': {'useful_part':['seeds (Bija)','dried fruit capsule (Phala)'],'indications':['Chhardi','Mukhadurgandhya','Mutrakrichhra','Trishna','Kasa','Shwasa']},
        'dravya_guna': {'rasa':['katu','madhura'],'guna':['laghu','ruksha'],'virya':'sheeta','vipaka':'madhura','prabhava':'Mutrala / Chhardighna / Anulomana','karma':['Deepana','Pachana','Chhardighna','Mutrala','Hridya','Swarya','Mukhashodhaka']},
        'formulations':[{'name':'Eladi Churna'},{'name':'Eladi Gutika'},{'name':'Chaturjata Churna'},{'name':'Sitopaladi Churna'},{'name':'Eladi Ghrita'}],
        'identification':{'description':'Small aromatic greenish-yellow capsules containing numerous dark angular seeds.'},
        'classical_reference':{'shlokas':['सूक्ष्मोपकुञ्चिका तुत्था कोरङ्गी द्राविडी त्रुटिः ।\nएला सूक्ष्मा कफश्वासकासार्शोमूत्रकृच्छ्रहृत् ।\nरसे तु कटुका शीता लघ्वी वातहरी मता ॥६३॥'],'nighantu_references':['Bhavaprakasha Nighantu, Karpuradi Varga, verse 63'],'shloka_reference_status':'verified searchable text; edition numbering may vary'},
    },
}

with DATA.open(encoding='utf-8') as f:
    plants = json.load(f)

def merge(dst, src):
    if isinstance(src, dict):
        for k,v in src.items():
            if isinstance(v, dict):
                dst.setdefault(k, {})
                merge(dst[k], v)
            else:
                dst[k] = v
    else:
        return src

by_name = {p.get('identity',{}).get('name','').strip().lower(): p for p in plants}
for name, patch in BATCH.items():
    p = by_name.get(name.lower())
    if not p:
        raise SystemExit(f'Missing plant: {name}')
    merge(p, patch)
    p.setdefault('metadata', {})['last_enrichment'] = 'curated batch 64-68'

with DATA.open('w', encoding='utf-8') as f:
    json.dump(plants, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('Applied batch 64-68:', ', '.join(BATCH))
