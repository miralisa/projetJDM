
drop database jdm;
create database jdm;
use jdm;
create table noeuds (
	eid int primary key,
	name varchar(1000),
	type smallint,
	weight int,
	definition varchar(20000),
	nf varchar(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table type_relation (
	name varchar(24) primary key,
	nom_etendu varchar(27),
	info varchar(315)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table name_noeud (
	name varchar(1000),
	INDEX ind_name (name(10))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO type_relation VALUES
("r_associated","idée associée","Il est demandé d'énumérer les termes les plus étroitement associés au mot cible... Ce mot vous fait penser à quoi ?"),
("r_raff_sem","raffinement sémantique","Raffinement sémantique vers un usage particulier du terme source"),
("r_raff_morpho","raffinement morphologique","Raffinement morphologique vers un usage particulier du terme source"),
("r_domain","domaine","Il est demandé de fournir des domaines relatifs au mot cible. Par exemple, pour 'corner', on pourra donner les domaines 'football' ou 'sport'."),
("r_pos","POS","Partie du discours (Nom, Verbe, Adjectif, Adverbe, etc.)"),
("r_syn","synonyme","Il est demandé d'énumérer les synonymes ou quasi-synonymes de ce terme."),
("r_isa","générique","Il est demandé d'énumérer les GENERIQUES/hyperonymes du terme. Par exemple, 'animal' et 'mammifère' sont des génériques de 'chat'."),
("r_anto","contraire","Il est demandé d'énumérer des contraires du terme. Par exemple, 'chaud' est le contraire de 'froid'."),
("r_hypo","spécifique","Il est demandé d'énumérer des SPECIFIQUES/hyponymes du terme. Par exemple, 'mouche', 'abeille', 'guêpe' pour 'insecte'."),
("r_has_part","partie","Il faut donner des PARTIES/constituants/éléments (a pour méronymes) du mot cible. Par exemple, 'voiture' a comme parties : 'porte', 'roue', 'moteur', ..."),
("r_holo","tout","Il est démandé d'énumérer des 'TOUT' (a pour holonymes)  de l'objet en question. Pour 'main', on aura 'bras', 'corps', 'personne', etc... Le tout est aussi l'ensemble comme 'classe' pour 'élève'."),
("r_locution","locution","A partir d'un terme, il est demandé d'énumérer les locutions, expression ou mots composés en rapport avec ce terme. Par exemple, pour 'moulin', ou pourra avoir 'moulin à vent', 'moulin à eau', 'moulin à café'. Pour 'vendre', on pourra avoir 'vendre la peau de l'ours avant de l'avoir tué', 'vendre à perte', etc.."),
("r_agent","action>agent","L'agent (qu'on appelle aussi le sujet) est l'entité qui effectue l'action, OU la subit pour des formes passives ou des verbes d'état. Par exemple, dans - Le chat mange la souris -, l'agent est le chat. Des agents typiques de 'courir' peuvent être 'sportif', 'enfant',..."),
("r_patient","action>patient","Le patient (qu'on appelle aussi l'objet) est l'entité qui subit l'action. Par exemple dans - Le chat mange la souris -, le patient est la souris. Des patients typiques de manger peuvent être 'viande', 'légume', 'pain', ..."),
("r_flpot"," 	r_flpot","(relation interne) potentiel de relation"),
("r_lieu","chose>lieu","Il est demandé d'énumérer les LIEUX typiques où peut se trouver le terme/objet en question."),
("r_instr","action>instrument","L'instrument est l'objet avec lequel on fait l'action. Dans - Il mange sa salade avec une fourchette -, fourchette est l'instrument. Des instruments typiques de 'tuer' peuvent être 'arme', 'pistolet', 'poison', ..."),
("r_carac","caractéristique","Pour un terme donné, souvent un objet, il est demandé d'en énumérer les CARACtéristiques (adjectifs) possibles/typiques. Par exemple, 'liquide', 'froide', 'chaude', pour 'eau'."),
("r_data","r_data","Informations diverses (plutôt d'ordre lexicales)"),
("r_lemma","r_lemma","Le lemme (par exemple 'mangent a pour lemme  'manger' ; 'avions' a pour lemme 'avion' ou 'avoir')."),
("r_magn","magn","La magnification ou amplification, par exemple - forte fièvre - ou - fièvre de cheval - pour fièvre. Ou encore - amour fou - pour amour, - peur bleue - pour peur."),
("r_antimagn","antimagn","L'inverse de la magnification, par exemple - bruine - pour pluie."),
("r_family","famille","Des mots de la même famille lexicale sont demandés (dérivation morphologique, par exemple). Par exemple, pour 'lait' on pourrait mettre 'laitier', 'laitage', 'laiterie', etc."),
("r_carac-1","caractéristique-1","Quels sont les objets (des noms) possédant typiquement/possiblement la caractérisque suivante ? Par exemple, 'soleil', 'feu', pour 'chaud'."),
("r_agent-1","agent typique-1","Que peut faire ce SUJET ? (par exemple chat => miauler, griffer, etc.)"),
("r_instr-1","instrument>action","L'instrument est l'objet avec lequel on fait l'action. Dans - Il mange sa salade avec une fourchette -, fourchette est l'instrument. On demande ici, ce qu'on peut faire avec un instrument donné..."),
("r_patient-1","patient-1","(inverse de r_patient) Que peut-on faire à cet OBJET. Pour 'pomme', on pourrait avoir 'manger', 'croquer', couper', 'éplucher',  etc."),
("r_domain-1","domaine-1","inverse de r_domain : à un domaine, on associe des termes"),
("r_lieu-1","lieu>chose","A partir d'un lieu, il est demandé d'énumérer ce qui peut typiquement s'y trouver."),
("r_chunk_pred","predicat","(interne) d'un prédicat quel chunk ?"),
("r_lieu_action","lieu>action","A partir d'un lieu, énumérer les actions typiques possibles dans ce lieu."),
("r_action_lieu","action>lieu","A partir d'une action (un verbe), énumérer les lieux typiques possibles où peut être réalisée cette action."),
("r_sentiment","sentiment","Pour un terme donné, évoquer des mots liés à des SENTIMENTS ou des EMOTIONS que vous pourriez associer à ce terme. Par exemple, la joie, le plaisir, le dégoût, la peur, la haine, l'amour, l'indifférence, l'envie, avoir peur, horrible, etc."),
("r_error","erreur","lien d'erreur"),
("r_manner","manière","De quelles MANIERES peut être effectuée l'action (le verbe) proposée. Il s'agira d'un adverbe ou d'un équivalent comme une locution adverbiale, par exemple : 'rapidement', 'sur le pouce', 'goulûment', 'salement' ... pour 'manger'."),
("r_meaning","sens/signification","Quels SENS/SIGNIFICATIONS pouvez vous donner au terme proposé. Il s'agira de termes évoquant chacun des sens possibles, par exemple : 'forces de l'ordre', 'contrat d'assurance', 'police typographique', ... pour 'police'."),
("r_infopot","information potentielle","Information sémantique potentielle"),
("r_telic_role","rôle télique","Le rôle télique indique le but ou la fonction du nom ou du verbe. Par exemple, couper pour couteau, scier pour scie, etc. C'est le rôle qu'on lui destine communément pour un artéfact, ou bien un rôle qu'on peut attribuer à un objet naturel (réchauffer, éclairer pour soleil)."),
("r_agentif_role","rôle agentif","De quelle(s)  manière(s)  peut être CRÉE/CONSTRUIT le terme suivant. On demande des verbes transitifs (le terme en est un complément d'objet) qui DONNENT NAISSANCE à l'entité désignée par le terme,  par exemple, 'construire' pour 'maison', 'rédiger'/'imprimer' pour 'livre' ou 'lettre'."),
("r_verbe-action","verbe>action","du verbe vers l'action. Par exemple, construire -> construction , jardiner -> jardinage . C'est un terme directement dérivé (ayant la même racine). Applicable que pour un verbe et inverse de la relation 40 (action vers verbe)."),
("r_action-verbe","action>verbe","de l'action vers le verbe. Par exemple, construction -> construire, jardinage -> jardiner. C'est un terme directement dérivé (ayant la même racine). Applicable que pour un nom et inverse de la relation 39 (verbe vers action)."),
("r_causatif","cause","B (que vous devez donner) est une CAUSE possible de A. A et B sont des verbes ou des noms.  Exemples : se blesser -> tomber ; vol -> pauvreté ; incendie -> négligence ; mort --> maladie ; etc."),
("r_conseq","conséquence","B (que vous devez donner) est une CONSEQUENCE possible de A. A et B sont des verbes ou des noms.  Exemples : tomber -> se blesser ; faim -> voler ; allumer -> incendie ; négligence --> accident ; etc."),
("r_adj-verbe","adj>verbe","Pour un adjectif de potentialité/possibilité, son verbe correspondant. Par exemple pour 'lavable' -> 'laver'"),
("r_verbe-adj","verbe>adj","Pour un verbe, son adjectif de potentialité/possibilité correspondant. Par exemple pour 'laver' -> 'lavable'"),
("r_chunk_sujet","r_chunk_sujet","(interne)"),
("r_chunk_objet","r_chunk_objet","(interne)"),
("r_chunk_loc","r_chunk_loc","(interne)"),
("r_chunk_instr","r_chunk_instr","(interne)"),
("r_aki","r_aki","(TOTAKI) equivalent pour TOTAKI de l'association libre"),
("r_time","action>temps","Donner une valeur temporelle -quel moment- peut-on associer au terme indiqué (par exemple 'dormir' -> nuit, 'bronzer' -> été, 'fatigue' -> 'soir')"),
("r_prev","r_prev","(interne)"),
("r_succ","r_succ","(interne)"),
("r_inhib","r_inhib","relation d'inhibition, le terme inhibe les termes suivants... ce terme a tendance à exclure le terme associé."),
("r_object>mater","objet>matiere","Quel est la ou les MATIERE/SUBSTANCE pouvant composer l'objet qui suit. Par exemple, 'bois' pour 'poutre'."),
("r_mater>object","matière>objet","Quel est la ou les CHOSES qui sont composés de la MATIERE/SUBSTANCE qui suit (exemple 'bois' -> poutre, table, ...)."),
("r_successeur-time","successeur","Qu'est ce qui peut SUIVRE temporellement (par exemple Noêl -> jour de l'an, guerre -> paix, jour -> nuit,  pluie -> beau temps, repas -> sieste, etc) le terme suivant :"),
("r_make","produit","Que peut PRODUIRE le terme ? (par exemple abeille -> miel, usine -> voiture, agriculteur -> blé,  moteur -> gaz carbonique ...)"),
("r_product_of","est le produit de","Le terme est le RESULTAT/PRODUIT de qui/quoi ?"),
("r_against","s'oppose à","A quoi le terme suivant S'OPPOSE/COMBAT/EMPECHE ? Par exemple, un médicament s'oppose à la maladie."),
("r_against-1","a comme opposition","Inverse de r_against (s'oppose à) - a comme opposition active (S'OPPOSE/COMBAT/EMPECHE). Par exemple, une bactérie à comme opposition antibiotique."),
("r_implication","implication","Qu'est-ce que le terme implique logiquement ? Par exemple : ronfler implique dormir, courir implique se déplacer, câlin implique contact physique. (attention ce n'est pas la cause ni le but...)"),
("r_quantificateur","quantificateur","Quantificateur(s) typique(s) pour le terme,  indiquant une quantité. Par exemples, sucre -> grain, morceau - sel -> grain, pincée - herbe -> brin, touffe - ..."),
("r_masc","équivalent masc","L'équivalent masculin du terme : lionne --> lion."),
("r_fem","équivalent fem","L'équivalent féminin du terme : lion --> lionne."),
("r_equiv","équivalent","Termes strictement équivalent/identique : acronymes et sigles (PS -> parti socialiste), apocopes (ciné -> cinéma), entités nommées (Louis XIV -> Le roi soleil), etc. (attention il ne s'agit pas de synonyme)"),
("r_manner-1","maniere-1","Quelles ACTIONS (verbes) peut-on effectuer de cette manière ? Par exemple, rapidement -> courir, manger, ..."),
("r_agentive_implication","implication agentive","Les verbes ou actions qui sont impliqués dans la création de l'objet. Par exemple pour 'construire' un livre, il faut, imprimer, relier, brocher, etc. Il s'agit des étapes nécessaires à la réalisation du rôle agentif."),
("r_instance","instance","Une instance d'un 'type' est un individu particulier de ce type. Il s'agit d'une entité nommée (personne, lieu, organisation, etc) - par exemple, 'Jolly Jumper' est une instance de 'cheval', 'Titanic' en est une de 'transatlantique'."),
("r_verb_real","verbe>real","Pour un verbe, celui qui réalise l'action (par dérivation morphologique). Par exemple, chasser -> chasseur, naviguer -> navigateur."),
("r_termgroup","r_termgroup",""),
("r_chunk_head","r_chunk_head",""),
("r_similar","similaire","Similaire/ressemble à ; par exemple le congre est similaire à une anguille, ..."),
("r_set>item","ensemble>item","Quel est l'ELEMENT qui compose l'ENSEMBLE qui suit (par exemple, un essaim est composé d'aveilles)"),
("r_item>set","item>ensemble","Quel est l'ENSEMBLE qui est composé de l'ELEMENT qui suit (par exemple, un essaim est composé d'aveilles)"),
("r_processus>agent","processus>agent","Quel est l'acteur de ce processus/événement ? Par exemple,  'nettoyage' peut avoir comme acteur 'technicien de surface'."),
("r_variante","variante","Variantes du termes cible. Par exemple, yaourt, yahourt, ou encore évènement, événement."),
("r_has_personnage","a comme personnages","Quels sont les personnages présents dans l'oeuvre qui suit ?"),
("r_has_auteur","a comme auteur","Quel est l'auteur de l'oeuvre suivante ?"),
("r_can_eat","se nourrit de","De quoi peut se nourir l'animal suivant ?"),
("r_syn_strict","r_syn_strict","Termes strictement substituables, pour des termes hors du domaine général, et pour la plupart des noms (exemple : endométriose intra-utérine --> adénomyose)"),
("r_has_actors","a comme acteurs","A comme acteurs (pour un film ou similaire)."),
("r_deplac_mode","mode de déplacement","Mode de déplacement"),
("r_der_morpho","dérivation morphologique","Des termes dériviés morphologiquement sont demandés). Par exemple, pour 'lait' on pourrait mettre 'laitier', 'laitage', 'laiterie', etc. (mais pas 'lactose'). Pour 'jardin', on mettra 'jardinier', 'jardinage', 'jardiner', etc. "),
("r_has_interpret","a comme interprètes",""),
("r_color","couleur","A comme couleur(s)..."),
("r_learning_model","r_learning_model",""),
("r_wiki","r_wiki","Associations issues de wikipedia..."),
("r_annotation","r_annotation",""),
("r_cible","a comme cible","Cible de la maladie : myxomatose => lapin, rougeole => enfant, ..."),
("r_symptomes","a comme symptomes","Symptomes de la maladie : myxomatose => yeux rouges, rougeole => boutons, ..."),
("r_annotation_exception","r_annotation_exception",""),
("r_predecesseur-time","prédécesseur","Qu'est ce qui peut PRECEDER temporellement (par exemple -  inverse de successeur) le terme suivant :"),
("r_diagnostique","diagnostique","Diagnostique pour la maladie : diabète => prise de sang, rougeole => examen clinique, ..."),
("r_is_smaller_than","est plus petit que","Qu'est-ce qui est physiquement plus gros que... (la comparaison doit être pertinente)"),
("r_is_bigger_than","est plus gros que","Qu'est-ce qui est physiquement moins gros que... (la comparaison doit être pertinente)"),
("r_accomp","accompagne","Est souvent accompagné de, se trouve avec... Par exemple : Astérix et Obelix, le pain et le fromage, les fraises et la chantilly."),
("r_predecesseur-space","prédécesseur","Qu'est ce qui peut PRECEDER spatialement (par exemple -  inverse de successeur spatial) le terme suivant :"),
("r_successeur-space","successeur","Qu'est ce qui peut SUIVRE spatialement (par exemple Locomotive à vapeur -> tender, wagon etc.) le terme suivant :"),
("r_beneficiaire","action>bénéficiaire","Le bénéficiaire est l'entité qui tire bénéfice/préjudice de l'action (un complément d'objet indirect introduit par 'à', 'pour', ...). Par exemple dans - La sorcière donne une pomme à Blanche Neige -, la bénéficiaire est Blanche Neige ... enfin, bref, vous avez compris l'idée."),
("r_descend_de","descend de","Descend de (évolution)..."),
("r_social_tie","relation sociale/famille","Relation sociale entre les individus..."),
("r_tributary","r_tributary",""),
("r_sentiment-1","sentiment-1","Pour un SENTIMENT ou EMOTION donné, il est demandé d'énumérer les termes que vous pourriez associer. Par exemple, pour 'joie', on aurait 'cadeau', 'naissance', 'bonne nouvelle', etc."),
("r_linked-with","linked-with","A quoi est-ce relié (un wagon est relié à un autre wagon ou à une locomotive) ?"),
("r_domain_subst","domain_subst","Quels sont le ou les domaines de substitution pour ce terme quand il est utilisé comme domaine (par exemple, 'muscle' => 'anatomie du système musculaire')"),
("r_prop","propriété","Pour le terme donné, il faut indiquer les noms de propriétés pertinents (par exemple pour 'voiture', le 'prix', la 'puissance', la 'longueur', le 'poids', etc. On ne met que des noms et pas des adjectifs)."),
("r_foncteur","r_foncteur","La fonction de ce terme par rapport à d'autres. Pour les prépositions notamment, 'chez' => relation r_location. (demande un type de relation comme valeur)"),
("r_comparison","r_comparison",""),
("r_but","r_but","But de l'action"),
("r_processus>patient","processus>patient","Quel est le patient de ce processus/événement ? Par exemple,  'découpe' peut avoir comme patient 'viande'."),
("r_but-1","r_but-1","Quel sont les action ou verbe qui le terme cible comme but ?"),
("r_own","pers>possession","Que POSSEDE le terme suivant ? (un soldat possède un fusil, une cavalière des bottes, ...)"),
("r_own-1","possession>pers","Qui ou quoi POSSEDE le terme suivant ? (par exemple, soldat r_own fusil)"),
("r_compl_agent","complément d'agent","Le complément d'agent est celui qui effectue l'action dans les formes passives. Par exemple, pour 'être mangé', la souris est l'agent et le chat le complément d'agent."),
("r_activ_voice","voix active","Pour un verbe à la voix passive, sa voix active. Par exemple, pour 'être mangé' on aura 'manger'."),
("r_cooccurrence","r_cooccurrence",""),
("r_make_use_of","r_make_use_of",""),
("r_is_used_by","r_is_used_by",""),
("r_verb_ppas","r_verb_ppas","Le participe passé (au masculin singulier) du verbe infinitif. Par exemple, pour manger => mangé"),
("r_verb_aux","r_verb_aux","Auxiliaire utilisé pour ce verbe"),
("r_cohypo","co-hyponyme","Il est demandé d'énumérer les CO-HYPONYMES du terme. Par exemple, 'chat' et 'tigre' sont des co-hyponymes (de 'félin')."),
("r_adj-nomprop","adj>nomprop","Pour un adjectif, donner le nom de propriété correspondant. Par exemple, pour 'friable' -> 'friabilité'"),
("r_nomprop-adj","nomprop>adj","Pour un nom de propriété, donner l'adjectif correspondant. Par exemple, pour 'friabilité' -> 'friable'"),
("r_adj-adv","adj>adv","Pour un adjectif, donner l'adverbe correspondant. Par exemple, pour 'rapide' -> 'rapidement'"),
("r_adv-adj","adv>adj","Pour un adverbe, donner l'adjectif correspondant. Par exemple, pour 'rapidement' -> 'rapide'"),
("r_predecesseur-logic","prédécesseur logique","Qu'est ce qui peut PRECEDER logiquement (par exemple : A précède B -  inverse de successeur logique) le terme suivant :"),
("r_successeur-logic","successeur logique","Qu'est ce qui peut SUIVRE logiquement (par exemple A -> B, C etc.) le terme suivant :"),
("r_link","r_link","Lien vers une ressource externe (WordNet, RadLex, UMLS, Wikipedia, etc...)"),
("r_isa-incompatible","r_isa-incompatible","Relation d'incompatibilité pour les génériques. Si A r_isa-incompatible B alors X ne peut pas être à la fois A et B ou alors X est polysémique. Par exemple, poisson r_isa-incompatible oiseau. Colin est à la fois un oiseau et un poisson, donc colin est polysémique."),
("r_verb_ppre","r_verb_ppre","Le participe présent(au masculin singulier) du verbe infinitif. Par exemple, pour manger => mangeant"),
("r_homophone","homophone","Il est demandé d'énumérer les homophones ou quasi-homophones de ce terme."),
("r_potential_confusion","confusion potentielle","Confusion potentielle avec un autre terme (par exemple, acre et âcre, détonner et détoner)."),
("r_incompatible","r_incompatible","Relation d'incompatibilité, ne doivent pas être présents ensemble. Par exemple, alcool r_incompatible antibiotique."),
("r_translation","r_translation","Traduction vers une autre langue.");


DELIMITER |
CREATE PROCEDURE creation_tables()
BEGIN
	DECLARE relation_name varchar(24);
	DECLARE relation_name2 varchar(24);
	/*DECLARE @table_name_entrant varchar(50);
	DECLARE @table_name_sortant varchar(50);
	DECLARE @SQL1 varchar(500);
	DECLARE @SQL2 varchar(500);*/
	DECLARE done INT DEFAULT 0;
	DECLARE relation_cursor CURSOR FOR SELECT name from type_relation;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
	OPEN relation_cursor;
	 
	relation_loop: LOOP
	   FETCH relation_cursor INTO relation_name;
	   IF done THEN
	      LEAVE relation_loop;
	   END IF;
	   SET relation_name2 = replace(relation_name, '-', '_');
	   SET relation_name = replace(relation_name2, '>', '_');

	   SET @table_name_entrant = CONCAT(relation_name, '_entrant');
	   SET @table_name_sortant = CONCAT(relation_name, '_sortant');
	   
	   SET @SQL1 = CONCAT('CREATE TABLE ', @table_name_entrant, ' (n2 int, name varchar(1000), w int, FOREIGN KEY (n2) REFERENCES noeuds(eid), INDEX ind_n2 (n2)) DEFAULT CHARSET=utf8');
	   SET @SQL2 = CONCAT('CREATE TABLE ', @table_name_sortant, ' (n1 int, name varchar(1000), w int, FOREIGN KEY (n1) REFERENCES noeuds(eid), INDEX ind_n1 (n1)) DEFAULT CHARSET=utf8');

	   PREPARE stmt FROM @SQL1;
	   EXECUTE stmt;
	   DEALLOCATE PREPARE stmt;

	   PREPARE stmt FROM @SQL2;
	   EXECUTE stmt;
	   DEALLOCATE PREPARE stmt;
	END LOOP;
	  
	CLOSE relation_cursor;
END|
DELIMITER ;
CALL creation_tables();