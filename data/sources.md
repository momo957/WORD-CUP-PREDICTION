# Sources des données — CDM 2026 Modèle de prédiction

## 1. Classement FIFA (`fifa_rank`, `elo_rating`)
- **Source primaire :** FIFA.com — Classement officiel FIFA/Coca-Cola, **publication du 1er avril 2026**
- **Source secondaire :** whereig.com (agrégateur officiel) — points exacts vérifiés pour les 48 équipes
- **URL FIFA officielle :** https://inside.fifa.com/fifa-world-ranking/men
- **URL vérification :** https://www.whereig.com/football/fifa-world-rankings.html
- **Note :** Le classement FIFA est publié officiellement 4 fois par an. La publication du 1er avril 2026 est la **dernière publication officielle disponible avant le début du tournoi**. La prochaine mise à jour officielle est prévue le 11 juin 2026 (jour d'ouverture du Mondial). Des classements live non officiels existent (football-ranking.com, mise à jour quotidienne) mais ne sont pas retenus pour la rigueur scientifique.
- **Points FIFA exacts utilisés (valeurs officielles) :** France 1877.32, Espagne 1876.40, Argentine 1874.81, Angleterre 1825.97... jusqu'à Nouvelle-Zélande 1281.57 (liste complète dans teams_features.csv)
- **Statut :** ✅ Vérifié — Source officielle FIFA, date certifiée 01/04/2026

## 2. Joueurs dans les 5 grands championnats (`players_top5_leagues`)
- **Source :** Wikipedia — 2026 FIFA World Cup squads (listes officielles 26 joueurs par pays)
- **URL :** https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_squads
- **Méthode :** Comptage joueur par joueur, club par club. Seuls PL, La Liga, Bundesliga, Serie A, Ligue 1 comptabilisés.
- **Clubs promus vérifiés :** Sunderland (PL ✓), Leeds United (PL ✓), Burnley (PL ✓), Como (Serie A ✓), Sassuolo (Serie A ✓), Cremonese (Serie A ✓), Pisa (Serie A ✓), St. Pauli (Bundesliga ✓), Lorient (Ligue 1 ✓), Le Havre (Ligue 1 ✓), Paris FC (Ligue 1 ✓)
- **Statut :** ✅ Vérifié (joueur par joueur)

## 3. Âge moyen des sélections (`avg_age_squad`)
- **Source :** RotoWire — 2026 World Cup Squad Ages
- **URL :** https://www.rotowire.com/soccer/article/2026-fifa-world-cup-squad-ages-youngest-oldest-teams-ranked-116813
- **Statut :** ✅ Vérifié

## 4. Statistiques qualification (`avg_goals_scored`, `avg_goals_conceded` — base qualification)
- **Source :** Footiqo.com — World Cup Goals Stats 2026
- **URL :** https://footiqo.com/statistics/teams/goals/full-time-world-cup/
- **Note :** Données mises à jour avec les 10 derniers matchs officiels (voir section 7)
- **Statut :** ✅ Vérifié (partiellement — hôtes Canada/USA/Mexico exemptés)

## 5. Résultat dernière CDM (`last_wc_stage`, `best_wc_result`)
- **Source :** Wikipedia — 2022 FIFA World Cup
- **URL :** https://en.wikipedia.org/wiki/2022_FIFA_World_Cup
- **URL :** https://www.espn.com/soccer/story/_/id/37626851/2022-world-cup-finals-bracket-fixtures-schedule
- **Statut :** ✅ Vérifié

## 6. Sélectionneurs (`coach_name`, `coach_years`)
- **Source :** Sites officiels des fédérations, Wikipedia, FIFA.com
- Deschamps (France) : https://en.wikipedia.org/wiki/Didier_Deschamps — nommé 08/07/2012
- De la Fuente (Espagne) : https://en.wikipedia.org/wiki/Luis_de_la_Fuente — nommé 08/12/2022
- Scaloni (Argentine) : https://en.wikipedia.org/wiki/Lionel_Scaloni — nommé 03/08/2018
- Tuchel (Angleterre) : https://www.thefa.com — nommé 01/01/2025
- Martinez (Portugal) : https://www.fpf.pt — nommé 09/01/2023
- Ancelotti (Brésil) : https://cbf.com.br — nommé 26/05/2025
- Ouahbi (Maroc) : https://www.fifa.com — nommé 05/03/2026 (remplace Regragui)
- Garcia (Belgique) : https://www.urbsfa.be — nommé 24/01/2025
- Nagelsmann (Allemagne) : https://www.dfb.de — nommé 22/09/2023
- Koeman (Pays-Bas) : https://www.knvb.nl — nommé 01/01/2023
- Dalic (Croatie) : https://hns.team — nommé 07/10/2017
- Lorenzo (Colombie) : https://fcf.com.co — nommé 02/06/2022
- Thiaw (Sénégal) : https://en.wikipedia.org/wiki/Pape_Thiaw — nommé 13/12/2024
- Aguirre (Mexique) : https://www.femexfut.org.mx — nommé 22/07/2024
- Pochettino (USA) : https://www.ussoccer.com — nommé 10/09/2024
- Bielsa (Uruguay) : https://auf.org.uy — nommé 15/05/2023
- Moriyasu (Japon) : https://www.jfa.jp — nommé 26/07/2018
- Yakin (Suisse) : https://www.football.ch — nommé 09/08/2021
- Ghalenoei (Iran) : https://www.ffiri.ir — nommé 12/03/2023
- Montella (Turquie) : https://www.tff.org — nommé 21/09/2023
- Beccacece (Équateur) : https://www.federacionecuatorianafutbol.com — nommé 01/08/2024
- Rangnick (Autriche) : https://www.oefb.at — nommé 29/04/2022
- Hong Myung-bo (Corée du Sud) : https://www.kfa.or.kr — nommé 08/07/2024
- Popovic (Australie) : https://www.footballaustralia.com.au — nommé 23/09/2024
- Petkovic (Algérie) : https://www.faf.dz — nommé 29/02/2024
- Hassan (Égypte) : https://www.efa.com.eg — nommé 06/02/2024
- Marsch (Canada) : https://www.canadasoccer.com — nommé 13/05/2024
- Solbakken (Norvège) : https://www.fotball.no — nommé 03/12/2020
- Christiansen (Panama) : https://www.fepafut.com — nommé 23/07/2020
- Fae (Côte d'Ivoire) : https://www.fif.ci — nommé 19/02/2024
- Tomasson (Suède) : https://www.svenskfotboll.se — nommé 26/02/2024
- Alfaro (Paraguay) : https://apf.org.py — nommé 16/08/2024
- Koubek (République Tchèque) : https://www.fotbal.cz — nommé 01/12/2025
- Clarke (Écosse) : https://www.scottishfa.co.uk — nommé 20/05/2019
- Desabre (RD Congo) : https://www.fecofa.org — nommé 06/08/2022
- Lamouchi (Tunisie) : https://www.ftf.org.tn — nommé 14/01/2026
- Kapadze (Ouzbékistan) : https://www.ufa.uz — nommé 22/01/2025
- Lopetegui (Qatar) : https://www.qfa.qa — nommé 01/05/2025
- Arnold (Irak) : https://www.iraqi-fa.org — nommé 09/05/2025
- Broos (Afrique du Sud) : https://www.safa.net — nommé 05/05/2021
- Donis (Arabie Saoudite) : https://www.saff.com.sa — nommé 24/04/2026
- Sellami (Jordanie) : https://www.jfa.jo — nommé 01/06/2024
- Barbarez (Bosnie) : https://www.nfsbih.ba — nommé 19/04/2024
- Bubista (Cap-Vert) : https://www.fcf.cv — nommé 01/01/2020
- Queiroz (Ghana) : https://www.ghanafa.org — nommé 13/04/2026
- Migne (Haïti) : https://www.fhf.ht — nommé 08/03/2024
- Advocaat (Curaçao) : https://www.fifa.com — nommé 12/05/2026
- Bazeley (Nouvelle-Zélande) : https://www.nzfootball.co.nz — nommé 01/07/2023
- **Statut :** ✅ Vérifié (sources primaires)

## 7. Forme récente — 10 derniers matchs officiels (`win/draw/loss_pct_last10`, `clean_sheets_last10`, `avg_goals_scored`, `avg_goals_conceded`)
- **Méthode :** Matchs FIFA officiels uniquement (qualifications CDM, Ligues des Nations, AFCON 2025, Copa América 2024, Gold Cup 2025, Asian Cup 2024). Les matchs amicaux sont exclus. Les résultats aux tirs au but comptent comme nuls.
- **Sources principales :**
  - UEFA : https://www.uefa.com/european-qualifiers/
  - CONMEBOL : https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_qualification_(CONMEBOL)
  - CAF : https://www.cafonline.com / AFCON 2025 : https://en.wikipedia.org/wiki/2025_Africa_Cup_of_Nations
  - AFC : https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_qualification_(AFC)
  - CONCACAF : https://www.concacaf.com / Gold Cup 2025 : https://www.olympics.com/en/news/concacaf-gold-cup-2025-soccer-full-schedule-all-results-scorers-standings-complete-list
  - Nations League UEFA 2025 : https://en.wikipedia.org/wiki/2024%E2%80%9325_UEFA_Nations_League
  - ESPN résultats : https://www.espn.com/soccer/
  - Wikipedia pages résultats nationales
- **Caveat scientifique :** Les données pour Cap-Vert, Haïti, Ouzbékistan, DR Congo et Irak sont partiellement vérifiées. Une vérification complémentaire via Soccerway.com ou FBRef.com est recommandée avant publication.
- **Statut :** ✅ Vérifié pour 38/48 équipes | ⚠️ Partiel pour 10 équipes

## 8. Titres continentaux (`continental_titles`)
- Copa América : https://en.wikipedia.org/wiki/Copa_Am%C3%A9rica
- UEFA Euro : https://en.wikipedia.org/wiki/UEFA_European_Championship
- AFCON : https://en.wikipedia.org/wiki/Africa_Cup_of_Nations
- AFC Asian Cup : https://en.wikipedia.org/wiki/AFC_Asian_Cup
- CONCACAF Gold Cup : https://en.wikipedia.org/wiki/CONCACAF_Gold_Cup
- OFC Nations Cup : https://en.wikipedia.org/wiki/OFC_Nations_Cup
- **Note AFCON 2025 :** Le Maroc a été déclaré vainqueur par le comité d'appel de la CAF suite au forfait du Sénégal en finale (décision du 17/03/2026). Source : https://www.espn.com/soccer/story/_/id/48233884/senegal-afcon-final-morocco-winner-caf-overturn
- **Statut :** ✅ Vérifié

## 9. Groupes et calendrier (`wc2026_groups.csv`, `wc2026_fixtures.csv`)
- **Source :** Tirage FIFA du 05/12/2025 (Kennedy Center, Washington D.C.)
- **URL groupes :** https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_draw
- **URL fixtures :** https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket
- **Statut :** ✅ Vérifié

## 10. Variables estimées (non sourcées — à exclure ou annoter dans la publication)
| Variable | Raison | Recommandation |
|---|---|---|
| `win_pct_vs_top20` | Calculée manuellement sans base de données complète | Exclure ou calculer via FBRef |
| `wc_participations` | Connaissance générale, non vérifiée systématiquement | Vérifier via Wikipedia historique CDM |
