-- =============================================================================
-- Script de création des vues
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Vue vue_predictions : inputs + outputs
-- source = 'dataset' (référence) ou 'api' (requêtes live)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vue_predictions AS
SELECT
    i.id AS input_id,
    i.source,
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
