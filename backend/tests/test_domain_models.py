from app.domain.models import (
    ResearchProject,
    ResearchQuestion,
    ResearchRun,
    ResearchRunStatus,
    EvidenceLocator,
    LocatorType,
)

import pytest
from pydantic import ValidationError
from uuid import uuid4

from app.domain.models import (
    SourceRecord,
    SourceType,
    SourceOrigin,
    SourceAccessLevel,
    EvidenceClaim,
    ClaimType,
)


def test_project_generates_unique_ids():
    project_one = ResearchProject(name="Distillation Research")
    project_two = ResearchProject(name="Medical Imaging Research")

    assert project_one.project_id != project_two.project_id


def test_question_belongs_to_project():
    project = ResearchProject(name="Distillation Research")

    question = ResearchQuestion(
        project_id=project.project_id,
        text="How does reflux ratio affect distillation efficiency?",
        domain="engineering",
    )

    assert question.project_id == project.project_id


def test_research_run_references_question_and_project():
    project = ResearchProject(name="Distillation Research")

    question = ResearchQuestion(
        project_id=project.project_id,
        text="How does reflux ratio affect distillation efficiency?",
    )

    run = ResearchRun(
        project_id=project.project_id,
        question_id=question.question_id,
    )

    assert run.project_id == project.project_id
    assert run.question_id == question.question_id
    assert run.status == ResearchRunStatus.DRAFT


def test_research_run_defaults_to_hybrid_memory():
    project = ResearchProject(name="Distillation Research")

    question = ResearchQuestion(
        project_id=project.project_id,
        text="How does reflux ratio affect distillation efficiency?",
    )

    run = ResearchRun(
        project_id=project.project_id,
        question_id=question.question_id,
    )

    assert run.memory_scope == "both"
    assert run.autonomy == "hybrid"

def test_source_record_creation():
    source = SourceRecord(
        title="Influence of Reflux Ratio on Distillation Efficiency",
        source_type=SourceType.JOURNAL_ARTICLE,
        authors=["Jane Smith", "John Doe"],
        doi="10.1234/example.2026",
        origin=SourceOrigin.PROVIDER_DISCOVERED,
        provider="Crossref",
        access_level=SourceAccessLevel.ABSTRACT_ONLY,
    )

    assert source.title == "Influence of Reflux Ratio on Distillation Efficiency"
    assert source.source_type == SourceType.JOURNAL_ARTICLE
    assert len(source.authors) == 2
    assert source.provider == "Crossref"
    assert source.access_level == SourceAccessLevel.ABSTRACT_ONLY


def test_source_record_generates_unique_ids():
    source_one = SourceRecord(
        title="Research Paper One",
        source_type=SourceType.JOURNAL_ARTICLE,
        origin=SourceOrigin.MANUALLY_ADDED,
        access_level=SourceAccessLevel.METADATA_ONLY,
    )

    source_two = SourceRecord(
        title="Research Paper Two",
        source_type=SourceType.JOURNAL_ARTICLE,
        origin=SourceOrigin.MANUALLY_ADDED,
        access_level=SourceAccessLevel.METADATA_ONLY,
    )

    assert source_one.source_id != source_two.source_id


def test_source_record_defaults_to_empty_authors():
    source = SourceRecord(
        title="Technical Report",
        source_type=SourceType.TECHNICAL_REPORT,
        origin=SourceOrigin.USER_UPLOADED,
        access_level=SourceAccessLevel.FULL_TEXT,
    )

    assert source.authors == []


def test_source_record_rejects_invalid_sha256_hash():
    with pytest.raises(ValidationError):
        SourceRecord(
            title="Research Paper",
            source_type=SourceType.JOURNAL_ARTICLE,
            origin=SourceOrigin.USER_UPLOADED,
            access_level=SourceAccessLevel.FULL_TEXT,
            content_hash_sha256="not-a-valid-sha256-hash",
        )


def test_source_record_rejects_invalid_source_type():
    with pytest.raises(ValidationError):
        SourceRecord(
            title="Research Paper",
            source_type="random_document_type",
            origin=SourceOrigin.MANUALLY_ADDED,
            access_level=SourceAccessLevel.METADATA_ONLY,
        )


def test_source_record_rejects_unexpected_fields():
    with pytest.raises(ValidationError):
        SourceRecord(
            title="Research Paper",
            source_type=SourceType.JOURNAL_ARTICLE,
            origin=SourceOrigin.MANUALLY_ADDED,
            access_level=SourceAccessLevel.METADATA_ONLY,
            unexpected_field="not allowed",
        )

def test_evidence_claim_creation():
    source = SourceRecord(
        title="Reflux Ratio and Distillation Performance",
        source_type=SourceType.JOURNAL_ARTICLE,
        origin=SourceOrigin.PROVIDER_DISCOVERED,
        access_level=SourceAccessLevel.FULL_TEXT,
    )

    claim = EvidenceClaim(
        source_id=source.source_id,
        run_id=uuid4(),
        statement=(
            "Increasing reflux ratio improved distillate purity "
            "under the reported operating conditions."
        ),
        source_excerpt=(
            "An increase in reflux ratio resulted in improved "
            "distillate purity."
        ),
        claim_type=ClaimType.FINDING,
        qualifiers=["Specific feed composition", "Fixed operating pressure"],
    )

    assert claim.source_id == source.source_id
    assert claim.claim_type == ClaimType.FINDING
    assert len(claim.qualifiers) == 2
    assert claim.source_excerpt is not None


def test_evidence_claim_generates_unique_ids():
    source_id = uuid4()
    run_id = uuid4()

    claim_one = EvidenceClaim(
        source_id=source_id,
        run_id=run_id,
        statement="Increasing reflux ratio improved product purity.",
    )

    claim_two = EvidenceClaim(
        source_id=source_id,
        run_id=run_id,
        statement="Increasing reflux ratio increased energy consumption.",
    )

    assert claim_one.claim_id != claim_two.claim_id


def test_evidence_claim_defaults():
    claim = EvidenceClaim(
        source_id=uuid4(),
        run_id=uuid4(),
        statement="The experiment measured product purity.",
    )

    assert claim.claim_type == ClaimType.FINDING
    assert claim.source_excerpt is None
    assert claim.qualifiers == []
    assert claim.limitations == []


def test_evidence_claim_rejects_invalid_claim_type():
    with pytest.raises(ValidationError):
        EvidenceClaim(
            source_id=uuid4(),
            run_id=uuid4(),
            statement="Increasing reflux ratio improved product purity.",
            claim_type="unsupported_category",
        )


def test_evidence_claim_rejects_short_statement():
    with pytest.raises(ValidationError):
        EvidenceClaim(
            source_id=uuid4(),
            run_id=uuid4(),
            statement="Too short",
        )


def test_evidence_claim_rejects_unexpected_fields():
    with pytest.raises(ValidationError):
        EvidenceClaim(
            source_id=uuid4(),
            run_id=uuid4(),
            statement="Increasing reflux ratio improved product purity.",
            unsupported_field="not allowed",
        )

def test_evidence_locator_creation():
    claim_id = uuid4()

    locator = EvidenceLocator(
        claim_id=claim_id,
        locator_type=LocatorType.PARAGRAPH,
        page_start=8,
        section="3.2 Results and Discussion",
        paragraph=2,
        content_hash_sha256="a" * 64,
    )
    
    assert locator.claim_id == claim_id
    assert locator.page_start == 8
    assert locator.section == "3.2 Results and Discussion"
    assert locator.paragraph == 2


def test_evidence_locator_supports_html_locations():
    locator = EvidenceLocator(
        claim_id=uuid4(),
        locator_type=LocatorType.HTML_ANCHOR,
        html_anchor="results-section",
    )

    assert locator.html_anchor == "results-section"
    assert locator.page_start is None


def test_evidence_locator_supports_dataset_locations():
    locator = EvidenceLocator(
        claim_id=uuid4(),
        locator_type=LocatorType.DATASET_LOCATION,
        dataset_sheet="Experimental Results",
        dataset_row=12,
        dataset_column="Product Purity",
    )

    assert locator.dataset_sheet == "Experimental Results"
    assert locator.dataset_row == 12
    assert locator.dataset_column == "Product Purity"


def test_evidence_locator_generates_unique_ids():
    claim_id = uuid4()

    locator_one = EvidenceLocator(
        claim_id=claim_id,
        locator_type=LocatorType.PAGE,
        page_start=8,
    )

    locator_two = EvidenceLocator(
        claim_id=claim_id,
        locator_type=LocatorType.PAGE,
        page_start=9,
    )

    assert locator_one.locator_id != locator_two.locator_id


def test_evidence_locator_rejects_missing_location():
    with pytest.raises(ValidationError):
        EvidenceLocator(
            source_id=uuid4(),
            claim_id=uuid4(),
            locator_type=LocatorType.OTHER,
        )


def test_evidence_locator_rejects_invalid_page_range():
    with pytest.raises(ValidationError):
        EvidenceLocator(
            source_id=uuid4(),
            claim_id=uuid4(),
            locator_type=LocatorType.PAGE,
            page_start=12,
            page_end=8,
        )


def test_evidence_locator_rejects_invalid_character_range():
    with pytest.raises(ValidationError):
        EvidenceLocator(
            source_id=uuid4(),
            claim_id=uuid4(),
            locator_type=LocatorType.TEXT_OFFSET,
            character_start=500,
            character_end=200,
        )


def test_evidence_locator_rejects_invalid_content_hash():
    with pytest.raises(ValidationError):
        EvidenceLocator(
            source_id=uuid4(),
            claim_id=uuid4(),
            locator_type=LocatorType.PAGE,
            page_start=8,
            content_hash_sha256="invalid-hash",
        )
