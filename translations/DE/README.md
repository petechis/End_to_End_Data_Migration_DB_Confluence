# 📦 Document Migration Demo

### PostgreSQL → Confluence Cloud (Raw REST API)

**Simulation einer Documentum → Confluence Migration (Metadaten + Dateien)**

# 🇩🇪 Deutsche Version

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Relationale%20DB-blue)
![Python](https://img.shields.io/badge/Python-3.x-yellow)
![Confluence](https://img.shields.io/badge/Confluence-Cloud-blue)
![REST API](https://img.shields.io/badge/API-REST-orange)
![Migration](https://img.shields.io/badge/Migration-PostgreSQL→Confluence-red)

[English](../EN/README.md) | [German](README.md)

---

## 🎯 Projektziel

Dieses Projekt demonstriert eine strukturierte Migration von Dokumenten und Metadaten aus einer lokalen PostgreSQL-Datenbank (Simulation eines OpenText Documentum-Systems) nach Confluence Cloud.

Migriert werden:

* 📄 Dokumente (Dateien aus dem Dateisystem)
* 🏷 Metadaten (Key/Value)
* 🏗 Hierarchie (Kunde → Projekt → Dokument)

Ohne spezielle Migrationstools – nur:

* SQL
* Python
* Confluence REST API

---

## 🏗 Zielstruktur in Confluence

Space: `DOCMIG`

```
DOCMIG
 ├── BMW AG
 │     └── PRJ-001 – Project Overview
 │            ├── SOW v1
 │            └── Invoice v1
 └── Siemens Healthineers
        └── PRJ-002 – Project Overview
               └── Spec v3
```

Jede Dokumentseite enthält:

* Metadaten-Tabelle
* Dokumentinformationen
* Datei-Anhang

---

## 🚀 Ablauf

1. Verbindung zur PostgreSQL-Datenbank
2. Dokumente & Metadaten auslesen
3. Kundenseite erzeugen
4. Projektseite erzeugen
5. Dokumentseite erstellen
6. Metadaten als HTML-Tabelle einfügen
7. Datei als Attachment hochladen

---

## 🎥 5-Minuten Präsentation

👉 **Präsentation:**
[Loom Video:](https://www.loom.com/share/3d1526ff3d034ed38cf41c0343816173)

---

## ⭐ Ergebnis

✔ Vollautomatische Migration

✔ Klare Confluence-Hierarchie

✔ Metadaten korrekt übertragen

✔ Dateien sauber angehängt

✔ Lokal reproduzierbar

---

## 👤 Author

**Pete Chisamba**
Munich, Germany
BI | Data | DMS | Confluence Administration

---
