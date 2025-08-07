#!/usr/bin/env python3
"""
AI Running Training Plan Generator

A scientific, evidence-based training plan generator that follows the principles
outlined in the .cursorrules file, including periodization, progressive overload,
and injury prevention.
"""

import sys
from datetime import date, timedelta
from typing import Optional

from src.models import RunnerProfile, RaceDistance, ExperienceLevel
from src.plan_generator import TrainingPlanGenerator
from src.formatter import TrainingPlanFormatter


def create_runner_profile(
    target_distance: str,
    race_date: str,
    experience_level: str,
    weekly_mileage: int,
    days_per_week: int,
    current_mileage: Optional[int] = None
) -> RunnerProfile:
    """Create a runner profile from user inputs"""
    
    # Convert string inputs to enums
    try:
        distance = RaceDistance(target_distance)
    except ValueError:
        raise ValueError(f"Invalid distance: {target_distance}. Choose from: {[d.value for d in RaceDistance]}")
    
    try:
        experience = ExperienceLevel(experience_level)
    except ValueError:
        raise ValueError(f"Invalid experience level: {experience_level}. Choose from: {[e.value for e in ExperienceLevel]}")
    
    # Parse race date
    try:
        race_date_obj = date.fromisoformat(race_date)
    except ValueError:
        raise ValueError(f"Invalid date format: {race_date}. Use YYYY-MM-DD format.")
    
    return RunnerProfile(
        experience_level=experience,
        target_distance=distance,
        peak_race_date=race_date_obj,
        weekly_mileage_target=weekly_mileage,
        days_per_week=days_per_week,
        current_weekly_mileage=current_mileage
    )


def interactive_input() -> RunnerProfile:
    """Get runner profile through interactive input"""
    print("🏃‍♀️ AI Running Training Plan Generator 🏃‍♂️")
    print("=" * 50)
    print()
    
    # Available options
    distances = [d.value for d in RaceDistance]
    experience_levels = [e.value for e in ExperienceLevel]
    
    print("Available race distances:")
    for i, distance in enumerate(distances, 1):
        print(f"  {i}. {distance}")
    
    print("\nAvailable experience levels:")
    for i, level in enumerate(experience_levels, 1):
        print(f"  {i}. {level}")
    
    print()
    
    # Get user inputs
    while True:
        try:
            distance_choice = int(input("Select race distance (1-5): ")) - 1
            if 0 <= distance_choice < len(distances):
                target_distance = distances[distance_choice]
                break
            else:
                print("Invalid choice. Please select 1-5.")
        except ValueError:
            print("Please enter a number.")
    
    while True:
        try:
            experience_choice = int(input("Select experience level (1-3): ")) - 1
            if 0 <= experience_choice < len(experience_levels):
                experience_level = experience_levels[experience_choice]
                break
            else:
                print("Invalid choice. Please select 1-3.")
        except ValueError:
            print("Please enter a number.")
    
    while True:
        race_date = input("Enter race date (YYYY-MM-DD): ")
        try:
            date.fromisoformat(race_date)
            break
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
    
    while True:
        try:
            weekly_mileage = int(input("Enter target weekly mileage: "))
            if weekly_mileage > 0:
                break
            else:
                print("Mileage must be positive.")
        except ValueError:
            print("Please enter a number.")
    
    while True:
        try:
            days_per_week = int(input("Enter training days per week (3-7): "))
            if 3 <= days_per_week <= 7:
                break
            else:
                print("Days per week must be between 3 and 7.")
        except ValueError:
            print("Please enter a number.")
    
    current_mileage_input = input("Enter current weekly mileage (optional, press Enter to skip): ")
    current_mileage = None
    if current_mileage_input.strip():
        try:
            current_mileage = int(current_mileage_input)
        except ValueError:
            print("Invalid current mileage. Using default calculation.")
    
    return create_runner_profile(
        target_distance=target_distance,
        race_date=race_date,
        experience_level=experience_level,
        weekly_mileage=weekly_mileage,
        days_per_week=days_per_week,
        current_mileage=current_mileage
    )


def generate_example_plans():
    """Generate example training plans for demonstration"""
    examples = [
        {
            "name": "Beginner 5K",
            "profile": RunnerProfile(
                experience_level=ExperienceLevel.BEGINNER,
                target_distance=RaceDistance.FIVE_K,
                peak_race_date=date.today() + timedelta(weeks=12),
                weekly_mileage_target=20,
                days_per_week=4
            )
        },
        {
            "name": "Intermediate Half Marathon",
            "profile": RunnerProfile(
                experience_level=ExperienceLevel.INTERMEDIATE,
                target_distance=RaceDistance.HALF_MARATHON,
                peak_race_date=date.today() + timedelta(weeks=16),
                weekly_mileage_target=35,
                days_per_week=5
            )
        },
        {
            "name": "Advanced Marathon",
            "profile": RunnerProfile(
                experience_level=ExperienceLevel.ADVANCED,
                target_distance=RaceDistance.MARATHON,
                peak_race_date=date.today() + timedelta(weeks=20),
                weekly_mileage_target=50,
                days_per_week=6
            )
        }
    ]
    
    generator = TrainingPlanGenerator()
    formatter = TrainingPlanFormatter()
    
    for example in examples:
        print(f"\n{'='*60}")
        print(f"EXAMPLE: {example['name']}")
        print(f"{'='*60}")
        
        plan = generator.generate_plan(example['profile'])
        print(formatter.format_plan_summary(plan))
        
        # Show first week as preview
        print("\n📅 WEEK 1 PREVIEW:")
        print(formatter.format_weekly_plan(plan.weeks[0], plan.runner_profile))


def main():
    """Main application entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "examples":
            generate_example_plans()
            return
        elif command == "help":
            print("""
AI Running Training Plan Generator

Usage:
  python main.py                    # Interactive mode
  python main.py examples          # Show example plans
  python main.py help              # Show this help

The generator creates scientifically-based training plans following:
• 80/20 polarized training model
• Progressive overload with 10% rule
• Periodization (Base → Build → Peak → Taper)
• Injury prevention principles
• Individual customization based on experience level
            """)
            return
        else:
            print(f"Unknown command: {command}")
            print("Use 'python main.py help' for usage information.")
            return
    
    try:
        # Interactive mode
        profile = interactive_input()
        
        print("\n" + "="*50)
        print("GENERATING YOUR TRAINING PLAN...")
        print("="*50)
        
        # Generate plan
        generator = TrainingPlanGenerator()
        plan = generator.generate_plan(profile)
        
        # Format and display
        formatter = TrainingPlanFormatter()
        
        print(formatter.format_plan_summary(plan))
        
        # Ask if user wants to see full plan
        show_full = input("\nWould you like to see the complete weekly breakdown? (y/n): ").lower()
        if show_full in ['y', 'yes']:
            print(formatter.format_full_plan(plan))
        
        # Ask if user wants to export
        export = input("\nWould you like to export to markdown file? (y/n): ").lower()
        if export in ['y', 'yes']:
            markdown = formatter.export_to_markdown(plan)
            filename = f"training_plan_{profile.target_distance.value.lower().replace(' ', '_')}.md"
            
            with open(filename, 'w') as f:
                f.write(markdown)
            
            print(f"Training plan exported to: {filename}")
        
        print("\n" + "="*50)
        print("RECOVERY & INJURY PREVENTION GUIDELINES")
        print("="*50)
        print(formatter.format_recovery_guidelines(profile))
        print(formatter.format_injury_prevention(profile))
        
    except KeyboardInterrupt:
        print("\n\nTraining plan generation cancelled.")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please try again or use 'python main.py help' for assistance.")


if __name__ == "__main__":
    main()
