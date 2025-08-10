from typing import Dict
from .models import DistanceConfig, RaceDistance, ExperienceLevel, TrainingZone


# Distance-specific training configurations based on energy system demands
DISTANCE_CONFIGS: Dict[RaceDistance, DistanceConfig] = {
    RaceDistance.MILE: DistanceConfig(
        distance=RaceDistance.MILE,
        min_training_weeks=8,
        max_training_weeks=12,
        base_phase_weeks=4,
        build_phase_weeks=4,
        peak_phase_weeks=2,
        taper_weeks=2,
        energy_system_aerobic=85.0,
        energy_system_anaerobic=15.0,
        key_focus="Neuromuscular power and speed endurance",
        long_run_percentage=0.15
    ),
    
    RaceDistance.FIVE_K: DistanceConfig(
        distance=RaceDistance.FIVE_K,
        min_training_weeks=10,
        max_training_weeks=16,
        base_phase_weeks=6,
        build_phase_weeks=6,
        peak_phase_weeks=2,
        taper_weeks=2,
        energy_system_aerobic=92.5,
        energy_system_anaerobic=7.5,
        key_focus="VO2 max development",
        long_run_percentage=0.20
    ),
    
    RaceDistance.TEN_K: DistanceConfig(
        distance=RaceDistance.TEN_K,
        min_training_weeks=12,
        max_training_weeks=18,
        base_phase_weeks=6,
        build_phase_weeks=8,
        peak_phase_weeks=2,
        taper_weeks=2,
        energy_system_aerobic=96.0,
        energy_system_anaerobic=4.0,
        key_focus="Lactate threshold training",
        long_run_percentage=0.25
    ),
    
    RaceDistance.HALF_MARATHON: DistanceConfig(
        distance=RaceDistance.HALF_MARATHON,
        min_training_weeks=14,
        max_training_weeks=20,
        base_phase_weeks=8,
        build_phase_weeks=8,
        peak_phase_weeks=2,
        taper_weeks=2,
        energy_system_aerobic=97.5,
        energy_system_anaerobic=2.5,
        key_focus="Aerobic threshold and endurance",
        long_run_percentage=0.30
    ),
    
    RaceDistance.MARATHON: DistanceConfig(
        distance=RaceDistance.MARATHON,
        min_training_weeks=16,
        max_training_weeks=24,
        base_phase_weeks=8,
        build_phase_weeks=10,
        peak_phase_weeks=2,
        taper_weeks=4,
        energy_system_aerobic=98.5,
        energy_system_anaerobic=1.5,
        key_focus="Pure endurance and metabolic efficiency",
        long_run_percentage=0.35
    )
}


# Experience level adjustments for training progression
EXPERIENCE_ADJUSTMENTS = {
    ExperienceLevel.BEGINNER: {
        "mileage_increase_rate": 0.05,  # 5% weekly increase (more conservative)
        "max_weekly_mileage_multiplier": 0.8,  # 80% of target
        "recovery_weeks_frequency": 3,  # Every 3rd week
        "strength_training_days": 2,
        "base_phase_extension": 2,  # Extra weeks in base phase
    },
    
    ExperienceLevel.INTERMEDIATE: {
        "mileage_increase_rate": 0.08,  # 8% weekly increase
        "max_weekly_mileage_multiplier": 0.9,  # 90% of target
        "recovery_weeks_frequency": 4,  # Every 4th week
        "strength_training_days": 2,
        "base_phase_extension": 1,  # Extra week in base phase
    },
    
    ExperienceLevel.ADVANCED: {
        "mileage_increase_rate": 0.10,  # 10% weekly increase
        "max_weekly_mileage_multiplier": 1.0,  # Full target mileage
        "recovery_weeks_frequency": 5,  # Every 5th week
        "strength_training_days": 3,
        "base_phase_extension": 0,  # Standard base phase
    }
}


# Training zone distribution following 80/20 polarized training model
ZONE_DISTRIBUTION = {
    "easy_zones": [TrainingZone.ZONE_1, TrainingZone.ZONE_2],  # 80% of training
    "hard_zones": [TrainingZone.ZONE_4, TrainingZone.ZONE_5],  # 20% of training
    "avoid_zone": TrainingZone.ZONE_3,  # Gray zone - minimize
    "easy_percentage": 0.80,
    "hard_percentage": 0.20
}


# Workout type distribution by training phase
PHASE_WORKOUT_DISTRIBUTION = {
    "BASE": {
        "easy_runs": 0.70,
        "long_runs": 0.20,
        "tempo_runs": 0.05,
        "strides": 0.05,
        "intervals": 0.00,
        "hills": 0.00
    },
    "BUILD": {
        "easy_runs": 0.60,
        "long_runs": 0.20,
        "tempo_runs": 0.10,
        "strides": 0.05,
        "intervals": 0.05,
        "hills": 0.00
    },
    "PEAK": {
        "easy_runs": 0.50,
        "long_runs": 0.15,
        "tempo_runs": 0.15,
        "strides": 0.05,
        "intervals": 0.10,
        "hills": 0.05
    },
    "TAPER": {
        "easy_runs": 0.70,
        "long_runs": 0.10,
        "tempo_runs": 0.10,
        "strides": 0.05,
        "intervals": 0.05,
        "hills": 0.00
    }
}


# Injury prevention guidelines
INJURY_PREVENTION = {
    "max_mileage_increase": 0.10,  # 10% rule
    "consecutive_hard_days": 0,  # No consecutive hard days
    "recovery_days_between_hard_sessions": 2,
    "strength_training_frequency": 2,  # Minimum 2x per week
    "down_week_frequency": 4,  # Every 4th week
    "down_week_reduction": 0.25,  # 25% volume reduction
}


# Recovery and adaptation guidelines
RECOVERY_GUIDELINES = {
    "sleep_hours": 8,
    "nutrition_window_minutes": 60,
    "active_recovery_intensity": 0.30,  # 30% of training intensity
    "adaptation_weeks": 3,  # Weeks before major changes
    "supercompensation_cycle_days": 7
}
