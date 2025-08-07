from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import date, timedelta


class RaceDistance(Enum):
    """Supported race distances with their energy system demands"""
    MILE = "1 Mile"
    FIVE_K = "5K"
    TEN_K = "10K"
    HALF_MARATHON = "Half Marathon"
    MARATHON = "Marathon"


class ExperienceLevel(Enum):
    """Runner experience levels affecting training progression"""
    BEGINNER = "Beginner"  # < 1 year running
    INTERMEDIATE = "Intermediate"  # 1-3 years running
    ADVANCED = "Advanced"  # 3+ years running


class TrainingZone(Enum):
    """Training intensity zones based on heart rate"""
    ZONE_1 = "Zone 1"  # 50-60% HRmax - Active recovery
    ZONE_2 = "Zone 2"  # 60-70% HRmax - Aerobic base
    ZONE_3 = "Zone 3"  # 70-80% HRmax - Moderate intensity (gray zone)
    ZONE_4 = "Zone 4"  # 80-90% HRmax - Lactate threshold
    ZONE_5 = "Zone 5"  # 90-100% HRmax - VO2 max


class WorkoutType(Enum):
    """Types of training workouts"""
    EASY_RUN = "Easy Run"
    LONG_RUN = "Long Run"
    TEMPO_RUN = "Tempo Run"
    INTERVALS = "Intervals"
    STRIDES = "Strides"
    HILLS = "Hills"
    RACE_PACE = "Race Pace"
    RECOVERY = "Recovery"
    REST = "Rest"


class TrainingPhase(Enum):
    """Training periodization phases"""
    BASE = "Base"
    BUILD = "Build"
    PEAK = "Peak"
    TAPER = "Taper"


@dataclass
class RunnerProfile:
    """Runner profile with training preferences and history"""
    experience_level: ExperienceLevel
    target_distance: RaceDistance
    peak_race_date: date
    weekly_mileage_target: int
    days_per_week: int
    current_weekly_mileage: Optional[int] = None
    previous_injuries: List[str] = None
    strength_training_days: int = 2
    
    def __post_init__(self):
        if self.previous_injuries is None:
            self.previous_injuries = []
        if self.current_weekly_mileage is None:
            self.current_weekly_mileage = self.weekly_mileage_target * 0.7  # Conservative start


@dataclass
class Workout:
    """Individual workout definition"""
    day: int
    workout_type: WorkoutType
    distance_miles: float
    duration_minutes: Optional[int] = None
    intensity_zone: TrainingZone = TrainingZone.ZONE_2
    description: str = ""
    notes: str = ""
    
    def __post_init__(self):
        if self.duration_minutes is None:
            # Estimate duration based on distance and zone
            pace_minutes_per_mile = self._estimate_pace()
            self.duration_minutes = int(self.distance_miles * pace_minutes_per_mile)
    
    def _estimate_pace(self) -> float:
        """Estimate pace in minutes per mile based on training zone"""
        zone_paces = {
            TrainingZone.ZONE_1: 10.0,  # Very easy
            TrainingZone.ZONE_2: 9.0,   # Easy/conversational
            TrainingZone.ZONE_3: 8.0,   # Moderate
            TrainingZone.ZONE_4: 7.0,   # Tempo
            TrainingZone.ZONE_5: 6.0,   # Hard
        }
        return zone_paces.get(self.intensity_zone, 9.0)


@dataclass
class TrainingWeek:
    """Weekly training plan"""
    week_number: int
    phase: TrainingPhase
    workouts: List[Workout]
    total_mileage: float
    notes: str = ""
    
    def __post_init__(self):
        if not self.total_mileage:
            self.total_mileage = sum(w.distance_miles for w in self.workouts)


@dataclass
class TrainingPlan:
    """Complete training plan"""
    runner_profile: RunnerProfile
    weeks: List[TrainingWeek]
    total_weeks: int
    peak_mileage: float
    notes: str = ""
    
    def __post_init__(self):
        if not self.total_weeks:
            self.total_weeks = len(self.weeks)
        if not self.peak_mileage:
            self.peak_mileage = max(w.total_mileage for w in self.weeks)


@dataclass
class DistanceConfig:
    """Configuration for different race distances"""
    distance: RaceDistance
    min_training_weeks: int
    max_training_weeks: int
    base_phase_weeks: int
    build_phase_weeks: int
    peak_phase_weeks: int
    taper_weeks: int
    energy_system_aerobic: float  # Percentage aerobic contribution
    energy_system_anaerobic: float  # Percentage anaerobic contribution
    key_focus: str
    long_run_percentage: float  # Percentage of weekly mileage for long run
