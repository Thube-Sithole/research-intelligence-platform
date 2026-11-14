from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

def utc_now() -> datetime:
    """Return the current timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


class DomainModel(BaseModel):
    """Common configuration for research domain objects."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )


class MemoryScope(StrEnum):
    PROJECT = "project"
    SHARED = "shared"
    BOTH = "both"


class AutonomyMode(StrEnum):
    HYBRID = "hybrid"


class ResearchRunStatus(StrEnum):
    DRAFT = "draft"
    PLANNING = "planning"
    PLAN_READY_FOR_REVIEW = "plan_ready_for_review"
    AWAITING_SOURCE_INTEGRATION = "awaiting_source_integration"
    DISCOVERY = "discovery"
    EXTRACTION = "extraction"
    APPRAISAL = "appraisal"
    ANALYSIS = "analysis"
    CRITIQUE = "critique"
    AWAITING_FINAL_REVIEW = "awaiting_final_review"
    REPORT_READY = "report_ready"
    BLOCKED = "blocked"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ResearchProject(DomainModel):
    """A workspace containing related research investigations."""

    project_id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=2, max_length=200)
    description: str | None = None
    created_at: datetime = Field(default_factory=utc_now)


class ResearchQuestion(DomainModel):
    """The research objective that one or more runs investigate."""

    question_id: UUID = Field(default_factory=uuid4)
    project_id: UUID
    text: str = Field(min_length=12, max_length=4000)
    domain: str = Field(default="general", min_length=2, max_length=80)
    created_at: datetime = Field(default_factory=utc_now)


class ResearchRun(DomainModel):
    """One execution of a research question."""

    run_id: UUID = Field(default_factory=uuid4)
    project_id: UUID
    question_id: UUID

    status: ResearchRunStatus = ResearchRunStatus.DRAFT
    memory_scope: MemoryScope = MemoryScope.BOTH
    autonomy: AutonomyMode = AutonomyMode.HYBRID

    started_at: datetime = Field(default_factory=utc_now)
    completed_at: datetime | None = None

class SourceType(StrEnum):
    JOURNAL_ARTICLE = "journal_article"
    CONFERENCE_PAPER = "conference_paper"
    BOOK = "book"
    BOOK_CHAPTER = "book_chapter"
    TECHNICAL_REPORT = "technical_report"
    THESIS = "thesis"
    DATASET = "dataset"
    REGULATORY_DOCUMENT = "regulatory_document"
    WEBPAGE = "webpage"
    OTHER = "other"


class SourceOrigin(StrEnum):
    PROVIDER_DISCOVERED = "provider_discovered"
    USER_UPLOADED = "user_uploaded"
    MANUALLY_ADDED = "manually_added"


class SourceAccessLevel(StrEnum):
    FULL_TEXT = "full_text"
    ABSTRACT_ONLY = "abstract_only"
    METADATA_ONLY = "metadata_only"
    UNAVAILABLE = "unavailable"

class SourceRecord(DomainModel):
    """A bibliographic or informational record for an original research source."""

    source_id: UUID = Field(default_factory=uuid4)

    title: str = Field(min_length=1, max_length=1000)
    source_type: SourceType

    authors: list[str] = Field(default_factory=list)
    publication_date: datetime | None = None

    doi: str | None = Field(default=None, max_length=255)
    url: AnyHttpUrl | None = None

    origin: SourceOrigin
    provider: str | None = Field(default=None, max_length=120)

    access_level: SourceAccessLevel

    content_type: str | None = Field(default=None, max_length=120)
    content_hash_sha256: str | None = Field(
        default=None,
        pattern=r"^[a-fA-F0-9]{64}$",
    )

    retrieved_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)

class ClaimType(StrEnum):
    FINDING = "finding"
    METHODOLOGY = "methodology"
    LIMITATION = "limitation"
    RECOMMENDATION = "recommendation"
    BACKGROUND = "background"
    OTHER = "other"


class EvidenceClaim(DomainModel):
    """A source-supported statement extracted during a research run."""

    claim_id: UUID = Field(default_factory=uuid4)

    # Provenance: where the claim came from and which run extracted it
    source_id: UUID
    run_id: UUID

    # The research information
    statement: str = Field(min_length=10, max_length=4000)
    source_excerpt: str | None = Field(default=None, max_length=10000)

    claim_type: ClaimType = ClaimType.FINDING

    # Context that must be preserved when interpreting the claim
    qualifiers: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=utc_now)

class LocatorType(StrEnum):
    PAGE = "page"
    SECTION = "section"
    PARAGRAPH = "paragraph"
    TABLE = "table"
    FIGURE = "figure"
    HTML_ANCHOR = "html_anchor"
    DATASET_LOCATION = "dataset_location"
    TEXT_OFFSET = "text_offset"
    OTHER = "other"


class EvidenceLocator(DomainModel):
    """Identifies where an evidence claim can be verified in a source."""

    locator_id: UUID = Field(default_factory=uuid4)

    # The claim and source this location belongs to
    claim_id: UUID
    source_id: UUID

    locator_type: LocatorType

    # Identifies the exact version of the source content
    content_hash_sha256: str | None = Field(
        default=None,
        pattern=r"^[a-fA-F0-9]{64}$",
    )

    # Document location
    page_start: int | None = Field(default=None, ge=1)
    page_end: int | None = Field(default=None, ge=1)

    section: str | None = Field(default=None, max_length=500)
    paragraph: int | None = Field(default=None, ge=1)

    table: str | None = Field(default=None, max_length=100)
    figure: str | None = Field(default=None, max_length=100)

    # HTML location
    html_anchor: str | None = Field(default=None, max_length=500)

    # Dataset location
    dataset_sheet: str | None = Field(default=None, max_length=255)
    dataset_row: int | None = Field(default=None, ge=1)
    dataset_column: str | None = Field(default=None, max_length=100)

    # Character offsets in extracted text, when available
    character_start: int | None = Field(default=None, ge=0)
    character_end: int | None = Field(default=None, ge=0)

    # Optional descriptive context
    locator_text: str | None = Field(default=None, max_length=2000)

    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_location(self):
        """Ensure the locator identifies a meaningful source location."""

        location_fields = [
            self.page_start,
            self.section,
            self.paragraph,
            self.table,
            self.figure,
            self.html_anchor,
            self.dataset_sheet,
            self.dataset_row,
            self.dataset_column,
            self.character_start,
            self.locator_text,
        ]

        if not any(value is not None for value in location_fields):
            raise ValueError(
                "An evidence locator must identify at least one source location."
            )

        if (
            self.page_start is not None
            and self.page_end is not None
            and self.page_end < self.page_start
        ):
            raise ValueError("page_end cannot be earlier than page_start.")

        if (
            self.character_start is not None
            and self.character_end is not None
            and self.character_end < self.character_start
        ):
            raise ValueError(
                "character_end cannot be earlier than character_start."
            )

        return self
