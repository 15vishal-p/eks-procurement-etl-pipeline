"""
Transform stage: basic cleaning only. No analysis, no aggregation, no stats.
Adjust the column names below to match your actual dataset once you have it.
"""
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    original_count = len(df)

    # 1. Standardize column names: lowercase, no spaces
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # 2. Drop exact duplicate rows
    df = df.drop_duplicates()

    # 3. Strip whitespace from string/object columns
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()

    # 4. Drop rows that are entirely empty
    df = df.dropna(how="all")

    # 5. Drop the leftover index columns pandas/Excel exports often leave behind
    for col in ("unnamed:_0", "unnamed:_0.1"):
        if col in df.columns:
            df = df.drop(columns=col)

    # 6. Fix decimal-comma numbers (Slovak locale writes "4,0000" instead of "4.0000")
    money_cols = [
        "cenabezdph", "cenavratanedph", "uspora", "vstupnacena",
        "predlozenacenabezdph", "predlozenacenasdph",
        "final_value_amount", "estimated_value_amount", "saving", "bid_value",
        "mnozstvohodnota",
    ]
    for col in money_cols:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.replace(",", ".", regex=False)
                .replace("nan", pd.NA)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 7. Parse European-format datetime columns (e.g. "30.9.2014 10:54:01")
    date_cols = [
        "datumvyhlasenia", "datumzazmluvnenia", "lehotaplneniaod",
        "lehotaplneniado", "lehotanapredkladanieponuk", "zaciatokaukcie",
        "datumpredlozeniaponuky",
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%d.%m.%Y %H:%M:%S", errors="coerce")

    # 8. Translate Slovak column names to English for readability
    COLUMN_TRANSLATIONS = {
        "contract_id": "contract_id",
        "zakazkaurl": "contract_url",
        "stavzakazky": "contract_status",
        "pouzitypostup": "procurement_procedure",
        "objednavateldruh": "buyer_type",
        "objednavatelobchodnemeno": "buyer_name",
        "ca_ico": "buyer_company_id",
        "objednavatelstat": "buyer_country",
        "objednavatelobec": "buyer_city",
        "objednavatelpsc": "buyer_zip",
        "objednavatelulica": "buyer_street",
        "datumvyhlasenia": "announcement_date",
        "datumzazmluvnenia": "contract_signed_date",
        "opisnyformularnazov": "tender_title",
        "opisnyformularklucoveslova": "tender_keywords",
        "opisnyformularcpv": "cpv_code",
        "opisnyformulardruh": "tender_type",
        "opisnyformularkategoriasluzieb": "service_category",
        "miestoplneniastat": "delivery_country",
        "miestoplneniakraj": "delivery_region",
        "miestoplneniaokres": "delivery_district",
        "miestoplneniaobec": "delivery_city",
        "miestoplneniaulica": "delivery_street",
        "lehotaplneniaod": "delivery_period_start",
        "lehotaplneniado": "delivery_period_end",
        "lehotaplneniapresne": "delivery_period_exact",
        "mnozstvojednotka": "quantity_unit",
        "mnozstvohodnota": "quantity_value",
        "maximalnavyskazdrojov": "max_funding_amount",
        "zmluvnyvztah": "contract_relationship_type",
        "financovanieeu": "eu_funded",
        "hodnotiacekriterium": "evaluation_criteria",
        "lehotanapredkladanieponuk": "bid_submission_deadline",
        "pocetnotifikovanychdodavatelov": "notified_suppliers_count",
        "vstupnacena": "starting_price",
        "pocetsutaziacich": "competitors_count",
        "pocetpredlozenychponuk": "bids_submitted_count",
        "zaciatokaukcie": "auction_start",
        "trvanieaukcie_minut": "auction_duration_minutes",
        "predlzovanieaukcie_minut": "auction_extension_minutes",
        "win_co_ico": "winner_company_id",
        "win_co_state": "winner_country",
        "win_co_city": "winner_city",
        "win_co_zip": "winner_zip",
        "win_co_street": "winner_street",
        "cenabezdph": "price_excl_vat",
        "cenasadzbadph": "vat_rate",
        "cenavratanedph": "price_incl_vat",
        "uspora": "savings",
        "idstavvcrz": "crz_status_id",
        "file_first": "source_file",
        "datumpredlozeniaponuky": "bid_submission_date",
        "co_ico": "bidder_company_id",
        "bid_co_name": "bidder_name",
        "bid_co_state": "bidder_country",
        "predlozenacenabezdph": "submitted_price_excl_vat",
        "sadzbadph": "vat_rate_bid",
        "predlozenacenasdph": "submitted_price_incl_vat",
        "vysledneporadie": "final_ranking",
        "stavkontraktacnejponuky": "contract_bid_status",
        "ponukatyp": "bid_type",
        "vstupnaponuka": "initial_bid",
        "platna": "valid",
        "pocet_ponuk": "bid_count",
        "final_value_amount": "final_value_amount",
        "estimated_value_amount": "estimated_value_amount",
        "saving": "saving",
        "saving1": "saving_alt",
        "bid_value": "bid_value",
        "sk_nace": "nace_code",
        "druh_vlastníctva": "ownership_type",
        "počet_zamestnancov": "employee_count",
        "číslo_osvedčenia": "certificate_number",
        "dátum_vydania_osvedčenia": "certificate_issue_date",
        "dátum_odobratia_osvedčenia": "certificate_revocation_date",
        "zánik_alebo_zrušenie_štatútu": "status_termination",
        "druh_registrovaného_sociálneho_podniku": "social_enterprise_type",
        "obchodné_meno_podniku_/_obchodný_názov": "company_name",
        "právna_forma": "legal_form",
        "sídlo_podniku_-_ulica": "registered_address_street",
        "sídlo_podniku_-_súpisné_číslo": "registered_address_building_number",
        "sídlo_podniku_-_orientačné_číslo": "registered_address_street_number",
        "sídlo_podniku_-_obec": "registered_address_city",
        "sídlo_podniku_-_psč": "registered_address_zip",
        "sídlo_podniku_-_okres": "registered_address_district",
        "sídlo_podniku_-_kraj": "registered_address_region",
        "prevádzka_podniku_-_ulica": "operating_address_street",
        "prevádzka_podniku_-_obec": "operating_address_city",
        "prevádzka_podniku_-_psč": "operating_address_zip",
        "kontaktné_údaje_-_telefón": "contact_phone",
        "kontaktné_údaje_-_e_-_mail": "contact_email",
        "predmet_podnikania_/_činnosti": "business_activity",
        "merateľný_pozitívny_soc._vplyv": "measurable_social_impact",
        "v_zmysle_§9_má_zriadený_poradný_výbor_alebo__v_zmylse_§10_uplatňuje_demokratickú_správu": "has_advisory_board_or_democratic_governance",
        "časť_zisku_%": "profit_share_pct",
        "štatutárny_orgán_-_meno_a_priezvisko": "statutory_body_name",
        "štatutárny_orgán_spôsob_konania": "statutory_body_acting_method",
        "štatutárny_orgán_-_vznik_funkcie": "statutory_body_start_date",
        "štatutárny_orgán_-_skončenie_funkcie": "statutory_body_end_date",
        "konečný_uživateľ_výhod": "ultimate_beneficial_owner",
    }
    df = df.rename(columns=COLUMN_TRANSLATIONS)

    dropped = original_count - len(df)
    logger.info(f"Transform complete: {dropped:,} rows removed, {len(df):,} rows remain")
    return df