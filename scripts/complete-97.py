import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
index = json.loads((ROOT / 'plant-index.json').read_text(encoding='utf-8'))['plants']
plants_path = ROOT / 'plants.json'
existing = json.loads(plants_path.read_text(encoding='utf-8')) if plants_path.exists() else []
by_id = {p['id']: p for p in existing}

# Botanical identity and principal prayojyanga for the syllabus drugs.
# The script preserves existing verified content and only fills genuinely missing structure.
D = {
'gokshura':('Tribulus terrestris L.','Zygophyllaceae','fruit'),'guduchi':('Tinospora cordifolia (Willd.) Hook.f. & Thomson','Menispermaceae','stem'),'guggulu':('Commiphora wightii (Arn.) Bhandari','Burseraceae','oleo-gum-resin'),'haridra':('Curcuma longa L.','Zingiberaceae','rhizome'),'haritaki':('Terminalia chebula Retz.','Combretaceae','fruit'),'hingu':('Ferula assa-foetida L.','Apiaceae','oleo-gum-resin'),'jambu':('Syzygium cumini (L.) Skeels','Myrtaceae','fruit/seed'),'jatamansi':('Nardostachys jatamansi (D.Don) DC.','Caprifoliaceae','rhizome'),'jyotishmati':('Celastrus paniculatus Willd.','Celastraceae','seed/oil'),'kanchanara':('Bauhinia variegata L.','Fabaceae','stem bark'),'kantakari':('Solanum xanthocarpum Schrad. & Wendl.','Solanaceae','whole plant/fruit'),'kapikachhu':('Mucuna pruriens (L.) DC.','Fabaceae','seed'),'karkatshrungi':('Pistacia integerrima J.L.Stewart ex Brandis','Anacardiaceae','gall'),'katuki':('Picrorhiza kurroa Royle ex Benth.','Plantaginaceae','rhizome'),'khadira':('Senegalia catechu (L.f.) P.J.Hurter & Mabb.','Fabaceae','heartwood'),'kumari':('Aloe vera (L.) Burm.f.','Asphodelaceae','leaf pulp'),'kutaja':('Holarrhena pubescens Wall. ex G.Don','Apocynaceae','stem bark/seed'),'latakaranja':('Caesalpinia bonduc (L.) Roxb.','Fabaceae','seed'),'lodhra':('Symplocos racemosa Roxb.','Symplocaceae','stem bark'),'agnimanth':('Premna integrifolia L.','Lamiaceae','root'),'ahiphena':('Papaver somniferum L.','Papaveraceae','latex'),'ajamoda':('Apium leptophyllum (Pers.) F.Muell. ex Benth.','Apiaceae','fruit'),'apamarga':('Achyranthes aspera L.','Amaranthaceae','whole plant'),'asthishrunkhala':('Cissus quadrangularis L.','Vitaceae','stem'),'bakuchi':('Cullen corylifolium (L.) Medik.','Fabaceae','seed'),'bruhati':('Solanum indicum L.','Solanaceae','root'),'chakramarda':('Senna tora (L.) Roxb.','Fabaceae','seed/whole plant'),'dhanyaka':('Coriandrum sativum L.','Apiaceae','fruit'),'ela':('Elettaria cardamomum (L.) Maton','Zingiberaceae','fruit/seed'),'gambhari':('Gmelina arborea Roxb.','Lamiaceae','root'),'japa':('Hibiscus rosa-sinensis L.','Malvaceae','flower'),'jatiphala':('Myristica fragrans Houtt.','Myristicaceae','seed'),'jeeraka':('Cuminum cyminum L.','Apiaceae','fruit'),'kalamegha':('Andrographis paniculata (Burm.f.) Nees','Acanthaceae','whole plant'),'kampillaka':('Mallotus philippensis (Lam.) Müll.Arg.','Euphorbiaceae','glandular powder of fruit'),'kulatha':('Macrotyloma uniflorum (Lam.) Verdc.','Fabaceae','seed'),'kumkum':('Crocus sativus L.','Iridaceae','stigma'),'lajjalu':('Mimosa pudica L.','Fabaceae','whole plant/root'),'lavanga':('Syzygium aromaticum (L.) Merr. & L.M.Perry','Myrtaceae','flower bud'),'madanphala':('Randia dumetorum (Retz.) Lam.','Rubiaceae','fruit'),'mandukaparni':('Centella asiatica (L.) Urb.','Apiaceae','whole plant'),'manjishta':('Rubia cordifolia L.','Rubiaceae','root'),'maricha':('Piper nigrum L.','Piperaceae','fruit'),'meshashrungi':('Gymnema sylvestre (Retz.) R.Br. ex Sm.','Apocynaceae','leaf'),'methika':('Trigonella foenum-graecum L.','Fabaceae','seed'),'musta':('Cyperus rotundus L.','Cyperaceae','rhizome'),'nagkeshar':('Mesua ferrea L.','Calophyllaceae','stamen'),'nimba':('Azadirachta indica A.Juss.','Meliaceae','bark/leaf'),'nirgundi':('Vitex negundo L.','Lamiaceae','leaf'),'palasha':('Butea monosperma (Lam.) Taub.','Fabaceae','seed/flower/bark'),'pashanabheda':('Bergenia ligulata (Wall.) Engl.','Saxifragaceae','rhizome'),'patha':('Cissampelos pareira L.','Menispermaceae','root'),'pippali':('Piper longum L.','Piperaceae','fruit'),'punarnava':('Boerhavia diffusa L.','Nyctaginaceae','root/whole plant'),'rasna':('Pluchea lanceolata (DC.) C.B.Clarke','Asteraceae','root'),'rasona':('Allium sativum L.','Amaryllidaceae','bulb'),'sarpagandha':('Rauvolfia serpentina (L.) Benth. ex Kurz','Apocynaceae','root'),'sairayak':('Barleria prionitis L.','Acanthaceae','root/whole plant'),'sariva':('Hemidesmus indicus (L.) R.Br.','Apocynaceae','root'),'shallaki':('Boswellia serrata Roxb. ex Colebr.','Burseraceae','oleo-gum-resin'),'shalmalimocharasa':('Bombax ceiba L.','Malvaceae','gum/mocharasa'),'shankhapushpi':('Convolvulus pluricaulis Choisy','Convolvulaceae','whole plant'),'shatavari':('Asparagus racemosus Willd.','Asparagaceae','root'),'shigru':('Moringa oleifera Lam.','Moringaceae','root/bark/leaf'),'shunthi':('Zingiber officinale Roscoe','Zingiberaceae','rhizome'),'talisapatra':('Abies webbiana Lindl.','Pinaceae','leaf'),'trivrut':('Operculina turpethum (L.) Silva Manso','Convolvulaceae','root bark'),'tulasi':('Ocimum tenuiflorum L.','Lamiaceae','leaf/whole plant'),'twak':('Cinnamomum verum J.Presl','Lauraceae','bark'),'usheera':('Chrysopogon zizanioides (L.) Roberty','Poaceae','root'),'vacha':('Acorus calamus L.','Acoraceae','rhizome'),'varuna':('Crataeva nurvala Buch.-Ham.','Capparaceae','stem bark'),'vasa':('Justicia adhatoda L.','Acanthaceae','leaf'),'vatsanabha':('Aconitum ferox Wall. ex Ser.','Ranunculaceae','root/tuber'),'vibhitaki':('Terminalia bellirica (Gaertn.) Roxb.','Combretaceae','fruit'),'vidanga':('Embelia ribes Burm.f.','Primulaceae','fruit'),'yashtimadhu':('Glycyrrhiza glabra L.','Fabaceae','root')}

# Safe defaults are intentionally labelled; they are not presented as verified classical data.
def scaffold(item, bot, family, part):
    return {
      'id': item['id'], 'order': item['order'],
      'identity': {'name':item['name'],'sanskrit_name':item.get('sanskrit_name',''),'transliteration':'','botanical_name':bot,'family':family,'english_name':'','hindi_name':'','regional_names':[],'synonyms':[]},
      'classification': {'kingdom':'Plantae','habit':'','habitat':'','distribution':''},
      'identification': {'description':'','whole_plant':'','root':'','stem':'','leaf':'','flower':'','fruit':'','seed':'','bark':'','identification_points':[]},
      'images': {'whole_plant':'','habit':'','root':'','stem':'','leaf':'','flower':'','fruit':'','seed':'','bark':''},
      'dravya_guna': {'rasa':[],'guna':[],'virya':'','vipaka':'','prabhava':'','karma':[]},
      'dosha': {'vata':'','pitta':'','kapha':''},
      'therapeutics': {'useful_part':[part] if part else [],'indications':[],'therapeutic_actions':[],'dose':'','anupana':'','duration':'','precautions':'','contraindications':''},
      'formulations': [],
      'classical_reference': {'shlokas':[],'nighantu_references':[],'samhita_references':[]},
      'phytochemistry': {'major_constituents':[],'chemical_notes':''},
      'modern_information': {'evidence_summary':'','recognized_uses':[],'safety_notes':'','sources':[]},
      'student': {'exam_points':[],'viva_questions':[],'identification_points':[],'mnemonics':[],'quick_revision':''},
      'teacher': {'teaching_points':[],'discussion_points':[],'practical_points':[]},
      'doctor': {'quick_reference':'','important_indications':[],'useful_part':part,'dose':'','anupana':'','key_precautions':[]},
      'sources': [
        {'type':'official_syllabus','title':'NCISM II BAMS Dravyaguna Vigyan curriculum','url':'https://www.ncismindia.org/NCISM_II%20BAMS_AyUG-DG.pdf'},
        {'type':'medicinal_plants_database','title':'TDU Indian Medicinal Plants Database','url':'https://www.tdu.edu.in/outreach/indian-medicinal-plants-database'}
      ],
      'metadata': {'status':'needs_classical_source_verification','last_verified':'','verified_by':'','version':'1.0'}
    }

for item in index:
    pid = item['id']
    if pid not in by_id:
        bot, family, part = D.get(pid, ('','',''))
        by_id[pid] = scaffold(item, bot, family, part)
    else:
        p = by_id[pid]
        # Preserve curated fields while ensuring the expanded schema exists.
        bot, family, part = D.get(pid, ('','',''))
        p.setdefault('identity', {})
        if bot and not p['identity'].get('botanical_name'): p['identity']['botanical_name'] = bot
        if family and not p['identity'].get('family'): p['identity']['family'] = family
        p.setdefault('therapeutics', {})
        if part and not p['therapeutics'].get('useful_part'): p['therapeutics']['useful_part'] = [part]
        for key, default in scaffold(item, bot, family, part).items():
            if key not in p: p[key] = default
        p.setdefault('sources', [])
        if not any(s.get('type') == 'official_syllabus' for s in p['sources']):
            p['sources'].append({'type':'official_syllabus','title':'NCISM II BAMS Dravyaguna Vigyan curriculum','url':'https://www.ncismindia.org/NCISM_II%20BAMS_AyUG-DG.pdf'})
        if not any(s.get('type') == 'medicinal_plants_database' for s in p['sources']):
            p['sources'].append({'type':'medicinal_plants_database','title':'TDU Indian Medicinal Plants Database','url':'https://www.tdu.edu.in/outreach/indian-medicinal-plants-database'})

out = [by_id[item['id']] for item in sorted(index,key=lambda x:x['order'])]
assert len(out) == len(index) and len({p['id'] for p in out}) == len(out)
ncism = [p for p in out if p.get('category', 'NCISM-97') == 'NCISM-97']
assert len(ncism) >= 97, f'Expected at least 97 NCISM records, found {len(ncism)}'
plants_path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Validated {len(out)} records, including {len(ncism)} NCISM records, with expanded schema and source metadata')
