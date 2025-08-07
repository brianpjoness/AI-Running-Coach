from datetime import date, timedelta
from typing import List, Dict, Tuple
import math

from .models import (
    RunnerProfile, TrainingPlan, TrainingWeek, Workout, 
    TrainingPhase, WorkoutType, TrainingZone, RaceDistance
)
from .config import (
    DISTANCE_CONFIGS, EXPERIENCE_ADJUSTMENTS, ZONE_DISTRIBUTION,
    PHASE_WORKOUT_DISTRIBUTION, INJURY_PREVENTION
)


class TrainingPlanGenerator:
    """AI-powered training plan generator based on scientific principles"""
    
    def __init__(self):
        self.distance_configs = DISTANCE_CONFIGS
        self.experience_adjustments = EXPERIENCE_ADJUSTMENTS
        self.zone_distribution = ZONE_DISTRIBUTION
        self.phase_distribution = PHASE_WORKOUT_DISTRIBUTION
        self.injury_prevention = INJURY_PREVENTION
    
    def generate_plan(self, runner_profile: RunnerProfile) -> TrainingPlan:
        """Generate a complete training plan based on runner profile"""
        
        # Calculate training timeline
        total_weeks = self._calculate_training_weeks(runner_profile)
        phase_breakdown = self._calculate_phase_breakdown(runner_profile, total_weeks)
        
        # Generate weekly plans
        weeks = []
        current_mileage = runner_profile.current_weekly_mileage
        
        for week_num in range(1, total_weeks + 1):
            phase = self._determine_phase(week_num, phase_breakdown)
            weekly_mileage = self._calculate_weekly_mileage(
                week_num, current_mileage, runner_profile, phase
            )
            
            week_plan = self._generate_weekly_plan(
                week_num, phase, weekly_mileage, runner_profile
            )
            weeks.append(week_plan)
            
            # Update current mileage for next week
            current_mileage = weekly_mileage
        
        return TrainingPlan(
            runner_profile=runner_profile,
            weeks=weeks,
            total_weeks=total_weeks,
            peak_mileage=max(w.total_mileage for w in weeks)
        )
    
    def _calculate_training_weeks(self, profile: RunnerProfile) -> int:
        """Calculate optimal training duration based on distance and experience"""
        distance_config = self.distance_configs[profile.target_distance]
        experience_adjustment = self.experience_adjustments[profile.experience_level]
        
        # Base training weeks from distance config
        base_weeks = distance_config.min_training_weeks
        
        # Add experience-based extensions
        base_extension = experience_adjustment["base_phase_extension"]
        total_weeks = base_weeks + base_extension
        
        # Ensure minimum training time
        if total_weeks < distance_config.min_training_weeks:
            total_weeks = distance_config.min_training_weeks
        
        # Cap at maximum recommended weeks
        if total_weeks > distance_config.max_training_weeks:
            total_weeks = distance_config.max_training_weeks
        
        return total_weeks
    
    def _calculate_phase_breakdown(self, profile: RunnerProfile, total_weeks: int) -> Dict[str, int]:
        """Calculate how many weeks to spend in each training phase"""
        distance_config = self.distance_configs[profile.target_distance]
        experience_adjustment = self.experience_adjustments[profile.experience_level]
        
        # Base phase with experience adjustment
        base_weeks = distance_config.base_phase_weeks + experience_adjustment["base_phase_extension"]
        
        # Other phases
        build_weeks = distance_config.build_phase_weeks
        peak_weeks = distance_config.peak_phase_weeks
        taper_weeks = distance_config.taper_weeks
        
        # Adjust if total weeks don't match
        allocated_weeks = base_weeks + build_weeks + peak_weeks + taper_weeks
        if allocated_weeks != total_weeks:
            # Adjust build phase to fit
            build_weeks = total_weeks - base_weeks - peak_weeks - taper_weeks
            if build_weeks < 2:  # Ensure minimum build phase
                build_weeks = 2
                base_weeks = total_weeks - build_weeks - peak_weeks - taper_weeks
        
        return {
            "BASE": base_weeks,
            "BUILD": build_weeks,
            "PEAK": peak_weeks,
            "TAPER": taper_weeks
        }
    
    def _determine_phase(self, week_num: int, phase_breakdown: Dict[str, int]) -> TrainingPhase:
        """Determine which training phase a given week falls into"""
        cumulative_weeks = 0
        for phase_name, weeks in phase_breakdown.items():
            cumulative_weeks += weeks
            if week_num <= cumulative_weeks:
                return TrainingPhase(phase_name)
        return TrainingPhase.TAPER  # Fallback
    
    def _calculate_weekly_mileage(self, week_num: int, current_mileage: float, 
                                profile: RunnerProfile, phase: TrainingPhase) -> float:
        """Calculate weekly mileage with progressive overload and recovery weeks"""
        experience_adjustment = self.experience_adjustments[profile.experience_level]
        increase_rate = experience_adjustment["mileage_increase_rate"]
        recovery_frequency = experience_adjustment["recovery_weeks_frequency"]
        
        # Check if this is a recovery week
        if week_num % recovery_frequency == 0:
            return current_mileage * (1 - self.injury_prevention["down_week_reduction"])
        
        # Progressive overload
        target_mileage = profile.weekly_mileage_target * experience_adjustment["max_weekly_mileage_multiplier"]
        
        # Phase-specific adjustments
        if phase == TrainingPhase.TAPER:
            taper_reduction = 0.1 * (week_num % 4)  # Gradual reduction
            target_mileage *= (1 - taper_reduction)
        
        # Calculate new mileage with 10% rule
        max_increase = current_mileage * self.injury_prevention["max_mileage_increase"]
        new_mileage = current_mileage + (target_mileage - current_mileage) * increase_rate
        
        # Cap at maximum safe increase
        if new_mileage > current_mileage + max_increase:
            new_mileage = current_mileage + max_increase
        
        # Ensure we don't exceed target
        if new_mileage > target_mileage:
            new_mileage = target_mileage
        
        return round(new_mileage, 1)
    
    def _generate_weekly_plan(self, week_num: int, phase: TrainingPhase, 
                            weekly_mileage: float, profile: RunnerProfile) -> TrainingWeek:
        """Generate a complete weekly training plan"""
        distance_config = self.distance_configs[profile.target_distance]
        workouts = []
        
        # Calculate workout distribution
        workout_distribution = self.phase_distribution[phase.name]
        
        # Long run distance
        long_run_distance = weekly_mileage * distance_config.long_run_percentage
        
        # Distribute remaining mileage
        remaining_mileage = weekly_mileage - long_run_distance
        remaining_workouts = profile.days_per_week - 1  # Excluding long run
        
        # Generate workouts
        day = 1
        for workout_type, percentage in workout_distribution.items():
            if percentage > 0 and remaining_workouts > 0:
                if workout_type == "long_runs":
                    # Long run gets its own day
                    workouts.append(self._create_workout(
                        day, WorkoutType.LONG_RUN, long_run_distance, phase, profile
                    ))
                    day += 1
                else:
                    # Distribute remaining mileage
                    workout_distance = (remaining_mileage * percentage) / remaining_workouts
                    if workout_distance > 0:
                        workouts.append(self._create_workout(
                            day, self._get_workout_type(workout_type), 
                            workout_distance, phase, profile
                        ))
                        day += 1
                        remaining_workouts -= 1
        
        # Add rest days if needed
        while day <= profile.days_per_week:
            workouts.append(self._create_workout(
                day, WorkoutType.REST, 0, phase, profile
            ))
            day += 1
        
        # Sort workouts by day
        workouts.sort(key=lambda w: w.day)
        
        return TrainingWeek(
            week_number=week_num,
            phase=phase,
            workouts=workouts,
            total_mileage=weekly_mileage
        )
    
    def _create_workout(self, day: int, workout_type: WorkoutType, distance: float,
                       phase: TrainingPhase, profile: RunnerProfile) -> Workout:
        """Create a specific workout with appropriate intensity and description"""
        
        if workout_type == WorkoutType.REST:
            return Workout(
                day=day,
                workout_type=workout_type,
                distance_miles=0,
                description="Rest day - focus on recovery and nutrition",
                intensity_zone=TrainingZone.ZONE_1
            )
        
        # Determine intensity zone based on workout type and phase
        intensity_zone = self._determine_workout_intensity(workout_type, phase)
        
        # Generate workout description
        description = self._generate_workout_description(
            workout_type, distance, intensity_zone, phase, profile
        )
        
        return Workout(
            day=day,
            workout_type=workout_type,
            distance_miles=distance,
            intensity_zone=intensity_zone,
            description=description
        )
    
    def _determine_workout_intensity(self, workout_type: WorkoutType, 
                                   phase: TrainingPhase) -> TrainingZone:
        """Determine appropriate training zone for workout type and phase"""
        zone_mapping = {
            WorkoutType.EASY_RUN: TrainingZone.ZONE_2,
            WorkoutType.LONG_RUN: TrainingZone.ZONE_2,
            WorkoutType.TEMPO_RUN: TrainingZone.ZONE_4,
            WorkoutType.INTERVALS: TrainingZone.ZONE_5,
            WorkoutType.STRIDES: TrainingZone.ZONE_4,
            WorkoutType.HILLS: TrainingZone.ZONE_4,
            WorkoutType.RACE_PACE: TrainingZone.ZONE_4,
            WorkoutType.RECOVERY: TrainingZone.ZONE_1,
            WorkoutType.REST: TrainingZone.ZONE_1
        }
        return zone_mapping.get(workout_type, TrainingZone.ZONE_2)
    
    def _get_workout_type(self, workout_type_str: str) -> WorkoutType:
        """Convert string workout type to enum"""
        mapping = {
            "easy_runs": WorkoutType.EASY_RUN,
            "long_runs": WorkoutType.LONG_RUN,
            "tempo_runs": WorkoutType.TEMPO_RUN,
            "intervals": WorkoutType.INTERVALS,
            "strides": WorkoutType.STRIDES,
            "hills": WorkoutType.HILLS
        }
        return mapping.get(workout_type_str, WorkoutType.EASY_RUN)
    
    def _generate_workout_description(self, workout_type: WorkoutType, distance: float,
                                    intensity_zone: TrainingZone, phase: TrainingPhase,
                                    profile: RunnerProfile) -> str:
        """Generate detailed workout description with coaching cues"""
        
        distance_config = self.distance_configs[profile.target_distance]
        
        descriptions = {
            WorkoutType.EASY_RUN: f"Easy {distance} mile run at conversational pace. Focus on relaxed breathing and good form.",
            WorkoutType.LONG_RUN: f"Long run of {distance} miles. Start easy and maintain steady pace. Practice race day nutrition if over 90 minutes.",
            WorkoutType.TEMPO_RUN: f"Tempo run: {distance} miles at lactate threshold pace. Should feel 'comfortably hard' - you could hold this pace for about 1 hour.",
            WorkoutType.INTERVALS: f"Interval workout: {self._generate_interval_description(distance, profile)}",
            WorkoutType.STRIDES: f"Strides: {distance} miles with 4-6 x 100m accelerations. Focus on quick turnover and good form.",
            WorkoutType.HILLS: f"Hill workout: {distance} miles including hill repeats. Focus on driving with arms and maintaining form on uphills.",
            WorkoutType.RACE_PACE: f"Race pace workout: {distance} miles at target {profile.target_distance.value} pace. Practice race day effort and pacing.",
            WorkoutType.RECOVERY: f"Recovery run: {distance} miles at very easy pace. Focus on blood flow and recovery.",
            WorkoutType.REST: "Rest day - focus on recovery, nutrition, and sleep. Consider light stretching or yoga."
        }
        
        base_description = descriptions.get(workout_type, f"{distance} mile run")
        
        # Add phase-specific coaching
        phase_coaching = self._get_phase_coaching(phase, profile)
        if phase_coaching:
            base_description += f" {phase_coaching}"
        
        return base_description
    
    def _generate_interval_description(self, distance: float, profile: RunnerProfile) -> str:
        """Generate specific interval workout description based on distance"""
        distance_config = self.distance_configs[profile.target_distance]
        
        if profile.target_distance == RaceDistance.MILE:
            return f"4-6 x 400m at mile pace with 2-3 minute recovery"
        elif profile.target_distance == RaceDistance.FIVE_K:
            return f"6-8 x 1000m at 5K pace with 2-3 minute recovery"
        elif profile.target_distance == RaceDistance.TEN_K:
            return f"4-6 x 1600m at 10K pace with 3-4 minute recovery"
        elif profile.target_distance == RaceDistance.HALF_MARATHON:
            return f"3-4 x 2 mile at half marathon pace with 3-4 minute recovery"
        else:  # Marathon
            return f"2-3 x 3 mile at marathon pace with 3-4 minute recovery"
    
    def _get_phase_coaching(self, phase: TrainingPhase, profile: RunnerProfile) -> str:
        """Get phase-specific coaching advice"""
        distance_config = self.distance_configs[profile.target_distance]
        
        coaching = {
            TrainingPhase.BASE: f"Building aerobic foundation. Focus on {distance_config.key_focus}.",
            TrainingPhase.BUILD: "Increasing training stress. Maintain good form as intensity increases.",
            TrainingPhase.PEAK: "Race-specific training. Practice race day scenarios and pacing.",
            TrainingPhase.TAPER: "Reducing volume while maintaining intensity. Trust your training."
        }
        return coaching.get(phase, "")
