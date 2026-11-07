"""Versioned API contracts. Missing evidence is represented explicitly."""
from datetime import date, datetime, timezone
from typing import Annotated, Literal
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, AwareDatetime, model_validator, field_validator

OwnerId = GatheringId = RecipeId = PlanId = UUID
Revision = Annotated[int, Field(ge=1)]

def identity(): return str(uuid4())

class Schema(BaseModel):
    model_config = {'extra': 'forbid', 'validate_assignment': True}

class Interval(Schema):
    start: AwareDatetime
    end: AwareDatetime
    @model_validator(mode='after')
    def ordered(self):
        if self.end <= self.start: raise ValueError('Interval end must follow start')
        return self

class Helper(Schema):
    id: str
    name: str
    skills: list[str] = []
    available: list[Interval] = []
    supervision: bool = False

class HostProfile(Schema):
    timezone: str = 'America/New_York'
    weekday_minutes: int = Field(120, ge=0, le=1440)
    weekend_minutes: int = Field(120, ge=0, le=1440)
    protected: list[Interval] = []
    equipment: dict[str, int | None] = Field(default_factory=lambda: {'oven':1,'stovetop':2,'air_fryer':1,'instant_pot':1})
    helpers: list[Helper] = []
    @field_validator('equipment', mode='before')
    @classmethod
    def standard_kitchen(cls, value):
        defaults={'oven':1,'stovetop':2,'air_fryer':1,'instant_pot':1}
        return defaults | (value or {})
    @field_validator('timezone')
    @classmethod
    def timezone_exists(cls,v): ZoneInfo(v); return v

class Contribution(Schema):
    id: str = Field(default_factory=identity)
    name: str
    person: str = ''
    servings: int | None = Field(None, ge=1)
    confirmed: bool = False
    arrival: AwareDatetime | None = None
    warming_minutes: int | None = Field(None, ge=0)
    equipment: str | None = None

class Gathering(Schema):
    id: str = Field(default_factory=identity)
    revision: Revision = 1
    title: str = 'Diwali gathering'
    occasion: str = 'Diwali'
    arrival: AwareDatetime | None = None
    earliest_prep: date | None = None
    prep_days: list[date] = []
    daily_limits: dict[str, Annotated[int, Field(ge=0, le=1440)]] = {}
    prep_windows: list[Interval] = []
    guests: int = Field(15, ge=1, le=100)
    vegetarian_guests: int = Field(0, ge=0)
    allergies: list[str] | None = None
    preferences: list[str] = []
    relax_minutes: int = Field(60, ge=0, le=240)
    finishing_minutes: int = Field(20, ge=0, le=240)
    cleanup_overrun_minutes: int = Field(15, ge=0, le=60)
    single_batch_kitchen: bool = True
    profile: HostProfile = Field(default_factory=HostProfile)
    selected_calendars: list[str] = []
    contributions: list[Contribution] = []
    spread: Literal['manageable','generous','custom'] = 'manageable'
    category_counts: dict[str, Annotated[int, Field(ge=0, le=12)]] = {}
    @model_validator(mode='after')
    def sane(self):
        if self.vegetarian_guests > self.guests: raise ValueError('Vegetarian count exceeds guests')
        if self.finishing_minutes > self.relax_minutes: raise ValueError('Finishing allowance exceeds final buffer')
        return self

class QuantityDetail(Schema):
    kind: Literal['exact','range','to_taste','unknown'] = 'unknown'
    minimum: float | None = Field(None, ge=0, allow_inf_nan=False)
    maximum: float | None = Field(None, ge=0, allow_inf_nan=False)
    optional: bool = False
    source_text: str = ''
    basis: Literal['source','estimate','unverified'] = 'unverified'
    @model_validator(mode='after')
    def valid_range(self):
        if self.kind == 'range':
            if self.minimum is None or self.maximum is None or self.minimum > self.maximum:
                raise ValueError('A range needs ordered minimum and maximum amounts')
        elif self.minimum is not None or self.maximum is not None:
            raise ValueError('Bounds are only valid for a range')
        return self

class Ingredient(Schema):
    name: str
    quantity: float | None = Field(None, ge=0, allow_inf_nan=False)
    unit: str | None = None
    amount_detail: QuantityDetail | None = None

class AttentionSegment(Schema):
    offset_minutes: int = Field(ge=0)
    minutes: int = Field(gt=0)

class PrepTask(Schema):
    id: str
    title: str
    recipe_id: str = ''
    dependencies: list[str] = []
    minutes: int | None = Field(None, ge=1, le=10080)
    active_minutes: int | None = Field(None, ge=0)
    presence_minutes: int | None = Field(None, ge=0)
    skill: str = 'cook'
    resource: str | None = None
    capacity: int = Field(1, ge=1)
    temperature: int | None = None
    eligible: Interval | None = None
    max_ahead_hours: float | None = Field(None, ge=0)
    evidence: str | None = None
    ingredients: list[Ingredient] = []
    guidance: str | None = None
    phase: Literal['cooking','finishing','cleanup','serving'] = 'cooking'
    unattended: bool = False
    scale_mode: Literal['batch','combined'] = 'batch'
    preparation_policy: Literal['unknown','same_day','advance'] = 'unknown'
    storage_anchor: Literal['serving','next_step'] = 'serving'
    max_dependency_gap_minutes: int | None = Field(None, ge=0, le=10080)
    min_dependency_gap_minutes: int = Field(0, ge=0, le=10080)
    attention_segments: list[AttentionSegment] = []
    timing_basis: Literal['estimate','source'] = 'estimate'
    @model_validator(mode='after')
    def consistent_dependency_gap(self):
        if self.max_dependency_gap_minutes is not None and self.min_dependency_gap_minutes>self.max_dependency_gap_minutes:
            raise ValueError('Minimum dependency gap cannot exceed maximum gap')
        return self

class RecipeSnapshot(Schema):
    id: str = Field(default_factory=identity)
    version: str = '1'
    title: str
    source: str
    servings: int | None = Field(None, ge=1)
    category: Literal['starters','mains','sides','desserts','drinks'] = 'mains'
    vegetarian: bool | None = None
    allergens: list[str] | None = None
    ingredients: list[Ingredient] = []
    tasks: list[PrepTask] = []
    source_text: str = ''
    reviewed: bool = False
    image_url: str | None = None
    image_credit: str | None = None
    uncertainties: list[str] = []
    preparation_provenance: dict[str, str] = {}

class MenuSelection(Schema):
    id: str = Field(default_factory=identity)
    title: str
    category: str = 'mains'
    recipe: RecipeSnapshot | None = None
    mode: Literal['cook','buy','semi','guest'] = 'cook'
    servings: int = Field(1, ge=1)
    must_have: bool = False
    preparation: list[PrepTask] = []
    vegetarian: bool | None = None
    contribution: Contribution | None = None

class AvailabilitySnapshot(Schema):
    busy: list[Interval] = []
    checked_at: AwareDatetime | None = None
    status: Literal['fresh','stale','unavailable','fixture'] = 'unavailable'
    errors: list[str] = []

class InventoryItem(Ingredient):
    id: str = Field(default_factory=identity)
    confirmed: bool = False
    source: Literal['manual','receipt','photo'] = 'manual'

class PlanInputs(Schema):
    gathering: Gathering
    selections: list[MenuSelection] = []
    inventory: list[InventoryItem] = []
    availability: AvailabilitySnapshot = Field(default_factory=AvailabilitySnapshot)

class Assignment(Schema):
    task: PrepTask
    interval: Interval
    person: str = 'host'

class ConstraintViolation(Schema):
    code: str
    affected_ids: list[str] = []
    explanation: str
    evidence: str | None = None

class TimeAdjustment(Schema):
    day: date
    current_minutes: int
    proposed_minutes: int
    window: Interval | None = None
    reason: str

class SchedulingOutcome(Schema):
    code: Literal['complete','needs_input','search_exhausted','unsupported','no_fit_found','validation_failed']
    message: str
    solver_status: str | None = None

class PlanCandidate(Schema):
    id: str = Field(default_factory=identity)
    gathering_id: str
    revision: Revision
    input_hash: str
    content_hash: str = ''
    assignments: list[Assignment] = []
    shopping: list[Ingredient] = []
    checklist: list[str] = []
    generated_at: AwareDatetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    advisories: list[ConstraintViolation] = []
    fit_days: list[dict] = []
    status: Literal['feasible','incomplete','conflict'] = 'incomplete'
    violations: list[ConstraintViolation] = []
    adjustments: list[TimeAdjustment] = []
    outcome: SchedulingOutcome | None = None

class Approval(Schema):
    id: str = Field(default_factory=identity)
    plan_id: str
    revision: Revision
    content_hash: str
    events: list[dict]

class BookingResult(Schema):
    approval_id: str
    outcomes: list[dict]
    notion_status: str = 'pending'
