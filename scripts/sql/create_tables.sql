-- =============================================================================
-- Script de création des tables
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Table inputs : caractéristiques (dataset ou requêtes API)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS inputs (
    id                              SERIAL PRIMARY KEY,
    source                          VARCHAR(20)    NOT NULL DEFAULT 'api',
    created_at                      TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    -- Features SIRH
    age                             INTEGER        NOT NULL,
    genre                           VARCHAR(1)     NOT NULL,
    revenu_mensuel                  DOUBLE PRECISION NOT NULL,
    statut_marital                  VARCHAR(50)    NOT NULL,
    departement                     VARCHAR(50)    NOT NULL,
    poste                           VARCHAR(100)   NOT NULL,
    nombre_experiences_precedentes  INTEGER        NOT NULL,
    annee_experience_totale         INTEGER        NOT NULL,
    annees_dans_l_entreprise        INTEGER        NOT NULL,
    annees_dans_le_poste_actuel     INTEGER        NOT NULL,
    -- Features sondage
    nombre_participation_pee        INTEGER        NOT NULL,
    nb_formations_suivies           INTEGER        NOT NULL,
    distance_domicile_travail       INTEGER        NOT NULL,
    niveau_education                INTEGER        NOT NULL,
    domaine_etude                   VARCHAR(100)   NOT NULL,
    frequence_deplacement           VARCHAR(50)    NOT NULL,
    annees_depuis_la_derniere_promotion INTEGER    NOT NULL,
    annes_sous_responsable_actuel   INTEGER        NOT NULL,
    -- Features évaluation
    satisfaction_employee_environnement INTEGER    NOT NULL,
    note_evaluation_precedente      INTEGER        NOT NULL,
    niveau_hierarchique_poste       INTEGER        NOT NULL,
    satisfaction_employee_nature_travail INTEGER   NOT NULL,
    satisfaction_employee_equipe    INTEGER        NOT NULL,
    satisfaction_employee_equilibre_pro_perso INTEGER NOT NULL,
    note_evaluation_actuelle        INTEGER        NOT NULL,
    heure_supplementaires           VARCHAR(3)     NOT NULL,
    augementation_salaire_precedente INTEGER       NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_inputs_id ON inputs (id);


-- -----------------------------------------------------------------------------
-- 2. Table outputs : résultat du modèle, lié 1–1 à un input
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS outputs (
    id                              SERIAL PRIMARY KEY,
    prediction                      INTEGER        NOT NULL,  -- 0 ou 1
    probability                     DOUBLE PRECISION NOT NULL,
    created_at                      TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    input_id                        INTEGER        NOT NULL UNIQUE
        REFERENCES inputs (id)
);

CREATE INDEX IF NOT EXISTS ix_outputs_id ON outputs (id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_outputs_input_id ON outputs (input_id);
