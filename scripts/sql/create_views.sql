-- =============================================================================
-- Script de création des vues
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Vue vue_predictions : inputs + outputs (prédictions API)
--    Une ligne = une requête API avec sa prédiction et sa probabilité
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vue_predictions AS
SELECT
    i.id AS input_id,
    i.created_at AS input_created_at,
    i.age,
    i.genre,
    i.revenu_mensuel,
    i.statut_marital,
    i.departement,
    i.poste,
    i.nombre_experiences_precedentes,
    i.annee_experience_totale,
    i.annees_dans_l_entreprise,
    i.annees_dans_le_poste_actuel,
    i.nombre_participation_pee,
    i.nb_formations_suivies,
    i.distance_domicile_travail,
    i.niveau_education,
    i.domaine_etude,
    i.frequence_deplacement,
    i.annees_depuis_la_derniere_promotion,
    i.annes_sous_responsable_actuel,
    i.satisfaction_employee_environnement,
    i.note_evaluation_precedente,
    i.niveau_hierarchique_poste,
    i.satisfaction_employee_nature_travail,
    i.satisfaction_employee_equipe,
    i.satisfaction_employee_equilibre_pro_perso,
    i.note_evaluation_actuelle,
    i.heure_supplementaires,
    i.augementation_salaire_precedente,
    o.id AS output_id,
    o.prediction,
    o.probability,
    o.created_at AS output_created_at
FROM inputs i
JOIN outputs o ON o.input_id = i.id;


-- -----------------------------------------------------------------------------
-- 2. Vue vue_datas : regroupes les données de la table datas et la combinaison des inputs / outputs
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vue_datas AS
SELECT
    'dataset'::text AS source,
    d.id AS ref_id,
    d.age,
    d.genre,
    d.revenu_mensuel,
    d.statut_marital,
    d.departement,
    d.poste,
    d.nombre_experiences_precedentes,
    d.annee_experience_totale,
    d.annees_dans_l_entreprise,
    d.annees_dans_le_poste_actuel,
    d.nombre_participation_pee,
    d.nb_formations_suivies,
    d.distance_domicile_travail,
    d.niveau_education,
    d.domaine_etude,
    d.frequence_deplacement,
    d.annees_depuis_la_derniere_promotion,
    d.annes_sous_responsable_actuel,
    d.satisfaction_employee_environnement,
    d.note_evaluation_precedente,
    d.niveau_hierarchique_poste,
    d.satisfaction_employee_nature_travail,
    d.satisfaction_employee_equipe,
    d.satisfaction_employee_equilibre_pro_perso,
    d.note_evaluation_actuelle,
    d.heure_supplementaires,
    d.augementation_salaire_precedente,
    d.a_quitte_l_entreprise AS label_or_prediction,
    NULL::float AS probability
FROM datas d

UNION ALL

SELECT
    'api'::text AS source,
    i.id AS ref_id,
    i.age,
    i.genre,
    i.revenu_mensuel,
    i.statut_marital,
    i.departement,
    i.poste,
    i.nombre_experiences_precedentes,
    i.annee_experience_totale,
    i.annees_dans_l_entreprise,
    i.annees_dans_le_poste_actuel,
    i.nombre_participation_pee,
    i.nb_formations_suivies,
    i.distance_domicile_travail,
    i.niveau_education,
    i.domaine_etude,
    i.frequence_deplacement,
    i.annees_depuis_la_derniere_promotion,
    i.annes_sous_responsable_actuel,
    i.satisfaction_employee_environnement,
    i.note_evaluation_precedente,
    i.niveau_hierarchique_poste,
    i.satisfaction_employee_nature_travail,
    i.satisfaction_employee_equipe,
    i.satisfaction_employee_equilibre_pro_perso,
    i.note_evaluation_actuelle,
    i.heure_supplementaires,
    i.augementation_salaire_precedente,
    o.prediction AS label_or_prediction,
    o.probability
FROM inputs i
JOIN outputs o ON o.input_id = i.id;
