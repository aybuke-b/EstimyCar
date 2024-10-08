"""
Module contenant des fonctions pour interagir avec la base de données contenant les véhicules, notamment pour la récupération d'informations
telles que la plage d'années, les noms de marques, de modèles, les différentes générations, les moteurs, les types de cylindres, les finitions et les types de batteries.
"""

import duckdb
from typing import cast


def get_plage_annee(
    user_role: str, marque: str = "", modele: str = ""
) -> tuple[int, int]:
    """
    Récupère la plage d'années des véhicules disponibles en fonction du rôle choisi par l'utilisateur.

    ## Parameters:
        user_role (str): Le rôle de l'utilisateur, soit "Acheteur" ou "Vendeur".
        marque (str, optional): Le nom de la marque du véhicule.
        modele (str, optional): Le nom du modèle du véhicule.

    ## Returns:
        tuple[int]: Un tuple contenant la plage d'années [annee_min, annee_max].

    ## Example(s):
        >>> get_plage_annee("Acheteur")
        # Retourne la valeur minimum et maximum d'année sur toute la base de données.

        >>> get_plage_annee("Vendeur", marque="MERCEDES", modele="C220")
        # Retourne la valeur minimum et maximum d'année pour un véhicule de la marque MERCEDES et du modèle C220 disponible dans la base de données.
    """

    if user_role == "Acheteur":
        return cast(
            tuple[int, int],
            tuple(
                duckdb.sql(
                    """
                SELECT MIN(annee) as annee_min,
                MAX(annee) as annee_max
                FROM 'data/database.parquet'
                """
                )
                .pl()
                .to_numpy()[0]
            ),
        )
    elif user_role == "Vendeur":
        try:
            return cast(
                tuple[int, int],
                tuple(
                    duckdb.sql(
                        f"""
                    SELECT MIN(annee) as annee_min,
                    MAX(annee) as annee_max
                    FROM 'data/database.parquet'
                    WHERE marque == '{marque.upper()}' 
                    AND modele == '{modele.upper()}'
                    """
                    )
                    .pl()
                    .to_numpy()[0]
                ),
            )
        except:
            return (1928, 2024)
    else:
        return (1928, 2024)


def get_unique_marque(user_role: str) -> list:
    """
    Récupère la liste des marques disponibles dans la base de données.

    ## Parameters:
        user_role (str): Le rôle de l'utilisateur, soit "Acheteur" ou "Vendeur".

    ## Returns:
        list: Liste des noms de marques uniques.
    """
    if user_role == "Acheteur":
        marques = duckdb.sql(
            """
            SELECT DISTINCT(marque) as unique_mar
            FROM 'data/database.parquet'
            WHERE marque IS NOT NULL
            ORDER BY unique_mar
            """
        ).df()
    if user_role == "Vendeur":
        marques = (
            duckdb.sql(
                """
            SELECT COUNT(*) as nb_annonces, 
            marque as unique_mar
            FROM 'data/database.parquet'
            WHERE marque IS NOT NULL
            GROUP BY marque
            ORDER BY COUNT(*) DESC
            """
            )
            .df()
            .head(40)
            .sort_values("unique_mar")
        )
    return list(marques["unique_mar"])


def get_unique_modele(marque: str) -> list:
    """
    Récupère la liste des modèles uniques d'une marque donnée.

    ## Parameters:
        marque (str): Le nom de la marque.

    ## Returns:
        list: Liste des noms de modèles uniques pour la marque spécifiée.

    ## Example(s):
        >>> get_unique_modele("MERCEDES")
        # Retourne la liste des modèles uniques disponible dans la base de données pour la marque MERCEDES.
    """
    modeles = duckdb.sql(
        f"""
        SELECT DISTINCT(modele) as unique_mod
        FROM 'data/database.parquet'
        WHERE marque == '{marque.upper()}'
        AND modele IS NOT NULL
        ORDER BY unique_mod
        """
    ).df()
    return list(modeles["unique_mod"])


def get_unique_generation(marque: str, modele: str) -> list:
    """
    Récupère la liste des générations uniques pour une marque et un modèle donnés.

    ## Parameters:
        marque (str): Le nom de la marque.
        modele (str): Le nom du modèle.

    ## Returns:
        list: Liste des générations uniques pour la marque et le modèle spécifiés.

    ## Example(s):
        >>> get_unique_generation("MERCEDES", "C220")
        # Retourne la liste des générations uniques pour la marque MERCEDES et le modèle C220.
    """
    generations = duckdb.sql(
        f"""
        SELECT DISTINCT(generation) as unique_gen
        FROM 'data/database.parquet'
        WHERE marque == '{marque.upper()}' 
        AND modele == '{modele.upper()}'
        AND generation IS NOT NULL
        ORDER BY unique_gen
        """
    ).df()
    return list(generations["unique_gen"])


def get_unique_moteur(marque: str, modele: str) -> list:
    """
    Récupère la liste des moteurs uniques pour une marque et un modèle donnés.

    ## Parameters:
        marque (str): Le nom de la marque.
        modele (str): Le nom du modèle.

    ## Returns:
        list: Liste des moteurs uniques pour la marque et le modèle spécifiés.
    """
    moteurs = duckdb.sql(
        f"""
        SELECT DISTINCT(moteur) as unique_mot
        FROM 'data/database.parquet'
        WHERE marque == '{marque.upper()}' 
        AND modele == '{modele.upper()}'
        AND moteur IS NOT NULL
        ORDER BY unique_mot 
        """
    ).df()
    return list(moteurs["unique_mot"])


def get_unique_cylindre(marque: str, modele: str) -> list:
    """
    Récupère la liste des cylindres uniques pour une marque et un modèle donnés.

    ## Parameters:
        marque (str): Le nom de la marque.
        modele (str): Le nom du modèle.

    ## Returns:
        list: Liste des cylindres uniques pour la marque et le modèle spécifiés.

    """

    cylindres = duckdb.sql(
        f"""
        SELECT DISTINCT(cylindre) as unique_cyl
        FROM 'data/database.parquet'
        WHERE marque == '{marque.upper()}' 
        AND modele == '{modele.upper()}'
        AND cylindre IS NOT NULL
        ORDER BY unique_cyl
        """
    ).df()
    return list(cylindres["unique_cyl"])


def get_unique_finition(marque: str, modele: str) -> list:
    """
    Récupère la liste des finitions uniques pour une marque et un modèle donnés.

    ## Parameters:
        marque (str): Le nom de la marque.
        modele (str): Le nom du modèle.

    ## Returns:
        list: Liste des finitions uniques pour la marque et le modèle spécifiés.
    """
    finitions = duckdb.sql(
        f"""
        SELECT DISTINCT(finition) as unique_fin
        FROM 'data/database.parquet'
        WHERE marque == '{marque.upper()}' 
        AND modele == '{modele.upper()}'
        AND finition IS NOT NULL
        ORDER BY unique_fin
        """
    ).df()
    return list(finitions["unique_fin"])


def get_unique_batterie() -> list:
    """
    Récupère la liste des types de batteries uniques disponibles dans les données.

    ## Returns:
        - list: Liste des types de batteries uniques.
    """
    batteries = duckdb.sql(
        """
        SELECT DISTINCT(batterie) as unique_bat
        FROM 'data/database.parquet'
        WHERE batterie IS NOT NULL
        ORDER BY unique_bat
        """
    ).df()
    return list(batteries["unique_bat"])
