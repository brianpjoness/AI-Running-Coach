from typing import List, Dict
from datetime import date, timedelta

from .models import TrainingPlan, TrainingWeek, Workout, RunnerProfile, TrainingPhase


class TrainingPlanFormatter:
    """Formats training plans for display and export"""
    
    def __init__(self):
        self.phase_colors = {
            TrainingPhase.BASE: "🟢",
            TrainingPhase.BUILD: "🟡", 
            TrainingPhase.PEAK: "🟠",
            TrainingPhase.TAPER: "🔴"
        }
        
        self.workout_icons = {
            "Easy Run": "🏃",
            "Long Run": "🏃‍♂️",
            "Tempo Run": "⚡",
            "Intervals": "🎯",
            "Strides": "💨",
            "Hills": "⛰️",
            "Race Pace": "🏁",
            "Recovery": "🔄",
            "Rest": "😴"
        }
    
    def format_plan_summary(self, plan: TrainingPlan) -> str:
        """Generate a comprehensive plan summary"""
        profile = plan.runner_profile
        
        summary = f"""
🏃‍♀️ TRAINING PLAN SUMMARY 🏃‍♂️
{'='*50}

📊 RUNNER PROFILE:
• Target Race: {profile.target_distance.value}
• Race Date: {profile.peak_race_date.strftime('%B %d, %Y')}
• Experience Level: {profile.experience_level.value}
• Weekly Mileage Target: {profile.weekly_mileage_target} miles
• Training Days: {profile.days_per_week} days/week

📈 PLAN OVERVIEW:
• Total Training Weeks: {plan.total_weeks}
• Peak Weekly Mileage: {plan.peak_mileage} miles
• Training Start Date: {(profile.peak_race_date - timedelta(weeks=plan.total_weeks)).strftime('%B %d, %Y')}

🎯 TRAINING PHASES:
{self._format_phase_breakdown(plan)}

💪 STRENGTH TRAINING:
• Recommended: {profile.strength_training_days} days per week
• Focus: Hip, core, and single-leg exercises
• Timing: On non-running days or after easy runs

📋 KEY PRINCIPLES:
• 80/20 Training: 80% easy, 20% hard
• Progressive Overload: Gradual mileage increases
• Recovery: Every {self._get_recovery_frequency(profile)} weeks
• Injury Prevention: 10% rule for mileage increases
"""
        return summary
    
    def format_weekly_plan(self, week: TrainingWeek, profile: RunnerProfile) -> str:
        """Format a single week's training plan"""
        phase_icon = self.phase_colors.get(week.phase, "⚪")
        
        header = f"""
{phase_icon} WEEK {week.week_number}: {week.phase.value.upper()} PHASE
{'='*40}
Total Mileage: {week.total_mileage} miles
"""
        
        workouts = []
        for workout in week.workouts:
            icon = self.workout_icons.get(workout.workout_type.value, "🏃")
            workouts.append(f"""
{icon} Day {workout.day}: {workout.workout_type.value}
   Distance: {workout.distance_miles} miles
   Duration: {workout.duration_minutes} minutes
   Intensity: {workout.intensity_zone.value}
   Description: {workout.description}
""")
        
        return header + "".join(workouts)
    
    def format_full_plan(self, plan: TrainingPlan) -> str:
        """Format the complete training plan"""
        full_plan = self.format_plan_summary(plan)
        full_plan += "\n\n" + "="*60 + "\n"
        full_plan += "DETAILED WEEKLY PLANS\n" + "="*60 + "\n"
        
        for week in plan.weeks:
            full_plan += self.format_weekly_plan(week, plan.runner_profile)
            full_plan += "\n" + "-"*40 + "\n"
        
        return full_plan
    
    def format_phase_breakdown(self, plan: TrainingPlan) -> str:
        """Format the training phase breakdown"""
        phase_counts = {}
        for week in plan.weeks:
            phase_counts[week.phase] = phase_counts.get(week.phase, 0) + 1
        
        breakdown = "📅 PHASE BREAKDOWN:\n"
        for phase, count in phase_counts.items():
            icon = self.phase_colors.get(phase, "⚪")
            breakdown += f"• {icon} {phase.value}: {count} weeks\n"
        
        return breakdown
    
    def format_mileage_progression(self, plan: TrainingPlan) -> str:
        """Format weekly mileage progression"""
        progression = "📊 MILEAGE PROGRESSION:\n"
        for week in plan.weeks:
            progression += f"Week {week.week_number}: {week.total_mileage} miles ({week.phase.value})\n"
        return progression
    
    def format_workout_distribution(self, plan: TrainingPlan) -> str:
        """Format workout type distribution across the plan"""
        workout_counts = {}
        total_workouts = 0
        
        for week in plan.weeks:
            for workout in week.workouts:
                workout_type = workout.workout_type.value
                workout_counts[workout_type] = workout_counts.get(workout_type, 0) + 1
                total_workouts += 1
        
        distribution = "🎯 WORKOUT DISTRIBUTION:\n"
        for workout_type, count in sorted(workout_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_workouts) * 100
            icon = self.workout_icons.get(workout_type, "🏃")
            distribution += f"• {icon} {workout_type}: {count} ({percentage:.1f}%)\n"
        
        return distribution
    
    def format_recovery_guidelines(self, profile: RunnerProfile) -> str:
        """Format recovery and adaptation guidelines"""
        guidelines = f"""
💤 RECOVERY GUIDELINES:

🛏️ SLEEP:
• Target: 8+ hours per night
• Quality: Deep, uninterrupted sleep
• Timing: Consistent sleep schedule

🍎 NUTRITION:
• Post-workout: Within 30-60 minutes
• Carbohydrates: Match training demands
• Protein: {profile.strength_training_days * 20}g daily minimum
• Hydration: Monitor urine color (light yellow)

🔄 ACTIVE RECOVERY:
• Light movement on rest days
• Stretching and mobility work
• Consider yoga or swimming

📈 ADAPTATION MONITORING:
• Track resting heart rate
• Monitor sleep quality
• Note energy levels and mood
• Adjust training if needed
"""
        return guidelines
    
    def format_injury_prevention(self, profile: RunnerProfile) -> str:
        """Format injury prevention guidelines"""
        prevention = f"""
🛡️ INJURY PREVENTION:

💪 STRENGTH TRAINING:
• Frequency: {profile.strength_training_days} days per week
• Focus: Hip abductors, core, single-leg exercises
• Examples: Single-leg deadlifts, squats, planks

📏 TRAINING LOAD:
• Follow 10% rule for mileage increases
• Include recovery weeks every {self._get_recovery_frequency(profile)} weeks
• Avoid consecutive hard days
• Listen to your body

🏃‍♀️ FORM & TECHNIQUE:
• Maintain good posture
• Land midfoot
• Keep cadence around 180 steps/minute
• Relax shoulders and arms

⚠️ WARNING SIGNS:
• Persistent pain (not just soreness)
• Decreased performance
• Changes in running form
• Fatigue that doesn't improve with rest
"""
        return prevention
    
    def _format_phase_breakdown(self, plan: TrainingPlan) -> str:
        """Format the training phase breakdown for summary"""
        phase_counts = {}
        for week in plan.weeks:
            phase_counts[week.phase] = phase_counts.get(week.phase, 0) + 1
        
        breakdown = ""
        for phase, count in phase_counts.items():
            icon = self.phase_colors.get(phase, "⚪")
            breakdown += f"• {icon} {phase.value}: {count} weeks\n"
        
        return breakdown
    
    def _get_recovery_frequency(self, profile: RunnerProfile) -> int:
        """Get recovery week frequency based on experience level"""
        from .config import EXPERIENCE_ADJUSTMENTS
        return EXPERIENCE_ADJUSTMENTS[profile.experience_level]["recovery_weeks_frequency"]
    
    def export_to_markdown(self, plan: TrainingPlan, filename: str = None) -> str:
        """Export training plan to markdown format"""
        if filename is None:
            filename = f"training_plan_{plan.runner_profile.target_distance.value.lower().replace(' ', '_')}.md"
        
        markdown = f"""# {plan.runner_profile.target_distance.value} Training Plan

{self.format_plan_summary(plan)}

## Weekly Plans

"""
        
        for week in plan.weeks:
            markdown += f"### Week {week.week_number}: {week.phase.value} Phase\n\n"
            markdown += f"**Total Mileage:** {week.total_mileage} miles\n\n"
            
            for workout in week.workouts:
                icon = self.workout_icons.get(workout.workout_type.value, "🏃")
                markdown += f"#### Day {workout.day}: {workout.workout_type.value} {icon}\n\n"
                markdown += f"- **Distance:** {workout.distance_miles} miles\n"
                markdown += f"- **Duration:** {workout.duration_minutes} minutes\n"
                markdown += f"- **Intensity:** {workout.intensity_zone.value}\n"
                markdown += f"- **Description:** {workout.description}\n\n"
            
            markdown += "---\n\n"
        
        markdown += f"""
## Recovery Guidelines

{self.format_recovery_guidelines(plan.runner_profile)}

## Injury Prevention

{self.format_injury_prevention(plan.runner_profile)}
"""
        
        return markdown
