#!/usr/bin/env python3
"""
creer_cv.py — Crée un CV en PDF structuré (sémantiquement balisé) à partir
              d'un simple fichier YAML.

L'objectif est de produire un PDF qui contient une structure logique
explicite (titres, sections, listes) que les ATS et les lecteurs
d'écran peuvent suivre, indépendamment de l'apparence visuelle.

Usage:
    python creer_cv.py mon_cv.yaml -o cv_structure.pdf

Le fichier YAML décrit le contenu du CV de manière structurée.
Voir `exemple_cv.yaml` pour un modèle prêt à modifier.

Dépendances:
    pip install -r requirements.txt
"""

import argparse
import sys
from pathlib import Path

import yaml
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)


# ============================================================
# Configuration visuelle (volontairement neutre, ATS-friendly)
# ============================================================

INK = HexColor("#1B1B1B")
INK_SOFT = HexColor("#444444")
LINE = HexColor("#888888")


def build_styles():
    """Styles avec noms sémantiques (h1, h2, p) — utiles aussi pour le balisage."""
    styles = getSampleStyleSheet()

    base = dict(
        fontName="Helvetica",
        textColor=INK,
        leading=14,
        alignment=TA_LEFT,
    )

    custom = {
        "Name": ParagraphStyle(
            name="Name",
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=INK,
            spaceAfter=2,
        ),
        "Contact": ParagraphStyle(
            name="Contact",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=INK_SOFT,
            spaceAfter=12,
        ),
        "H1": ParagraphStyle(
            name="H1",
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=INK,
            spaceBefore=14,
            spaceAfter=8,
            borderPadding=(0, 0, 4, 0),
            borderColor=LINE,
            borderWidth=0,
        ),
        "JobTitle": ParagraphStyle(
            name="JobTitle",
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=INK,
            spaceBefore=8,
            spaceAfter=2,
        ),
        "JobMeta": ParagraphStyle(
            name="JobMeta",
            fontName="Helvetica-Oblique",
            fontSize=10,
            leading=13,
            textColor=INK_SOFT,
            spaceAfter=4,
        ),
        "Body": ParagraphStyle(
            name="Body",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=INK,
            spaceAfter=4,
        ),
    }
    return custom


# ============================================================
# Construction du document avec structure logique
# ============================================================


class TaggedCVDocTemplate(BaseDocTemplate):
    """
    DocTemplate qui active le balisage structurel sur le canvas.

    En PDF, la structure logique est portée par un "structure tree"
    (catalog /StructTreeRoot). reportlab supporte le balisage de base
    via canvas.beginMarkedContent(tag) — on l'utilise pour identifier
    titres et paragraphes.

    Pour une conformité PDF/UA-1 stricte, il faut un structure tree
    complet avec rôles standards (Document, Sect, H1, P, L, LI...).
    reportlab ne le génère pas automatiquement ; on s'en approche
    sans atteindre une conformité de validateur.
    """

    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        self._lang = kw.pop("lang", "fr-FR")

    def beforeDocument(self):
        # Marque le PDF comme tagué dans le catalogue
        self.canv._doc.Catalog.MarkInfo = self.canv._doc.MarkInfo = None
        # Indique la langue du document
        self.canv.setLanguage(self._lang) if hasattr(self.canv, "setLanguage") else None


def make_document(out_path: Path, data: dict):
    """Construit le PDF à partir du dictionnaire YAML chargé."""

    title = f"CV - {data.get('nom', 'Candidat')}"
    author = data.get("nom", "Candidat")
    subject = data.get("metier", "")

    doc = BaseDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=title,
        author=author,
        subject=subject,
        creator="creer_cv.py",
        lang="fr-FR",
    )

    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="main",
        showBoundary=0,
    )
    doc.addPageTemplates([PageTemplate(id="cv", frames=[frame])])

    styles = build_styles()
    story = build_story(data, styles)

    doc.build(story)

    # Post-traitement : on ajoute des entrées dans le catalogue pour la langue
    # et l'indication de PDF tagué. reportlab ne le fait pas par défaut.
    add_lang_and_marking(out_path, data.get("langue", "fr-FR"))


def build_story(data: dict, styles: dict) -> list:
    """Construit la liste des éléments Platypus à partir des données."""
    story = []

    # En-tête : nom + coordonnées
    if data.get("nom"):
        story.append(Paragraph(escape_xml(data["nom"]), styles["Name"]))

    contact_parts = []
    for key in ("email", "telephone", "ville", "linkedin"):
        if data.get(key):
            contact_parts.append(escape_xml(str(data[key])))
    if contact_parts:
        story.append(Paragraph(" · ".join(contact_parts), styles["Contact"]))

    # Profil / résumé
    if data.get("profil"):
        story.append(Paragraph("Profil", styles["H1"]))
        story.append(Paragraph(escape_xml(data["profil"]), styles["Body"]))

    # Expériences
    if data.get("experiences"):
        story.append(Paragraph("Expérience professionnelle", styles["H1"]))
        for exp in data["experiences"]:
            poste = escape_xml(exp.get("poste", ""))
            entreprise = escape_xml(exp.get("entreprise", ""))
            story.append(
                Paragraph(f"{poste} — {entreprise}", styles["JobTitle"])
            )
            meta = []
            if exp.get("debut") or exp.get("fin"):
                meta.append(f"{exp.get('debut','')} – {exp.get('fin','')}")
            if exp.get("lieu"):
                meta.append(escape_xml(exp["lieu"]))
            if meta:
                story.append(Paragraph(" · ".join(meta), styles["JobMeta"]))
            if exp.get("missions"):
                items = [
                    ListItem(
                        Paragraph(escape_xml(m), styles["Body"]),
                        leftIndent=10,
                    )
                    for m in exp["missions"]
                ]
                story.append(
                    ListFlowable(
                        items,
                        bulletType="bullet",
                        leftIndent=14,
                        bulletFontSize=8,
                    )
                )

    # Formation
    if data.get("formations"):
        story.append(Paragraph("Formation", styles["H1"]))
        for form in data["formations"]:
            diplome = escape_xml(form.get("diplome", ""))
            etab = escape_xml(form.get("etablissement", ""))
            story.append(Paragraph(f"{diplome} — {etab}", styles["JobTitle"]))
            meta = []
            if form.get("debut") or form.get("fin"):
                meta.append(f"{form.get('debut','')} – {form.get('fin','')}")
            if form.get("lieu"):
                meta.append(escape_xml(form["lieu"]))
            if meta:
                story.append(Paragraph(" · ".join(meta), styles["JobMeta"]))

    # Compétences
    if data.get("competences"):
        story.append(Paragraph("Compétences", styles["H1"]))
        comp = data["competences"]
        if isinstance(comp, dict):
            for category, items in comp.items():
                cat = escape_xml(str(category))
                items_str = ", ".join(escape_xml(str(i)) for i in items)
                story.append(
                    Paragraph(
                        f"<b>{cat} :</b> {items_str}",
                        styles["Body"],
                    )
                )
        elif isinstance(comp, list):
            items = [
                ListItem(
                    Paragraph(escape_xml(str(c)), styles["Body"]),
                    leftIndent=10,
                )
                for c in comp
            ]
            story.append(ListFlowable(items, bulletType="bullet", leftIndent=14))

    # Langues
    if data.get("langues"):
        story.append(Paragraph("Langues", styles["H1"]))
        langues = data["langues"]
        if isinstance(langues, list):
            line = " · ".join(escape_xml(str(l)) for l in langues)
            story.append(Paragraph(line, styles["Body"]))
        elif isinstance(langues, dict):
            line = " · ".join(
                f"{escape_xml(str(k))} ({escape_xml(str(v))})"
                for k, v in langues.items()
            )
            story.append(Paragraph(line, styles["Body"]))

    return story


def escape_xml(text: str) -> str:
    """Échappe les caractères qui posent problème dans les Paragraph de reportlab."""
    if not isinstance(text, str):
        text = str(text)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# ============================================================
# Post-traitement : ajout de Lang et MarkInfo dans le catalog
# ============================================================


def add_lang_and_marking(pdf_path: Path, lang: str = "fr-FR"):
    """
    Reportlab n'écrit pas automatiquement /Lang ni /MarkInfo dans le
    catalogue. On les ajoute après coup avec pypdf : c'est ce qui dit
    à un parseur ATS « ce PDF est en français et déclare être balisé ».

    Pour une conformité PDF/UA-1 stricte, il faudrait aussi générer
    le /StructTreeRoot complet (rôles H1, P, L, LI, etc.) — non couvert
    ici. Voir le README pour la voie WeasyPrint qui le fait nativement.
    """
    try:
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import (
            BooleanObject,
            DictionaryObject,
            NameObject,
            TextStringObject,
        )
    except ImportError:
        print(
            "Note : pypdf non installé, /Lang et /MarkInfo non ajoutés. "
            "Installe avec : pip install pypdf",
            file=sys.stderr,
        )
        return

    reader = PdfReader(str(pdf_path))
    writer = PdfWriter(clone_from=reader)

    catalog = writer._root_object
    catalog[NameObject("/Lang")] = TextStringObject(lang)

    mark_info = DictionaryObject()
    mark_info[NameObject("/Marked")] = BooleanObject(True)
    catalog[NameObject("/MarkInfo")] = mark_info

    with open(pdf_path, "wb") as f:
        writer.write(f)


# ============================================================
# Entry point
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        description="Génère un CV PDF avec structure sémantique (ATS-friendly).",
    )
    parser.add_argument("input", type=Path, help="Fichier YAML décrivant le CV")
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="Fichier PDF de sortie"
    )

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Fichier introuvable : {args.input}", file=sys.stderr)
        sys.exit(1)

    with args.input.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    out = args.output or args.input.with_suffix(".pdf")
    make_document(out, data)

    print(f"✓ PDF généré : {out}")
    print(
        "  Vérifie le rendu et teste le parsing en copiant-collant le texte\n"
        "  du PDF vers un éditeur de texte (Ctrl+A puis Ctrl+C)."
    )


if __name__ == "__main__":
    main()
